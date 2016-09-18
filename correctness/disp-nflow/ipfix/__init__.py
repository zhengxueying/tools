# encoding: utf-8

MSG_HEADER_LEN = 16
SET_HEADER_LEN = 4

# IPFIX

MSG_VER = 'MsgVer'
MSG_LEN = 'MsgLen'
MSG_EXP_TIME = 'MsgExpTime'
MSG_SEQ_NUM = 'MsgSeqNum'
MSG_OB_DOM_ID = 'ObservationDomainId'
SET_ID = 'SetId'
SET_LEN = 'SetLen'
TEMP_ID = 'TempId'
SOURCE_ID = 'SourceId'
FLD_CNT = 'FldCnt'
SCOPE_FLD_CNT = 'ScopeFldCnt'
FLD_ID = 'FldId'
FLD_LEN = 'FldLen'
FLD_ENT_NUM = 'FldEntNum'
FLD_IDX = 'FldIdx'
FLD_NAME = 'FldName'
FLD_TYPE = 'FldType'
FLD_VAL = 'FldVal'
REC_IDX = 'RecIdx'
REC_SIZE = 'RecSize'

FLD_END_E_MASK = 0x8000
FLD_END_V_MASK = 0x7fff

SET_TYP_V9_TEMPLATE = 0
SET_TYP_V9_OPTIONS_TEMPLATE = 1
SET_TYP_TEMPLATE = 2
SET_TYP_OPTIONS_TEMPLATE = 3
SET_TYP_DATA = 256

KEY_FIELD_DEF = 'FldDef'
KEY_FIELDS_DEF = 'FldsDef'
KEY_FIELDS_LEN = 'FldsLen'

# Netflow V9
# https://tools.ietf.org/html/rfc3954
# https://www.plixer.com/support/netflow_v9.html
# http://www.cisco.com/en/US/technologies/tk648/tk362/technologies_white_paper09186a00800a3db9.html

PKT_V9_HEADER_LEN = 20
PKT_VER = 'PktVer'
PKT_SET_CNT = 'SetCnt'
PKT_SYS_UPTIME = 'SysUpTime'
PKT_SECS = 'PktSecs'
PKT_EXP_TIME = 'PktExpTime'
PKT_PKG_SEQ = 'PktPkgSeq'
PKT_SOURCE_ID = 'PktSrcId'


# Netflow V5
# https://www.plixer.com/support/netflow_v5.html
# https://bto.bluecoat.com/packetguide/8.7/info/netflow5-records.htm

PKT_V5_HEADER_LEN = 24
REC_V5_REC_LEN = 48
PKT_NSECS = 'PktNSecs'
PKT_FLOW_SEQ = 'PktFlowSeq'
PKT_ENG_TYPE = 'PktEngType'
PKT_ENG_ID = 'PktEngId'
PKT_SAMPLE_INTERVAL = 'PktSampleInterval'


ENT_FLAG = "entFlag"

# wrap frame
WRAP_TIME = "WrapTime"
WRAP_LEN1 = "WrapLen1"
WRAP_LEN2 = "WrapLen2"
WRAP_SRC_IP = "WrapSrcIp"


from _file import IpfixFile
from _obj import obj_bind_log_func
from _set import ipfix_load_template, ipfix_dump_template
from _udp import UdpChannel


