# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)



DESCRIPTOR = descriptor.FileDescriptor(
  name='YiJianHeCheng3606.proto',
  package='protoFile.fate.YiJianHeCheng3606',
  serialized_pb='\n\x17YiJianHeCheng3606.proto\x12 protoFile.fate.YiJianHeCheng3606\"\"\n\x14YiJianHeChengRequest\x12\n\n\x02id\x18\x01 \x02(\x05\"8\n\x15YiJianHeChengResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\x0e\n\x06result\x18\x02 \x01(\x08')




_YIJIANHECHENGREQUEST = descriptor.Descriptor(
  name='YiJianHeChengRequest',
  full_name='protoFile.fate.YiJianHeCheng3606.YiJianHeChengRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='id', full_name='protoFile.fate.YiJianHeCheng3606.YiJianHeChengRequest.id', index=0,
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
  serialized_start=61,
  serialized_end=95,
)


_YIJIANHECHENGRESPONSE = descriptor.Descriptor(
  name='YiJianHeChengResponse',
  full_name='protoFile.fate.YiJianHeCheng3606.YiJianHeChengResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='message', full_name='protoFile.fate.YiJianHeCheng3606.YiJianHeChengResponse.message', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='result', full_name='protoFile.fate.YiJianHeCheng3606.YiJianHeChengResponse.result', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=97,
  serialized_end=153,
)

DESCRIPTOR.message_types_by_name['YiJianHeChengRequest'] = _YIJIANHECHENGREQUEST
DESCRIPTOR.message_types_by_name['YiJianHeChengResponse'] = _YIJIANHECHENGRESPONSE

class YiJianHeChengRequest(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _YIJIANHECHENGREQUEST
  
  # @@protoc_insertion_point(class_scope:protoFile.fate.YiJianHeCheng3606.YiJianHeChengRequest)

class YiJianHeChengResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _YIJIANHECHENGRESPONSE
  
  # @@protoc_insertion_point(class_scope:protoFile.fate.YiJianHeCheng3606.YiJianHeChengResponse)

# @@protoc_insertion_point(module_scope)
