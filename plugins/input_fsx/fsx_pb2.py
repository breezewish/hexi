# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: fsx.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='fsx.proto',
  package='FsxProtocol',
  syntax='proto3',
  serialized_pb=_b('\n\tfsx.proto\x12\x0b\x46sxProtocol\"\xae\x04\n\x11TcpRequestMessage\x12\x37\n\x07msgType\x18\x01 \x01(\x0e\x32&.FsxProtocol.TcpRequestMessage.MsgType\x12\x45\n\rsetConfigBody\x18\x02 \x01(\x0b\x32,.FsxProtocol.TcpRequestMessage.SetConfigBodyH\x00\x12;\n\x08pingBody\x18\x03 \x01(\x0b\x32\'.FsxProtocol.TcpRequestMessage.PingBodyH\x00\x12\x43\n\x0ctestConnBody\x18\x04 \x01(\x0b\x32+.FsxProtocol.TcpRequestMessage.TestConnBodyH\x00\x1a\x32\n\rSetConfigBody\x12\x0f\n\x07udpPort\x18\x01 \x01(\x05\x12\x10\n\x08udpToken\x18\x02 \x01(\x05\x1a\x1d\n\x08PingBody\x12\x11\n\ttimeStamp\x18\x01 \x01(\x05\x1a\"\n\x0cTestConnBody\x12\x12\n\nmagicToken\x18\x01 \x01(\x05\"\x94\x01\n\x07MsgType\x12\x17\n\x13MSG_TYPE_SET_CONFIG\x10\x00\x12\x11\n\rMSG_TYPE_PING\x10\x01\x12\x1c\n\x18MSG_TYPE_TEST_CONNECTION\x10\x02\x12\x1f\n\x1bMSG_TYPE_START_TRANSMISSION\x10\x03\x12\x1e\n\x1aMSG_TYPE_STOP_TRANSMISSION\x10\x04\x42\t\n\x07msgBody\"8\n\x12TcpResponseMessage\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x11\n\ttimeStamp\x18\x02 \x01(\x05\"\xc8\x04\n\x12UdpResponseMessage\x12\x38\n\x07msgType\x18\x01 \x01(\x0e\x32\'.FsxProtocol.UdpResponseMessage.MsgType\x12\x14\n\x0cserialNumber\x18\x02 \x01(\x05\x12\r\n\x05token\x18\x03 \x01(\x05\x12T\n\x14testConnCallbackBody\x18\x04 \x01(\x0b\x32\x34.FsxProtocol.UdpResponseMessage.TestConnCallbackBodyH\x00\x12T\n\x14transmissionDataBody\x18\x05 \x01(\x0b\x32\x34.FsxProtocol.UdpResponseMessage.TransmissionDataBodyH\x00\x1a*\n\x14TestConnCallbackBody\x12\x12\n\nmagicToken\x18\x01 \x01(\x05\x1a\x9d\x01\n\x14TransmissionDataBody\x12\x15\n\rxAcceleration\x18\x01 \x01(\x01\x12\x15\n\ryAcceleration\x18\x02 \x01(\x01\x12\x15\n\rzAcceleration\x18\x03 \x01(\x01\x12\x15\n\rpitchVelocity\x18\x04 \x01(\x01\x12\x14\n\x0crollVelocity\x18\x05 \x01(\x01\x12\x13\n\x0byawVelocity\x18\x06 \x01(\x01\"P\n\x07MsgType\x12%\n!MSG_TYPE_TEST_CONNECTION_CALLBACK\x10\x00\x12\x1e\n\x1aMSG_TYPE_TRANSMISSION_DATA\x10\x01\x42\t\n\x07msgBodyb\x06proto3')
)



_TCPREQUESTMESSAGE_MSGTYPE = _descriptor.EnumDescriptor(
  name='MsgType',
  full_name='FsxProtocol.TcpRequestMessage.MsgType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='MSG_TYPE_SET_CONFIG', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MSG_TYPE_PING', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MSG_TYPE_TEST_CONNECTION', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MSG_TYPE_START_TRANSMISSION', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MSG_TYPE_STOP_TRANSMISSION', index=4, number=4,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=426,
  serialized_end=574,
)
_sym_db.RegisterEnumDescriptor(_TCPREQUESTMESSAGE_MSGTYPE)

_UDPRESPONSEMESSAGE_MSGTYPE = _descriptor.EnumDescriptor(
  name='MsgType',
  full_name='FsxProtocol.UdpResponseMessage.MsgType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='MSG_TYPE_TEST_CONNECTION_CALLBACK', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MSG_TYPE_TRANSMISSION_DATA', index=1, number=1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1139,
  serialized_end=1219,
)
_sym_db.RegisterEnumDescriptor(_UDPRESPONSEMESSAGE_MSGTYPE)


_TCPREQUESTMESSAGE_SETCONFIGBODY = _descriptor.Descriptor(
  name='SetConfigBody',
  full_name='FsxProtocol.TcpRequestMessage.SetConfigBody',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='udpPort', full_name='FsxProtocol.TcpRequestMessage.SetConfigBody.udpPort', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='udpToken', full_name='FsxProtocol.TcpRequestMessage.SetConfigBody.udpToken', index=1,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=306,
  serialized_end=356,
)

_TCPREQUESTMESSAGE_PINGBODY = _descriptor.Descriptor(
  name='PingBody',
  full_name='FsxProtocol.TcpRequestMessage.PingBody',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='timeStamp', full_name='FsxProtocol.TcpRequestMessage.PingBody.timeStamp', index=0,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=358,
  serialized_end=387,
)

_TCPREQUESTMESSAGE_TESTCONNBODY = _descriptor.Descriptor(
  name='TestConnBody',
  full_name='FsxProtocol.TcpRequestMessage.TestConnBody',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='magicToken', full_name='FsxProtocol.TcpRequestMessage.TestConnBody.magicToken', index=0,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=389,
  serialized_end=423,
)

_TCPREQUESTMESSAGE = _descriptor.Descriptor(
  name='TcpRequestMessage',
  full_name='FsxProtocol.TcpRequestMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='msgType', full_name='FsxProtocol.TcpRequestMessage.msgType', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='setConfigBody', full_name='FsxProtocol.TcpRequestMessage.setConfigBody', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='pingBody', full_name='FsxProtocol.TcpRequestMessage.pingBody', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='testConnBody', full_name='FsxProtocol.TcpRequestMessage.testConnBody', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_TCPREQUESTMESSAGE_SETCONFIGBODY, _TCPREQUESTMESSAGE_PINGBODY, _TCPREQUESTMESSAGE_TESTCONNBODY, ],
  enum_types=[
    _TCPREQUESTMESSAGE_MSGTYPE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='msgBody', full_name='FsxProtocol.TcpRequestMessage.msgBody',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=27,
  serialized_end=585,
)


_TCPRESPONSEMESSAGE = _descriptor.Descriptor(
  name='TcpResponseMessage',
  full_name='FsxProtocol.TcpResponseMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='FsxProtocol.TcpResponseMessage.success', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='timeStamp', full_name='FsxProtocol.TcpResponseMessage.timeStamp', index=1,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=587,
  serialized_end=643,
)


_UDPRESPONSEMESSAGE_TESTCONNCALLBACKBODY = _descriptor.Descriptor(
  name='TestConnCallbackBody',
  full_name='FsxProtocol.UdpResponseMessage.TestConnCallbackBody',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='magicToken', full_name='FsxProtocol.UdpResponseMessage.TestConnCallbackBody.magicToken', index=0,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=935,
  serialized_end=977,
)

_UDPRESPONSEMESSAGE_TRANSMISSIONDATABODY = _descriptor.Descriptor(
  name='TransmissionDataBody',
  full_name='FsxProtocol.UdpResponseMessage.TransmissionDataBody',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='xAcceleration', full_name='FsxProtocol.UdpResponseMessage.TransmissionDataBody.xAcceleration', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='yAcceleration', full_name='FsxProtocol.UdpResponseMessage.TransmissionDataBody.yAcceleration', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='zAcceleration', full_name='FsxProtocol.UdpResponseMessage.TransmissionDataBody.zAcceleration', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='pitchVelocity', full_name='FsxProtocol.UdpResponseMessage.TransmissionDataBody.pitchVelocity', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='rollVelocity', full_name='FsxProtocol.UdpResponseMessage.TransmissionDataBody.rollVelocity', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='yawVelocity', full_name='FsxProtocol.UdpResponseMessage.TransmissionDataBody.yawVelocity', index=5,
      number=6, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=980,
  serialized_end=1137,
)

_UDPRESPONSEMESSAGE = _descriptor.Descriptor(
  name='UdpResponseMessage',
  full_name='FsxProtocol.UdpResponseMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='msgType', full_name='FsxProtocol.UdpResponseMessage.msgType', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='serialNumber', full_name='FsxProtocol.UdpResponseMessage.serialNumber', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='token', full_name='FsxProtocol.UdpResponseMessage.token', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='testConnCallbackBody', full_name='FsxProtocol.UdpResponseMessage.testConnCallbackBody', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='transmissionDataBody', full_name='FsxProtocol.UdpResponseMessage.transmissionDataBody', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_UDPRESPONSEMESSAGE_TESTCONNCALLBACKBODY, _UDPRESPONSEMESSAGE_TRANSMISSIONDATABODY, ],
  enum_types=[
    _UDPRESPONSEMESSAGE_MSGTYPE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='msgBody', full_name='FsxProtocol.UdpResponseMessage.msgBody',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=646,
  serialized_end=1230,
)

_TCPREQUESTMESSAGE_SETCONFIGBODY.containing_type = _TCPREQUESTMESSAGE
_TCPREQUESTMESSAGE_PINGBODY.containing_type = _TCPREQUESTMESSAGE
_TCPREQUESTMESSAGE_TESTCONNBODY.containing_type = _TCPREQUESTMESSAGE
_TCPREQUESTMESSAGE.fields_by_name['msgType'].enum_type = _TCPREQUESTMESSAGE_MSGTYPE
_TCPREQUESTMESSAGE.fields_by_name['setConfigBody'].message_type = _TCPREQUESTMESSAGE_SETCONFIGBODY
_TCPREQUESTMESSAGE.fields_by_name['pingBody'].message_type = _TCPREQUESTMESSAGE_PINGBODY
_TCPREQUESTMESSAGE.fields_by_name['testConnBody'].message_type = _TCPREQUESTMESSAGE_TESTCONNBODY
_TCPREQUESTMESSAGE_MSGTYPE.containing_type = _TCPREQUESTMESSAGE
_TCPREQUESTMESSAGE.oneofs_by_name['msgBody'].fields.append(
  _TCPREQUESTMESSAGE.fields_by_name['setConfigBody'])
_TCPREQUESTMESSAGE.fields_by_name['setConfigBody'].containing_oneof = _TCPREQUESTMESSAGE.oneofs_by_name['msgBody']
_TCPREQUESTMESSAGE.oneofs_by_name['msgBody'].fields.append(
  _TCPREQUESTMESSAGE.fields_by_name['pingBody'])
_TCPREQUESTMESSAGE.fields_by_name['pingBody'].containing_oneof = _TCPREQUESTMESSAGE.oneofs_by_name['msgBody']
_TCPREQUESTMESSAGE.oneofs_by_name['msgBody'].fields.append(
  _TCPREQUESTMESSAGE.fields_by_name['testConnBody'])
_TCPREQUESTMESSAGE.fields_by_name['testConnBody'].containing_oneof = _TCPREQUESTMESSAGE.oneofs_by_name['msgBody']
_UDPRESPONSEMESSAGE_TESTCONNCALLBACKBODY.containing_type = _UDPRESPONSEMESSAGE
_UDPRESPONSEMESSAGE_TRANSMISSIONDATABODY.containing_type = _UDPRESPONSEMESSAGE
_UDPRESPONSEMESSAGE.fields_by_name['msgType'].enum_type = _UDPRESPONSEMESSAGE_MSGTYPE
_UDPRESPONSEMESSAGE.fields_by_name['testConnCallbackBody'].message_type = _UDPRESPONSEMESSAGE_TESTCONNCALLBACKBODY
_UDPRESPONSEMESSAGE.fields_by_name['transmissionDataBody'].message_type = _UDPRESPONSEMESSAGE_TRANSMISSIONDATABODY
_UDPRESPONSEMESSAGE_MSGTYPE.containing_type = _UDPRESPONSEMESSAGE
_UDPRESPONSEMESSAGE.oneofs_by_name['msgBody'].fields.append(
  _UDPRESPONSEMESSAGE.fields_by_name['testConnCallbackBody'])
_UDPRESPONSEMESSAGE.fields_by_name['testConnCallbackBody'].containing_oneof = _UDPRESPONSEMESSAGE.oneofs_by_name['msgBody']
_UDPRESPONSEMESSAGE.oneofs_by_name['msgBody'].fields.append(
  _UDPRESPONSEMESSAGE.fields_by_name['transmissionDataBody'])
_UDPRESPONSEMESSAGE.fields_by_name['transmissionDataBody'].containing_oneof = _UDPRESPONSEMESSAGE.oneofs_by_name['msgBody']
DESCRIPTOR.message_types_by_name['TcpRequestMessage'] = _TCPREQUESTMESSAGE
DESCRIPTOR.message_types_by_name['TcpResponseMessage'] = _TCPRESPONSEMESSAGE
DESCRIPTOR.message_types_by_name['UdpResponseMessage'] = _UDPRESPONSEMESSAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TcpRequestMessage = _reflection.GeneratedProtocolMessageType('TcpRequestMessage', (_message.Message,), dict(

  SetConfigBody = _reflection.GeneratedProtocolMessageType('SetConfigBody', (_message.Message,), dict(
    DESCRIPTOR = _TCPREQUESTMESSAGE_SETCONFIGBODY,
    __module__ = 'fsx_pb2'
    # @@protoc_insertion_point(class_scope:FsxProtocol.TcpRequestMessage.SetConfigBody)
    ))
  ,

  PingBody = _reflection.GeneratedProtocolMessageType('PingBody', (_message.Message,), dict(
    DESCRIPTOR = _TCPREQUESTMESSAGE_PINGBODY,
    __module__ = 'fsx_pb2'
    # @@protoc_insertion_point(class_scope:FsxProtocol.TcpRequestMessage.PingBody)
    ))
  ,

  TestConnBody = _reflection.GeneratedProtocolMessageType('TestConnBody', (_message.Message,), dict(
    DESCRIPTOR = _TCPREQUESTMESSAGE_TESTCONNBODY,
    __module__ = 'fsx_pb2'
    # @@protoc_insertion_point(class_scope:FsxProtocol.TcpRequestMessage.TestConnBody)
    ))
  ,
  DESCRIPTOR = _TCPREQUESTMESSAGE,
  __module__ = 'fsx_pb2'
  # @@protoc_insertion_point(class_scope:FsxProtocol.TcpRequestMessage)
  ))
_sym_db.RegisterMessage(TcpRequestMessage)
_sym_db.RegisterMessage(TcpRequestMessage.SetConfigBody)
_sym_db.RegisterMessage(TcpRequestMessage.PingBody)
_sym_db.RegisterMessage(TcpRequestMessage.TestConnBody)

TcpResponseMessage = _reflection.GeneratedProtocolMessageType('TcpResponseMessage', (_message.Message,), dict(
  DESCRIPTOR = _TCPRESPONSEMESSAGE,
  __module__ = 'fsx_pb2'
  # @@protoc_insertion_point(class_scope:FsxProtocol.TcpResponseMessage)
  ))
_sym_db.RegisterMessage(TcpResponseMessage)

UdpResponseMessage = _reflection.GeneratedProtocolMessageType('UdpResponseMessage', (_message.Message,), dict(

  TestConnCallbackBody = _reflection.GeneratedProtocolMessageType('TestConnCallbackBody', (_message.Message,), dict(
    DESCRIPTOR = _UDPRESPONSEMESSAGE_TESTCONNCALLBACKBODY,
    __module__ = 'fsx_pb2'
    # @@protoc_insertion_point(class_scope:FsxProtocol.UdpResponseMessage.TestConnCallbackBody)
    ))
  ,

  TransmissionDataBody = _reflection.GeneratedProtocolMessageType('TransmissionDataBody', (_message.Message,), dict(
    DESCRIPTOR = _UDPRESPONSEMESSAGE_TRANSMISSIONDATABODY,
    __module__ = 'fsx_pb2'
    # @@protoc_insertion_point(class_scope:FsxProtocol.UdpResponseMessage.TransmissionDataBody)
    ))
  ,
  DESCRIPTOR = _UDPRESPONSEMESSAGE,
  __module__ = 'fsx_pb2'
  # @@protoc_insertion_point(class_scope:FsxProtocol.UdpResponseMessage)
  ))
_sym_db.RegisterMessage(UdpResponseMessage)
_sym_db.RegisterMessage(UdpResponseMessage.TestConnCallbackBody)
_sym_db.RegisterMessage(UdpResponseMessage.TransmissionDataBody)


# @@protoc_insertion_point(module_scope)
