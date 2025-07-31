import ctypes
import os

def lock_folder(path):
    if os.name == 'nt':
        ctypes.windll.kernel32.SetFileAttributesW(path, 0x02)  # hidden

def unlock_folder(path):
    if os.name == 'nt':
        ctypes.windll.kernel32.SetFileAttributesW(path, 0x80)  # normal

def hide_folder(path):
    lock_folder(path) 