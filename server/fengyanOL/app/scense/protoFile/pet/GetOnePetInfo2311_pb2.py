# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


import app.scense.protoFile.pet.petInfo_pb2

DESCRIPTOR = descriptor.FileDescriptor(
  name='GetOnePetInfo2311.proto',
  package='protoFile.pet.GetOnePetInfo2311',
  serialized_pb='\n\x17GetOnePetInfo2311.proto\x12\x1fprotoFile.pet.GetOnePetInfo2311\x1a\x1bprotoFile/pet/petInfo.proto\"C\n\x14GetOnePetInfoRequest\x12\n\n\x02id\x18\x01 \x02(\x05\x12\r\n\x05petId\x18\x02 \x02(\x05\x12\x10\n\x08masterId\x18\x03 \x02(\x05\"\xb1\x01\n\x15GetOnePetInfoResponse\x12\x0e\n\x06result\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\x12$\n\x04info\x18\x03 \x01(\x0b\x32\x16.protoFile.pet.PetInfo\x12\x12\n\nextendsExp\x18\x04 \x01(\x05\x12=\n\tziZhiInfo\x18\x05 \x01(\x0b\x32*.protoFile.pet.GetOnePetInfo2311.ZiZhiInfo\"\xa9\x01\n\tZiZhiInfo\x12\x11\n\tcur_zi_li\x18\x01 \x01(\x05\x12\x11\n\tmax_zi_li\x18\x02 \x01(\x05\x12\x12\n\ncur_zi_zhi\x18\x03 \x01(\x05\x12\x12\n\nmax_zi_zhi\x18\x04 \x01(\x05\x12\x12\n\ncur_zi_nai\x18\x05 \x01(\x05\x12\x12\n\nmax_zi_nai\x18\x06 \x01(\x05\x12\x12\n\ncur_zi_min\x18\x07 \x01(\x05\x12\x12\n\nmax_zi_min\x18\x08 \x01(\x05')




_GETONEPETINFOREQUEST = descriptor.Descriptor(
  name='GetOnePetInfoRequest',
  full_name='protoFile.pet.GetOnePetInfo2311.GetOnePetInfoRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='id', full_name='protoFile.pet.GetOnePetInfo2311.GetOnePetInfoRequest.id', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='petId', full_name='protoFile.pet.GetOnePetInfo2311.GetOnePetInfoRequest.petId', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='masterId', full_name='protoFile.pet.GetOnePetInfo2311.GetOnePetInfoRequest.masterId', index=2,
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
  serialized_start=89,
  serialized_end=156,
)


_GETONEPETINFORESPONSE = descriptor.Descriptor(
  name='GetOnePetInfoResponse',
  full_name='protoFile.pet.GetOnePetInfo2311.GetOnePetInfoResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='result', full_name='protoFile.pet.GetOnePetInfo2311.GetOnePetInfoResponse.result', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='message', full_name='protoFile.pet.GetOnePetInfo2311.GetOnePetInfoResponse.message', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='info', full_name='protoFile.pet.GetOnePetInfo2311.GetOnePetInfoResponse.info', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='extendsExp', full_name='protoFile.pet.GetOnePetInfo2311.GetOnePetInfoResponse.extendsExp', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='ziZhiInfo', full_name='protoFile.pet.GetOnePetInfo2311.GetOnePetInfoResponse.ziZhiInfo', index=4,
      number=5, type=11, cpp_type=10, label=1,
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
  serialized_start=159,
  serialized_end=336,
)


_ZIZHIINFO = descriptor.Descriptor(
  name='ZiZhiInfo',
  full_name='protoFile.pet.GetOnePetInfo2311.ZiZhiInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='cur_zi_li', full_name='protoFile.pet.GetOnePetInfo2311.ZiZhiInfo.cur_zi_li', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='max_zi_li', full_name='protoFile.pet.GetOnePetInfo2311.ZiZhiInfo.max_zi_li', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='cur_zi_zhi', full_name='protoFile.pet.GetOnePetInfo2311.ZiZhiInfo.cur_zi_zhi', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='max_zi_zhi', full_name='protoFile.pet.GetOnePetInfo2311.ZiZhiInfo.max_zi_zhi', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='cur_zi_nai', full_name='protoFile.pet.GetOnePetInfo2311.ZiZhiInfo.cur_zi_nai', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='max_zi_nai', full_name='protoFile.pet.GetOnePetInfo2311.ZiZhiInfo.max_zi_nai', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='cur_zi_min', full_name='protoFile.pet.GetOnePetInfo2311.ZiZhiInfo.cur_zi_min', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='max_zi_min', full_name='protoFile.pet.GetOnePetInfo2311.ZiZhiInfo.max_zi_min', index=7,
      number=8, type=5, cpp_type=1, label=1,
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
  serialized_start=339,
  serialized_end=508,
)

_GETONEPETINFORESPONSE.fields_by_name['info'].message_type = app.scense.protoFile.pet.petInfo_pb2._PETINFO
_GETONEPETINFORESPONSE.fields_by_name['ziZhiInfo'].message_type = _ZIZHIINFO
DESCRIPTOR.message_types_by_name['GetOnePetInfoRequest'] = _GETONEPETINFOREQUEST
DESCRIPTOR.message_types_by_name['GetOnePetInfoResponse'] = _GETONEPETINFORESPONSE
DESCRIPTOR.message_types_by_name['ZiZhiInfo'] = _ZIZHIINFO

class GetOnePetInfoRequest(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _GETONEPETINFOREQUEST
  
  # @@protoc_insertion_point(class_scope:protoFile.pet.GetOnePetInfo2311.GetOnePetInfoRequest)

class GetOnePetInfoResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _GETONEPETINFORESPONSE
  
  # @@protoc_insertion_point(class_scope:protoFile.pet.GetOnePetInfo2311.GetOnePetInfoResponse)

class ZiZhiInfo(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ZIZHIINFO
  
  # @@protoc_insertion_point(class_scope:protoFile.pet.GetOnePetInfo2311.ZiZhiInfo)

# @@protoc_insertion_point(module_scope)