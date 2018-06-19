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
"""This file contains declarations gleaned from the evntprov.h file from
the Platform SDK. Many of the ct.Structures here are simplified from their
Platform SDK version by not in-lining one of the options of unions they
contain.
"""

import ctypes as ct
import ctypes.wintypes as wt
import exceptions
from guiddef import GUID
from evntrace import CheckWinError

def _CheckWinBool(result, func, arguments):
    if not result:
        raise exceptions.WindowsError(ct.GetLastError())
    return result


EVENT_MIN_LEVEL =                      (0)
EVENT_MAX_LEVEL =                      (0xff)

EVENT_ACTIVITY_CTRL_GET_ID =           (1)
EVENT_ACTIVITY_CTRL_SET_ID =           (2)
EVENT_ACTIVITY_CTRL_CREATE_ID =        (3)
EVENT_ACTIVITY_CTRL_GET_SET_ID =       (4)
EVENT_ACTIVITY_CTRL_CREATE_SET_ID =    (5)

REGHANDLE = ct.c_ulonglong

MAX_EVENT_DATA_DESCRIPTORS =           (128)
MAX_EVENT_FILTER_DATA_SIZE =           (1024)

EVENT_FILTER_TYPE_SCHEMATIZED =        (0x80000000)

#
# EVENT_DATA_DESCRIPTOR is used to pass in user data items
# in events.
#
class EVENT_DATA_DESCRIPTOR(ct.Structure):
    _fields_ = [('Ptr', ct.c_ulonglong),
                ('Size', ct.c_ulong),
                ('Reserved', ct.c_ulong)]

#
# EVENT_DESCRIPTOR describes and categorizes an event.
#
class EVENT_DESCRIPTOR(ct.Structure):
    _fields_ = [('Id', ct.c_ushort),
                ('Version', ct.c_ubyte),
                ('Channel', ct.c_ubyte),
                ('Level', ct.c_ubyte),
                ('Opcode', ct.c_ubyte),
                ('Task', ct.c_ushort),
                ('Keyword', ct.c_ulonglong)]

#
# EVENT_FILTER_DESCRIPTOR is used to pass in enable filter
# data item to a user callback function.
#
class EVENT_FILTER_DESCRIPTOR(ct.Structure):
    _fields_ = [('Ptr', ct.c_ulonglong),
                ('Size', ct.c_ulong),
                ('Type', ct.c_ulong)]

class EVENT_FILTER_HEADER(ct.Structure):
    _fields_ = [('Id', ct.c_ushort),
                ('Version', ct.c_ubyte),
                ('Reserved', ct.c_ubyte * 5),
                ('InstanceId', ct.c_ulonglong),
                ('Size', ct.c_ulong),
                ('NextOffset', ct.c_ulong)]

#
# Optional callback function that users provide
#
ENABLE_CALLBACK = ct.WINFUNCTYPE(
    None,
    ct.POINTER(GUID), # SourceId,
    ct.c_ulong, # IsEnabled,
    ct.c_ubyte, # Level,
    ct.c_ulonglong, # MatchAnyKeyword,
    ct.c_ulonglong, # MatchAllKeyword,
    ct.POINTER(EVENT_FILTER_DESCRIPTOR), # FilterData,
    ct.c_void_p # CallbackContext
)

#
# Registration APIs
#

_ = EventRegister = ct.windll.advapi32.EventRegister
_.argtypes = [
    ct.POINTER(GUID), # ProviderId,
    ENABLE_CALLBACK, # EnableCallback,
    ct.c_void_p, # CallbackContext,
    ct.POINTER(REGHANDLE), # RegHandle
]
_.restype = ct.c_ulong
_.errcheck = CheckWinError

_ = EventUnregister = ct.windll.advapi32.EventUnregister
_.argtypes = [
    REGHANDLE, # RegHandle
]
_.restype = ct.c_ulong
_.errcheck = CheckWinError

#
# Control (Is Enabled) APIs
#

_ = EventEnabled = ct.windll.advapi32.EventEnabled
_.argtypes = [
    REGHANDLE, # RegHandle
    ct.POINTER(EVENT_DESCRIPTOR), # EventDescriptor
]
_.restype = ct.c_ulong
_.errcheck = _CheckWinBool

_ = EventProviderEnabled = ct.windll.advapi32.EventProviderEnabled
_.argtypes = [
    REGHANDLE, # RegHandle
    ct.c_ubyte, # Level
    ct.c_ulonglong, # Keyword
]
_.restype = ct.c_ulong
_.errcheck = _CheckWinBool

#
# Writing (Publishing/Logging) APIs
#

_ = EventWrite = ct.windll.advapi32.EventWrite
_.argtypes = [
    REGHANDLE, # RegHandle
    ct.POINTER(EVENT_DESCRIPTOR), # EventDescriptor
    ct.c_ulong, # UserDataCount
    ct.POINTER(EVENT_DATA_DESCRIPTOR), # UserData
]
_.restype = ct.c_ulong
_.errcheck = CheckWinError

_ = EventWriteTransfer = ct.windll.advapi32.EventWriteTransfer
_.argtypes = [
    REGHANDLE, # RegHandle
    ct.POINTER(EVENT_DESCRIPTOR), # EventDescriptor
    ct.POINTER(GUID), # ActivityId
    ct.POINTER(GUID), # RelatedActivityId
    ct.c_ulong, # UserDataCount
    ct.POINTER(EVENT_DATA_DESCRIPTOR), # UserData
]
_.restype = ct.c_ulong
_.errcheck = CheckWinError

_ = EventWriteEx = ct.windll.advapi32.EventWriteEx
_.argtypes = [
    REGHANDLE, # RegHandle,
    ct.POINTER(EVENT_DESCRIPTOR), # EventDescriptor
    ct.c_uint64, # Filter
    ct.c_ulong, # Flags
    ct.POINTER(GUID), # ActivityId
    ct.POINTER(GUID), # RelatedActivityId
    ct.c_ulong, # UserDataCount
    ct.POINTER(EVENT_DATA_DESCRIPTOR), # UserData
]
_.restype = ct.c_ulong
_.errcheck = CheckWinError

_ = EventWriteString = ct.windll.advapi32.EventWriteString
_.argtypes = [
    REGHANDLE, # RegHandle,
    ct.c_ubyte, # Level
    ct.c_ulonglong, # Keyword
    ct.c_wchar_p, # String
]
_.restype = ct.c_ulong
_.errcheck = CheckWinError


#
# ActivityId Control APIs
#

_ = EventActivityIdControl = ct.windll.advapi32.EventActivityIdControl
_.argtypes = [
    ct.c_ulong, # ControlCode,
    ct.POINTER(GUID), # ActivityId
]
_.restype = ct.c_ulong
_.errcheck = CheckWinError


#
# Macros to create Event and Event Data Descriptors
#

# FORCEINLINE
# VOID
# EventDataDescCreate(
#     __out PEVENT_DATA_DESCRIPTOR EventDataDescriptor,
#     __in const VOID* DataPtr,
#     __in ULONG DataSize
#     )
# {
#     EventDataDescriptor->Ptr = (ULONGLONG)(ULONG_PTR)DataPtr;
#     EventDataDescriptor->Size = DataSize;
#     EventDataDescriptor->Reserved = 0;
#     return;
# }

# FORCEINLINE
# VOID
# EventDescCreate(
#     __out PEVENT_DESCRIPTOR EventDescriptor,
#     __in USHORT Id,
#     __in UCHAR Version,
#     __in UCHAR Channel,
#     __in UCHAR Level,
#     __in USHORT Task,
#     __in UCHAR Opcode,
#     __in ULONGLONG Keyword
#     )
# {
#     EventDescriptor->Id = Id;
#     EventDescriptor->Version = Version;
#     EventDescriptor->Channel = Channel;
#     EventDescriptor->Level = Level;
#     EventDescriptor->Task = Task;
#     EventDescriptor->Opcode = Opcode;
#     EventDescriptor->Keyword = Keyword;
#     return;
# }

# FORCEINLINE
# VOID
# EventDescZero(
#     __out PEVENT_DESCRIPTOR EventDescriptor
#     )
# {
#     memset(EventDescriptor, 0, sizeof(EVENT_DESCRIPTOR));
#     return;
# }

#
# Macros to extract info from an Event Descriptor
#

# FORCEINLINE
# USHORT
# EventDescGetId(
#     __in PCEVENT_DESCRIPTOR EventDescriptor
#     )
# {
#     return (EventDescriptor->Id);
# }

# FORCEINLINE
# UCHAR
# EventDescGetVersion(
#     __in PCEVENT_DESCRIPTOR EventDescriptor
#     )
# {
#     return (EventDescriptor->Version);
# }

# FORCEINLINE
# USHORT
# EventDescGetTask(
#     __in PCEVENT_DESCRIPTOR EventDescriptor
#     )
# {
#     return (EventDescriptor->Task);
# }

# FORCEINLINE
# UCHAR
# EventDescGetOpcode(
#     __in PCEVENT_DESCRIPTOR EventDescriptor
#     )
# {
#     return (EventDescriptor->Opcode);
# }

# FORCEINLINE
# UCHAR
# EventDescGetChannel(
#     __in PCEVENT_DESCRIPTOR EventDescriptor
#     )
# {
#     return (EventDescriptor->Channel);
# }

# FORCEINLINE
# UCHAR
# EventDescGetLevel(
#     __in PCEVENT_DESCRIPTOR EventDescriptor
#     )
# {
#     return (EventDescriptor->Level);
# }

# FORCEINLINE
# ULONGLONG
# EventDescGetKeyword(
#     __in PCEVENT_DESCRIPTOR EventDescriptor
#     )
# {
#     return (EventDescriptor->Keyword);
# }

#
# Macros to set info into an Event Descriptor
#

# FORCEINLINE
# PEVENT_DESCRIPTOR
# EventDescSetId(
#     __in PEVENT_DESCRIPTOR EventDescriptor,
#     __in USHORT Id
#     )
# {
#     EventDescriptor->Id         = Id;
#     return (EventDescriptor);
# }

# FORCEINLINE
# PEVENT_DESCRIPTOR
# EventDescSetVersion(
#     __in PEVENT_DESCRIPTOR EventDescriptor,
#     __in UCHAR Version
#     )
# {
#     EventDescriptor->Version    = Version;
#     return (EventDescriptor);
# }

# FORCEINLINE
# PEVENT_DESCRIPTOR
# EventDescSetTask(
#     __in PEVENT_DESCRIPTOR EventDescriptor,
#     __in USHORT Task
#     )
# {
#     EventDescriptor->Task       = Task;
#     return (EventDescriptor);
# }

# FORCEINLINE
# PEVENT_DESCRIPTOR
# EventDescSetOpcode(
#     __in PEVENT_DESCRIPTOR EventDescriptor,
#     __in UCHAR Opcode
#     )
# {
#     EventDescriptor->Opcode     = Opcode;
#     return (EventDescriptor);
# }

# FORCEINLINE
# PEVENT_DESCRIPTOR
# EventDescSetLevel(
#     __in PEVENT_DESCRIPTOR EventDescriptor,
#     __in UCHAR  Level
#     )
# {
#     EventDescriptor->Level      = Level;
#     return (EventDescriptor);
# }

# FORCEINLINE
# PEVENT_DESCRIPTOR
# EventDescSetChannel(
#     __in PEVENT_DESCRIPTOR EventDescriptor,
#     __in UCHAR Channel
#     )
# {
#     EventDescriptor->Channel    = Channel;
#     return (EventDescriptor);
# }

# FORCEINLINE
# PEVENT_DESCRIPTOR
# EventDescSetKeyword(
#     __in PEVENT_DESCRIPTOR EventDescriptor,
#     __in ULONGLONG Keyword
#     )
# {
#     EventDescriptor->Keyword    = Keyword;
#     return (EventDescriptor);
# }


# FORCEINLINE
# PEVENT_DESCRIPTOR
# EventDescOrKeyword(
#     __in PEVENT_DESCRIPTOR EventDescriptor,
#     __in ULONGLONG Keyword
#     )
# {
#     EventDescriptor->Keyword    |= Keyword;
#     return (EventDescriptor);
# }
