# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)



DESCRIPTOR = descriptor.FileDescriptor(
  name='protoFile/itemInfo.proto',
  package='protoFile',
  serialized_pb='\n\x18protoFile/itemInfo.proto\x12\tprotoFile\"\xd2\x0b\n\tItemsInfo\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04type\x18\x02 \x01(\x05\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x12\n\nprefixNmae\x18\x04 \x01(\t\x12\x12\n\nsuffixName\x18\x05 \x01(\t\x12\x10\n\x08\x62indType\x18\x06 \x01(\x05\x12\x0f\n\x07isBound\x18\x07 \x01(\x05\x12\x13\n\x0b\x64\x65scription\x18\x08 \x01(\t\x12\x19\n\x11professionRequire\x18\t \x01(\x05\x12\x14\n\x0c\x63\x61nInjection\x18\n \x01(\x05\x12\x10\n\x08\x62odyType\x18\x0b \x01(\x05\x12\x12\n\nweaponType\x18\x0c \x01(\x05\x12\x12\n\nnowQuality\x18\r \x01(\x05\x12\x12\n\nbaseAttack\x18\x0e \x01(\x05\x12\x11\n\textAttack\x18\x0f \x01(\x05\x12\x12\n\nattackType\x18\x10 \x01(\x05\x12\x11\n\tbaseSpeed\x18\x11 \x01(\x05\x12\x14\n\x0clevelRequire\x18\x12 \x01(\x05\x12\x0f\n\x07\x62\x61seStr\x18\x13 \x01(\x05\x12\x0e\n\x06\x65xtStr\x18\x14 \x01(\x05\x12\x0f\n\x07\x62\x61seVit\x18\x15 \x01(\x05\x12\x0e\n\x06\x65xtVit\x18\x16 \x01(\x05\x12\x0f\n\x07\x62\x61seDex\x18\x17 \x01(\x05\x12\x0e\n\x06\x65xtDex\x18\x18 \x01(\x05\x12\x0f\n\x07\x62\x61seWis\x18\x19 \x01(\x05\x12\x0e\n\x06\x65xtWis\x18\x1a \x01(\x05\x12\x0f\n\x07\x62\x61seSpi\x18\x1b \x01(\x05\x12\x0e\n\x06\x65xtSpi\x18\x1c \x01(\x05\x12\x1a\n\x12\x62\x61sePhysicalAttack\x18\x1d \x01(\x05\x12\x19\n\x11\x65xtPhysicalAttack\x18\x1e \x01(\x05\x12\x17\n\x0f\x62\x61seMagicAttack\x18\x1f \x01(\x05\x12\x16\n\x0e\x65xtMagicAttack\x18  \x01(\x05\x12\x1b\n\x13\x62\x61sePhysicalDefense\x18! \x01(\x05\x12\x1a\n\x12\x65xtPhysicalDefense\x18\" \x01(\x05\x12\x18\n\x10\x62\x61seMagicDefense\x18# \x01(\x05\x12\x17\n\x0f\x65xtMagicDefense\x18$ \x01(\x05\x12\x18\n\x10\x62\x61seHpAdditional\x18% \x01(\x05\x12\x17\n\x0f\x65xtHpAdditional\x18& \x01(\x05\x12\x18\n\x10\x62\x61seMpAdditional\x18\' \x01(\x05\x12\x17\n\x0f\x65xtMpAdditional\x18( \x01(\x05\x12\x19\n\x11\x62\x61seHitAdditional\x18) \x01(\x05\x12\x18\n\x10\x65xtHitAdditional\x18* \x01(\x05\x12\x1a\n\x12\x62\x61seCritAdditional\x18+ \x01(\x05\x12\x19\n\x11\x65xtCritAdditional\x18, \x01(\x05\x12\x1b\n\x13\x62\x61seDodgeAdditional\x18- \x01(\x05\x12\x1a\n\x12\x65xtDodgeAdditional\x18. \x01(\x05\x12\x1d\n\x15\x62\x61seSquelchAdditional\x18/ \x01(\x05\x12\x1c\n\x14\x65xtSquelchAdditional\x18\x30 \x01(\x05\x12\x1b\n\x13\x62\x61seSpeedAdditional\x18\x31 \x01(\x05\x12\x1a\n\x12\x65xtSpeedAdditional\x18\x32 \x01(\x05\x12\x1b\n\x13\x62\x61seBogeyAdditional\x18\x33 \x01(\x05\x12\x1a\n\x12\x65xtBogeyAdditional\x18\x34 \x01(\x05\x12\x13\n\x0b\x65quipEffect\x18\x35 \x01(\t\x12\x13\n\x0b\x64\x65vilEffect\x18\x36 \x01(\t\x12\x13\n\x0bsuiteEffect\x18\x37 \x01(\t\x12$\n\nSuiteItems\x18\x38 \x03(\x0b\x32\x10.protoFile.Suite\x12\x16\n\x0e\x62uyingRateCoin\x18\x39 \x01(\x05\x12\x16\n\x0e\x62\x61seDurability\x18: \x01(\x05\x12\x15\n\rnowDurability\x18; \x01(\x05\x12\x13\n\x0b\x62\x61seDefense\x18< \x01(\x05\x12\x12\n\nextDefense\x18= \x01(\x05\x12\r\n\x05stack\x18> \x01(\x05\x12\x11\n\tstarLevel\x18? \x01(\x05\x12\x0c\n\x04icon\x18@ \x01(\x05\x12\x12\n\ntemplateId\x18\x41 \x01(\x05\x12\x10\n\x08maxstack\x18\x42 \x01(\x05\x12\x10\n\x08itemPage\x18\x43 \x01(\x05\"2\n\x05Suite\x12\x14\n\x0csuitItemName\x18\x01 \x01(\t\x12\x13\n\x0bhasSiutitem\x18\x02 \x01(\x05')




_ITEMSINFO = descriptor.Descriptor(
  name='ItemsInfo',
  full_name='protoFile.ItemsInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='id', full_name='protoFile.ItemsInfo.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='type', full_name='protoFile.ItemsInfo.type', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='name', full_name='protoFile.ItemsInfo.name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='prefixNmae', full_name='protoFile.ItemsInfo.prefixNmae', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='suffixName', full_name='protoFile.ItemsInfo.suffixName', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='bindType', full_name='protoFile.ItemsInfo.bindType', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='isBound', full_name='protoFile.ItemsInfo.isBound', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='description', full_name='protoFile.ItemsInfo.description', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='professionRequire', full_name='protoFile.ItemsInfo.professionRequire', index=8,
      number=9, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='canInjection', full_name='protoFile.ItemsInfo.canInjection', index=9,
      number=10, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='bodyType', full_name='protoFile.ItemsInfo.bodyType', index=10,
      number=11, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='weaponType', full_name='protoFile.ItemsInfo.weaponType', index=11,
      number=12, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='nowQuality', full_name='protoFile.ItemsInfo.nowQuality', index=12,
      number=13, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='baseAttack', full_name='protoFile.ItemsInfo.baseAttack', index=13,
      number=14, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='extAttack', full_name='protoFile.ItemsInfo.extAttack', index=14,
      number=15, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='attackType', full_name='protoFile.ItemsInfo.attackType', index=15,
      number=16, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='baseSpeed', full_name='protoFile.ItemsInfo.baseSpeed', index=16,
      number=17, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='levelRequire', full_name='protoFile.ItemsInfo.levelRequire', index=17,
      number=18, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='baseStr', full_name='protoFile.ItemsInfo.baseStr', index=18,
      number=19, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='extStr', full_name='protoFile.ItemsInfo.extStr', index=19,
      number=20, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='baseVit', full_name='protoFile.ItemsInfo.baseVit', index=20,
      number=21, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='extVit', full_name='protoFile.ItemsInfo.extVit', index=21,
      number=22, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='baseDex', full_name='protoFile.ItemsInfo.baseDex', index=22,
      number=23, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='extDex', full_name='protoFile.ItemsInfo.extDex', index=23,
      number=24, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='baseWis', full_name='protoFile.ItemsInfo.baseWis', index=24,
      number=25, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='extWis', full_name='protoFile.ItemsInfo.extWis', index=25,
      number=26, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='baseSpi', full_name='protoFile.ItemsInfo.baseSpi', index=26,
      number=27, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='extSpi', full_name='protoFile.ItemsInfo.extSpi', index=27,
      number=28, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='basePhysicalAttack', full_name='protoFile.ItemsInfo.basePhysicalAttack', index=28,
      number=29, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='extPhysicalAttack', full_name='protoFile.ItemsInfo.extPhysicalAttack', index=29,
      number=30, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='baseMagicAttack', full_name='protoFile.ItemsInfo.baseMagicAttack', index=30,
      number=31, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='extMagicAttack', full_name='protoFile.ItemsInfo.extMagicAttack', index=31,
      number=32, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='basePhysicalDefense', full_name='protoFile.ItemsInfo.basePhysicalDefense', index=32,
      number=33, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='extPhysicalDefense', full_name='protoFile.ItemsInfo.extPhysicalDefense', index=33,
      number=34, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='baseMagicDefense', full_name='protoFile.ItemsInfo.baseMagicDefense', index=34,
      number=35, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='extMagicDefense', full_name='protoFile.ItemsInfo.extMagicDefense', index=35,
      number=36, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='baseHpAdditional', full_name='protoFile.ItemsInfo.baseHpAdditional', index=36,
      number=37, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='extHpAdditional', full_name='protoFile.ItemsInfo.extHpAdditional', index=37,
      number=38, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='baseMpAdditional', full_name='protoFile.ItemsInfo.baseMpAdditional', index=38,
      number=39, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='extMpAdditional', full_name='protoFile.ItemsInfo.extMpAdditional', index=39,
      number=40, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='baseHitAdditional', full_name='protoFile.ItemsInfo.baseHitAdditional', index=40,
      number=41, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='extHitAdditional', full_name='protoFile.ItemsInfo.extHitAdditional', index=41,
      number=42, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='baseCritAdditional', full_name='protoFile.ItemsInfo.baseCritAdditional', index=42,
      number=43, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='extCritAdditional', full_name='protoFile.ItemsInfo.extCritAdditional', index=43,
      number=44, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='baseDodgeAdditional', full_name='protoFile.ItemsInfo.baseDodgeAdditional', index=44,
      number=45, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='extDodgeAdditional', full_name='protoFile.ItemsInfo.extDodgeAdditional', index=45,
      number=46, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='baseSquelchAdditional', full_name='protoFile.ItemsInfo.baseSquelchAdditional', index=46,
      number=47, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='extSquelchAdditional', full_name='protoFile.ItemsInfo.extSquelchAdditional', index=47,
      number=48, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='baseSpeedAdditional', full_name='protoFile.ItemsInfo.baseSpeedAdditional', index=48,
      number=49, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='extSpeedAdditional', full_name='protoFile.ItemsInfo.extSpeedAdditional', index=49,
      number=50, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='baseBogeyAdditional', full_name='protoFile.ItemsInfo.baseBogeyAdditional', index=50,
      number=51, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='extBogeyAdditional', full_name='protoFile.ItemsInfo.extBogeyAdditional', index=51,
      number=52, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='equipEffect', full_name='protoFile.ItemsInfo.equipEffect', index=52,
      number=53, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='devilEffect', full_name='protoFile.ItemsInfo.devilEffect', index=53,
      number=54, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='suiteEffect', full_name='protoFile.ItemsInfo.suiteEffect', index=54,
      number=55, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='SuiteItems', full_name='protoFile.ItemsInfo.SuiteItems', index=55,
      number=56, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='buyingRateCoin', full_name='protoFile.ItemsInfo.buyingRateCoin', index=56,
      number=57, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='baseDurability', full_name='protoFile.ItemsInfo.baseDurability', index=57,
      number=58, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='nowDurability', full_name='protoFile.ItemsInfo.nowDurability', index=58,
      number=59, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='baseDefense', full_name='protoFile.ItemsInfo.baseDefense', index=59,
      number=60, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='extDefense', full_name='protoFile.ItemsInfo.extDefense', index=60,
      number=61, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='stack', full_name='protoFile.ItemsInfo.stack', index=61,
      number=62, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='starLevel', full_name='protoFile.ItemsInfo.starLevel', index=62,
      number=63, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='icon', full_name='protoFile.ItemsInfo.icon', index=63,
      number=64, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='templateId', full_name='protoFile.ItemsInfo.templateId', index=64,
      number=65, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='maxstack', full_name='protoFile.ItemsInfo.maxstack', index=65,
      number=66, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='itemPage', full_name='protoFile.ItemsInfo.itemPage', index=66,
      number=67, type=5, cpp_type=1, label=1,
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
  serialized_start=40,
  serialized_end=1530,
)


_SUITE = descriptor.Descriptor(
  name='Suite',
  full_name='protoFile.Suite',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='suitItemName', full_name='protoFile.Suite.suitItemName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='hasSiutitem', full_name='protoFile.Suite.hasSiutitem', index=1,
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
  serialized_start=1532,
  serialized_end=1582,
)

_ITEMSINFO.fields_by_name['SuiteItems'].message_type = _SUITE
DESCRIPTOR.message_types_by_name['ItemsInfo'] = _ITEMSINFO
DESCRIPTOR.message_types_by_name['Suite'] = _SUITE

class ItemsInfo(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ITEMSINFO
  
  # @@protoc_insertion_point(class_scope:protoFile.ItemsInfo)

class Suite(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SUITE
  
  # @@protoc_insertion_point(class_scope:protoFile.Suite)

# @@protoc_insertion_point(module_scope)
