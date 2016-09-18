# encoding: utf-8
# @version 2.0

from collections import OrderedDict
from sys import stderr

_func_log = None
_func_output_text = None
_func_output_binary = None


class _DictObj(object):
    
    def __init__(self):
        self._items = OrderedDict()    

    def __len__(self):
        return len(self._items) 

    def __contains__(self, key):
        return key in self._items
    
    def __getitem__(self, key):
        return self._items[key]

    def __delitem__(self, key):
        del self._items[key]

    def __setitem__(self, key, value):
        self._items[key] = value
        
    def clone_items(self):
        import copy
        return copy.deepcopy(self._items)

    def format_items(self):
        return ', '.join('%s=%s' % (k, v) for k, v in self._items.iteritems())

    def direct_print(self, *args):
        def _get_msg():
            if (isinstance(args, str)):
                return args
            else:
                return " ".join(args)    
        print >> stderr, "%s %s" % ('  ==>', _get_msg())

    def debug_print_items(self):
        self.direct_print(self.format_items())

    
class LogObj(_DictObj):
    
    def log(self, level, *args):
        if _func_log:
            _func_log(level, *args)    

    def output(self, *args):
        if _func_output_text:
            _func_output_text(*args)    

    def output_binary(self, msg):
        if _func_output_binary:
            _func_output_binary(msg)    
            
    def check_debug(self, **kwargs):
        return kwargs.get('debug', False)
    
    def check_level(self, level, **kwargs):
        if 'log_level' in kwargs:
            # pre-defined log-level is higher than the running log-level
            return level >= kwargs['log_level'] 
        else:
            return False


class VisitObj(LogObj):
    
    def __init__(self, off):
        super(VisitObj, self).__init__()
        self._offset = off
    
    def offset(self, pos=0):
        return self._offset + pos
    
    def format_offset_prefix(self, off, prefix, **kwargs):
        if kwargs.get('show_offset', False):
            return '%s0x%06x:' % (prefix, off)
        else: 
            if prefix:
                return '%s:' % prefix
            else:
                return ""
    
    def format_prefix(self, prefix, **kwargs):
        return self.format_offset_prefix(self.offset(), prefix, **kwargs)

    def can_visit(self, **kwargs):
        return True 
        
    def visit(self, prefix, result, **kwargs):
        if not self.can_visit(**kwargs):
            return
        self.do_visit(prefix, result, **kwargs)
    
    def do_visit(self, prefix, result, **kwargs):
        self.output(self.format_prefix(prefix, **kwargs), self.format_items())

    def is_hide_frame(self, **kwargs):
        return kwargs.get('hide_frame', False)


class VisitList(VisitObj):
    
    def __init__(self, off):
        super(VisitList, self).__init__(off)
        self.children = []

    def reset_children(self):
        self.children = []
        
    def add_child(self, obj):
        self.children.append(obj)
        
    def can_visit_self(self, **kwargs):
        return True
            
    def can_summary_children(self, **kwargs):
        return True
        
    def can_visit_children(self, **kwargs):
        return True

    def is_compensate_prefix_for_hide_frame(self, **kwargs):
        return True

    def visit(self, prefix, result, **kwargs):
        if not self.can_visit(**kwargs):
            return

        prefix_children = prefix
        if self.can_visit_self(**kwargs):
            self.do_visit(prefix, result, **kwargs)
            if not self.is_compensate_prefix_for_hide_frame(**kwargs) or not self.is_hide_frame(**kwargs):
                prefix_children = " " * len(prefix)

        if self.can_summary_children(**kwargs):
            self.do_summary_children(prefix_children, result, **kwargs)

        if self.can_visit_children(**kwargs):
            self.do_visit_children(prefix_children, result, **kwargs)
    
    def do_summary_children(self, prefix, result, **kwargs):
        pass
        
    def do_visit_children(self, prefix, result, **kwargs):
        for obj in self.children:
            obj.visit(prefix, result, **kwargs)


def obj_bind_log_func(fn_log, fn_output_text, fn_output_binary):
    global _func_log, _func_output_text, _func_output_binary
    _func_log = fn_log
    _func_output_text = fn_output_text
    _func_output_binary = fn_output_binary

