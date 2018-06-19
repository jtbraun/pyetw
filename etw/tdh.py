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
"""This file contains declarations gleaned from the tdh.h file from
the Platform SDK. Many of the ct.Structures here are simplified from their
Platform SDK version by not in-lining one of the options of unions they
contain.
"""

import ctypes as ct
import ctypes.wintypes as wt
import exceptions
from guiddef import GUID
from evntrace import CheckWinError
from relogger import EVENT_DESCRIPTOR, EVENT_RECORD
import winerror

#import evntrace
#import evntcons

TDHSTATUS = ct.c_ulong

class _U(ct.Union):
    _fields_ = [('Value', ct.c_ulong),       # For ULONG value (valuemap and bitmap).
                ('InputOffset', ct.c_ulong)] # For String value (patternmap or valuemap in WBEM).

class EVENT_MAP_ENTRY(ct.Structure):
    _anonymous_ = ['u']
    _fields_ = [('OutputOffset', ct.c_ulong),
                ('u', _U)]

# typedef enum MAP_FLAGS {
MAP_FLAGS = ct.c_int32
EVENTMAP_INFO_FLAG_MANIFEST_VALUEMAP = 0x1
EVENTMAP_INFO_FLAG_MANIFEST_BITMAP = 0x2
EVENTMAP_INFO_FLAG_MANIFEST_PATTERNMAP = 0x4
EVENTMAP_INFO_FLAG_WBEM_VALUEMAP = 0x8
EVENTMAP_INFO_FLAG_WBEM_BITMAP = 0x10
EVENTMAP_INFO_FLAG_WBEM_FLAG = 0x20
EVENTMAP_INFO_FLAG_WBEM_NO_MAP = 0x40


# typedef enum MAP_VALUETYPE {
MAP_VALUETYPE = ct.c_int32
EVENTMAP_ENTRY_VALUETYPE_ULONG = 0
EVENTMAP_ENTRY_VALUETYPE_STRING = 1

class _U(ct.Union):
    _fields_ = [('MapEntryValueType', MAP_VALUETYPE),
                ('FormatStringOffset', ct.c_ulong)]

class EVENT_MAP_INFO(ct.Structure):
    EntryCount = 0
    _anonymous_ = ['u']
    _fields_ = [('NameOffset', ct.c_ulong),
                ('Flag', MAP_FLAGS),
                ('EntryCount', ct.c_ulong),
                ('u', _U),
                ('MapEntryArray', EVENT_MAP_ENTRY * EntryCount)]

# Intypes and outtypes are defined in winmeta.xml.

# enum TDH_IN_TYPE
TDH_INTYPE_NULL = 0
TDH_INTYPE_UNICODESTRING = 1
TDH_INTYPE_ANSISTRING = 2
TDH_INTYPE_INT8 = 3
TDH_INTYPE_UINT8 = 4
TDH_INTYPE_INT16 = 5
TDH_INTYPE_UINT16 = 6
TDH_INTYPE_INT32 = 7
TDH_INTYPE_UINT32 = 8
TDH_INTYPE_INT64 = 9
TDH_INTYPE_UINT64 = 10
TDH_INTYPE_FLOAT = 11
TDH_INTYPE_DOUBLE = 12
TDH_INTYPE_BOOLEAN = 13
TDH_INTYPE_BINARY = 14
TDH_INTYPE_GUID = 15
TDH_INTYPE_POINTER = 16
TDH_INTYPE_FILETIME = 17
TDH_INTYPE_SYSTEMTIME = 18
TDH_INTYPE_SID = 19
TDH_INTYPE_HEXINT32 = 20
TDH_INTYPE_HEXINT64 = 21                # End of winmeta intypes.
TDH_INTYPE_COUNTEDSTRING = 300          # Start of TDH intypes for WBEM.
TDH_INTYPE_COUNTEDANSISTRING = 301
TDH_INTYPE_REVERSEDCOUNTEDSTRING = 302
TDH_INTYPE_REVERSEDCOUNTEDANSISTRING = 303
TDH_INTYPE_NONNULLTERMINATEDSTRING = 304
TDH_INTYPE_NONNULLTERMINATEDANSISTRING = 305
TDH_INTYPE_UNICODECHAR = 306
TDH_INTYPE_ANSICHAR = 307
TDH_INTYPE_SIZET = 308
TDH_INTYPE_HEXDUMP = 309
TDH_INTYPE_WBEMSID = 310

# enum TDH_OUT_TYPE
TDH_OUTTYPE_NULL = 0
TDH_OUTTYPE_STRING = 1
TDH_OUTTYPE_DATETIME = 2
TDH_OUTTYPE_BYTE = 3
TDH_OUTTYPE_UNSIGNEDBYTE = 4
TDH_OUTTYPE_SHORT = 5
TDH_OUTTYPE_UNSIGNEDSHORT = 6
TDH_OUTTYPE_INT = 7
TDH_OUTTYPE_UNSIGNEDINT = 8
TDH_OUTTYPE_LONG = 9
TDH_OUTTYPE_UNSIGNEDLONG = 10
TDH_OUTTYPE_FLOAT = 11
TDH_OUTTYPE_DOUBLE = 12
TDH_OUTTYPE_BOOLEAN = 13
TDH_OUTTYPE_GUID = 14
TDH_OUTTYPE_HEXBINARY = 15
TDH_OUTTYPE_HEXINT8 = 16
TDH_OUTTYPE_HEXINT16 = 17
TDH_OUTTYPE_HEXINT32 = 18
TDH_OUTTYPE_HEXINT64 = 19
TDH_OUTTYPE_PID = 20
TDH_OUTTYPE_TID = 21
TDH_OUTTYPE_PORT = 22
TDH_OUTTYPE_IPV4 = 23
TDH_OUTTYPE_IPV6 = 24
TDH_OUTTYPE_SOCKETADDRESS = 25
TDH_OUTTYPE_CIMDATETIME = 26
TDH_OUTTYPE_ETWTIME = 27
TDH_OUTTYPE_XML = 28
TDH_OUTTYPE_ERRORCODE = 29
TDH_OUTTYPE_WIN32ERROR = 30
TDH_OUTTYPE_NTSTATUS = 31
TDH_OUTTYPE_HRESULT = 32          # End of winmeta outtypes.
TDH_OUTTYPE_CULTURE_INSENSITIVE_DATETIME = 33 # Culture neutral datetime string.
TDH_OUTTYPE_REDUCEDSTRING = 300 # Start of TDH outtypes for WBEM.
TDH_OUTTYPE_NOPRINT = 301

#define TDH_OUTYTPE_ERRORCODE TDH_OUTTYPE_ERRORCODE

# enum PROPERTY_FLAGS
PROPERTY_FLAGS = ct.c_int32
PropertyStruct        = 0x1      # Type is struct.
PropertyParamLength   = 0x2      # Length field is index of param with length.
PropertyParamCount    = 0x4      # Count file is index of param with count.
PropertyWBEMXmlFragment = 0x8    # WBEM extension flag for property.
PropertyParamFixedLength = 0x10  # Length of the parameter is fixed.

class _nonStructType(ct.Structure):
    _fields_ = [
        ('InType', ct.c_ushort),
        ('OutType', ct.c_ushort),
        ('MapNameOffset', ct.c_ulong)]

class _structType(ct.Structure):
    _fields_ = [
        ('StructStartIndex', ct.c_ushort),
        ('NumOfStructMembers', ct.c_ushort),
        ('padding', ct.c_ulong)]

class _U1(ct.Union):
    _fields_ = [('nonStructType', _nonStructType),
                ('structType', _structType)]


class _U2(ct.Union):
    _fields_ = [('count', ct.c_ushort),
                ('countPropertyIndex', ct.c_ushort)]

class _U3(ct.Union):
    _fields_ = [('length', ct.c_ushort),
                ('lengthPropertyIndex', ct.c_ushort)]

class EVENT_PROPERTY_INFO(ct.Structure):
    _anonymous_ = ['u', 'ucount', 'ulen']
    _fields = [('Flags', PROPERTY_FLAGS),
               ('NameOffset', ct.c_ulong),
               ('u', _U1),
               ('ucount', _U2),
               ('ulen', _U3),
               ('Reserved', ct.c_ulong)]

# typedef enum DECODING_SOURCE {
DECODING_SOURCE = ct.c_int32
DecodingSourceXMLFile = 0
DecodingSourceWbem = 1
DecodingSourceWPP = 2

# Copy from Binres.h
# typedef enum TEMPLATE_FLAGS
TEMPLATE_FLAGS = ct.c_int32
TEMPLATE_EVENT_DATA = 1, # Used when custom xml is not specified.
TEMPLATE_USER_DATA = 2   # Used when custom xml is specified.


class TRACE_EVENT_INFO(ct.Structure):
    PropertyCount = 0
    _flags_ = [('ProviderGuid', GUID),
    ('EventGuid', GUID),
    ('EventDescriptor', EVENT_DESCRIPTOR),
    ('DecodingSource', DECODING_SOURCE),
    ('ProviderNameOffset', ct.c_ulong),
    ('LevelNameOffset', ct.c_ulong),
    ('ChannelNameOffset', ct.c_ulong),
    ('KeywordsNameOffset', ct.c_ulong),
    ('TaskNameOffset', ct.c_ulong),
    ('OpcodeNameOffset', ct.c_ulong),
    ('EventMessageOffset', ct.c_ulong),
    ('ProviderMessageOffset', ct.c_ulong),
    ('BinaryXMLOffset', ct.c_ulong),
    ('BinaryXMLSize', ct.c_ulong),
    ('ActivityIDNameOffset', ct.c_ulong),
    ('RelatedActivityIDNameOffset', ct.c_ulong),
    ('PropertyCount', ct.c_ulong),
    ('TopLevelPropertyCount', ct.c_ulong),
    ('Flags', TEMPLATE_FLAGS),
    ('EventPropertyInfoArray', EVENT_PROPERTY_INFO * PropertyCount)]

class PROPERTY_DATA_DESCRIPTOR(ct.Structure):
    _fields_ = [('PropertyName', ct.c_ulonglong), # Pointer to property name.
                ('ArrayIndex', ct.c_ulong),       # Array Index.
                ('Reserved', ct.c_ulong)]

#
# Provider-side filters.
#

class PROVIDER_FILTER_INFO(ct.Structure):
    PropertyCount = 0
    _fields_ = [('Id', ct.c_ubyte),
                ('Version', ct.c_ubyte),
                ('MessageOffset', ct.c_ulong),
                ('Reserved', ct.c_ulong),
                ('PropertyCount', ct.c_ulong),
                ('EventPropertyInfoArray', EVENT_PROPERTY_INFO * PropertyCount)]

# Provider Enumeration.

# typedef enum EVENT_FIELD_TYPE
EVENT_FIELD_TYPE = ct.c_int32
EventKeywordInformation = 0,
EventLevelInformation = 1
EventChannelInformation = 2
EventTaskInformation = 3
EventOpcodeInformation = 4
EventInformationMax = 5


class PROVIDER_FIELD_INFO(ct.Structure):
    _fields_ = [('NameOffset', ct.c_ulong), # English only.
                ('DescriptionOffset', ct.c_ulong), # Localizable String.
                ('Value', ct.c_ulonglong)]

class PROVIDER_FIELD_INFOARRAY(ct.Structure):
    NumberOfElements = 0
    _fields_ = [('NumberOfElements', ct.c_ulong),
                ('FieldType', EVENT_FIELD_TYPE),
                ('FieldInfoArray', PROVIDER_FIELD_INFO * NumberOfElements)]

class TRACE_PROVIDER_INFO(ct.Structure):
    _fields_ = [('ProviderGuid', GUID),
                ('SchemaSource', ct.c_ulong),
                ('ProviderNameOffset', ct.c_ulong)]

class _PROVIDER_ENUMERATION_INFO(ct.Structure):
    _fields_ = [('NumberOfProviders', ct.c_ulong),
                ('Reserved', ct.c_ulong),
                #('TraceProviderInfoArray', TRACE_PROVIDER_INFO * NumberOfProviders)
                #('TraceProviderInfoArray', ct.c_ubyte), #TRACE_PROVIDER_INFO * NumberOfProviders)
    ]

#typedef enum TDH_CONTEXT_TYPE
TDH_CONTEXT_TYPE = ct.c_int32
TDH_CONTEXT_WPP_TMFFILE = 0,
TDH_CONTEXT_WPP_TMFSEARCHPATH = 1
TDH_CONTEXT_WPP_GMT = 2
TDH_CONTEXT_POINTERSIZE = 3
TDH_CONTEXT_MAXIMUM = 4

class TDH_CONTEXT(ct.Structure):
    _fields_ = [('ParameterValue', ct.c_ulonglong), # Pointer to Data.
                ('ParameterType', TDH_CONTEXT_TYPE),
                ('ParameterSize', ct.c_ulong)]

CheckTdhError = CheckWinError

def CheckTdhSizeError(result, func, arguments):
    if result != winerror.ERROR_INSUFFICIENT_BUFFER:
        CheckWinError(result, func, arguments)
    return result

_ = TdhGetEventInformation = ct.windll.tdh.TdhGetEventInformation
_.argtypes = [
    ct.POINTER(EVENT_RECORD), # Event,
    ct.c_ulong, # TdhContextCount,
    ct.POINTER(TDH_CONTEXT), # TdhContext,
    ct.POINTER(TRACE_EVENT_INFO), # Buffer,
    ct.POINTER(ct.c_ulong), # BufferSize
]
_.restype = TDHSTATUS
_.errcheck = CheckTdhError

_ = TdhGetEventMapInformation = ct.windll.tdh.TdhGetEventMapInformation
_.argtypes = [
    ct.POINTER(EVENT_RECORD), # pEvent,
    ct.c_wchar_p, # pMapName,
    ct.POINTER(EVENT_MAP_INFO), # pBuffer,
    ct.POINTER(ct.c_ulong) # pBufferSize
]
_.restype = TDHSTATUS
_.errcheck = CheckTdhError

_ = TdhGetPropertySize = ct.windll.tdh.TdhGetPropertySize
_.argtypes = [
    ct.POINTER(EVENT_RECORD), # pEvent,
    ct.c_ulong, # TdhContextCount,
    ct.POINTER(TDH_CONTEXT), # pTdhContext,
    ct.c_ulong, # PropertyDataCount,
    ct.POINTER(PROPERTY_DATA_DESCRIPTOR), # pPropertyData,
    ct.POINTER(ct.c_ulong), # pPropertySize
]
_.restype = TDHSTATUS
_.errcheck = CheckTdhError

_ = TdhGetProperty = ct.windll.tdh.TdhGetProperty
_.argtypes = [
    ct.POINTER(EVENT_RECORD), # pEvent,
     ct.c_ulong, # TdhContextCount,
    ct.POINTER(TDH_CONTEXT), # pTdhContext,
    ct.c_ulong, # PropertyDataCount,
    ct.POINTER(PROPERTY_DATA_DESCRIPTOR), # pPropertyData,
    ct.c_ulong, # BufferSize,
    ct.POINTER(ct.c_ubyte), # pBuffer
]
_.restype = TDHSTATUS
_.errcheck = CheckTdhError

_ = _TdhEnumerateProviders = ct.windll.tdh.TdhEnumerateProviders
_.argtypes = [
    #ct.POINTER(PROVIDER_ENUMERATION_INFO), # pBuffer,
    ct.POINTER(ct.c_ubyte), # pBuffer,
    ct.POINTER(ct.c_ulong), # *pBufferSize
]
_.restype = TDHSTATUS
_.errcheck = CheckTdhSizeError

def TdhEnumerateProviders():
    buf = None
    buffersize = ct.c_ulong(0)
    status = _TdhEnumerateProviders(buf, ct.byref(buffersize))
    while status == winerror.ERROR_INSUFFICIENT_BUFFER:
        buf = (ct.c_ubyte * buffersize.value)()
        status = _TdhEnumerateProviders(buf, ct.byref(buffersize))
    count = ct.c_ulong.from_buffer(buf).value
    # BUGBUG: This is gross, is there a better way to do this?
    info = _PROVIDER_ENUMERATION_INFO.from_address(ct.addressof(buf))
    providers = []
    for i in xrange(info.NumberOfProviders):
        provider = TRACE_PROVIDER_INFO.from_address(
            ct.addressof(buf) + 8 + i * ct.sizeof(TRACE_PROVIDER_INFO))
        offset = provider.ProviderNameOffset
        setattr(provider, 'Name', ct.wstring_at(ct.addressof(buf)+offset))
        providers.append(provider)
    setattr(info, 'providers', providers)
    setattr(info, '__buffer', buf)
    return info

_ = TdhQueryProviderFieldInformation = ct.windll.tdh.TdhQueryProviderFieldInformation
_.argtypes = [
    ct.POINTER(GUID), # lpGuid,
    ct.c_ulonglong, # EventFieldValue,
    EVENT_FIELD_TYPE, # EventFieldType,
    ct.POINTER(PROVIDER_FIELD_INFOARRAY), # pBuffer,
    ct.POINTER(ct.c_ulong), # pBufferSize
]
_.restype = TDHSTATUS
_.errcheck = CheckTdhError

_ = TdhEnumerateProviderFieldInformation = ct.windll.tdh.TdhEnumerateProviderFieldInformation
_.argtypes = [
    ct.POINTER(GUID), # pGuid,
    EVENT_FIELD_TYPE, # EventFieldType,
    ct.POINTER(PROVIDER_FIELD_INFOARRAY), # pBuffer,
    ct.POINTER(ct.c_ulong), # pBufferSize
]
_.restype = TDHSTATUS
_.errcheck = CheckTdhError

_ = TdhEnumerateProviderFilters = ct.windll.tdh.TdhEnumerateProviderFilters
_.argtypes = [
    ct.POINTER(GUID), # Guid,
    ct.c_ulong, # TdhContextCount,
    ct.POINTER(TDH_CONTEXT), # TdhContext,
    ct.POINTER(ct.c_ulong), # FilterCount,
    ct.POINTER(PROVIDER_FILTER_INFO), # *Buffer,
    ct.POINTER(ct.c_ulong), # *BufferSize
]
_.restype = TDHSTATUS
_.errcheck = CheckTdhError

_ = TdhLoadManifest = ct.windll.tdh.TdhLoadManifest
_.argtypes = [
    ct.c_wchar_p, # Manifest
]
_.restype = TDHSTATUS
_.errcheck = CheckTdhError

_ = TdhUnloadManifest = ct.windll.tdh.TdhUnloadManifest
_.argtypes = [
    ct.c_wchar_p, # Manifest
]
_.restype = TDHSTATUS
_.errcheck = CheckTdhError

_ = TdhFormatProperty = ct.windll.tdh.TdhFormatProperty
_.argtypes = [
    ct.POINTER(TRACE_EVENT_INFO), # EventInfo,
    ct.POINTER(EVENT_MAP_INFO), # MapInfo,
    ct.c_ulong, # PointerSize,
    ct.c_ushort, # PropertyInType,
    ct.c_ushort, # PropertyOutType,
    ct.c_ushort, # PropertyLength,
    ct.c_ushort, # UserDataLength,
    ct.POINTER(ct.c_ubyte), # UserData,
    ct.POINTER(ct.c_ulong), # BufferSize,
    ct.c_wchar_p, # Buffer
    ct.POINTER(ct.c_ushort), # UserDataConsumed
]
_.restype = TDHSTATUS
_.errcheck = CheckTdhError

#
#  Helper macros to access strings from variable length Tdh structures.
#

# FORCEINLINE
# PWSTR
# EMI_MAP_NAME(
#      PEVENT_MAP_INFO MapInfo
#     )
# {
#     return (MapInfo->NameOffset == 0) ?
#            NULL :
#            (PWSTR)((PBYTE)MapInfo + MapInfo->NameOffset);
# }

# FORCEINLINE
# PWSTR
# EMI_MAP_FORMAT(
#      PEVENT_MAP_INFO MapInfo
#     )
# {
#     if ((MapInfo->Flag & EVENTMAP_INFO_FLAG_MANIFEST_PATTERNMAP) &&
#         (MapInfo->FormatStringOffset)) {
#         return (PWSTR)((PBYTE)MapInfo + MapInfo->FormatStringOffset);
#     } else {
#         return NULL;
#     }
# }

# FORCEINLINE
# PWSTR
# EMI_MAP_OUTPUT(
#      PEVENT_MAP_INFO MapInfo,
#      PEVENT_MAP_ENTRY Map
#     )
# {
#     return (Map->OutputOffset == 0) ?
#            NULL :
#            (PWSTR)((PBYTE)MapInfo + Map->OutputOffset);
# }

# FORCEINLINE
# PWSTR
# EMI_MAP_INPUT(
#      PEVENT_MAP_INFO MapInfo,
#      PEVENT_MAP_ENTRY Map
#     )
# {
#     if ((MapInfo->Flag & EVENTMAP_INFO_FLAG_MANIFEST_PATTERNMAP) &&
#         (Map->InputOffset != 0)) {
#         return (PWSTR)((PBYTE)MapInfo + Map->InputOffset);
#     } else {
#         return NULL;
#     }
# }

# FORCEINLINE
# PWSTR
# TEI_MAP_NAME(
#      PTRACE_EVENT_INFO EventInfo,
#      PEVENT_PROPERTY_INFO Property
#     )
# {
#     return (Property->nonStructType.MapNameOffset == 0) ?
#            NULL :
#            (PWSTR)((PBYTE)EventInfo + Property->nonStructType.MapNameOffset);
# }

# FORCEINLINE
# PWSTR
# TEI_PROPERTY_NAME(
#      PTRACE_EVENT_INFO EventInfo,
#      PEVENT_PROPERTY_INFO Property
#     )
# {
#     return (Property->NameOffset == 0) ?
#            NULL :
#            (PWSTR)((PBYTE)EventInfo + Property->NameOffset);
# }

# FORCEINLINE
# PWSTR
# TEI_PROVIDER_NAME(
#      PTRACE_EVENT_INFO EventInfo
#     )
# {
#     return (EventInfo->ProviderNameOffset == 0) ?
#            NULL :
#            (PWSTR)((PBYTE)EventInfo + EventInfo->ProviderNameOffset);
# }

# FORCEINLINE
# PWSTR
# TEI_LEVEL_NAME(
#      PTRACE_EVENT_INFO EventInfo
#     )
# {
#     return (EventInfo->LevelNameOffset == 0) ?
#            NULL :
#            (PWSTR)((PBYTE)EventInfo + EventInfo->LevelNameOffset);
# }

# FORCEINLINE
# PWSTR
# TEI_CHANNEL_NAME(
#      PTRACE_EVENT_INFO EventInfo
#     )
# {
#     return (EventInfo->ChannelNameOffset == 0) ?
#            NULL :
#            (PWSTR)((PBYTE)EventInfo + EventInfo->ChannelNameOffset);
# }

# FORCEINLINE
# PWSTR
# TEI_KEYWORDS_NAME(
#      PTRACE_EVENT_INFO EventInfo
#     )
# {
#     return (EventInfo->KeywordsNameOffset == 0) ?
#            NULL :
#            (PWSTR)((PBYTE)EventInfo + EventInfo->KeywordsNameOffset);
# }

# FORCEINLINE
# PWSTR
# TEI_TASK_NAME(
#      PTRACE_EVENT_INFO EventInfo
#     )
# {
#     return (EventInfo->TaskNameOffset == 0) ?
#            NULL :
#            (PWSTR)((PBYTE)EventInfo + EventInfo->TaskNameOffset);
# }

# FORCEINLINE
# PWSTR
# TEI_OPCODE_NAME(
#      PTRACE_EVENT_INFO EventInfo
#     )
# {
#     return (EventInfo->OpcodeNameOffset == 0) ?
#            NULL :
#            (PWSTR)((PBYTE)EventInfo + EventInfo->OpcodeNameOffset);
# }

# FORCEINLINE
# PWSTR
# TEI_EVENT_MESSAGE(
#      PTRACE_EVENT_INFO EventInfo
#     )
# {
#     return (EventInfo->EventMessageOffset == 0) ?
#            NULL :
#            (PWSTR)((PBYTE)EventInfo + EventInfo->EventMessageOffset);
# }

# FORCEINLINE
# PWSTR
# TEI_PROVIDER_MESSAGE(
#      PTRACE_EVENT_INFO EventInfo
#     )
# {
#     return (EventInfo->ProviderMessageOffset == 0) ?
#            NULL :
#            (PWSTR)((PBYTE)EventInfo + EventInfo->ProviderMessageOffset);
# }

# FORCEINLINE
# PWSTR
# TEI_ACTIVITYID_NAME(
#      PTRACE_EVENT_INFO EventInfo
#     )
# {
#     return (EventInfo->ActivityIDNameOffset == 0) ?
#            NULL :
#            (PWSTR)((PBYTE)EventInfo + EventInfo->ActivityIDNameOffset);
# }

# FORCEINLINE
# PWSTR
# TEI_RELATEDACTIVITYID_NAME(
#      PTRACE_EVENT_INFO EventInfo
#     )
# {
#     return (EventInfo->RelatedActivityIDNameOffset == 0) ?
#            NULL :
#            (PWSTR)((PBYTE)EventInfo + EventInfo->RelatedActivityIDNameOffset);
# }

# #if (WINVER >= _WIN32_WINNT_WIN7)
# FORCEINLINE
# PWSTR
# PFI_FILTER_MESSAGE(
#      PPROVIDER_FILTER_INFO FilterInfo
#     )
# {
#     return (FilterInfo->MessageOffset == 0) ?
#            NULL :
#            (PWSTR)((PBYTE)FilterInfo + FilterInfo->MessageOffset);
# }
# #endif

# #if (WINVER >= _WIN32_WINNT_WIN7)
# FORCEINLINE
# PWSTR
# PFI_PROPERTY_NAME(
#      PPROVIDER_FILTER_INFO FilterInfo,
#      PEVENT_PROPERTY_INFO Property
#     )
# {
#     return (Property->NameOffset == 0) ?
#            NULL :
#            (PWSTR)((PBYTE)FilterInfo + Property->NameOffset);
# }
# #endif

# FORCEINLINE
# PWSTR
# PFI_FIELD_NAME(
#      PPROVIDER_FIELD_INFOARRAY FieldInfoArray,
#      PPROVIDER_FIELD_INFO FieldInfo
#     )
# {
#     return (FieldInfo->NameOffset == 0) ?
#            NULL :
#            (PWSTR)((PBYTE)FieldInfoArray + FieldInfo->NameOffset);
# }

# FORCEINLINE
# PWSTR
# PFI_FIELD_MESSAGE(
#      PPROVIDER_FIELD_INFOARRAY FieldInfoArray,
#      PPROVIDER_FIELD_INFO FieldInfo
#     )
# {
#     return (FieldInfo->DescriptionOffset == 0) ?
#            NULL :
#            (PWSTR)((PBYTE)FieldInfoArray + FieldInfo->DescriptionOffset);
# }

# FORCEINLINE
# PWSTR
# PEI_PROVIDER_NAME(
#      PPROVIDER_ENUMERATION_INFO ProviderEnum,
#      PTRACE_PROVIDER_INFO ProviderInfo
#     )
# {
#     return (ProviderInfo->ProviderNameOffset == 0) ?
#            NULL :
#            (PWSTR)((PBYTE)ProviderEnum + ProviderInfo->ProviderNameOffset);
# }
