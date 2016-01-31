#!/usr/sbin/python

import os
import shutil
import string
import ctypes
from ctypes import byref, wintypes, windll
import platform
import sys

GENERIC_READ              = wintypes.DWORD(0x80000000)
IOCTL_STORAGE_EJECT_MEDIA = wintypes.DWORD(0x002D4808)
OPEN_EXISTING             = wintypes.DWORD(0x00000003)
INVALID_HANDLE            = -1

#http://stackoverflow.com/questions/51658/cross-platform-space-remaining-on-volume-using-python/2372171#2372171
def get_disksize_kb(dirname):
    """Return folder/drive size (in megabytes)."""
    if platform.system() == 'Windows':
        total_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dirname), None, ctypes.pointer(total_bytes), None)
        return total_bytes.value / 1024 
    else:
        st = os.statvfs(dirname)
        return st.f_bavail * st.f_frsize / 1024


if __name__ == '__main__':
    print("Bootloading!")

    # windows!
    available_drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]


    # mac!
    # todo

    #linux!
    #todo
    
    print(available_drives)
    uploaddrive = ""
    for drive in available_drives:
        disksize = get_disksize_kb(drive)
        print("Drive %s = %d kB" % (drive, disksize))
        if (disksize == 40):
            print("Found Circuitplayground disk "+drive)
            uploaddrive = drive
            break
    if not uploaddrive:
        print("Did not find a circuit playground")
        exit(-1)

    # copy over the file!
    print("copying over %s" % sys.argv[1])

    os.system("copy %s %s\\flash.bin" % (sys.argv[1], drive))
    
    # eject drive
    # requires devcon from windows https://www.microsoft.com/en-us/download/details.aspx?id=11800
    os.system("EjectMedia64.exe %s" % drive)
