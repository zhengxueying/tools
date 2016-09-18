# encoding: utf-8

import struct, logging

from ipfix import PKT_V9_HEADER_LEN
from ipfix import PKT_VER, PKT_SET_CNT, PKT_SYS_UPTIME, PKT_SECS, PKT_PKG_SEQ, PKT_SOURCE_ID, PKT_EXP_TIME
from ipfix._field import format_time
from ipfix._obj import VisitObj, VisitList
from ipfix._set import ipfix_create_set_obj


class Nflow9PktHdr(VisitObj):

    def __init__(self, offset, buff, wrap_frame, **kwargs):
        super(Nflow9PktHdr, self).__init__(offset)
        self.wrap_frame = wrap_frame

        vals = struct.unpack_from('>HHIIII', buff)
        self[PKT_VER] = vals[0]
        self[PKT_SET_CNT] = vals[1]
        self[PKT_EXP_TIME] = format_time(vals[3], 1, 0)
        self[PKT_SOURCE_ID] = vals[5]

        if self.check_level(logging.INFO, **kwargs):
            self[PKT_SYS_UPTIME] = vals[2]
            self[PKT_PKG_SEQ] = vals[4]

        if self.check_level(logging.DEBUG, **kwargs):
            self[PKT_SECS] = vals[3]

        self._body_len = len(buff) - PKT_V9_HEADER_LEN

        if self.check_debug(**kwargs):
            self.debug_print_items()

    def body_offset(self):
        return self.offset(PKT_V9_HEADER_LEN)

    def body_set_count(self):
        return self[PKT_SET_CNT]

    def do_visit(self, prefix, result, **kwargs):
        if self.wrap_frame:
            self.wrap_frame.visit(prefix, result, **kwargs)
            if self.wrap_frame.can_visit( **kwargs):
                prefix = " " * len(prefix)
        super(Nflow9PktHdr, self).do_visit(prefix, result, **kwargs)


class Nflow9Pkt(VisitList):

    def __init__(self, header, fn_read, fn_seek, **kwargs):
        super(Nflow9Pkt, self).__init__(header.body_offset())

        self.header = header
        self.source_id = header[PKT_SOURCE_ID]
        self.body_len = 0
        self.fn_read = fn_read
        self.fn_seek = fn_seek
        self.parse(**kwargs)

    def parse(self, **kwargs):
        count = self.header.body_set_count()
        if self.header.wrap_frame:
            expected_body_length = self.header.wrap_frame.wrap_message_length() - PKT_V9_HEADER_LEN
        else:
            expected_body_length = 0

        apply_v9_field = kwargs.get("apply_v9_field", False)
        self.reset_children()
        index = 0
        while index < count:
            if self.body_len >= expected_body_length > 0:
                break

            byte4 = self.fn_read(4)
            l = len(byte4)
            if l == 0:
                # no more bytes, just STOP
                break
            if l != 4:
                raise Exception('Failed to read 4 bytes (%d bytes available) for the ID and length of the flow set index=%d in total=%d, offset=%d' %
                            (l, index, count, self.offset(self.body_len)))
            set_id, set_len = struct.unpack('>HH', byte4)

            # check truncate case for next is not a set but a V9 Packet
            if set_id == 9:
                self.fn_seek(-4, 1)
                break
            obj = ipfix_create_set_obj(set_id, self.offset(self.body_len), self.source_id, apply_v9_field)

            buff = self.fn_read(set_len - 4)
            if len(buff) != set_len - 4:
                raise Exception('Failed to read %d bytes of the flow set index=%d in total=%d, ID=%d, offset=%d.' %
                            (set_len, index, count, set_id, self.offset(self.body_len)))

            try:
                obj.parse(byte4 + buff, 0, **kwargs)
            except Exception, e:
                self.log(logging.warn, 'Netflow V9 failed to parse, error: %s. set_id=%d, index=%d, count-%d'
                         % (str(e), set_id, index, count))

            if self.check_debug(**kwargs):
                obj.debug_print_items()
                obj.visit("  ==> #%d(%d)," % (index, count), {}, **kwargs)

            self.add_child(obj)
            self.body_len += set_len
            index += 1

    def do_visit(self, prefix, result, **kwargs):
        self.header.visit(prefix, result, **kwargs)
