# encoding: utf-8

from ipfix import FLD_IDX, FLD_NAME, FLD_VAL, KEY_FIELDS_DEF, KEY_FIELD_DEF, FLD_TYPE
from ipfix._field import IpfixField
from ipfix._obj import VisitList


class IpfixRec(VisitList):
    
    def __init__(self, offset):
        super(IpfixRec, self).__init__(offset)
        self.export = True

    def parse(self, buff, pos, **kwargs):
        self.reset_children()
        
        size = 0
        index = 1
        fields_def = kwargs[KEY_FIELDS_DEF]
        fkeys = kwargs.get("fkeys", [])
        
        ip_filter = kwargs.get("ip_filter", "")
        if ip_filter:
            self.export = False
        else:
            self.export = True
        
        for field_def in fields_def:
            kwargs[FLD_IDX] = index
            kwargs[KEY_FIELD_DEF] = field_def
            obj = IpfixField(self.offset(size))
            delta = obj.parse(buff, pos + size, **kwargs)
            
            if kwargs.get('show_all_fields', False):
                self.add_child(obj)
            elif (not fkeys) or (field_def[FLD_NAME] in fkeys):
                self.add_child(obj)

            size += delta
            index += 1
            if (field_def[FLD_TYPE] == 'ipv4Address') and ip_filter and (not self.export):
                self.export = ip_filter in obj[FLD_VAL]
        
        return size

    def can_visit_self(self, **kwargs):
        return False
            
    def can_summary_children(self, **kwargs):
        return False
        
    def can_visit_children(self, **kwargs):
        return True        
        
    def get_summary(self, result, **kwargs):
        vals = []
        for obj in self.children:
            vals.append("%s=%s" % (obj[FLD_NAME], obj[FLD_VAL]))
        return ', '.join(vals)
