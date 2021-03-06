# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)



DESCRIPTOR = descriptor.FileDescriptor(
  name='protoFile/mail/addMail.proto',
  package='protoFile.mail.addMail',
  serialized_pb='\n\x1cprotoFile/mail/addMail.proto\x12\x16protoFile.mail.addMail\"f\n\x0e\x61\x64\x64MailRequest\x12\n\n\x02id\x18\x01 \x02(\x05\x12\x12\n\nplayerName\x18\x02 \x02(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x02(\t\x12\x11\n\treference\x18\x04 \x02(\t\x12\x10\n\x08systemId\x18\x05 \x02(\x05\"2\n\x0f\x61\x64\x64MailResponse\x12\x0e\n\x06result\x18\x01 \x02(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t')




_ADDMAILREQUEST = descriptor.Descriptor(
  name='addMailRequest',
  full_name='protoFile.mail.addMail.addMailRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='id', full_name='protoFile.mail.addMail.addMailRequest.id', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='playerName', full_name='protoFile.mail.addMail.addMailRequest.playerName', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='content', full_name='protoFile.mail.addMail.addMailRequest.content', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='reference', full_name='protoFile.mail.addMail.addMailRequest.reference', index=3,
      number=4, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='systemId', full_name='protoFile.mail.addMail.addMailRequest.systemId', index=4,
      number=5, type=5, cpp_type=1, label=2,
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
  serialized_start=56,
  serialized_end=158,
)


_ADDMAILRESPONSE = descriptor.Descriptor(
  name='addMailResponse',
  full_name='protoFile.mail.addMail.addMailResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='result', full_name='protoFile.mail.addMail.addMailResponse.result', index=0,
      number=1, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='message', full_name='protoFile.mail.addMail.addMailResponse.message', index=1,
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
  serialized_start=160,
  serialized_end=210,
)

DESCRIPTOR.message_types_by_name['addMailRequest'] = _ADDMAILREQUEST
DESCRIPTOR.message_types_by_name['addMailResponse'] = _ADDMAILRESPONSE

class addMailRequest(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ADDMAILREQUEST
  
  # @@protoc_insertion_point(class_scope:protoFile.mail.addMail.addMailRequest)

class addMailResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ADDMAILRESPONSE
  
  # @@protoc_insertion_point(class_scope:protoFile.mail.addMail.addMailResponse)

# @@protoc_insertion_point(module_scope)
