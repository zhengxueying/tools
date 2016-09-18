# encoding: utf-8

import struct

from ipfix import FLD_ID, FLD_LEN, FLD_NAME, FLD_TYPE, FLD_IDX
from ipfix._obj import VisitObj


class Nflow9FieldDef(VisitObj):
    
    def __init__(self, offset):
        super(Nflow9FieldDef, self).__init__(offset)
        
    def parse(self, buff, pos, **kwargs):
        vals = struct.unpack_from('>HH', buff, pos)
        self[FLD_ID] = vals[0]
        self[FLD_LEN] = vals[1]

        vals = nflow9_lookup_field_name(self[FLD_ID])
            
        self[FLD_NAME] = vals[FLD_NAME]
        self[FLD_TYPE] = vals[FLD_TYPE]
        self[FLD_IDX] = kwargs[FLD_IDX]
        
        return 4
    
    
def nflow9_lookup_field_name(field_id):
    global FIELD_DEFS
    if (field_id > 0) and (field_id <= len(NFLOW9_FIELD_DEFS)):
        item = NFLOW9_FIELD_DEFS[field_id - 1]
        return { FLD_NAME: item[0], FLD_TYPE: item[2] }
    else:
        return { FLD_NAME: 'RESERVED%d' % field_id, FLD_TYPE: 'octetArray' }


NFLOW9_FIELD_DEFS = [    
    ('IN_BYTES', 1, 'unsigned32', 4),
    ('IN_PKTS', 2, 'unsigned32', 4),
    ('FLOWS', 3, 'unsigned32', 4),
    ('PROTOCOL', 4, 'unsigned8', 1),
    ('SRC_TOS', 5, 'unsigned8', 1),
    ('TCP_FLAGS', 6, 'unsigned8', 1),
    ('L4_SRC_PORT', 7, 'unsigned16', 2),
    ('IPV4_SRC_ADDR', 8, 'ipv4Address', 4),
    ('SRC_MASK', 9, 'unsigned8', 1),
    ('INPUT_SNMP', 10, 'unsigned16', 2,),
    ('L4_DST_PORT', 11, 'unsigned16', 2),
    ('IPV4_DST_ADDR', 12, 'ipv4Address', 4),
    ('DST_MASK', 13, 'unsigned8', 1),
    ('OUTPUT_SNMP', 14, 'unsigned16', 2),
    ('IPV4_NEXT_HOP', 15, 'unsigned32', 4),
    ('SRC_AS', 16, 'unsigned16', 2),
    ('DST_AS', 17, 'unsigned16', 2),
    ('BGP_IPV4_NEXT_HOP', 18, 'unsigned32', 4),
    ('MUL_DST_PKTS', 19, 'unsigned32', 4),
    ('MUL_DST_BYTES', 20, 'unsigned32', 4),
    ('LAST_SWITCHED', 21, 'unsigned32', 4),
    ('FIRST_SWITCHED', 22, 'unsigned32', 4),
    ('OUT_BYTES', 23, 'unsigned32', 4),
    ('OUT_PKTS', 24, 'unsigned32', 4),
    ('MIN_PKT_LNGTH', 25, 'unsigned16', 2),
    ('MAX_PKT_LNGTH', 26, 'unsigned16', 2),
    ('IPV6_SRC_ADDR', 27, 'ipv6Address', 16),
    ('IPV6_DST_ADDR', 28, 'ipv6Address', 16),
    ('IPV6_SRC_MASK', 29, 'unsigned8', 1),
    ('IPV6_DST_MASK', 30, 'unsigned8', 1),
    ('IPV6_FLOW_LABEL', 31, 'unsigned32', 3),
    ('ICMP_TYPE', 32, 'unsigned16', 2),
    ('MUL_IGMP_TYPE', 33, 'unsigned8', 1),
    ('SAMPLING_INTERVAL', 34, 'unsigned32', 4),
    ('SAMPLING_ALGORITHM', 35, 'unsigned8', 1),
    ('FLOW_ACTIVE_TIMEOUT', 36, 'unsigned16', 2),
    ('FLOW_INACTIVE_TIMEOUT', 37, 'unsigned16', 2),
    ('ENGINE_TYPE', 38, 'unsigned8', 1),
    ('ENGINE_ID', 39, 'unsigned8', 1),
    ('TOTAL_BYTES_EXP', 40, 'unsigned32', 4),
    ('TOTAL_PKTS_EXP', 41, 'unsigned32', 4),
    ('TOTAL_FLOWS_EXP', 42, 'unsigned32', 4),
    ('VENDOR_PROP_43', 43, 'octetArray', 65535),
    ('IPV4_SRC_PREFIX', 44, 'unsigned32', 4),
    ('IPV4_DST_PREFIX', 45, 'unsigned32', 4),
    ('MPLS_TOP_LABEL_TYPE', 46, 'unsigned8', 1),
    ('MPLS_TOP_LABEL_IP_ADDR', 47, 'ipv4Address', 4),
    ('FLOW_SAMPLER_ID', 48, 'unsigned8', 1),
    ('FLOW_SAMPLER_MODE', 49, 'unsigned8', 1),
    ('FLOW_SAMPLER_RANDOM_INTERVAL', 50, 'unsigned32', 4),
    ('VENDOR_PROP_51', 51, 'octetArray', 65535),
    ('MIN_TTL', 52, 'unsigned8', 1),
    ('MAX_TTL', 53, 'unsigned8', 1),
    ('IPV4_IDENT', 54, 'unsigned16', 2),
    ('DST_TOS', 55, 'unsigned8', 1),
    ('IN_SRC_MAC', 56, 'macAddress', 6),
    ('OUT_DST_MAC', 57, 'macAddress', 6),
    ('SRC_VLAN', 58, 'unsigned16', 2),
    ('DST_VLAN', 59, 'unsigned16', 2),
    ('IP_PROTOCOL_VERSION', 60, 'unsigned8', 1),
    ('DIRECTION', 61, 'unsigned8', 1),
    ('IPV6_NEXT_HOP', 62, 'ipv6Address', 16),
    ('BPG_IPV6_NEXT_HOP', 63, 'ipv6Address', 16),
    ('IPV6_OPTION_HEADERS', 64, 'unsigned32', 4),
    ('VENDOR_PROP_65', 65, 'octetArray', 65535),
    ('VENDOR_PROP_66', 66, 'octetArray', 65535),
    ('VENDOR_PROP_67', 67, 'octetArray', 65535),
    ('VENDOR_PROP_68', 68, 'octetArray', 65535),
    ('VENDOR_PROP_69', 69, 'octetArray', 65535),
    ('MPLS_LABEL_1', 70, 'unsigned16', 3),
    ('MPLS_LABEL_2', 71, 'unsigned32', 3),
    ('MPLS_LABEL_3', 72, 'unsigned32', 3),
    ('MPLS_LABEL_4', 73, 'unsigned32', 3),
    ('MPLS_LABEL_5', 74, 'unsigned32', 3),
    ('MPLS_LABEL_6', 75, 'unsigned32', 3),
    ('MPLS_LABEL_7', 76, 'unsigned32', 3),
    ('MPLS_LABEL_8', 77, 'unsigned32', 3),
    ('MPLS_LABEL_9', 78, 'unsigned32', 3),
    ('MPLS_LABEL_10', 79, 'unsigned32', 3),
    ('IN_DST_MAC', 80, 'macAddress', 6),
    ('OUT_SRC_MAC', 81, 'macAddress', 6),
    ('IF_NAME', 82, 'string', 65535),
    ('IF_DESC', 83, 'string', 65535),
    ('SAMPLER_NAME', 84, 'string', 65535),
    ('IN_PERMANENT_BYTES', 85, 'unsigned32', 4),
    ('IN_PERMANENT_PKTS', 86, 'unsigned32', 4),
    ('VENDOR_PROP_87', 87, 'octetArray', 65535),
    ('FRAGMENT_OFFSET', 88, 'unsigned16', 2),
    ('FORWARDING_STATUS', 89, 'unsigned8', 1),
    ('MPLS_PAL_RD', 90, 'octetArray', 8),
    ('MPLS_PREFIX_LEN', 91, 'unsigned8', 1),
    ('SRC_TRAFFIC_INDEX', 92, 'unsigned32', 4),
    ('DST_TRAFFIC_INDEX', 93, 'unsigned32', 4),
    ('APPLICATION_DESCRIPTION', 94, 'string', 65536),
    ('APPLICATION_TAG', 95, 'string', 65536),
    ('APPLICATION _NAME', 96, 'string', 65536),
    ('UNDEFINED_97', 97, 'octetArray', 65536),
    ('postipDiffServCodePoint', 98, 'unsigned8', 1),
    ('replication_factor', 99, 'unsigned32', 4),
    ('DEPRECATED_100', 100, 'octetArray', 65536),
    ('UNDEFINED_101', 101, 'octetArray', 65536),
    ('layer2packetSectionOffset', 102, 'octetArray', 65536),
    ('layer2packetSectionSize', 103, 'octetArray', 65536),
    ('ayer2packetSectionData', 104, 'octetArray', 65536),
]
