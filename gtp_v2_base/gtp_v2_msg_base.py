#       gtp_v2_base_msg.py
#       
#       Copyright 2017 Rosalia d'Alessandro <rosalia.dalessandro@telecomitalia.it>
#

#       Redistribution and use in source and binary forms, with or without
#       modification, are permitted provided that the following conditions are
#       met:
#       
#       * Redistributions of source code must retain the above copyright
#         notice, this list of conditions and the following disclaimer.
#       * Redistributions in binary form must reproduce the above
#         copyright notice, this list of conditions and the following disclaimer
#         in the documentation and/or other materials provided with the
#         distribution.
#       * Neither the name of the  nor the names of its
#         contributors may be used to endorse or promote products derived from
#         this software without specific prior written permission.
#       
#       THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#       "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#       LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#       A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#       OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#       SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#       LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#       DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#       THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#       (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#       OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#!/usr/bin/env  python
# -*- coding: utf-8 -*-
import random
import struct
from gtp_v2_information_elements import *
from gtp_v2_commons import *
'''
TEID NOT PRESENT

    8     7     6     5     4     3     2     1    Octets
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|     Version     | P   | 0   | 0   | 0   | 0   |   1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                  Message Type                 |   2
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                 Message Length                |  3-4
|                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                 Sequence Number               |  5-7
|                                               |
|                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       0                       |   8
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


TEID PRESENT

    8     7     6     5     4     3     2     1    Octets
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|     Version     | P   | 1   | 0   | 0   | 0   |   1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                  Message Type                 |   2
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                 Message Length                |  3-4
|                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                 TEID                          |  5-8
|                                               |
|                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                 Sequence Number               |  9-11
|                                               |
|                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       0                       |   12
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
'''

class GTPV2MessageBase(object):
    '''
    classdocs
    '''


    def __init__(self, msg_type, t = 0x00, p = 0x00):
        '''
        Constructor
        '''
        if not GTPmessageTypeDigit.has_key(msg_type) :
            raise Exception("invalid mesg_type: %s"%(msg_type))
        self.__t_flag = t
        self.__p_flag = p
        self.__sequence_number = bytearray(random.getrandbits(8) for i in range(3))
        
        if (self.__t_flag == 0x00) :
            self.__hdr_len = 8
        else:
            self.__teid = 0x00000000
            self.__hdr_len = 12            
        self.__packed_ie_len = 0
        self.__msg_type = GTPmessageTypeDigit[msg_type]
        self.__version = 0x02
        self.__packed_ie= 0x00 # packed data containing all information elements
        self.__ie_array = []   # array containing all the information elements
 
    def __get_packed_ies(self):
        self.__packed_ie = 0x00
        for ie in self.__ie_array:
            self.__packed_ie += ie.get_packed_ie()
        self.__packed_ie_len = len(self.__packed_ie)

    def add_ie(self, ie):
        if ie:
            self.__ie_array.append(ie)
        
    def get_length(self):
        return (self.__packed_ie_len + self.__hdr_len)
              
    def get_hdr_length(self):
        return self.__hdr_len
    
    def get_packed_ie_length(self):
        return self.__packed_ie_len     

    def get_packed_ie(self):
        if self.__packed_ie == 0x00:
            self.__get_packed_ies()
        return self.__packed_ie
    
    def get_packed_header(self):
        msg_type = struct.pack("!B", self.__msg_type)
        
        flags = struct.pack("!B", (self.__version << 5) + (self.__t_flag << 4))
        spare = struct.pack("!B", 0)
        msg_len = struct.pack("!H", self.__len)
        
        out = flags + msg_type + msg_len
        if self.__t_flag :
            out += self.__teid
        out += (self.__sequence_number + spare)
        return out    
    
    def get_message(self):
        return (self.get_packed_header() + self.get_packed_ie())
    
    
    def set_packed_ie(self, packed_ie):
        self.__packed_ie = packed_ie
        self.__packed_ie_len = len(packed_ie)
    
    def set_teid(self, teid = bytearray(random.getrandbits(8) for i in range(3))):
        if teid != 0 :
            self.__t_flag = 1
            self.__teid = teid       



    

    