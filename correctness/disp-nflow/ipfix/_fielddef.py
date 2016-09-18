# encoding: utf-8

import struct

from ipfix import FLD_END_E_MASK, FLD_END_V_MASK, FLD_ID, FLD_LEN, FLD_ENT_NUM, FLD_NAME, \
    FLD_TYPE, FLD_IDX, ENT_FLAG
from ipfix._obj import VisitObj


class IpfixFieldDef(VisitObj):

    def __init__(self, offset):
        super(IpfixFieldDef, self).__init__(offset)
        
    def parse(self, buff, pos, **kwargs):
        vals = struct.unpack_from('>HH', buff, pos)
        if  kwargs.get(ENT_FLAG, True) and vals[0] >= FLD_END_E_MASK:
            self[FLD_ID] = vals[0] & FLD_END_V_MASK
            self[FLD_LEN] = vals[1]
            self[FLD_ENT_NUM], = struct.unpack_from('>I', buff, pos + 4)
            vals = ipfix_lookup_entprise_field_name(self[FLD_ENT_NUM], self[FLD_ID])
            size = 8
        else:
            self[FLD_ID] = vals[0]
            self[FLD_LEN] = vals[1]
            vals = ipfix_lookup_field_name(self[FLD_ID])
            size = 4
            
        self[FLD_NAME] = vals[FLD_NAME]
        self[FLD_TYPE] = vals[FLD_TYPE]
        self[FLD_IDX] = kwargs[FLD_IDX]
        
        return size

    def load_from_template(self, index, def_fields):
        '''
        :param index:
        :param [Field, ID, Ent.ID, Offset, Size]
        :return:
        '''

        def safe_convert(text):
            try:
                return int(text)
            except ValueError, e:
                return 0

        if len(def_fields) <= 5:
            self[FLD_ID] = safe_convert(def_fields[1])
            self[FLD_LEN] = safe_convert(def_fields[3])
            if self[FLD_ID] == 0 or self[FLD_LEN] == 0:
                return False
            vals = ipfix_lookup_field_name(self[FLD_ID])

            self[FLD_NAME] = vals[FLD_NAME]
            self[FLD_TYPE] = vals[FLD_TYPE]
            self[FLD_IDX] = index
            return True

        self[FLD_ID] = safe_convert(def_fields[1])
        ent_num =  safe_convert(def_fields[2])
        self[FLD_LEN] = safe_convert(def_fields[4])
        if self[FLD_ID] == 0 or self[FLD_LEN] == 0:
            return False

        if ent_num == 0:
            vals = ipfix_lookup_field_name(self[FLD_ID])
        else:
            self[FLD_ENT_NUM] = ent_num
            vals = ipfix_lookup_entprise_field_name(self[FLD_ENT_NUM], self[FLD_ID])

        self[FLD_NAME] = vals[FLD_NAME]
        self[FLD_TYPE] = vals[FLD_TYPE]
        self[FLD_IDX] = index
        return True
    
    
def ipfix_lookup_entprise_field_name(ent_num, field_id):
    global ENTERPRISE_FIELD_DEFS
    try:
        item = ENTERPRISE_FIELD_DEFS[ent_num][field_id]
        return { FLD_NAME: item[0], FLD_TYPE: item[2] }
    except:
        return { FLD_NAME: 'RESERVED%d' % field_id, FLD_TYPE: 'octetArray' }


CISCO_FIELD_DEFS = {    
    4245: ('timestampInterval', 4245, 'unsigned64', 8),
    4251: ('transportPacketsLostCounter', 4251, 'signed32', 4),
    4315: ('tcpWindowSizeMin', 4315, 'signed32', 4),
    4336: ('networkDelaySum', 4336, 'unsigned64', 8),
    4337: ('networkDelaySample', 4337, 'unsigned32', 4),
    8337: ('connectionServerCounterBytesNetwork', 8337, 'unsigned64', 8),
    8338: ('connectionClientCounterBytesNetwork', 8338, 'unsigned64', 8),
    9268: ('clinetRetransPackets', 9268, 'unsigned32', 4),
    9270: ('serverRetransPackets', 9270, 'unsigned32', 4),
    9272: ('transactionCountDelta', 9272, 'unsigned32', 4),
    9273: ('sumTransactionTime', 9273, 'unsigned32', 4),
    9303: ('sumRespTime', 9303, 'unsigned32', 4),
    9306: ('sumServerRespTime', 9306, 'unsigned32', 4),
    9309: ('sumTotalRespTime', 9309, 'unsigned32', 4),
    9313: ('sumNwkTime', 9313, 'unsigned32', 4),
    9316: ('sumClientNwkTime', 9316, 'unsigned32', 4),
    9319: ('sumServerNwkTime', 9319, 'unsigned32', 4),
    12236: ('connectionClientIPv4Address', 12336, 'ipv4Address', 4),
    12240: ('connectionClientTransportPort', 12240, 'unsigned16', 2),
    12241: ('connectionServerTransportPort', 12241, 'unsigned16', 2),
}

ENTERPRISE_FIELD_DEFS = {
    9: CISCO_FIELD_DEFS,
}   


def ipfix_lookup_field_name(field_id):
    global FIELD_DEFS
    if (field_id > 0) and (field_id <= len(FIELD_DEFS)):
        item = FIELD_DEFS[field_id - 1]
        return { FLD_NAME: item[0], FLD_TYPE: item[2] }
    else:
        return { FLD_NAME: 'RESERVED%d' % field_id, FLD_TYPE: 'octetArray' }


FIELD_DEFS = [    
    ('octetDeltaCount', 1, 'unsigned64', 8),
    ('packetDeltaCount', 2, 'unsigned64', 8),
    ('deltaFlowCount', 3, 'unsigned64', 8),
    ('protocolIdentifier', 4, 'unsigned8', 1),
    ('ipClassOfService', 5, 'unsigned8', 1),
    ('tcpControlBits', 6, 'unsigned8', 2),
    ('sourceTransportPort', 7, 'unsigned16', 2),
    ('sourceIPv4Address', 8, 'ipv4Address', 4),
    ('sourceIPv4PrefixLength', 9, 'unsigned8', 1),
    ('ingressInterface', 10, 'unsigned32', 4),
    ('destinationTransportPort', 11, 'unsigned16', 2),
    ('destinationIPv4Address', 12, 'ipv4Address', 4),
    ('destinationIPv4PrefixLength', 13, 'unsigned8', 1),
    ('egressInterface', 14, 'unsigned32', 4),
    ('ipNextHopIPv4Address', 15, 'ipv4Address', 4),
    ('bgpSourceAsNumber', 16, 'unsigned32', 4),
    ('bgpDestinationAsNumber', 17, 'unsigned32', 4),
    ('bgpNextHopIPv4Address', 18, 'ipv4Address', 4),
    ('postMCastPacketDeltaCount', 19, 'unsigned64', 8),
    ('postMCastOctetDeltaCount', 20, 'unsigned64', 8),
    ('flowEndSysUpTime', 21, 'unsigned32', 4),
    ('flowStartSysUpTime', 22, 'unsigned32', 4),
    ('postOctetDeltaCount', 23, 'unsigned64', 8),
    ('postPacketDeltaCount', 24, 'unsigned64', 8),
    ('minimumIpTotalLength', 25, 'unsigned64', 8),
    ('maximumIpTotalLength', 26, 'unsigned64', 8),
    ('sourceIPv6Address', 27, 'ipv6Address', 16),
    ('destinationIPv6Address', 28, 'ipv6Address', 16),
    ('sourceIPv6PrefixLength', 29, 'unsigned8', 1),
    ('destinationIPv6PrefixLength', 30, 'unsigned8', 1),
    ('flowLabelIPv6', 31, 'unsigned32', 4),
    ('icmpTypeCodeIPv4', 32, 'unsigned16', 2),
    ('igmpType', 33, 'unsigned8', 1),
    ('samplingInterval', 34, 'unsigned32', 4),
    ('samplingAlgorithm', 35, 'unsigned8', 1),
    ('flowActiveTimeout', 36, 'unsigned16', 2),
    ('flowIdleTimeout', 37, 'unsigned16', 2),
    ('engineType', 38, 'unsigned8', 1),
    ('engineId', 39, 'unsigned8', 1),
    ('exportedOctetTotalCount', 40, 'unsigned64', 8),
    ('exportedMessageTotalCount', 41, 'unsigned64', 8),
    ('exportedFlowRecordTotalCount', 42, 'unsigned64', 8),
    ('ipv4RouterSc', 43, 'ipv4Address', 4),
    ('sourceIPv4Prefix', 44, 'ipv4Address', 4),
    ('destinationIPv4Prefix', 45, 'ipv4Address', 4),
    ('mplsTopLabelType', 46, 'unsigned8', 1),
    ('mplsTopLabelIPv4Address', 47, 'ipv4Address', 4),
    ('samplerId', 48, 'unsigned8', 1),
    ('samplerMode', 49, 'unsigned8', 1),
    ('samplerRandomInterval', 50, 'unsigned32', 4),
    ('classId', 51, 'unsigned8', 1),
    ('minimumTTL', 52, 'unsigned8', 1),
    ('maximumTTL', 53, 'unsigned8', 1),
    ('fragmentIdentification', 54, 'unsigned32', 4),
    ('postIpClassOfService', 55, 'unsigned8', 1),
    ('sourceMacAddress', 56, 'macAddress', 6),
    ('postDestinationMacAddress', 57, 'macAddress', 6),
    ('vlanId', 58, 'unsigned16', 2),
    ('postVlanId', 59, 'unsigned16', 2),
    ('ipVersion', 60, 'unsigned8', 1),
    ('flowDirection', 61, 'unsigned8', 1),
    ('ipNextHopIPv6Address', 62, 'ipv6Address', 16),
    ('bgpNextHopIPv6Address', 63, 'ipv6Address', 16),
    ('ipv6ExtensionHeaders', 64, 'unsigned32', 4),
    ('RESERVED65', 65, 'octetArray', 65536),
    ('RESERVED66', 66, 'octetArray', 65536),
    ('RESERVED67', 67, 'octetArray', 65536),
    ('RESERVED67', 68, 'octetArray', 65536),
    ('RESERVED69', 69, 'octetArray', 65536),
    ('mplsTopLabelStackSection', 70, 'octetArray', 65535),
    ('mplsLabelStackSection2', 71, 'octetArray', 65535),
    ('mplsLabelStackSection3', 72, 'octetArray', 65535),
    ('mplsLabelStackSection4', 73, 'octetArray', 65535),
    ('mplsLabelStackSection5', 74, 'octetArray', 65535),
    ('mplsLabelStackSection6', 75, 'octetArray', 65535),
    ('mplsLabelStackSection7', 76, 'octetArray', 65535),
    ('mplsLabelStackSection8', 77, 'octetArray', 65535),
    ('mplsLabelStackSection9', 78, 'octetArray', 65535),
    ('mplsLabelStackSection10', 79, 'octetArray', 65535),
    ('destinationMacAddress', 80, 'macAddress', 6),
    ('postSourceMacAddress', 81, 'macAddress', 6),
    ('interfaceName', 82, 'string', 65535),
    ('interfaceDescription', 83, 'string', 65535),
    ('samplerName', 84, 'string', 65535),
    ('octetTotalCount', 85, 'unsigned64', 8),
    ('packetTotalCount', 86, 'unsigned64', 8),
    ('flagsAndSamplerId', 87, 'unsigned32', 4),
    ('fragmentOffset', 88, 'unsigned16', 2),
    ('forwardingStatus', 89, 'unsigned32', 4),
    ('mplsVpnRouteDistinguisher', 90, 'octetArray', 65535),
    ('mplsTopLabelPrefixLength', 91, 'unsigned8', 1),
    ('srcTrafficIndex', 92, 'unsigned32', 4),
    ('dstTrafficIndex', 93, 'unsigned32', 4),
    ('applicationDescription', 94, 'string', 65535),
    ('applicationId', 95, 'octetArray', 65535),
    ('applicationName', 96, 'string', 65535),
    ('RESERVED97', 97, 'octetArray', 65536),
    ('postIpDiffServCodePoint', 98, 'unsigned8', 1),
    ('multicastReplicationFactor', 99, 'unsigned32', 4),
    ('className', 100, 'string', 65535),
    ('classificationEngineId', 101, 'unsigned8', 1),
    ('layer2packetSectionOffset', 102, 'unsigned16', 2),
    ('layer2packetSectionSize', 103, 'unsigned16', 2),
    ('layer2packetSectionData', 104, 'octetArray', 65535),
    ('RESERVED105', 105, 'octetArray', 65536),
    ('RESERVED106', 106, 'octetArray', 65536),
    ('RESERVED107', 107, 'octetArray', 65536),
    ('RESERVED108', 108, 'octetArray', 65536),
    ('RESERVED109', 109, 'octetArray', 65536),
    ('RESERVED110', 110, 'octetArray', 65536),
    ('RESERVED111', 111, 'octetArray', 65536),
    ('RESERVED112', 112, 'octetArray', 65536),
    ('RESERVED113', 113, 'octetArray', 65536),
    ('RESERVED114', 114, 'octetArray', 65536),
    ('RESERVED115', 115, 'octetArray', 65536),
    ('RESERVED116', 116, 'octetArray', 65536),
    ('RESERVED117', 117, 'octetArray', 65536),
    ('RESERVED118', 118, 'octetArray', 65536),
    ('RESERVED119', 119, 'octetArray', 65536),
    ('RESERVED120', 120, 'octetArray', 65536),
    ('RESERVED121', 121, 'octetArray', 65536),
    ('RESERVED122', 122, 'octetArray', 65536),
    ('RESERVED123', 123, 'octetArray', 65536),
    ('RESERVED124', 124, 'octetArray', 65536),
    ('RESERVED125', 125, 'octetArray', 65536),
    ('RESERVED126', 126, 'octetArray', 65536),
    ('RESERVED127', 127, 'octetArray', 65536),
    ('bgpNextAdjacentAsNumber', 128, 'unsigned32', 4),
    ('bgpPrevAdjacentAsNumber', 129, 'unsigned32', 4),
    ('exporterIPv4Address', 130, 'ipv4Address', 4),
    ('exporterIPv6Address', 131, 'ipv6Address', 16),
    ('droppedOctetDeltaCount', 132, 'unsigned64', 8),
    ('droppedPacketDeltaCount', 133, 'unsigned64', 8),
    ('droppedOctetTotalCount', 134, 'unsigned64', 8),
    ('droppedPacketTotalCount', 135, 'unsigned64', 8),
    ('flowEndReason', 136, 'unsigned8', 1),
    ('commonPropertiesId', 137, 'unsigned64', 8),
    ('observationPointId', 138, 'unsigned32', 8),
    ('icmpTypeCodeIPv6', 139, 'unsigned16', 2),
    ('mplsTopLabelIPv6Address', 140, 'ipv6Address', 16),
    ('lineCardId', 141, 'unsigned32', 4),
    ('portId', 142, 'unsigned32', 4),
    ('meteringProcessId', 143, 'unsigned32', 4),
    ('exportingProcessId', 144, 'unsigned32', 4),
    ('templateId', 145, 'unsigned16', 2),
    ('wlanChannelId', 146, 'unsigned8', 1),
    ('wlanSSID', 147, 'string', 65535),
    ('flowId', 148, 'unsigned64', 8),
    ('observationDomainId', 149, 'unsigned32', 4),
    ('flowStartSeconds', 150, 'dateTimeSeconds', 4),
    ('flowEndSeconds', 151, 'dateTimeSeconds', 4),
    ('flowStartMilliseconds', 152, 'dateTimeMilliseconds', 8),
    ('flowEndMilliseconds', 153, 'dateTimeMilliseconds', 8),
    ('flowStartMicroseconds', 154, 'dateTimeMicroseconds', 8),
    ('flowEndMicroseconds', 155, 'dateTimeMicroseconds', 8),
    ('flowStartNanoseconds', 156, 'dateTimeNanoseconds', 8),
    ('flowEndNanoseconds', 157, 'dateTimeNanoseconds', 8),
    ('flowStartDeltaMicroseconds', 158, 'unsigned32', 4),
    ('flowEndDeltaMicroseconds', 159, 'unsigned32', 4),
    ('systemInitTimeMilliseconds', 160, 'dateTimeMilliseconds', 8),
    ('flowDurationMilliseconds', 161, 'unsigned32', 4),
    ('flowDurationMicroseconds', 162, 'unsigned32', 4),
    ('observedFlowTotalCount', 163, 'unsigned64', 8),
    ('ignoredPacketTotalCount', 164, 'unsigned64', 8),
    ('ignoredOctetTotalCount', 165, 'unsigned64', 8),
    ('notSentFlowTotalCount', 166, 'unsigned64', 8),
    ('notSentPacketTotalCount', 167, 'unsigned64', 8),
    ('notSentOctetTotalCount', 168, 'unsigned64', 8),
    ('destinationIPv6Prefix', 169, 'ipv6Address', 16),
    ('sourceIPv6Prefix', 170, 'ipv6Address', 16),
    ('postOctetTotalCount', 171, 'unsigned64', 8),
    ('postPacketTotalCount', 172, 'unsigned64', 8),
    ('flowKeyIndicator', 173, 'unsigned64', 8),
    ('postMCastPacketTotalCount', 174, 'unsigned64', 8),
    ('postMCastOctetTotalCount', 175, 'unsigned64', 8),
    ('icmpTypeIPv4', 176, 'unsigned8', 1),
    ('icmpCodeIPv4', 177, 'unsigned8', 1),
    ('icmpTypeIPv6', 178, 'unsigned8', 1),
    ('icmpCodeIPv6', 179, 'unsigned8', 1),
    ('udpSourcePort', 180, 'unsigned16', 2),
    ('udpDestinationPort', 181, 'unsigned16', 2),
    ('tcpSourcePort', 182, 'unsigned16', 2),
    ('tcpDestinationPort', 183, 'unsigned16', 2),
    ('tcpSequenceNumber', 184, 'unsigned32', 4),
    ('tcpAcknowledgementNumber', 185, 'unsigned32', 4),
    ('tcpWindowSize', 186, 'unsigned16', 2),
    ('tcpUrgentPointer', 187, 'unsigned16', 2),
    ('tcpHeaderLength', 188, 'unsigned8', 1),
    ('ipHeaderLength', 189, 'unsigned8', 1),
    ('totalLengthIPv4', 190, 'unsigned16', 2),
    ('payloadLengthIPv6', 191, 'unsigned16', 2),
    ('ipTTL', 192, 'unsigned8', 1),
    ('nextHeaderIPv6', 193, 'unsigned8', 1),
    ('mplsPayloadLength', 194, 'unsigned32', 4),
    ('ipDiffServCodePoint', 195, 'unsigned8', 1),
    ('ipPrecedence', 196, 'unsigned8', 1),
    ('fragmentFlags', 197, 'unsigned8', 1),
    ('octetDeltaSumOfSquares', 198, 'unsigned64', 8),
    ('octetTotalSumOfSquares', 199, 'unsigned64', 8),
    ('mplsTopLabelTTL', 200, 'unsigned8', 1),
    ('mplsLabelStackLength', 201, 'unsigned32', 4),
    ('mplsLabelStackDepth', 202, 'unsigned32', 4),
    ('mplsTopLabelExp', 203, 'unsigned8', 1),
    ('ipPayloadLength', 204, 'unsigned32', 4),
    ('udpMessageLength', 205, 'unsigned16', 2),
    ('isMulticast', 206, 'unsigned8', 1),
    ('ipv4IHL', 207, 'unsigned8', 1),
    ('ipv4Options', 208, 'unsigned32', 4),
    ('tcpOptions', 209, 'unsigned64', 8),
    ('paddingOctets', 210, 'octetArray', 65535),
    ('collectorIPv4Address', 211, 'ipv4Address', 4),
    ('collectorIPv6Address', 212, 'ipv6Address', 16),
    ('exportInterface', 213, 'unsigned32', 4),
    ('exportProtocolVersion', 214, 'unsigned8', 1),
    ('exportTransportProtocol', 215, 'unsigned8', 1),
    ('collectorTransportPort', 216, 'unsigned16', 2),
    ('exporterTransportPort', 217, 'unsigned16', 2),
    ('tcpSynTotalCount', 218, 'unsigned64', 8),
    ('tcpFinTotalCount', 219, 'unsigned64', 8),
    ('tcpRstTotalCount', 220, 'unsigned64', 8),
    ('tcpPshTotalCount', 221, 'unsigned64', 8),
    ('tcpAckTotalCount', 222, 'unsigned64', 8),
    ('tcpUrgTotalCount', 223, 'unsigned64', 8),
    ('ipTotalLength', 224, 'unsigned64', 8),
    ('postNATSourceIPv4Address', 225, 'ipv4Address', 4),
    ('postNATDestinationIPv4Address', 226, 'ipv4Address', 4),
    ('postNAPTSourceTransportPort', 227, 'unsigned16', 2),
    ('postNAPTDestinationTransportPort', 228, 'unsigned16', 2),
    ('natOriginatingAddressRealm', 229, 'unsigned8', 1),
    ('natEvent', 230, 'unsigned8', 1),
    ('initiatorOctets', 231, 'unsigned64', 8),
    ('responderOctets', 232, 'unsigned64', 8),
    ('firewallEvent', 233, 'unsigned8', 1),
    ('ingressVRFID', 234, 'unsigned32', 4),
    ('egressVRFID', 235, 'unsigned32', 4),
    ('VRFname', 236, 'string', 65535),
    ('postMplsTopLabelExp', 237, 'unsigned8', 1),
    ('tcpWindowScale', 238, 'unsigned16', 2),
    ('biflowDirection', 239, 'unsigned8', 1),
    ('ethernetHeaderLength', 240, 'unsigned8', 1),
    ('ethernetPayloadLength', 241, 'unsigned16', 2),
    ('ethernetTotalLength', 242, 'unsigned16', 2),
    ('dot1qVlanId', 243, 'unsigned16', 2),
    ('dot1qPriority', 244, 'unsigned8', 1),
    ('dot1qCustomerVlanId', 245, 'unsigned16', 2),
    ('dot1qCustomerPriority', 246, 'unsigned8', 1),
    ('metroEvcId', 247, 'string', 65535),
    ('metroEvcType', 248, 'unsigned8', 1),
    ('pseudoWireId', 249, 'unsigned32', 4),
    ('pseudoWireType', 250, 'unsigned16', 2),
    ('pseudoWireControlWord', 251, 'unsigned32', 4),
    ('ingressPhysicalInterface', 252, 'unsigned32', 4),
    ('egressPhysicalInterface', 253, 'unsigned32', 4),
    ('postDot1qVlanId', 254, 'unsigned16', 2),
    ('postDot1qCustomerVlanId', 255, 'unsigned16', 2),
    ('ethernetType', 256, 'unsigned16', 2),
    ('postIpPrecedence', 257, 'unsigned8', 1),
    ('collectionTimeMilliseconds', 258, 'dateTimeMilliseconds', 8),
    ('exportSctpStreamId', 259, 'unsigned16', 2),
    ('maxExportSeconds', 260, 'dateTimeSeconds', 4),
    ('maxFlowEndSeconds', 261, 'dateTimeSeconds', 4),
    ('messageMD5Checksum', 262, 'octetArray', 65535),
    ('messageScope', 263, 'unsigned8', 1),
    ('minExportSeconds', 264, 'dateTimeSeconds', 4),
    ('minFlowStartSeconds', 265, 'dateTimeSeconds', 4),
    ('opaqueOctets', 266, 'octetArray', 65535),
    ('sessionScope', 267, 'unsigned8', 1),
    ('maxFlowEndMicroseconds', 268, 'dateTimeMicroseconds', 8),
    ('maxFlowEndMilliseconds', 269, 'dateTimeMilliseconds', 8),
    ('maxFlowEndNanoseconds', 270, 'dateTimeNanoseconds', 8),
    ('minFlowStartMicroseconds', 271, 'dateTimeMicroseconds', 8),
    ('minFlowStartMilliseconds', 272, 'dateTimeMilliseconds', 8),
    ('minFlowStartNanoseconds', 273, 'dateTimeNanoseconds', 8),
    ('collectorCertificate', 274, 'octetArray', 65535),
    ('exporterCertificate', 275, 'octetArray', 65535),
    ('dataRecordsReliability', 276, 'boolean', 1),
    ('observationPointType', 277, 'unsigned8', 1),
    ('connectionCountNew', 278, 'unsigned32', 4),
    ('connectionSumDurationSeconds', 279, 'unsigned64', 8),
    ('connectionTransactionId', 280, 'unsigned64', 8),
    ('postNATSourceIPv6Address', 281, 'ipv6Address', 16),
    ('postNATDestinationIPv6Address', 282, 'ipv6Address', 16),
    ('natPoolId', 283, 'unsigned32', 4),
    ('natPoolName', 284, 'string', 65535),
    ('anonymizationFlags', 285, 'unsigned16', 2),
    ('anonymizationTechnique', 286, 'unsigned16', 2),
    ('informationElementIndex', 287, 'unsigned16', 2),
    ('p2pTechnology', 288, 'string', 65535),
    ('tunnelTechnology', 289, 'string', 65535),
    ('encryptedTechnology', 290, 'string', 65535),
    ('RESERVED291', 291, 'octetArray', 65536),
    ('RESERVED292', 292, 'octetArray', 65536),
    ('RESERVED293', 293, 'octetArray', 65536),
    ('bgpValidityState', 294, 'unsigned8', 1),
    ('IPSecSPI', 295, 'unsigned32', 4),
    ('greKey', 296, 'unsigned32', 4),
    ('natType', 297, 'unsigned8', 1),
    ('initiatorPackets', 298, 'unsigned64', 8),
    ('responderPackets', 299, 'unsigned64', 8),
    ('observationDomainName', 300, 'string', 65535),
    ('selectionSequenceId', 301, 'unsigned64', 8),
    ('selectorId', 302, 'unsigned64', 8),
    ('informationElementId', 303, 'unsigned16', 2),
    ('selectorAlgorithm', 304, 'unsigned16', 2),
    ('samplingPacketInterval', 305, 'unsigned32', 4),
    ('samplingPacketSpace', 306, 'unsigned32', 4),
    ('samplingTimeInterval', 307, 'unsigned32', 4),
    ('samplingTimeSpace', 308, 'unsigned32', 4),
    ('samplingSize', 309, 'unsigned32', 4),
    ('samplingPopulation', 310, 'unsigned32', 4),
    ('samplingProbability', 311, 'float64', 8),
    ('dataLinkFrameSize', 312, 'unsigned16', 2),
    ('ipHeaderPacketSection', 313, 'octetArray', 65535),
    ('ipPayloadPacketSection', 314, 'octetArray', 65535),
    ('dataLinkFrameSection', 315, 'octetArray', 65535),
    ('mplsLabelStackSection', 316, 'octetArray', 65535),
    ('mplsPayloadPacketSection', 317, 'octetArray', 65535),
    ('selectorIdTotalPktsObserved', 318, 'unsigned64', 8),
    ('selectorIdTotalPktsSelected', 319, 'unsigned64', 8),
    ('absoluteError', 320, 'float64', 8),
    ('relativeError', 321, 'float64', 8),
    ('observationTimeSeconds', 322, 'dateTimeSeconds', 4),
    ('observationTimeMilliseconds', 323, 'dateTimeMilliseconds', 8),
    ('observationTimeMicroseconds', 324, 'dateTimeMicroseconds', 8),
    ('observationTimeNanoseconds', 325, 'dateTimeNanoseconds', 8),
    ('digestHashValue', 326, 'unsigned64', 8),
    ('hashIPPayloadOffset', 327, 'unsigned64', 8),
    ('hashIPPayloadSize', 328, 'unsigned64', 8),
    ('hashOutputRangeMin', 329, 'unsigned64', 8),
    ('hashOutputRangeMax', 330, 'unsigned64', 8),
    ('hashSelectedRangeMin', 331, 'unsigned64', 8),
    ('hashSelectedRangeMax', 332, 'unsigned64', 8),
    ('hashDigestOutput', 333, 'boolean', 1),
    ('hashInitialiserValue', 334, 'unsigned64', 8),
    ('selectorName', 335, 'string', 65535),
    ('upperCILimit', 336, 'float64', 8),
    ('lowerCILimit', 337, 'float64', 8),
    ('confidenceLevel', 338, 'float64', 8),
    ('informationElementDataType', 339, 'unsigned8', 1),
    ('informationElementDescription', 340, 'string', 65535),
    ('informationElementName', 341, 'string', 65535),
    ('informationElementRangeBegin', 342, 'unsigned64', 8),
    ('informationElementRangeEnd', 343, 'unsigned64', 8),
    ('informationElementSemantics', 344, 'unsigned8', 1),
    ('informationElementUnits', 345, 'unsigned16', 2),
    ('privateEnterpriseNumber', 346, 'unsigned32', 4),
    ('virtualStationInterfaceId', 347, 'octetArray', 65535),
    ('virtualStationInterfaceName', 348, 'string', 65535),
    ('virtualStationUUID', 349, 'octetArray', 65535),
    ('virtualStationName', 350, 'string', 65535),
    ('layer2SegmentId', 351, 'unsigned64', 8),
    ('layer2OctetDeltaCount', 352, 'unsigned64', 8),
    ('layer2OctetTotalCount', 353, 'unsigned64', 8),
    ('ingressUnicastPacketTotalCount', 354, 'unsigned64', 8),
    ('ingressMulticastPacketTotalCount', 355, 'unsigned64', 8),
    ('ingressBroadcastPacketTotalCount', 356, 'unsigned64', 8),
    ('egressUnicastPacketTotalCount', 357, 'unsigned64', 8),
    ('egressBroadcastPacketTotalCount', 358, 'unsigned64', 8),
    ('monitoringIntervalStartMilliSeconds', 359, 'dateTimeMilliseconds', 8),
    ('monitoringIntervalEndMilliSeconds', 360, 'dateTimeMilliseconds', 8),
    ('portRangeStart', 361, 'unsigned16', 2),
    ('portRangeEnd', 362, 'unsigned16', 2),
    ('portRangeStepSize', 363, 'unsigned16', 2),
    ('portRangeNumPorts', 364, 'unsigned16', 2),
    ('staMacAddress', 365, 'macAddress', 6),
    ('staIPv4Address', 366, 'ipv4Address', 4),
    ('wtpMacAddress', 367, 'macAddress', 6),
    ('ingressInterfaceType', 368, 'unsigned32', 4),
    ('egressInterfaceType', 369, 'unsigned32', 4),
    ('rtpSequenceNumber', 370, 'unsigned16', 2),
    ('userName', 371, 'string', 65535),
    ('applicationCategoryName', 372, 'string', 65535),
    ('applicationSubCategoryName', 373, 'string', 65535),
    ('applicationGroupName', 374, 'string', 65535),
    ('originalFlowsPresent', 375, 'unsigned64', 8),
    ('originalFlowsInitiated', 376, 'unsigned64', 8),
    ('originalFlowsCompleted', 377, 'unsigned64', 8),
    ('distinctCountOfSourceIPAddress', 378, 'unsigned64', 8),
    ('distinctCountOfDestinationIPAddress', 379, 'unsigned64', 8),
    ('distinctCountOfSourceIPv4Address', 380, 'unsigned32', 4),
    ('distinctCountOfDestinationIPv4Address', 381, 'unsigned32', 4),
    ('distinctCountOfSourceIPv6Address', 382, 'unsigned64', 8),
    ('distinctCountOfDestinationIPv6Address', 383, 'unsigned64', 8),
    ('valueDistributionMethod', 384, 'unsigned8', 1),
    ('rfc3550JitterMilliseconds', 385, 'unsigned32', 4),
    ('rfc3550JitterMicroseconds', 386, 'unsigned32', 4),
    ('rfc3550JitterNanoseconds', 387, 'unsigned32', 4),
    ('dot1qDEI', 388, 'boolean', 1),
    ('dot1qCustomerDEI', 389, 'boolean', 1),
    ('flowSelectorAlgorithm', 390, 'unsigned16', 2),
    ('flowSelectedOctetDeltaCount', 391, 'unsigned64', 8),
    ('flowSelectedPacketDeltaCount', 392, 'unsigned64', 8),
    ('flowSelectedFlowDeltaCount', 393, 'unsigned64', 8),
    ('selectorIDTotalFlowsObserved', 394, 'unsigned64', 8),
    ('selectorIDTotalFlowsSelected', 395, 'unsigned64', 8),
    ('samplingFlowInterval', 396, 'unsigned64', 8),
    ('samplingFlowSpacing', 397, 'unsigned64', 8),
    ('flowSamplingTimeInterval', 398, 'unsigned64', 8),
    ('flowSamplingTimeSpacing', 399, 'unsigned64', 8),
    ('hashFlowDomain', 400, 'unsigned16', 2),
    ('transportOctetDeltaCount', 401, 'unsigned64', 8),
    ('transportPacketDeltaCount', 402, 'unsigned64', 8),
    ('originalExporterIPv4Address', 403, 'ipv4Address', 4),
    ('originalExporterIPv6Address', 404, 'ipv6Address', 16),
    ('originalObservationDomainId', 405, 'unsigned32', 4),
    ('intermediateProcessId', 406, 'unsigned32', 4),
    ('ignoredDataRecordTotalCount', 407, 'unsigned64', 8),
    ('dataLinkFrameType', 408, 'unsigned16', 2),
    ('sectionOffset', 409, 'unsigned16', 2),
    ('sectionExportedOctets', 410, 'unsigned16', 2),
    ('dot1qServiceInstanceTag', 411, 'octetArray', 65535),
    ('dot1qServiceInstanceId', 412, 'unsigned32', 4),
    ('dot1qServiceInstancePriority', 413, 'unsigned8', 1),
    ('dot1qCustomerSourceMacAddress', 414, 'macAddress', 6),
    ('dot1qCustomerDestinationMacAddress', 415, 'macAddress', 6),
    ('RESERVED416', 416, 'octetArray', 65536),
    ('postLayer2OctetDeltaCount', 417, 'unsigned64', 8),
    ('postMCastLayer2OctetDeltaCount', 418, 'unsigned64', 8),
    ('RESERVED419', 419, 'octetArray', 65536),
    ('postLayer2OctetTotalCount', 420, 'unsigned64', 8),
    ('postMCastLayer2OctetTotalCount', 421, 'unsigned64', 8),
    ('minimumLayer2TotalLength', 422, 'unsigned64', 8),
    ('maximumLayer2TotalLength', 423, 'unsigned64', 8),
    ('droppedLayer2OctetDeltaCount', 424, 'unsigned64', 8),
    ('droppedLayer2OctetTotalCount', 425, 'unsigned64', 8),
    ('ignoredLayer2OctetTotalCount', 426, 'unsigned64', 8),
    ('notSentLayer2OctetTotalCount', 427, 'unsigned64', 8),
    ('layer2OctetDeltaSumOfSquares', 428, 'unsigned64', 8),
    ('layer2OctetTotalSumOfSquares', 429, 'unsigned64', 8),
    ('layer2FrameDeltaCount', 430, 'unsigned64', 8),
    ('layer2FrameTotalCount', 431, 'unsigned64', 8),
    ('pseudoWireDestinationIPv4Address', 432, 'ipv4Address', 4)
]
