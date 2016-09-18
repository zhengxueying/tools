# encoding: utf-8

import logging
import struct
from _obj import LogObj
from _frame import WrapFrameObj, WRAP_FRAME_HDR_LEN


class IpfixFile(LogObj):
    '''
    Read and write ipfix file.
    '''
    src_file = None
    message = None

    _src_fd = None
    _msg_offset = 0
    _msg_index = 0

    def __init__(self, pathfile):
        '''
        Constructor
        '''
        self.src_file = pathfile

    def open(self, **kwargs):
        try:
            self._src_fd = open(self.src_file, 'rb')
            self.log(logging.INFO, 'open file: %s' % self.src_file)
        except Exception, e:
            self.log(logging.ERROR, 'failed to open file "%s", %s' % (self.src_file, e))
            if self.check_debug(**kwargs):
                import traceback
                print traceback.format_exc()
            raise e

    def read(self, **kwargs):
        if not self._src_fd:
            raise StopIteration

        self._msg_index = 0
        while self._read(**kwargs):
            yield self.message
            self._msg_index += 1

    def _read(self, **kwargs):
        buff, ver = self._read_byte2_ver(**kwargs)

        if ver == 10:
            return self._read_ipfix(buff, None, **kwargs)
        elif ver == 9:
            return self._read_netflow9(buff, None, **kwargs)
        elif ver == 5:
            return self._read_netflow5(buff, None, **kwargs)
        else:
            return self._read_wrap_frame(buff, ver, **kwargs)

    def _read_byte2_ver(self, **kwargs):
        buff = self._src_fd.read(2)
        if (not buff) or (len(buff) == 0):
            raise StopIteration
        ver, = struct.unpack(">H", buff)
        return buff, ver

    def close(self):
        if self._src_fd:
            self._src_fd.close()
            self.log(logging.INFO, 'close file: %s' % self.src_file)

    def _read_ipfix(self, byte2, wrap_frame, **kwargs):
        from ipfix import MSG_HEADER_LEN, MSG_LEN
        from ipfix._msg import IpfixMsgHdr, IpfixMsg

        buff = self._src_fd.read(MSG_HEADER_LEN - 2)
        if len(buff) < MSG_HEADER_LEN - 2:
            raise Exception('Found %d remaining bytes, offset=0x%x, message=%d' % 
                            (len(buff), self._msg_offset, self._msg_index))
        buff = byte2 + buff

        # store index and offset in header
        header = IpfixMsgHdr(self._msg_offset, buff, wrap_frame, **kwargs)

        # handle body as message
        buff = self._src_fd.read(header.body_len())
        self.message = IpfixMsg(header, buff, **kwargs)

        # next
        self._msg_offset += header[MSG_LEN]

        return True

    def _read_netflow9(self, byte2, wrap_frame, **kwargs):
        from ipfix import PKT_V9_HEADER_LEN
        from ipfix._v9pkt import Nflow9PktHdr, Nflow9Pkt

        buff = self._src_fd.read(PKT_V9_HEADER_LEN - 2)
        if len(buff) < PKT_V9_HEADER_LEN - 2:
            raise Exception('Found %d remaining bytes, offset=0x%x, message=%d' % 
                            (len(buff), self._msg_offset, self._msg_index))
        buff = byte2 + buff

        # store index and offset in header
        header = Nflow9PktHdr(self._msg_offset, buff, wrap_frame, **kwargs)

        # handle body as message
        self.message = Nflow9Pkt(header, self._src_fd.read, self._src_fd.seek, **kwargs)

        # next
        self._msg_offset += self.message.body_len + PKT_V9_HEADER_LEN
        return True

    def _read_netflow5(self, byte2, wrap_frame, **kwargs):
        from ipfix import PKT_V5_HEADER_LEN
        from ipfix._v5pkt import Nflow5PktHdr, Nflow5Pkt

        buff = self._src_fd.read(PKT_V5_HEADER_LEN - 2)
        if len(buff) < PKT_V5_HEADER_LEN - 2:
            raise Exception('Found %d remaining bytes, offset=0x%x, message=%d' % 
                            (len(buff), self._msg_offset, self._msg_index))
        buff = byte2 + buff

        # store index and offset in header
        header = Nflow5PktHdr(self._msg_offset, buff, wrap_frame, **kwargs)

        # handle body as message
        self.message = Nflow5Pkt(header, self._src_fd.read, **kwargs)

        # next
        self._msg_offset += self.message.body_len
        return True

    def _read_wrap_frame(self, byte2, ver, **kwargs):
        temp = self._src_fd.read(WRAP_FRAME_HDR_LEN - 2)
        buff = byte2 + temp
        wrap_frame = WrapFrameObj(self._msg_offset, buff)
        if not wrap_frame.is_valid():
            raise Exception('Invalid version=%d or wrap_frame=%s, offset=0x%x, message=%d'
                            % (ver, wrap_frame.visit(None, None), self._msg_offset, self._msg_index))
        self._msg_offset += WRAP_FRAME_HDR_LEN

        buff, ver = self._read_byte2_ver(**kwargs)
        if ver == 10:
            return self._read_ipfix(buff, wrap_frame, **kwargs)
        elif ver == 9:
            return self._read_netflow9(buff, wrap_frame, **kwargs)
        elif ver == 5:
            return self._read_netflow5(buff, wrap_frame, **kwargs)

        raise Exception('Invalid version=%d, offset=0x%x, message=%d' %
                            (ver, self._msg_offset, self._msg_index))