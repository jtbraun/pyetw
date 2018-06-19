
import lxml.etree
from pprint import pprint
from collections import OrderedDict
import re
import ctypes as ct
import etw.provider as prov
import etw.evntprov as evntprov
import etw.tdh as tdh
from etw.guiddef import GUID
from ctypes import addressof, byref, cast, pointer, sizeof
from ctypes import POINTER, Structure
import winerror
import subprocess as sp

SCHEMA = "{http://schemas.microsoft.com/win/2004/08/events}"

class ParseException(Exception):
    pass

# "c:\Program Files (x86)\Windows Kits\8.1\Include\um\eventman.xsd"

class Provider(object):
    class _Data(object):
        __types = {
            # BUGBUG: get other types???
            'win:Int8': ct.c_int8,
            'win:UInt8': ct.c_uint8,
            'win:Int16': ct.c_int16,
            'win:UInt16': ct.c_uint16,
            'win:Int32': ct.c_int32,
            'win:UInt32': ct.c_uint32,
            'win:Int64': ct.c_int64,
            'win:UInt64': ct.c_uint64,
            'win:AnsiString': ct.c_char_p,
            'win:UnicodeString': ct.c_wchar_p,
            'win:Float': ct.c_float,
            'win:Double': ct.c_double,
            'win:Boolean': ct.c_ulong,
            # 'win:Binary': ???,
            'win:GUID': GUID,
            'win:Pointer': ct.c_void_p,
            # win:FILETIME
            # win:SYSTEMTIME
            # win:SID
            # win:HexInt32
            # win:HexInt64
        }

        def __init__(self, node):
            self.name = node.attrib['name']
            self.typ = self.__types[node.attrib['inType']]
            assert len(node.attrib) == 2

    class _Template(object):
        def __init__(self, provider, node):
            self.tid = node.attrib['tid']
            self.name = self.tid # alias
            assert len(node.attrib) == 1
            self.args = map(Provider._Data, node.iterchildren(tag=lxml.etree.Element))
        def __call__(self, *args):
            raise Exception("implement me")

    class _Keyword(object):
        def __init__(self, provider, node):
            self.name = node.attrib['name']
            self.mask = ct.c_ulonglong(long(node.attrib['mask'], 0))
            assert len(node.attrib) == 2

    class _Opcode(object):
        def __init__(self, provider, node):
            self.name = node.attrib['name']
            self.symbol = node.attrib['symbol']
            self.value = ct.c_ulong(int(node.attrib['value']))
            assert len(node.attrib) == 3

    class _Task(object):
        def __init__(self, provider, node):
            self.name = node.attrib['name']
            self.symbol = node.attrib['symbol']
            self.value = ct.c_ulong(int(node.attrib['value']))
            self.event_guid = GUID(node.attrib['eventGUID'])
            assert len(node.attrib) == 4

    class _Event(object):
        def __init__(self, provider, node):
            self.symbol = node.attrib['symbol']
            self.name = self.symbol # Alias
            self.template = provider.template[node.attrib['template']]
            self.value = ct.c_ulong(int(node.attrib['value']))
            self.task = provider.task[node.attrib['task']]
            self.opcode = provider.opcode[node.attrib['opcode']]
            try:
                self.keywords = node.attrib['keywords'].split(',') # BUGBUG: format?
                assert len(node.attrib) == 6
            except KeyError:
                self.keywords = []
                assert len(node.attrib) == 5
            self.keywords = [provider.keyword[keyword]
                             for keyword in self.keywords]

            self.descriptor = evntprov.EVENT_DESCRIPTOR
            self.descriptor.Id = self.value
            self.descriptor.Version = 0 # BUGBUG: optional attrib?
            self.descriptor.Channel = 0 # BUGBUG: optional attrib?
            self.descriptor.Level = 0 # BUGBUG: optional attrib?
            self.descriptor.Opcode = self.opcode.value
            self.descriptor.Task = self.task.value
            self.descriptor.Keyword = 0 # BUGBUG: or of all keywords?

        @property
        def enabled(self):
            return (Multi_MainEnableBits[0] & 0x00000001) != 0

        def write(self):
            return self.template(*args) if self.enabled else winerror.ERROR_SUCCESS

    def __init__(self, root):
        self._registration_handle = evntprov.REGHANDLE()
        self._callback = evntprov.ENABLE_CALLBACK(self._EnableCallback)
        self._is_enabled = 0
        self._match_any_keyword = 0
        self._match_all_keyword = 0
        # self._filter_data

        assert root.tag == SCHEMA + "provider"
        self.guid = GUID(root.attrib['guid'])
        self.name = root.attrib['name']
        self.symbol = root.attrib['symbol'] # BUGBUG: defaults to name?
        self.message_filename = root.attrib['messageFileName'] # BUGBUG: substitute %FOO%
        self.resource_filename = root.attrib['resourceFileName'] # BUGBUG substitute %FOO%
        for node in root:
            assert node.tag.startswith(SCHEMA)
            assert node.tag[-1] == 's'
            tag = node.tag[len(SCHEMA):-1]
            klass = '_' + tag[0].upper() + tag[1:]
            assert not hasattr(self, tag)
            if hasattr(self, klass):
                klass = getattr(self, klass)
                values = map(lambda x: klass(self, x), node.iterchildren(tag=lxml.etree.Element))
                dvalues = OrderedDict(
                    (val.name, val) for val in values)
                assert len(dvalues) == len(values)
                setattr(self, tag, dvalues)
            else:
                raise ParseException("Can't handle " + node.tag)
                pass

        # TODO: add other stuff from the full eventman.xsd: levels, etc
        for klass in ['template', 'keyword', 'opcode', 'task',
                      'event']:
            assert hasattr(self, klass)

        # If the provider is enabled, the enable callback will fire from
        # within the call to EventRegister, so don't touch anything that
        # the callback uses past this point.
        evntprov.EventRegister(
            self.guid,
            self._callback,
            None,
            byref(self._registration_handle))


    def __del__(self):
        """Cleanup our registration if one is still in effect."""
        if self._registration_handle.value != 0:
            evntprov.EventUnregister(self._registration_handle)
            self._registration_handle = 0

    def _EnableCallback(self,
                        source_id, # GUID
                        is_enabled, # ULONG
                        level, # UCHAR
                        match_any_keyword, # ULONGLONG
                        match_all_keyword, # ULONGLONG
                        filter_data, # PEVENT_FILTER_DESCRIPTOR
                        callback_context, # PVOID
    ):
        print  "In EnableCallback", is_enabled

        # if request == evntrace.WMI_ENABLE_EVENTS:
        #   return self._EnableEvents(buffer)
        # elif request == evntrace.WMI_DISABLE_EVENTS:
        #   return self._DisableEvents()

        # return winerror.ERROR_INVALID_PARAMETER



    def WriteString(self, msg, level=0, keyword=0):
        assert self._registration_handle
        # BUGBUG: check if enabled, or does EventWriteString do that for us?
        evntprov.EventWriteString(
            self._registration_handle,
            level, # ct.c_ubyte(level),
            keyword, # ct.c_ulonglong(keyword),
            msg)


class ProvidersNotRegistered(Exception):
    pass

class Test(object):
    def __init__(self, manifest_filename, force_register=False,
                 message_file_path=None,
                 resource_file_path=None,
    ):
        with open(manifest_filename) as f:
            tree = lxml.etree.parse(f)

        root = tree.getroot()

        # remove comments
        for node in root.iterdescendants():
            if isinstance(node, lxml.etree._Comment):
                pass
                # BUGBUG:RE MOVE
                #node.remove()

        assert root.tag == SCHEMA + "instrumentationManifest"
        assert len(root) == 1
        root = root[0]

        assert root.tag == SCHEMA + "instrumentation"
        assert len(root) == 1
        root = root[0]

        assert root.tag == SCHEMA + "events"
        self.providers = []
        for node in root.iterchildren(tag=lxml.etree.Element):
            self.providers.append(Provider(node))

        info = tdh.TdhEnumerateProviders()
        guids = dict((prov.ProviderGuid, prov.Name)
                     for prov in info.providers)
        any_registered = any(
            prov.guid in guids
            for prov in self.providers)
        for prov in self.providers:
            print "Checking if registered", prov.guid, prov.name, prov.guid in guids
        msgs = [(prov.name, prov.guid)
                for prov in self.providers
                if prov.guid not in guids]
        from pprint import pprint
        if force_register or msgs:
            if any_registered:
                print "Unregistering"
                args = ['wevtutil', 'uninstall-manifest', manifest_filename]
                sp.check_call(args)
            print "Registering"
            args = ['wevtutil', 'install-manifest', manifest_filename]
            if resource_file_path is not None:
                args.append('/resourceFilePath:' + resource_file_path)
            if message_file_path is not None:
                args.append('/messageFilePath:' + message_file_path)
            sp.check_call(args)
            info = tdh.TdhEnumerateProviders()
            guids = dict((prov.ProviderGuid, prov.Name)
                         for prov in info.providers)

        msgs = [(prov.name, prov.guid)
                for prov in self.providers
                if prov.guid not in guids]
        if msgs:
            raise ProvidersNotRegistered("Warning, these providers are not registered: %r" % (msgs,))

# for each event, generate:
#   EventEnabled<Symbol>: check mask against provider's enable bits
#   EventWrite<Symbol>: if enabled call template()
