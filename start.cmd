@echo off

REM xperf.exe -start "NT Kernel Logger" -on Latency+POWER+DISPATCHER+DISK_IO_INIT+FILE_IO+FILE_IO_INIT+VIRT_ALLOC+MEMINFO -stackwalk PROFILE+CSWITCH+READYTHREAD -buffersize 1024 -minbuffers 600 -maxbuffers 600 -f "C:\Users\jbraun\AppData\Local\Temp\kernel.etl" -start UIforETWSession -on Microsoft-Windows-Win32k:0xfdffffffefffffff+Multi-MAIN+Multi-FrameRate+Multi-Input+Multi-Worker+Microsoft-Windows-Kernel-Memory:0xE0 -buffersize 1024 -minbuffers 100 -maxbuffers 100 -f "C:\Users\jbraun\AppData\Local\Temp\user.etl"
REM Tracing is started.


xperf.exe -start UIforETWSession -on Multi-MAIN+Multi-FrameRate+Multi-Input+Multi-Worker -buffersize 1024 -minbuffers 100 -maxbuffers 100 -f "user.etl"
xperf.exe -capturestate UIforETWSession Multi-MAIN+Multi-FrameRate+Multi-Input+Multi-Worker

REM xperf.exe -stop UIforETWSession -stop "NT Kernel Logger"
