# encoding: utf-8

import struct, logging

from ipfix import MSG_HEADER_LEN, SET_HEADER_LEN
from ipfix import MSG_VER, MSG_LEN, MSG_EXP_TIME, MSG_SEQ_NUM, MSG_OB_DOM_ID, SET_LEN
from ipfix._field import format_time
from ipfix._obj import VisitObj, VisitList
from ipfix._set import ipfix_create_set_obj


class IpfixMsgHdr(VisitObj):
    
    def __init__(self, offset, buff, wrap_frame, **kwargs):
        super(IpfixMsgHdr, self).__init__(offset)
        self.wrap_frame = wrap_frame

        vals = struct.unpack_from('>HHIII', buff)
        self[MSG_VER] = vals[0]
        self[MSG_LEN] = vals[1]
        self[MSG_EXP_TIME] = format_time(vals[2], 1, 0)
        self[MSG_OB_DOM_ID] = vals[4]
        
        if self.check_level(logging.INFO, **kwargs):
            self[MSG_SEQ_NUM] = vals[3]

        if self.check_debug(**kwargs):
            self.debug_print_items()
        
    def body_offset(self):
        return self.offset(MSG_HEADER_LEN)

    def body_len(self):
        return self[MSG_LEN] - MSG_HEADER_LEN

    def can_visit(self, **kwargs):
        return not self.is_hide_frame(**kwargs)


class IpfixMsg(VisitList):
          
    def __init__(self, header, buff, **kwargs):
        super(IpfixMsg, self).__init__(header.body_offset())
        
        self.header = header
        self.source_id = header[MSG_OB_DOM_ID]
        self.buff = buff
        self.parse(**kwargs)
        
    def parse(self, **kwargs):
        pos = 0
        limit = len(self.buff)
              
        def remaining():
            return limit - pos

        apply_v9_field = kwargs.get("apply_v9_field", False)

        self.reset_children()
        while remaining() >= SET_HEADER_LEN:
            set_id, = struct.unpack_from('>H', self.buff, pos)
            # check truncate case for next is not a set but a V9 Packet
            if set_id == 10:
                break

            obj = ipfix_create_set_obj(set_id, self.offset(pos), self.source_id, apply_v9_field)
            try:
                obj.parse(self.buff, pos, **kwargs)
            except Exception, e:
                import traceback
                print traceback.format_exc()

                raise e
                self.log(logging.warn, 'IPFIX failed to parse message, error: %s. set_id=%d'
                         % (str(e), set_id))
            
            self.add_child(obj)
            pos = pos + obj[SET_LEN]
            
        if remaining() > 0:
            raise Exception('Found %d remaining message bytes, offset=0x%x' % 
                            (self.remaining(limit, pos), self.offset(pos)))
        
    def do_visit(self, prefix, result, **kwargs):
        self.header.visit(prefix, result, **kwargs)

    def do_visit_children(self, prefix, result, **kwargs):
        for obj in self.children:
            obj.visit(prefix, result, **kwargs)
