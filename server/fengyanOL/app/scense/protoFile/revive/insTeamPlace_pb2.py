# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)



DESCRIPTOR = descriptor.FileDescriptor(
  name='protoFile/revive/insTeamPlace.proto',
  package='protoFile.revive.insTeamPlace',
  serialized_pb='\n#protoFile/revive/insTeamPlace.proto\x12\x1dprotoFile.revive.insTeamPlace\"(\n\x14instanceTeamResponse\x12\x10\n\x08leaderid\x18\x01 \x02(\x05')




_INSTANCETEAMRESPONSE = descriptor.Descriptor(
  name='instanceTeamResponse',
  full_name='protoFile.revive.insTeamPlace.instanceTeamResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='leaderid', full_name='protoFile.revive.insTeamPlace.instanceTeamResponse.leaderid', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
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
  serialized_start=70,
  serialized_end=110,
)

DESCRIPTOR.message_types_by_name['instanceTeamResponse'] = _INSTANCETEAMRESPONSE

class instanceTeamResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _INSTANCETEAMRESPONSE
  
  # @@protoc_insertion_point(class_scope:protoFile.revive.insTeamPlace.instanceTeamResponse)

# @@protoc_insertion_point(module_scope)