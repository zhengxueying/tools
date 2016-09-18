# encoding: utf-8

import struct, logging

from ipfix import PKT_V5_HEADER_LEN, REC_V5_REC_LEN
from ipfix import PKT_VER, PKT_SET_CNT, PKT_SYS_UPTIME, PKT_SECS, PKT_NSECS, PKT_FLOW_SEQ, \
    PKT_ENG_TYPE, PKT_ENG_ID, PKT_SAMPLE_INTERVAL, PKT_EXP_TIME
from ipfix._field import format_time
from ipfix._obj import VisitObj, VisitList


class Nflow5PktHdr(VisitObj):

    def __init__(self, offset, buff, wrap_frame, **kwargs):
        super(Nflow5PktHdr, self).__init__(offset)
        self.wrap_frame = wrap_frame

        vals = struct.unpack_from('>HHIIIIBBH', buff, 0)
        self[PKT_VER] = vals[0]
        self[PKT_SET_CNT] = vals[1]
        self[PKT_EXP_TIME] = format_time(vals[3], 1, 0)

        if self.check_level(logging.INFO, **kwargs):
            self[PKT_SYS_UPTIME] = vals[2]
            self[PKT_FLOW_SEQ] = vals[5]

        if self.check_level(logging.DEBUG, **kwargs):
            self[PKT_SECS] = vals[3]
            self[PKT_NSECS] = vals[4]
            self[PKT_ENG_TYPE] = vals[6]
            self[PKT_ENG_ID] = vals[7]
            self[PKT_SAMPLE_INTERVAL] = vals[8]

        self._body_len = len(buff) - PKT_V5_HEADER_LEN

        if self.check_debug(**kwargs):
            self.debug_print_items()

    def body_offset(self):
        return self.offset(PKT_V5_HEADER_LEN)

    def body_set_count(self):
        return self[PKT_SET_CNT]

    def do_visit(self, prefix, result, **kwargs):
        if self.wrap_frame:
            self.wrap_frame.visit(prefix, result, **kwargs)
            if self.wrap_frame.can_visit( **kwargs):
                prefix = " " * len(prefix)
        super(Nflow5PktHdr, self).do_visit(prefix, result, **kwargs)


class Nflow5Pkt(VisitList):

    def __init__(self, header, fn_read, **kwargs):
        super(Nflow5Pkt, self).__init__(header.body_offset())
        
        self.header = header
        self.body_len = 0
        self.fn_read = fn_read
        self.parse(**kwargs)

    def parse(self, **kwargs):
        index = 0
        count = self.header.body_set_count()

        self.reset_children()
        while index < count:
            buff = self.fn_read(REC_V5_REC_LEN)
            l = len(buff)
            if l == 0:
                # no more bytes, just STOP
                break 
            if l != REC_V5_REC_LEN:
                raise Exception('Failed to read %d bytes (%d bytes available) for v5 packet record index=%d in total=%d, offset=%d' % 
                            (REC_V5_REC_LEN, l, index, count, self.offset(self.body_len)))

            obj = Nflow5Rec(self.offset(self.body_len))
            obj.parse(buff, 0, **kwargs)

            if self.check_debug(**kwargs):
                obj.debug_print_items()
                obj.visit("  ==> #%d(%d)," % (index, count), {}, **kwargs)
                
            if obj.export:
                self.add_child(obj)
            self.body_len = self.body_len + REC_V5_REC_LEN
            index += 1

    def do_visit(self, prefix, result, **kwargs):
        self.header.visit(prefix, result, **kwargs)


def _get_byte(value, byteIndex):
    return (value >> (byteIndex * 8)) & 0xff


def get_ip_text(value):
    return "%s.%s.%s.%s" % (
            _get_byte(value, 3), _get_byte(value, 2), _get_byte(value, 1), _get_byte(value, 0))


class Nflow5Rec(VisitObj):
    
    def __init__(self, offset):
        super(Nflow5Rec, self).__init__(offset)
        self.export = True
        
    def parse(self, buff, pos, **kwargs):
        ip_filter = kwargs.get("ip_filter", "")
        if ip_filter:
            self.export = False
        else:
            self.export = True
            
        vals = struct.unpack_from('>IIIHHIIIIHHBBBBHHBBH', buff, pos)

        self['srcaddr'] = get_ip_text(vals[0])
        self['dstaddr'] = get_ip_text(vals[1])
        self['dPkts'] = vals[5]
        self['dOctets'] = vals[6]
        self['srcport'] = vals[9]
        self['dstport'] = vals[10]
        self['prot'] = vals[13]
        
        if ip_filter:
            self.export = (ip_filter in self['srcaddr']) or  (ip_filter in self['dstaddr'])

        if kwargs.get('show_all_fields', False):
            self['nexthop'] = vals[2]
            self['input'] = vals[3]
            self['output'] = vals[4]
            start, last = vals[7], vals[8]
            self['first'] = start
            self['last'] = last
            self['tcp_flags'] = vals[12]
            self['tos'] = vals[14]
            self['src_as'] = vals[15]
            self['dst_as'] = vals[16]
            self['src_mask'] = vals[17]
            self['dst_mask'] = vals[18]
            self['pad1'] = vals[11]
            self['pad2'] = vals[19]
