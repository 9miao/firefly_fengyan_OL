# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)



DESCRIPTOR = descriptor.FileDescriptor(
  name='protoFile/defence/ActivationElixir2406.proto',
  package='protoFile.defence.ActivationElixir2406',
  serialized_pb='\n,protoFile/defence/ActivationElixir2406.proto\x12&protoFile.defence.ActivationElixir2406\"G\n\x17\x41\x63tivationElixirRequest\x12\n\n\x02id\x18\x01 \x02(\x05\x12\x0c\n\x04\x63_id\x18\x02 \x02(\x05\x12\x12\n\nelixirType\x18\x03 \x02(\x05\";\n\x18\x41\x63tibationElixirResponse\x12\x0e\n\x06result\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t')




_ACTIVATIONELIXIRREQUEST = descriptor.Descriptor(
  name='ActivationElixirRequest',
  full_name='protoFile.defence.ActivationElixir2406.ActivationElixirRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='id', full_name='protoFile.defence.ActivationElixir2406.ActivationElixirRequest.id', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='c_id', full_name='protoFile.defence.ActivationElixir2406.ActivationElixirRequest.c_id', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='elixirType', full_name='protoFile.defence.ActivationElixir2406.ActivationElixirRequest.elixirType', index=2,
      number=3, type=5, cpp_type=1, label=2,
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
  serialized_start=88,
  serialized_end=159,
)


_ACTIBATIONELIXIRRESPONSE = descriptor.Descriptor(
  name='ActibationElixirResponse',
  full_name='protoFile.defence.ActivationElixir2406.ActibationElixirResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='result', full_name='protoFile.defence.ActivationElixir2406.ActibationElixirResponse.result', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='message', full_name='protoFile.defence.ActivationElixir2406.ActibationElixirResponse.message', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_start=161,
  serialized_end=220,
)

DESCRIPTOR.message_types_by_name['ActivationElixirRequest'] = _ACTIVATIONELIXIRREQUEST
DESCRIPTOR.message_types_by_name['ActibationElixirResponse'] = _ACTIBATIONELIXIRRESPONSE

class ActivationElixirRequest(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ACTIVATIONELIXIRREQUEST
  
  # @@protoc_insertion_point(class_scope:protoFile.defence.ActivationElixir2406.ActivationElixirRequest)

class ActibationElixirResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ACTIBATIONELIXIRRESPONSE
  
  # @@protoc_insertion_point(class_scope:protoFile.defence.ActivationElixir2406.ActibationElixirResponse)

# @@protoc_insertion_point(module_scope)
