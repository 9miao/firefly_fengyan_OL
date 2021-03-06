# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)



DESCRIPTOR = descriptor.FileDescriptor(
  name='protoFile/playerInfo/addPoint.proto',
  package='protoFile.playerInfo.addPoint',
  serialized_pb='\n#protoFile/playerInfo/addPoint.proto\x12\x1dprotoFile.playerInfo.addPoint\"V\n\x0f\x61\x64\x64PointRequest\x12\n\n\x02id\x18\x01 \x02(\x05\x12\x11\n\tmanualStr\x18\x02 \x02(\x05\x12\x11\n\tmanualVit\x18\x03 \x02(\x05\x12\x11\n\tmanualDex\x18\x04 \x02(\x05\"n\n\x10\x61\x64\x64PointResponse\x12\x0e\n\x06result\x18\x01 \x02(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x39\n\x04\x64\x61ta\x18\x03 \x01(\x0b\x32+.protoFile.playerInfo.addPoint.ResponseData\"[\n\x0cResponseData\x12\x12\n\nsparePoint\x18\x01 \x02(\x05\x12\x11\n\tmanualStr\x18\x02 \x02(\x05\x12\x11\n\tmanualVit\x18\x03 \x02(\x05\x12\x11\n\tmanualDex\x18\x04 \x02(\x05')




_ADDPOINTREQUEST = descriptor.Descriptor(
  name='addPointRequest',
  full_name='protoFile.playerInfo.addPoint.addPointRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='id', full_name='protoFile.playerInfo.addPoint.addPointRequest.id', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='manualStr', full_name='protoFile.playerInfo.addPoint.addPointRequest.manualStr', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='manualVit', full_name='protoFile.playerInfo.addPoint.addPointRequest.manualVit', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='manualDex', full_name='protoFile.playerInfo.addPoint.addPointRequest.manualDex', index=3,
      number=4, type=5, cpp_type=1, label=2,
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
  serialized_end=156,
)


_ADDPOINTRESPONSE = descriptor.Descriptor(
  name='addPointResponse',
  full_name='protoFile.playerInfo.addPoint.addPointResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='result', full_name='protoFile.playerInfo.addPoint.addPointResponse.result', index=0,
      number=1, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='message', full_name='protoFile.playerInfo.addPoint.addPointResponse.message', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='data', full_name='protoFile.playerInfo.addPoint.addPointResponse.data', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=158,
  serialized_end=268,
)


_RESPONSEDATA = descriptor.Descriptor(
  name='ResponseData',
  full_name='protoFile.playerInfo.addPoint.ResponseData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='sparePoint', full_name='protoFile.playerInfo.addPoint.ResponseData.sparePoint', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='manualStr', full_name='protoFile.playerInfo.addPoint.ResponseData.manualStr', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='manualVit', full_name='protoFile.playerInfo.addPoint.ResponseData.manualVit', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='manualDex', full_name='protoFile.playerInfo.addPoint.ResponseData.manualDex', index=3,
      number=4, type=5, cpp_type=1, label=2,
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
  serialized_start=270,
  serialized_end=361,
)

_ADDPOINTRESPONSE.fields_by_name['data'].message_type = _RESPONSEDATA
DESCRIPTOR.message_types_by_name['addPointRequest'] = _ADDPOINTREQUEST
DESCRIPTOR.message_types_by_name['addPointResponse'] = _ADDPOINTRESPONSE
DESCRIPTOR.message_types_by_name['ResponseData'] = _RESPONSEDATA

class addPointRequest(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ADDPOINTREQUEST
  
  # @@protoc_insertion_point(class_scope:protoFile.playerInfo.addPoint.addPointRequest)

class addPointResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ADDPOINTRESPONSE
  
  # @@protoc_insertion_point(class_scope:protoFile.playerInfo.addPoint.addPointResponse)

class ResponseData(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RESPONSEDATA
  
  # @@protoc_insertion_point(class_scope:protoFile.playerInfo.addPoint.ResponseData)

# @@protoc_insertion_point(module_scope)
