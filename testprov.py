import etw.provider as prov
import messages
import subprocess as sp
from ctypes import cdll
import time

dll = cdll.LoadLibrary("C:\\Users\\jbraun\\AppData\\Local\\Temp\\ETWProviders64.dll")
print dll
t = messages.Test('../UIforETW/ETWProviders/etwproviders.man',
                  force_register=False)


provstr = ''
for p in t.providers:
    if len(provstr):
        provstr += '+'
    provstr += str(p.name)
    #provstr += ':0xffffff:5'
# sp.check_call(['xperf', '-start', 'UserTrace', '-on',
#                provstr])


for p in t.providers:
    print p
    p.WriteString(str(p))
    time.sleep(0.2)
print "TRACED!"

# sp.check_call(['xperf', '-stop', 'UserTrace', '-d', 'out.etl'])
