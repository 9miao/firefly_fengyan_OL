# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)



DESCRIPTOR = descriptor.FileDescriptor(
  name='protoFile/team/pushInvitedGroup.proto',
  package='protoFile.team.pushInvitedGroup',
  serialized_pb='\n%protoFile/team/pushInvitedGroup.proto\x12\x1fprotoFile.team.pushInvitedGroup\"9\n\x17pushInvitedGroupRequest\x12\x11\n\tinviterId\x18\x01 \x02(\x05\x12\x0b\n\x03msg\x18\x02 \x02(\t')




_PUSHINVITEDGROUPREQUEST = descriptor.Descriptor(
  name='pushInvitedGroupRequest',
  full_name='protoFile.team.pushInvitedGroup.pushInvitedGroupRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='inviterId', full_name='protoFile.team.pushInvitedGroup.pushInvitedGroupRequest.inviterId', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='msg', full_name='protoFile.team.pushInvitedGroup.pushInvitedGroupRequest.msg', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=74,
  serialized_end=131,
)

DESCRIPTOR.message_types_by_name['pushInvitedGroupRequest'] = _PUSHINVITEDGROUPREQUEST

class pushInvitedGroupRequest(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _PUSHINVITEDGROUPREQUEST
  
  # @@protoc_insertion_point(class_scope:protoFile.team.pushInvitedGroup.pushInvitedGroupRequest)

# @@protoc_insertion_point(module_scope)