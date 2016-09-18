# encoding: utf-8

import struct, logging

from ipfix import SET_ID, SET_LEN, SET_HEADER_LEN, SOURCE_ID, TEMP_ID, FLD_CNT, FLD_IDX, FLD_LEN, \
    KEY_FIELDS_DEF, KEY_FIELDS_LEN, SCOPE_FLD_CNT, REC_IDX, FLD_NAME, ENT_FLAG, REC_SIZE
from ipfix import SET_TYP_DATA, SET_TYP_TEMPLATE, SET_TYP_OPTIONS_TEMPLATE, \
    SET_TYP_V9_TEMPLATE, SET_TYP_V9_OPTIONS_TEMPLATE 
from ipfix._fielddef import IpfixFieldDef
from ipfix._load_template import load_template, dump_template
from ipfix._obj import VisitList
from ipfix._rec import IpfixRec
from ipfix._v9fielddef import Nflow9FieldDef


TEMPLATES = {}


def ipfix_create_set_obj(set_id, offset, source_id, apply_v9_field):
    if set_id >= SET_TYP_DATA:
        return IpfixDataSet(offset, source_id)
    elif set_id == SET_TYP_TEMPLATE:
        return IpfixTemplateSet(offset, source_id, IpfixFieldDef, True)
    elif set_id == SET_TYP_OPTIONS_TEMPLATE:
        return IpfixOptionsTemplateSet(offset, source_id, IpfixFieldDef, True)
    elif set_id == SET_TYP_V9_TEMPLATE:
        field_def = Nflow9FieldDef if apply_v9_field else IpfixFieldDef
        return IpfixTemplateSet(offset, source_id, field_def, False)
    elif set_id == SET_TYP_V9_OPTIONS_TEMPLATE:
        field_def = Nflow9FieldDef if apply_v9_field else IpfixFieldDef
        return IpfixOptionsTemplateSet(offset, source_id, field_def, False)

    raise Exception('Found invalid SetID=%d, offset=0x%x' % (set_id, offset))


def ipfix_load_template(filename, **kwargs):
    if not filename:
        return

    global TEMPLATES
    try:
        print "try to load templates from: ", filename
        with open(filename, 'r') as fp:
            count = 0
            for temp, fields in load_template(fp, **kwargs):
                TEMPLATES.update({(temp[SOURCE_ID], temp[TEMP_ID]):
                                      {KEY_FIELDS_DEF: fields, KEY_FIELDS_LEN: temp[REC_SIZE]}})
                print ".. load template=%s" % temp
                count += 1
        print "total %d templates loaded" % count

    except IOError, e1:
        raise e1
    except Exception, e:
        if kwargs.get('debug', False):
            import traceback
            print traceback.format_exc()


def ipfix_dump_template(**kwargs):
    import datetime, time, os.path
    global TEMPLATES
    try:
        name = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
        filename = '.'.join([name, "template"])
        with open(filename, 'w+') as fp:
            dump_template(fp, TEMPLATES, **kwargs)
    except IOError, e1:
        raise e1
    except Exception, e:
        if kwargs.get('debug', False):
            import traceback
            print traceback.format_exc()
            

class _IpfixSet(VisitList):
    
    def __init__(self, offset, source_id):
        super(_IpfixSet, self).__init__(offset)
        self[SOURCE_ID] = source_id
        
    def name(self):
        return 'Set'
        
    def parse(self, buff, pos, **kwargs):
        vals = struct.unpack_from('>HH', buff, pos)
        self[SET_ID] = vals[0]
        self[SET_LEN] = vals[1]
        return SET_HEADER_LEN
    
    def can_visit_self(self, **kwargs):
        return self.check_level(logging.WARN, **kwargs)
            
    def can_summary_children(self, **kwargs):
        return self.check_level(logging.ERROR, **kwargs)
        
    def can_visit_children(self, **kwargs):
        return self.check_level(logging.DEBUG, **kwargs)


TEMPLATE_HEADER_LEN = 4


class _IpfixTemplate(VisitList):

    def __init__(self, offset, source_id):
        super(_IpfixTemplate, self).__init__(offset)
        self[SOURCE_ID] = source_id

    def name(self):
        return 'Template'

    def parse(self, buff, pos, **kwargs):
        vals = struct.unpack_from('>HH', buff, pos)
        self[TEMP_ID] = vals[0]
        self[FLD_CNT] = vals[1]
        return TEMPLATE_HEADER_LEN

    def can_visit_self(self, **kwargs):
        return self.check_level(logging.WARN, **kwargs)

    def can_summary_children(self, **kwargs):
        return self.check_level(logging.ERROR, **kwargs)

    def can_visit_children(self, **kwargs):
        return self.check_level(logging.DEBUG, **kwargs)


class IpfixTemplate(_IpfixTemplate):

    # klass = IpfixFieldDef.__class__

    def __init__(self, offset, source_id, klass):
        super(IpfixTemplate, self).__init__(offset, source_id)
        self.klass = klass

    def parse(self, buff, pos, **kwargs):
        # template headers
        size = super(IpfixTemplate, self).parse(buff, pos, **kwargs)
        pos += size
        off = size

        # fields
        self.reset_children()
        fields_len = 0

        template_size = size

        for i in xrange(self[FLD_CNT]):
            obj = self.klass(self.offset(off))
            kwargs[FLD_IDX] = i + 1
            size = obj.parse(buff, pos, **kwargs)
            self.add_child(obj)
            pos += size
            off += size
            template_size += size
            fields_len += obj[FLD_LEN]

        global TEMPLATES
        TEMPLATES.update({(self[SOURCE_ID], self[TEMP_ID]): {KEY_FIELDS_DEF: self.children, KEY_FIELDS_LEN: fields_len}})

        self[KEY_FIELDS_LEN] = fields_len
        return template_size

    def can_visit(self, **kwargs):
        return kwargs.get('show_template', False)

    def do_summary_children(self, prefix, result, **kwargs):
        vals = []
        i = 1
        vals.append('Template Id=%d' % self[TEMP_ID])
        for obj in self.children:
            vals.append('%d=%s' % (i, obj[FLD_NAME]))
            i += 1
        if vals:
            self.output(self.format_prefix(prefix, **kwargs), ', '.join(vals))


class IpfixTemplateSet(_IpfixSet):

    def __init__(self, offset, source_id, klass, entFlag=True):
        super(IpfixTemplateSet, self).__init__(offset, source_id)
        self.klass = klass
        self.entFlag = entFlag

    def parse(self, buff, pos, **kwargs):
        # set header
        size = super(IpfixTemplateSet, self).parse(buff, pos, **kwargs)
        pos += size
        off = size

        remaining_size = self[SET_LEN] - size

        self.reset_children()
        kwargs[ENT_FLAG] = self.entFlag

        while remaining_size > TEMPLATE_HEADER_LEN:
            obj = IpfixTemplate(self.offset(off), self[SOURCE_ID], self.klass)
            size = obj.parse(buff, pos, **kwargs)
            self.add_child(obj)
            pos += size
            off += size
            remaining_size -= size

        return self[SET_LEN]
    
    def can_visit(self, **kwargs):
        return kwargs.get('show_template', False)
    
    def do_summary_children(self, prefix, result, **kwargs):
        for obj in self.children:
            obj.do_summary_children(prefix, result, **kwargs )


class IpfixOptionsTemplateSet(_IpfixSet):

    def __init__(self, offset, source_id, klass, entFlag):
        super(IpfixOptionsTemplateSet, self).__init__(offset, source_id)
        self.klass = klass
        self.entFlag = entFlag

    def parse(self, buff, pos, **kwargs):
        # set header
        size = super(IpfixOptionsTemplateSet, self).parse(buff, pos, **kwargs)
        pos += size
        off = size

        # template headers
        vals = struct.unpack_from('>HHH', buff, pos)
        self[TEMP_ID] = vals[0]
        self[FLD_CNT] = vals[1]
        self[SCOPE_FLD_CNT] = vals[2]
        pos += 6
        
        # fields
        self.reset_children()
        fields_len = 0
        kwargs[ENT_FLAG] = self.entFlag

        for i in xrange(self[SCOPE_FLD_CNT]):
            obj = self.klass(self.offset(off))
            kwargs[FLD_IDX] = i + 1
            size = obj.parse(buff, pos, **kwargs)
            self.add_child(obj)
            pos += size
            off += size
            fields_len += obj[FLD_LEN]
            
        for i in xrange(self[FLD_CNT] - self[SCOPE_FLD_CNT]):
            obj = self.klass(self.offset(off))
            kwargs[FLD_IDX] = self[SCOPE_FLD_CNT] + i + 1
            size = obj.parse(buff, pos, **kwargs)
            self.add_child(obj)
            pos += size
            off += size
            fields_len += obj[FLD_LEN]
        
        # handle global templates
        global TEMPLATES
        TEMPLATES.update({(self[SOURCE_ID], self[TEMP_ID]): {KEY_FIELDS_DEF: self.children, KEY_FIELDS_LEN: fields_len}})
        self[KEY_FIELDS_LEN] = fields_len
        
        return self[SET_LEN]
    
    def can_visit(self, **kwargs):
        return kwargs.get('show_template', False)

    def do_summary_children(self, prefix, result, **kwargs):
        vals = []
        i = 1
        for obj in self.children:
            vals.append('%d=%s' % (i, obj[FLD_NAME]))
            i += 1
        if vals:
            self.output(self.format_prefix(prefix, **kwargs), ', '.join(vals))
 
    
class IpfixDataSet(_IpfixSet):
    
    def parse(self, buff, pos, **kwargs):
        # set header
        vals = struct.unpack_from('>HH', buff, pos)
        
        self[TEMP_ID] = vals[0]
        self[SET_LEN] = vals[1]
        size = 4

        if self[TEMP_ID] == 0:
            raise Exception('template')
       
        # handle global templates
        global TEMPLATES
        template = TEMPLATES.get((self[SOURCE_ID], self[TEMP_ID]))
        if not template:
            if self.check_debug(**kwargs):
                self.direct_print('%s=%d, %s=%d not defined, Offset=0x%x' %
                                  (SOURCE_ID, self[SOURCE_ID], TEMP_ID, self[TEMP_ID], self.offset()))
            return self[SET_LEN]
        else:
            kwargs[KEY_FIELDS_DEF] = template[KEY_FIELDS_DEF]

        # fields
        self.reset_children()
        fields_len = template[KEY_FIELDS_LEN]
        self['BuffLen'] = len(buff)
        self['BuffEndOffset'] = '0x%x' % self.offset(pos + len(buff))

        if self.check_debug(**kwargs):
            self.debug_print_items()

        def remaining():
            return self[SET_LEN] - size
        
        index = 1
        while remaining() >= fields_len:
            if self.check_debug(**kwargs):
                offset_now = self.offset(size)
                self.direct_print('OffsetNow=0x%x, OffsetNext=0x%x+0x%x=0x%x, BuffEndOffset=%s' % 
                      (offset_now, offset_now, fields_len, offset_now + fields_len, self['BuffEndOffset']))
            
            obj = IpfixRec(self.offset(size))
            kwargs[REC_IDX] = index
            obj.parse(buff, pos + size, **kwargs)
            if obj.export:
                self.add_child(obj)
            size += fields_len
            index += 1

        if remaining() > 0:
            if self.check_debug(**kwargs):
                offset_now = self.offset(size)
                self.direct_print('Offset=0x%x, PaddingCnt=%d, BuffEndOffset=%s' % 
                      (offset_now, remaining(), self['BuffEndOffset']))

        return self[SET_LEN]

    def can_visit(self, **kwargs):
        return not kwargs.get('hide_data', False)

    def do_summary_children(self, prefix, result, **kwargs):
        i = 1
        for obj in self.children:
            text = '%s=%d, %s' % (REC_IDX, i, obj.get_summary(result, **kwargs))
            self.output(self.format_offset_prefix(obj.offset(), prefix, **kwargs), text)
            i += 1

