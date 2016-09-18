#!/usr/local/bin/python2.7
# encoding: utf-8
'''
 -- Display the ipfix data, either from the dump file or the UDP channel.

  Display the ipfix data, either from the dump file or the UDP channel.
  Use direct file path, e.g. "/path/to/file", or "file:///path/to/file" for the dump.
  Use "udp://ip:port" for the UDP channel.

@author:     William Cai

@copyright:  2015 Netis Technologies. All rights reserved.

@contact:    william.cai@netis.com.cn
@deffield    updated: Updated

@change:    0.1     initial version
            0.2     add IP filter feature
            0.3     add roughly Netflow V9 format support
                    add Netflow V5 format support
            0.4     add --show-field parameter
                    add --load-template feature
                    add UDP support
                    add appId translation support
            0.5     fix multiple template bug
                    add --hide-frame to hide record frame
                    add --dump-template to dump template
            0.5.1   fix version issue
                    fix dump template "Record Size" issue
                    improve format dumped template
            0.5.2   fix bug for Netflow V9 data
            0.6     handle truncate read for Netflow V9 packet
                    use ipfix field def for Netflow V9 packet in default
            0.7     compatible support for wrap frame Netflow V9 or V5 data
            0.7.1   fix field definition and field data offset issue
                    add try/except for unprocessable data reading, and set ErrorValue for it
            0.8     fix the the bug which templateId is binding to Observation Domain ID
                    rename "MsgObDomID" to "ObservationDomainId"
            0.9     add --load-template support
'''

from argparse import ArgumentParser, FileType
from argparse import RawDescriptionHelpFormatter
import logging
import os
import sys

from helper import log, verbosity_to_log_level, log_level_to_verbosity, get_log_level, get_path_protocol
from ipfix import obj_bind_log_func, IpfixFile, UdpChannel, ipfix_load_template, ipfix_dump_template

__all__ = []
__version__ = "0.8"
__date__ = '2015-01-08'
__updated__ = '2016-01-19'

DEBUG = 0
TESTRUN = 0
PROFILE = 0
LOG_LEVEL = logging.ERROR
VERBOSITY_LEVEL = log_level_to_verbosity(LOG_LEVEL)


FKEYS_EMPTY = []
FKEYS_DEF = [
    # IPFIX
    'sourceIPv4Address', 'destinationIPv4Address', 'protocolIdentifier', 'applicationId',
    'monitoringIntervalStartMilliSeconds', 'ingressInterface', 'egressInterface', 'flowDirection',
    'packetDeltaCount', 'octetDeltaCount',
    # Netflow v9
    'IPV4_SRC_ADDR', 'IPV4_DST_ADDR',
    'PROTOCOL',
    # Netflow V5
    'srcaddr', 'dstaddr', 'prot',
]
FKEYS = FKEYS_DEF


class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg


def _process_file(infile, result, **kwargs):
    number = kwargs.get('number', 0)

    obj = IpfixFile(os.path.abspath(infile))
    obj.open(**kwargs)

    count = 0
    for msg in obj.read(**kwargs):
        prefix = "#%d," % count
        msg.visit(prefix, result, **kwargs)

        count += 1
        if (number > 0) and (count >= number):
            log(logging.DEBUG, 'break on "-n, --number" argument, whose value is "%d"' % number)
            break

    log(logging.WARN, 'loaded %d messages' % count, 'from dump file:', infile)
    obj.close()


def _process_udp(infile, result, **kwargs):
    try: 
        obj = UdpChannel(infile)
        obj.run(**kwargs)
    finally:
        log(logging.WARN, 'loaded %d packets' % obj.count, 'from udp://%s' % obj.endpoint)  


def _cli_entry(args):
    result = {}
    
    # load the template at first
    ipfix_load_template(args.load_template,
                        log_level=get_log_level(),
                        debug=args.debug,)
    
    def _inc_result(key):
        result[key] = result.get(key, 0) + 1

    for infile in args.paths:
        proto, realfile = get_path_protocol(infile)
        if proto == None:
            log(logging.ERROR, realfile)
            _inc_result('errorPathCnt')

        elif proto == 'file':
            _process_file(realfile, result,
                          log_level=get_log_level(),
                          number=args.number,
                          show_offset=args.show_offset,
                          debug=args.debug,
                          show_template=args.show_template,
                          show_all_fields=args.show_all_fields,
                          show_wrap_frame=args.show_wrap_frame,
                          hide_frame=args.hide_frame,
                          hide_data=args.hide_data,
                          ip_filter=args.ip_filter,
                          disable_app_trans=args.disable_app_trans,
                          apply_v9_field=args.apply_v9_field,
                          fkeys=args.show_field)
            _inc_result('fileCnt')

        elif proto == 'udp':
            _process_udp(realfile, result,
                         log_level=get_log_level(),
                         show_offset=args.show_offset,
                         debug=args.debug,
                         show_template=args.show_template,
                         show_all_fields=args.show_all_fields,
                         hide_frame=args.hide_frame,
                         hide_data=args.hide_data,
                         ip_filter=args.ip_filter,
                         disable_app_trans=args.disable_app_trans,
                         apply_v9_field=args.apply_v9_field,
                         fkeys=args.show_field)
            _inc_result('udpCnt')

        else:
            log(logging.ERROR, 'invalid path protocol="%s" in the input path "%s" only support "udp://" and "file://", default is "file" protocol.' % (proto, infile))
            _inc_result('errorPathCnt')

    log(logging.DEBUG, "paths: %s" % str(result))

    if args.dump_template:
        ipfix_dump_template(log_level=get_log_level(),
                            debug=args.debug,)

    return 0


def main(argv=None):  # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by William Cai on %s.
  Copyright 2015 Netis Technologies. All rights reserved.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("--show-offset", dest="show_offset", action='store_true',
                            help="switch to show offset [default: %(default)s]")
        parser.add_argument("--show-template", dest="show_template", action='store_true',
                            help="switch to show template [default: %(default)s]")
        parser.add_argument("--show-all-fields", dest="show_all_fields", action='store_true',
                            help="switch to show all fields [default: %(default)s]")
        parser.add_argument("-f", "--show-field", dest="show_field", action='append', default=FKEYS,
                            help="show the field in normal mode [default: %(default)s]")
        parser.add_argument("--show-wrap-frame", dest="show_wrap_frame", action='store_true',
                            help="show wrap frame [default: %(default)s]")
        parser.add_argument("--hide-frame", dest="hide_frame", action='store_true',
                            help="hide record frame, to find template with '--show-template' argument [default: %(default)s]")
        parser.add_argument("--hide-data", dest="hide_data", action='store_true',
                            help="hide data record, to find template with '--show-template' argument [default: %(default)s]")
        parser.add_argument("--debug", dest="debug", help="switch to debug mode [default: %(default)s]", action='store_true')
        parser.add_argument("--ip-filter", dest="ip_filter",
                            help="set to IP filter, either full or part, e.g. '172.16.11.1', '172.16', or '11.1' [default: %(default)s]")
        parser.add_argument("--load-template", dest="load_template",
                            help="load the template file.' [default: %(default)s]")
        parser.add_argument("--disable-app-translation", dest="disable_app_trans", action='store_true',
                            help="switch to disable translation application id [default: %(default)s]")
        # parser.add_argument("--enable-dump", dest="enable_dump", help="switch to enable dump file [default: %(default)s]", action='store_true')
        parser.add_argument("--apply-v9-field", dest="apply_v9_field",  action='store_true',
                            help="switch to apply v9 field for Netflow V9 packet [default: %(default)s]")
        parser.add_argument("--dump-template", dest="dump_template", action='store_true',
                            help="dump the template to a file [default: %(default)s]")
        parser.add_argument("-n", "--number", dest="number", type=int, default=0,
                            help="set packet number to exit [default: %(default)d]")
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", default=VERBOSITY_LEVEL,
                            help="set verbosity level [default: %d (%s)]" % (VERBOSITY_LEVEL, logging.getLevelName(LOG_LEVEL)))
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument(dest="paths", metavar="path", nargs='+',
                            help='paths to the dump file(s) or the UDP channel. Dump file format "/path/to/file" or "file:///path/to/file". UDP format "udp://ip:port".')
        parser.set_defaults(func=_cli_entry)

        # Process arguments
        args = parser.parse_args()
        verbosity_to_log_level(args.verbose, VERBOSITY_LEVEL)
        global DEBUG
        DEBUG = args.debug

        # handle log and output
        from helper import output_text, output_binary
        obj_bind_log_func(log, output_text, output_binary)

        # Execute
        return args.func(args)
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        if DEBUG or TESTRUN:
            import traceback
            print traceback.format_exc()
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + ". " + str(e) + "\n")
        sys.stderr.write(indent + "  for help use --help\n")
        return 2

if __name__ == "__main__":
    if DEBUG:
        pass
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = '_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
