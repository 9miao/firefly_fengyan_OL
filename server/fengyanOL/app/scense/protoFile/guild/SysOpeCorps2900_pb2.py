# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)



DESCRIPTOR = descriptor.FileDescriptor(
  name='protoFile/guild/SysOpeCorps2900.proto',
  package='protoFile.guild.SysOpeCorps2900',
  serialized_pb='\n%protoFile/guild/SysOpeCorps2900.proto\x12\x1fprotoFile.guild.SysOpeCorps2900\"\x91\x02\n\x13SysOpeCorpsResponse\x12\x0e\n\x06roleId\x18\x01 \x01(\x05\x12\x10\n\x08roleName\x18\x02 \x01(\t\x12\x12\n\nsysOpeType\x18\x03 \x01(\x05\x12\x0c\n\x04icon\x18\x04 \x01(\x05\x12\x0c\n\x04type\x18\x05 \x01(\x05\x12\x0b\n\x03pos\x18\x06 \x01(\x05\x12\x0f\n\x07\x63urPage\x18\x07 \x01(\x05\x12\x10\n\x08tishiStr\x18\x08 \x01(\t\x12\x12\n\ncontentStr\x18\t \x01(\t\x12\x11\n\tcaozuoStr\x18\n \x01(\t\x12\x12\n\ntoposition\x18\x0b \x01(\x05\x12=\n\tguaJiInfo\x18\x0c \x01(\x0b\x32*.protoFile.guild.SysOpeCorps2900.GuaJiInfo\"&\n\tGuaJiInfo\x12\x0b\n\x03\x65xp\x18\x01 \x01(\x05\x12\x0c\n\x04time\x18\x02 \x01(\x05')




_SYSOPECORPSRESPONSE = descriptor.Descriptor(
  name='SysOpeCorpsResponse',
  full_name='protoFile.guild.SysOpeCorps2900.SysOpeCorpsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='roleId', full_name='protoFile.guild.SysOpeCorps2900.SysOpeCorpsResponse.roleId', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='roleName', full_name='protoFile.guild.SysOpeCorps2900.SysOpeCorpsResponse.roleName', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='sysOpeType', full_name='protoFile.guild.SysOpeCorps2900.SysOpeCorpsResponse.sysOpeType', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='icon', full_name='protoFile.guild.SysOpeCorps2900.SysOpeCorpsResponse.icon', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='type', full_name='protoFile.guild.SysOpeCorps2900.SysOpeCorpsResponse.type', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='pos', full_name='protoFile.guild.SysOpeCorps2900.SysOpeCorpsResponse.pos', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='curPage', full_name='protoFile.guild.SysOpeCorps2900.SysOpeCorpsResponse.curPage', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='tishiStr', full_name='protoFile.guild.SysOpeCorps2900.SysOpeCorpsResponse.tishiStr', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='contentStr', full_name='protoFile.guild.SysOpeCorps2900.SysOpeCorpsResponse.contentStr', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='caozuoStr', full_name='protoFile.guild.SysOpeCorps2900.SysOpeCorpsResponse.caozuoStr', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='toposition', full_name='protoFile.guild.SysOpeCorps2900.SysOpeCorpsResponse.toposition', index=10,
      number=11, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='guaJiInfo', full_name='protoFile.guild.SysOpeCorps2900.SysOpeCorpsResponse.guaJiInfo', index=11,
      number=12, type=11, cpp_type=10, label=1,
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
  serialized_start=75,
  serialized_end=348,
)


_GUAJIINFO = descriptor.Descriptor(
  name='GuaJiInfo',
  full_name='protoFile.guild.SysOpeCorps2900.GuaJiInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='exp', full_name='protoFile.guild.SysOpeCorps2900.GuaJiInfo.exp', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='time', full_name='protoFile.guild.SysOpeCorps2900.GuaJiInfo.time', index=1,
      number=2, type=5, cpp_type=1, label=1,
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
  serialized_start=350,
  serialized_end=388,
)

_SYSOPECORPSRESPONSE.fields_by_name['guaJiInfo'].message_type = _GUAJIINFO
DESCRIPTOR.message_types_by_name['SysOpeCorpsResponse'] = _SYSOPECORPSRESPONSE
DESCRIPTOR.message_types_by_name['GuaJiInfo'] = _GUAJIINFO

class SysOpeCorpsResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SYSOPECORPSRESPONSE
  
  # @@protoc_insertion_point(class_scope:protoFile.guild.SysOpeCorps2900.SysOpeCorpsResponse)

class GuaJiInfo(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _GUAJIINFO
  
  # @@protoc_insertion_point(class_scope:protoFile.guild.SysOpeCorps2900.GuaJiInfo)

# @@protoc_insertion_point(module_scope)