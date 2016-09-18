# encoding: utf-8

import SocketServer

from _obj import LogObj

UDP_HANDLER_CALLBACK = None

class UdpHandler(SocketServer.BaseRequestHandler):
    
    def handle(self):
        if UDP_HANDLER_CALLBACK:
            UDP_HANDLER_CALLBACK(self.request[0])

def _get_endpoint_address(endpoint):
    items = endpoint.split(':')
    return (items[0], int(items[1]))

class UdpChannel(LogObj):

    endpoint = None
    count = 0
    offset = 0
    
    kwargs = {}
    result = {}
    
    _udp_server = None
    
    def __init__(self, endpoint):
        '''
        Constructor
        '''   
        self.endpoint = endpoint
        self.address = _get_endpoint_address(self.endpoint)
        
    def run(self, **kwargs):
        global UDP_HANDLER_CALLBACK
        UDP_HANDLER_CALLBACK = self.callback
        
        self.kwargs = kwargs
        self.result = {}
        
        self._udp_server = SocketServer.UDPServer(self.address, UdpHandler)
        self.count = 0
        self.offset = 0
        
        # run
        self._udp_server.serve_forever()
        
    def callback(self, buff):
        self._msg_offset = 0
        self._msg_index = 0
        
        self._read_offset = 0
        self._buff = buff
        
        while self._msg_offset < len(buff): 
            if not self._read(** self.kwargs):
                break
            prefix = "#%d," % self.count
            self.message.visit(prefix, self.result, **self.kwargs)

        self.count += 1
        self.offset += len(buff)
        
    def _read_buff(self, size):
        result = self._buff[self._read_offset: self._read_offset + size]
        self._read_offset += size
        return result

    def _read(self, **kwargs):
        import struct

        buff = self._read_buff(2)
        if (not buff) or (len(buff) == 0):
            return False

        ver, = struct.unpack(">H", buff)
        if ver == 10:
            return self._read_ipfix(buff, **kwargs)
        elif ver == 9:
            return self._read_netflow9(buff, **kwargs)
        elif ver == 5:
            return self._read_netflow5(buff, **kwargs)

        raise Exception('Invalid version=%d, offset=0x%x, message=%d' % 
                            (ver, self._msg_offset, self._msg_index))

    def _read_ipfix(self, byte2, **kwargs):
        from ipfix import MSG_HEADER_LEN, MSG_LEN
        from ipfix._msg import IpfixMsgHdr, IpfixMsg

        buff = self._read_buff(MSG_HEADER_LEN - 2)
        if len(buff) < MSG_HEADER_LEN - 2:
            raise Exception('Found %d remaining bytes, offset=0x%x, message=%d' % 
                            (len(buff), self._msg_offset, self._msg_index))
        buff = byte2 + buff

        # store index and offset in header
        header = IpfixMsgHdr(self._msg_offset, buff, None **kwargs)

        # handle body as message
        buff = self._read_buff(header.body_len())
        self.message = IpfixMsg(header, buff, **kwargs)

        # next
        self._msg_offset = self._msg_offset + header[MSG_LEN]

        return True

    def _read_netflow9(self, byte2, **kwargs):
        from ipfix import PKT_V9_HEADER_LEN
        from ipfix._v9pkt import Nflow9PktHdr, Nflow9Pkt

        buff = self._read_buff(PKT_V9_HEADER_LEN - 2)
        if len(buff) < PKT_V9_HEADER_LEN - 2:
            raise Exception('Found %d remaining bytes, offset=0x%x, message=%d' % 
                            (len(buff), self._msg_offset, self._msg_index))
        buff = byte2 + buff

        # store index and offset in header
        header = Nflow9PktHdr(self._msg_offset, buff, None, **kwargs)

        # handle body as message
        self.message = Nflow9Pkt(header, self._read_buff, **kwargs)

        # next
        self._msg_offset = self._msg_offset + self.message.body_len
        return True

    def _read_netflow5(self, byte2, **kwargs):
        from ipfix import PKT_V5_HEADER_LEN
        from ipfix._v5pkt import Nflow5PktHdr, Nflow5Pkt

        buff = self._read_buff(PKT_V5_HEADER_LEN - 2)
        if len(buff) < PKT_V5_HEADER_LEN - 2:
            raise Exception('Found %d remaining bytes, offset=0x%x, message=%d' % 
                            (len(buff), self._msg_offset, self._msg_index))
        buff = byte2 + buff

        # store index and offset in header
        header = Nflow5PktHdr(self._msg_offset, buff, None, **kwargs)

        # handle body as message
        self.message = Nflow5Pkt(header, self._read_buff, **kwargs)

        # next
        self._msg_offset = self._msg_offset + self.message.body_len
        return True
