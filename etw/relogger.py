#!python
# Copyright 2016 Jeremy T. Braun
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This file contains declarations gleaned from the relogger.h file from
the Platform SDK. Many of the ct.Structures here are simplified from their
Platform SDK version by not in-lining one of the options of unions they
contain.
"""

import ctypes as ct
import ctypes.wintypes as wt
import exceptions
from guiddef import GUID
# from evntrace import CheckWinError
# from relogger import EVENT_DESCRIPTOR

class EVENT_DESCRIPTOR(ct.Structure):
    _fields_ = [
        ('Id', ct.c_ushort),
        ('Version', ct.c_ubyte),
        ('Channel', ct.c_ubyte),
        ('Level', ct.c_ubyte),
        ('Opcode', ct.c_ubyte),
        ('Task', ct.c_ushort),
        ('Keyword', ct.c_ulonglong),
    ]

class DUMMYSTRUCTNAME(ct.Structure):
    _fields = [
        ('KernelTime', ct.c_ulong),
        ('UserTime', ct.c_ulong),
    ]

class DUMMYUNIONNAME(ct.Union):
    _fields = [
        ('DUMMYSTRUCTNAME', DUMMYSTRUCTNAME),
        ('ProcessorTime', ct.c_uint64),
    ]

class EVENT_HEADER(ct.Structure):
    _fields_ = [
        ('Size', ct.c_ushort),
        ('HeaderType', ct.c_ushort),
        ('Flags', ct.c_ushort),
        ('EventProperty', ct.c_ushort),
        ('ThreadId', ct.c_ulong),
        ('ProcessId', ct.c_ulong),
        # ('TimeStamp', LARGE_INTEGER),
        ('TimeStamp', ct.c_longlong),
        ('ProviderId', GUID),
        ('EventDescriptor', EVENT_DESCRIPTOR),
        ('DUMMYUNIONNAME', DUMMYUNIONNAME),
        ('ActivityId', GUID),
    ]


class DUMMYSTRUCTNAME(ct.Structure):
    _fields = [
        ('ProcessorNumber', ct.c_ubyte),
        ('Alignment', ct.c_ubyte),
    ]

class DUMMYUNIONNAME(ct.Union):
    _fields = [
        ('DUMMYSTRUCTNAME', DUMMYSTRUCTNAME),
        ('ProcessorIndex', ct.c_ushort),
    ]

class ETW_BUFFER_CONTEXT(ct.Structure):
    _fields_ = [
        ('DUMMYUNIONNAME', DUMMYUNIONNAME),
        ('LoggerId', ct.c_ushort),
    ]

class EVENT_HEADER_EXTENDED_DATA_ITEM(ct.Structure):
    _fields_ = [
        ('Reserved1', ct.c_ushort),
        ('ExtType', ct.c_ushort),
        ('Linkage', ct.c_ushort),
        ('DataSize', ct.c_ushort),
        ('DataPtr', ct.c_ulonglong),
    ]

class EVENT_RECORD(ct.Structure):
    _fields_ = [
        ('EventHeader', EVENT_HEADER),
        ('BufferContext', ETW_BUFFER_CONTEXT),
        ('ExtendedDataCount', ct.c_ushort),
        ('UserDataLength', ct.c_ushort),
        ('ExtendedData', ct.POINTER(EVENT_HEADER_EXTENDED_DATA_ITEM)),
        ('UserData', ct.c_void_p),
        ('UserContext', ct.c_void_p),
    ]
