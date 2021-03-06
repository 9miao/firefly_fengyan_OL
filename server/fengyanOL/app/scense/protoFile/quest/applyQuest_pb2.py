# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)



DESCRIPTOR = descriptor.FileDescriptor(
  name='protoFile/quest/applyQuest.proto',
  package='protoFile.quest.applyQuest',
  serialized_pb='\n protoFile/quest/applyQuest.proto\x12\x1aprotoFile.quest.applyQuest\"/\n\x11\x61pplyQuestRequest\x12\n\n\x02id\x18\x01 \x02(\x05\x12\x0e\n\x06taskId\x18\x02 \x02(\x05\"m\n\x12\x61pplyQuestResponse\x12\x0e\n\x06result\x18\x01 \x02(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x36\n\x04\x64\x61ta\x18\x03 \x01(\x0b\x32(.protoFile.quest.applyQuest.ResponseData\"\x1e\n\x0cResponseData\x12\x0e\n\x06taskId\x18\x01 \x01(\x05')




_APPLYQUESTREQUEST = descriptor.Descriptor(
  name='applyQuestRequest',
  full_name='protoFile.quest.applyQuest.applyQuestRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='id', full_name='protoFile.quest.applyQuest.applyQuestRequest.id', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='taskId', full_name='protoFile.quest.applyQuest.applyQuestRequest.taskId', index=1,
      number=2, type=5, cpp_type=1, label=2,
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
  serialized_start=64,
  serialized_end=111,
)


_APPLYQUESTRESPONSE = descriptor.Descriptor(
  name='applyQuestResponse',
  full_name='protoFile.quest.applyQuest.applyQuestResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='result', full_name='protoFile.quest.applyQuest.applyQuestResponse.result', index=0,
      number=1, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='message', full_name='protoFile.quest.applyQuest.applyQuestResponse.message', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='data', full_name='protoFile.quest.applyQuest.applyQuestResponse.data', index=2,
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
  serialized_start=113,
  serialized_end=222,
)


_RESPONSEDATA = descriptor.Descriptor(
  name='ResponseData',
  full_name='protoFile.quest.applyQuest.ResponseData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='taskId', full_name='protoFile.quest.applyQuest.ResponseData.taskId', index=0,
      number=1, type=5, cpp_type=1, label=1,
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
  serialized_start=224,
  serialized_end=254,
)

_APPLYQUESTRESPONSE.fields_by_name['data'].message_type = _RESPONSEDATA
DESCRIPTOR.message_types_by_name['applyQuestRequest'] = _APPLYQUESTREQUEST
DESCRIPTOR.message_types_by_name['applyQuestResponse'] = _APPLYQUESTRESPONSE
DESCRIPTOR.message_types_by_name['ResponseData'] = _RESPONSEDATA

class applyQuestRequest(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _APPLYQUESTREQUEST
  
  # @@protoc_insertion_point(class_scope:protoFile.quest.applyQuest.applyQuestRequest)

class applyQuestResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _APPLYQUESTRESPONSE
  
  # @@protoc_insertion_point(class_scope:protoFile.quest.applyQuest.applyQuestResponse)

class ResponseData(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RESPONSEDATA
  
  # @@protoc_insertion_point(class_scope:protoFile.quest.applyQuest.ResponseData)

# @@protoc_insertion_point(module_scope)
