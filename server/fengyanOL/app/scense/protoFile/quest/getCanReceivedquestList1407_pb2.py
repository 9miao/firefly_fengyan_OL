# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)



DESCRIPTOR = descriptor.FileDescriptor(
  name='protoFile/quest/getCanReceivedquestList1407.proto',
  package='protoFile.quest.getCanReceivedquestList1407',
  serialized_pb='\n1protoFile/quest/getCanReceivedquestList1407.proto\x12+protoFile.quest.getCanReceivedquestList1407\"j\n\x1fgetCanReceivedquestListResponse\x12G\n\x04\x64\x61ta\x18\x01 \x01(\x0b\x32\x39.protoFile.quest.getCanReceivedquestList1407.responseData\"`\n\x0cresponseData\x12P\n\x14\x63\x61nReceivedquestList\x18\x01 \x03(\x0b\x32\x32.protoFile.quest.getCanReceivedquestList1407.Quest\")\n\x05Quest\x12\x0e\n\x06taskId\x18\x01 \x01(\x05\x12\x10\n\x08taskname\x18\x02 \x01(\t')




_GETCANRECEIVEDQUESTLISTRESPONSE = descriptor.Descriptor(
  name='getCanReceivedquestListResponse',
  full_name='protoFile.quest.getCanReceivedquestList1407.getCanReceivedquestListResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='data', full_name='protoFile.quest.getCanReceivedquestList1407.getCanReceivedquestListResponse.data', index=0,
      number=1, type=11, cpp_type=10, label=1,
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
  serialized_start=98,
  serialized_end=204,
)


_RESPONSEDATA = descriptor.Descriptor(
  name='responseData',
  full_name='protoFile.quest.getCanReceivedquestList1407.responseData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='canReceivedquestList', full_name='protoFile.quest.getCanReceivedquestList1407.responseData.canReceivedquestList', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=206,
  serialized_end=302,
)


_QUEST = descriptor.Descriptor(
  name='Quest',
  full_name='protoFile.quest.getCanReceivedquestList1407.Quest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='taskId', full_name='protoFile.quest.getCanReceivedquestList1407.Quest.taskId', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='taskname', full_name='protoFile.quest.getCanReceivedquestList1407.Quest.taskname', index=1,
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
  serialized_start=304,
  serialized_end=345,
)

_GETCANRECEIVEDQUESTLISTRESPONSE.fields_by_name['data'].message_type = _RESPONSEDATA
_RESPONSEDATA.fields_by_name['canReceivedquestList'].message_type = _QUEST
DESCRIPTOR.message_types_by_name['getCanReceivedquestListResponse'] = _GETCANRECEIVEDQUESTLISTRESPONSE
DESCRIPTOR.message_types_by_name['responseData'] = _RESPONSEDATA
DESCRIPTOR.message_types_by_name['Quest'] = _QUEST

class getCanReceivedquestListResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _GETCANRECEIVEDQUESTLISTRESPONSE
  
  # @@protoc_insertion_point(class_scope:protoFile.quest.getCanReceivedquestList1407.getCanReceivedquestListResponse)

class responseData(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RESPONSEDATA
  
  # @@protoc_insertion_point(class_scope:protoFile.quest.getCanReceivedquestList1407.responseData)

class Quest(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _QUEST
  
  # @@protoc_insertion_point(class_scope:protoFile.quest.getCanReceivedquestList1407.Quest)

# @@protoc_insertion_point(module_scope)