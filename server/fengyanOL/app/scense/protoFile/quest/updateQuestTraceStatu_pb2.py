# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)



DESCRIPTOR = descriptor.FileDescriptor(
  name='protoFile/quest/updateQuestTraceStatu.proto',
  package='protoFile.quest.updateQuestTraceStatu',
  serialized_pb='\n+protoFile/quest/updateQuestTraceStatu.proto\x12%protoFile.quest.updateQuestTraceStatu\"N\n\x1cupdateQuestTraceStatuRequest\x12\n\n\x02id\x18\x01 \x02(\x05\x12\x0e\n\x06taskID\x18\x02 \x02(\x05\x12\x12\n\ntraceStatu\x18\x03 \x02(\x05\"@\n\x1dupdateQuestTraceStatuResponse\x12\x0e\n\x06result\x18\x01 \x02(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t')




_UPDATEQUESTTRACESTATUREQUEST = descriptor.Descriptor(
  name='updateQuestTraceStatuRequest',
  full_name='protoFile.quest.updateQuestTraceStatu.updateQuestTraceStatuRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='id', full_name='protoFile.quest.updateQuestTraceStatu.updateQuestTraceStatuRequest.id', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='taskID', full_name='protoFile.quest.updateQuestTraceStatu.updateQuestTraceStatuRequest.taskID', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='traceStatu', full_name='protoFile.quest.updateQuestTraceStatu.updateQuestTraceStatuRequest.traceStatu', index=2,
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
  serialized_start=86,
  serialized_end=164,
)


_UPDATEQUESTTRACESTATURESPONSE = descriptor.Descriptor(
  name='updateQuestTraceStatuResponse',
  full_name='protoFile.quest.updateQuestTraceStatu.updateQuestTraceStatuResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='result', full_name='protoFile.quest.updateQuestTraceStatu.updateQuestTraceStatuResponse.result', index=0,
      number=1, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='message', full_name='protoFile.quest.updateQuestTraceStatu.updateQuestTraceStatuResponse.message', index=1,
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
  serialized_start=166,
  serialized_end=230,
)

DESCRIPTOR.message_types_by_name['updateQuestTraceStatuRequest'] = _UPDATEQUESTTRACESTATUREQUEST
DESCRIPTOR.message_types_by_name['updateQuestTraceStatuResponse'] = _UPDATEQUESTTRACESTATURESPONSE

class updateQuestTraceStatuRequest(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _UPDATEQUESTTRACESTATUREQUEST
  
  # @@protoc_insertion_point(class_scope:protoFile.quest.updateQuestTraceStatu.updateQuestTraceStatuRequest)

class updateQuestTraceStatuResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _UPDATEQUESTTRACESTATURESPONSE
  
  # @@protoc_insertion_point(class_scope:protoFile.quest.updateQuestTraceStatu.updateQuestTraceStatuResponse)

# @@protoc_insertion_point(module_scope)
