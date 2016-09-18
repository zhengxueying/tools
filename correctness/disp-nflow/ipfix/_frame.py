# encoding: utf-8

from ipfix import WRAP_TIME, WRAP_LEN1, WRAP_LEN2, WRAP_SRC_IP
from _obj import VisitObj
import struct


WRAP_FRAME_HDR_LEN = 32


class WrapFrameObj(VisitObj):
    
    def __init__(self, offset, buff):
        super(WrapFrameObj, self).__init__(offset)

        vals = struct.unpack("<LLLLLLLL", buff)
        self[WRAP_TIME] = float(vals[0]) + (vals[1] / 1000000000.0)
        self[WRAP_LEN1] = vals[2]
        self[WRAP_LEN2] = vals[3]
        self[WRAP_SRC_IP] = vals[4]

    def can_visit(self, **kwargs):
        return kwargs.get("show_wrap_frame", False)

    def is_valid(self):
        return self[WRAP_LEN1] == self[WRAP_LEN2]

    def wrap_message_length(self):
        return self[WRAP_LEN2]

    def wrap_source_ip(self):
        return self[WRAP_SRC_IP]