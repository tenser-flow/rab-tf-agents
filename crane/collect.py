import os
import argparse
import struct
import datetime
from tqdm import tqdm

import numpy as np
import tensorflow as tf

from google.oauth2 import service_account

from protobuf.bytes_experience_replay_pb2 import Observations, Actions, Rewards, Info
from models.dqn_model import DQN_Model
from util.gcp_io import gcp_load_pipeline, gcs_load_weights, \
                        cbt_global_iterator, cbt_global_trajectory_buffer
from util.logging import TimeLogger
from util.unity_env import UnityEnvironmentWrapper

#SET API CREDENTIALS
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
SERVICE_ACCOUNT_FILE = 'cbt_credentials.json'

#SET HYPERPARAMETERS
VECTOR_OBS_SPEC = [8]
VISUAL_OBS_SPEC = [224,224,3]
NUM_ACTIONS=6
CONV_LAYER_PARAMS=((8,4,32),(4,2,64),(3,1,64))
FC_LAYER_PARAMS=(512,)
LEARNING_RATE=0.00042
EPSILON = 0.5

if __name__ == '__main__':
    #COMMAND-LINE ARGUMENTS
    parser = argparse.ArgumentParser('Environment-To-Bigtable Script')
    parser.add_argument('--gcp-project-id', type=str, default='for-robolab-cbai')
    parser.add_argument('--cbt-instance-id', type=str, default='rab-rl-bigtable')
    parser.add_argument('--cbt-table-name', type=str, default='crane-simplereward-experience-replay')
    parser.add_argument('--bucket-id', type=str, default='youngalou')
    parser.add_argument('--env-filename', type=str, default='envs/CraneML.x86_64')
    parser.add_argument('--prefix', type=str, default='crane-simplereward')
    parser.add_argument('--tmp-weights-filepath', type=str, default='/tmp/model_weights_tmp.h5')
    parser.add_argument('--num-cycles', type=int, default=1000000)
    parser.add_argument('--num-episodes', type=int, default=1)
    parser.add_argument('--max-steps', type=int, default=1000)
    parser.add_argument('--update-interval', type=int, default=1)
    parser.add_argument('--global-traj-buff-size', type=int, default=10)
    parser.add_argument('--log-time', default=False, action='store_true')
    parser.add_argument('--docker-training', type=bool, default=False)
    args = parser.parse_args()

    #INSTANTIATE CBT TABLE AND GCS BUCKET
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    cbt_table, gcs_bucket = gcp_load_pipeline(args.gcp_project_id, args.cbt_instance_id, args.cbt_table_name, args.bucket_id, credentials)
    max_row_bytes = (4*np.prod(VISUAL_OBS_SPEC) + 64)
    cbt_batcher = cbt_table.mutations_batcher(flush_count=args.num_episodes, max_row_bytes=max_row_bytes)

    #INITIALIZE ENVIRONMENT
    print("-> Initializing Crane environement...")
    env = UnityEnvironmentWrapper(environment_filename=args.env_filename,
                                  use_visual=True,
                                  docker_training=args.docker_training)
    print("-> Environment intialized.")

    #LOAD MODEL
    model = DQN_Model(input_shape=env._observation_space.shape,
                      num_actions=env._action_space.n,
                      conv_layer_params=CONV_LAYER_PARAMS,
                      fc_layer_params=FC_LAYER_PARAMS,
                      learning_rate=LEARNING_RATE)

    #INITIALIZE EXECUTION TIME LOGGER
    if args.log_time is True:
        time_logger = TimeLogger(["Load Weights     ",
                                  "Global Iterator  ",
                                  "Run Environment  ",
                                  "Data To Bytes    ",
                                  "Write Cells      ",
                                  "Mutate Rows      "])

    #COLLECT DATA FOR CBT
    print("-> Starting data collection...")
    for cycle in range(args.num_cycles):
        if args.log_time is True: time_logger.reset()

        if cycle % args.update_interval == 0:
            gcs_load_weights(model, gcs_bucket, args.prefix, args.tmp_weights_filepath)

        if args.log_time is True: time_logger.log("Load Weights     ")

        rows = []
        local_traj_buff = []
        print("Collecting cycle {}:".format(cycle))
        for episode in range(args.num_episodes):
            #UPDATE GLOBAL ITERATOR
            global_i = cbt_global_iterator(cbt_table)
            local_traj_buff.append(global_i)

            if args.log_time is True: time_logger.log("Global Iterator  ")

            #RL LOOP GENERATES A TRAJECTORY
            obs = np.asarray(env.reset() / 255).astype(np.float32)
            reward = 0
            done = False
            
            for step in tqdm(range(args.max_steps), "Episode {}".format(episode)):
                action = model.step_epsilon_greedy(obs, EPSILON)
                new_obs, reward, done, info = env.step(action)

                if done: break
                obs = np.asarray(new_obs / 255).astype(np.float32)
        
                if args.log_time is True: time_logger.log("Run Environment  ")

                observation = np.expand_dims(obs, axis=0).flatten().tobytes()
                action = np.asarray(action).astype(np.int32).tobytes()
                reward = np.asarray(reward).astype(np.float32).tobytes()

                #BUILD PB2 OBJECTS
                pb2_obs, pb2_actions, pb2_rewards, pb2_info = Observations(), Actions(), Rewards(), Info()
                pb2_obs.visual_obs = observation
                pb2_actions.actions = action
                pb2_rewards.rewards = reward
                pb2_info.visual_obs_spec.extend(VISUAL_OBS_SPEC)

                if args.log_time is True: time_logger.log("Data To Bytes    ")

                #WRITE TO AND APPEND ROW
                row_key = 'traj_{:05d}_step_{:05d}'.format(global_i, step).encode()
                row = cbt_table.row(row_key)
                row.set_cell(column_family_id='step',
                            column='obs'.encode(),
                            value=pb2_obs.SerializeToString())
                row.set_cell(column_family_id='step',
                            column='action'.encode(),
                            value=pb2_actions.SerializeToString())
                row.set_cell(column_family_id='step',
                            column='reward'.encode(),
                            value=pb2_rewards.SerializeToString())
                row.set_cell(column_family_id='step',
                            column='info'.encode(),
                            value=pb2_info.SerializeToString())
                rows.append(row)

                if args.log_time is True: time_logger.log("Write Cells      ")
        
        #ADD ROWS TO BIGTABLE
        cbt_global_trajectory_buffer(cbt_table, np.asarray(local_traj_buff).astype(np.int32), args.global_traj_buff_size)
        cbt_batcher.mutate_rows(rows)
        cbt_batcher.flush()

        if args.log_time is True: time_logger.log("Mutate Rows      ")

        print("-> Saved trajectories {}.".format(local_traj_buff))

        if args.log_time is True: time_logger.print_totaltime_logs()
    env.close()
    print("-> Done!")