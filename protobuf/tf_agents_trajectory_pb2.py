# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protobuf/tf_agents_trajectory.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='protobuf/tf_agents_trajectory.proto',
  package='tf_agents_trajectory',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n#protobuf/tf_agents_trajectory.proto\x12\x14tf_agents_trajectory\"9\n\x0f\x43urrentTimeStep\x12\x11\n\tstep_type\x18\x01 \x01(\x0c\x12\x13\n\x0bobservation\x18\x02 \x01(\x0c\"1\n\nActionStep\x12\x0e\n\x06\x61\x63tion\x18\x03 \x01(\x0c\x12\x13\n\x0bpolicy_info\x18\x04 \x01(\x0c\"C\n\x0cNextTimeStep\x12\x11\n\tstep_type\x18\x05 \x01(\x0c\x12\x0e\n\x06reward\x18\x06 \x01(\x0c\x12\x10\n\x08\x64iscount\x18\x07 \x01(\x0c\x62\x06proto3')
)




_CURRENTTIMESTEP = _descriptor.Descriptor(
  name='CurrentTimeStep',
  full_name='tf_agents_trajectory.CurrentTimeStep',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='step_type', full_name='tf_agents_trajectory.CurrentTimeStep.step_type', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='observation', full_name='tf_agents_trajectory.CurrentTimeStep.observation', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=61,
  serialized_end=118,
)


_ACTIONSTEP = _descriptor.Descriptor(
  name='ActionStep',
  full_name='tf_agents_trajectory.ActionStep',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='action', full_name='tf_agents_trajectory.ActionStep.action', index=0,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='policy_info', full_name='tf_agents_trajectory.ActionStep.policy_info', index=1,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=120,
  serialized_end=169,
)


_NEXTTIMESTEP = _descriptor.Descriptor(
  name='NextTimeStep',
  full_name='tf_agents_trajectory.NextTimeStep',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='step_type', full_name='tf_agents_trajectory.NextTimeStep.step_type', index=0,
      number=5, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='reward', full_name='tf_agents_trajectory.NextTimeStep.reward', index=1,
      number=6, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='discount', full_name='tf_agents_trajectory.NextTimeStep.discount', index=2,
      number=7, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=171,
  serialized_end=238,
)

DESCRIPTOR.message_types_by_name['CurrentTimeStep'] = _CURRENTTIMESTEP
DESCRIPTOR.message_types_by_name['ActionStep'] = _ACTIONSTEP
DESCRIPTOR.message_types_by_name['NextTimeStep'] = _NEXTTIMESTEP
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CurrentTimeStep = _reflection.GeneratedProtocolMessageType('CurrentTimeStep', (_message.Message,), {
  'DESCRIPTOR' : _CURRENTTIMESTEP,
  '__module__' : 'protobuf.tf_agents_trajectory_pb2'
  # @@protoc_insertion_point(class_scope:tf_agents_trajectory.CurrentTimeStep)
  })
_sym_db.RegisterMessage(CurrentTimeStep)

ActionStep = _reflection.GeneratedProtocolMessageType('ActionStep', (_message.Message,), {
  'DESCRIPTOR' : _ACTIONSTEP,
  '__module__' : 'protobuf.tf_agents_trajectory_pb2'
  # @@protoc_insertion_point(class_scope:tf_agents_trajectory.ActionStep)
  })
_sym_db.RegisterMessage(ActionStep)

NextTimeStep = _reflection.GeneratedProtocolMessageType('NextTimeStep', (_message.Message,), {
  'DESCRIPTOR' : _NEXTTIMESTEP,
  '__module__' : 'protobuf.tf_agents_trajectory_pb2'
  # @@protoc_insertion_point(class_scope:tf_agents_trajectory.NextTimeStep)
  })
_sym_db.RegisterMessage(NextTimeStep)


# @@protoc_insertion_point(module_scope)