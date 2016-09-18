# encoding: utf-8
# version 2.1

import logging, sys

_log_level = logging.DEBUG

LOGGING_TO_VERBOSE = {
    logging.CRITICAL: 0,
    logging.ERROR: 1,
    logging.WARN: 2,
    logging.INFO: 3,
    logging.DEBUG: 4,
    logging.NOTSET: 5,
}

VERBOSE_TO_LOGGING = {
    0: logging.CRITICAL,
    1: logging.ERROR,
    2: logging.WARN,
    3: logging.INFO,
    4: logging.DEBUG,
    5: logging.NOTSET,
}


def log_level_to_verbosity(log_level):
    return LOGGING_TO_VERBOSE.get(log_level, 5)


def verbosity_to_log_level(verbose, default_level):
    global _log_level
    _log_level = VERBOSE_TO_LOGGING.get(verbose, logging.NOTSET)
    name = logging.getLevelName(_log_level)
    if _log_level > default_level:
        print >> sys.stderr, "Verbose mode on [%d], as to set log level to [%s]" % (verbose, name)
    else:
        print >> sys.stderr, "Verbose mode off, set default log level to [%s]" % (name)
    return name


def get_log_level():
    return _log_level


def log(level, *args):
    ''' log to stderr only
    '''
    def _get_msg():
        if (isinstance(args, str)):
            return args
        else:
            return " ".join(args)
    
    if level >= _log_level:
        print >> sys.stderr, _get_msg()


_func_output_text = None
_func_output_binary = None
_output_text_to_screen = True


def output_text(*args):
    ''' output to callback or stdout
    '''
    def _get_msg():
        if (isinstance(args, str)):
            return args
        else:
            return " ".join(args)    
    msg = _get_msg()
    
    if _func_output_text:
        _func_output_text(msg)
    if _output_text_to_screen:
        print msg


def output_binary(msg):
    ''' output to callback only
    '''
    if _func_output_binary:
        _func_output_binary(msg)


def bind_output_function(fn_output_text, fn_output_binary):
    global _func_output_text, _func_output_binary
    _func_output_text = fn_output_text        
    _func_output_binary = fn_output_binary


def is_output_text_to_screen():
    return  _output_text_to_screen


def set_output_text_to_screen(value):
    global _output_text_to_screen
    _output_text_to_screen = value


def get_path_protocol(infile):
    import os
    
    segs = infile.split('://')
    if len(segs) > 2:
        return None, 'invalid path format for "%s", only support one protocol, either can be "udp://" or "file://", default is "file"' % infile

    elif len(segs) == 2:
        return segs[0].lower(), segs[1].replace('\\', os.sep).replace('/', os.sep)

    return 'file', infile
