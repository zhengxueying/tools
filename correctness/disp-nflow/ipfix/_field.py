# encoding: utf-8

import datetime
import struct
import logging

from ipfix import REC_IDX, FLD_IDX, FLD_NAME, FLD_TYPE, FLD_LEN, FLD_VAL, KEY_FIELD_DEF, FLD_ID
from ipfix._appiddef import get_app_name
from ipfix._obj import VisitObj


APPLICATION_ID = 95


class IpfixField(VisitObj):
    
    def __init__(self, offset):
        super(IpfixField, self).__init__(offset)
        
    def parse(self, buff, pos, **kwargs):
        self[REC_IDX] = kwargs[REC_IDX]
        self[FLD_IDX] = kwargs[FLD_IDX]
        
        field_def = kwargs[KEY_FIELD_DEF]
        self[FLD_NAME] = field_def[FLD_NAME]
        self[FLD_TYPE] = field_def[FLD_TYPE]
        self[FLD_LEN] = field_def[FLD_LEN]
        
        field_id = field_def[FLD_ID]
        try:
            if field_id == APPLICATION_ID:
                val = self._parse_app_id(buff, pos, field_def[FLD_TYPE], field_def[FLD_LEN])
                if not kwargs.get('disable_app_trans', False):
                    val = get_app_name(val)
            else:
                val = self.parse_value(buff, pos, field_def[FLD_TYPE], field_def[FLD_LEN])
            self[FLD_VAL] = str(val)
        except Exception, e:
            if self.check_debug(**kwargs):
                self.log(logging.debug, 'IPFIX failed to parse field, error: %s. rec=%s, field={id=%s, index=%s, name=%s, type=%s, len=%s}'
                             % (str(e), self[REC_IDX], field_id, self[FLD_IDX], self[FLD_NAME], self[FLD_TYPE], self[FLD_LEN]))
            self[FLD_VAL] = "ValueError"
        
        if self.check_debug(**kwargs):
            self.debug_print_items()
        
        return field_def[FLD_LEN]

    def _parse_app_id(self, buff, pos, field_type, field_len):
        if field_len == 4:
            v = struct.unpack_from('>BBBB', buff, pos)
            part2 = (v[1] * 16 + v[2]) * 16 + v[3]
            return "%d:%d" % (v[0], part2) 
        else:
            v = []
            for i in xrange(field_len):
                c = struct.unpack_from('>B', buff, pos + i)[0]
                v.append('%02x' % c)
            return ''.join(v)

    def parse_value(self, buff, pos, field_type, field_len):
        def _unsigned():
            v = 0
            for i in xrange(field_len):
                c = struct.unpack_from('>B', buff, pos + i)[0]
                v = v * 10 + c
            return v
        def _singed():
            v = 0
            for i in xrange(field_len):
                c = struct.unpack_from('>B', buff, pos + i)[0]
                v = v * 10 + c
            return v        
        
        if field_type == 'unsigned8':
            return struct.unpack_from('>B', buff, pos)[0]
        elif field_type == 'unsigned16':
            if field_len == 2:
                return struct.unpack_from('>H', buff, pos)[0]
            elif field_len == 4:
                return struct.unpack_from('>I', buff, pos)[0]
            else:
                return _unsigned()
        elif field_type == 'unsigned32':
            if field_len == 4:
                return struct.unpack_from('>I', buff, pos)[0]
            elif field_len == 8:
                return struct.unpack_from('>Q', buff, pos)[0]
            else:
                return _unsigned()
        elif field_type == 'unsigned64':
            if field_len == 8:
                return struct.unpack_from('>Q', buff, pos)[0]
            elif field_len == 4:
                return struct.unpack_from('>I', buff, pos)[0]
            else:
                return _unsigned()
        elif field_type == 'signed8':
            return struct.unpack_from('>b', buff, pos)[0]
        elif field_type == 'signed16':
            if field_len == 2:
                return struct.unpack_from('>h', buff, pos)[0]
            elif field_len == 4:
                return struct.unpack_from('>i', buff, pos)[0]
            else:
                return _singed()
        elif field_type == 'signed32':
            if field_len == 4:
                return struct.unpack_from('>i', buff, pos)[0]
            elif field_len == 8:
                return struct.unpack_from('>q', buff, pos)[0]
            else:
                return _singed()
        elif field_type == 'signed64':
            if field_len == 8:
                return struct.unpack_from('>q', buff, pos)[0]
            elif field_len == 4:
                return struct.unpack_from('>i', buff, pos)[0]
            else:
                return _singed()
        elif field_type == 'float32':
            return struct.unpack_from('>f', buff, pos)[0]
        elif field_type == 'float64':
            return struct.unpack_from('>d', buff, pos)[0]
        elif field_type == 'boolean':
            return struct.unpack_from('>?', buff, pos)[0]
        elif field_type == 'macAddress':
            v = struct.unpack_from('>BBBBBB', buff, pos)
            return "%x:%x:%x:%x:%x:%x" % (v[0], v[1], v[2], v[3], v[4], v[5])
        elif field_type == 'octetArray':
            v = []
            for i in xrange(field_len):
                c = struct.unpack_from('>B', buff, pos + i)[0]
                v.append('%02x' % c)
            return ''.join(v)
        elif field_type == 'string':
            return struct.unpack_from('>%ds' % field_len, buff, pos)[0]
        elif field_type == 'dateTimeSeconds':
            v = struct.unpack_from('>I', buff, pos)
            return format_time(v, 1, 0)
        elif field_type == 'dateTimeMilliseconds':
            v = struct.unpack_from('>Q', buff, pos)[0]
            return format_time(v, 1000.0, 3)
        elif field_type == 'dateTimeMicroseconds':
            v = struct.unpack_from('>Q', buff, pos)[0]
            return format_time(v, 1000000.0, 6)
        elif field_type == 'dateTimeNanoseconds':
            v = struct.unpack_from('>Q', buff, pos)[0]
            return format_time(v, 1000000000.0, 9)
        elif field_type == 'ipv4Address':
            v = struct.unpack_from('>BBBB', buff, pos)
            return "%d.%d.%d.%d" % v
        elif field_type == 'ipv6Address':
            v = []
            for i in xrange(field_len):
                c = struct.unpack_from('>%B', buff, pos + i)[0]
                v.append('%02x' % c)
            return ':'.join(v)
        
        raise Exception('Invalid %s=%s with %s=%d' % (FLD_TYPE, field_type, FLD_LEN, field_len))
        

APPLY_UTC = True
UTC_FMT = "%Y-%m-%dT%H:%M:%S"


def format_time(epoch, factor, num):
    if APPLY_UTC:
        return format_utc_time(epoch, factor, num)
    else:
        return format_iso_time(epoch, factor, num)


def format_utc_time(epoch, factor, num):
    dt = datetime.datetime.utcfromtimestamp(epoch / factor)
    if num == 0:
        return "%s" % dt.strftime(UTC_FMT)
    else:
        return ("%%s.%%0%du" % num) % (dt.strftime(UTC_FMT), dt.microsecond / factor)


def format_iso_time(epoch, factor, num):
    if num == 0:
        return "%s" % datetime.datetime.fromtimestamp(epoch).isoformat()
    else:
        s = epoch / factor
        ss = epoch % factor
        return ("%%s.%%0%du" % num) % (datetime.datetime.fromtimestamp(s).isoformat(), ss)
