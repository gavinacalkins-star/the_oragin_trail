import ctypes
import os
import shutil
import subprocess
import sys
import time
from ctypes import wintypes
from pathlib import Path


ROOT = Path(__file__).parent
DIST = ROOT / "dist"
MEDIA_SRC = ROOT / "media"
MEDIA_DST = DIST / "media"
SAVES_DST = DIST / "saves"

USB_DRIVE = Path("E:/")
USB_DIST = USB_DRIVE / "dist"


def build():
    if DIST.exists():
        shutil.rmtree(DIST)

    subprocess.run(
        [sys.executable, "-m", "PyInstaller", "--onefile", "main.py"],
        cwd=ROOT,
        check=True,
    )

    SAVES_DST.mkdir(parents=True, exist_ok=True)

    shutil.copytree(MEDIA_SRC, MEDIA_DST)


def wait_for_usb_drive(poll_seconds=2):
    print("Waiting for drive E: to be connected...")
    while not USB_DRIVE.exists():
        time.sleep(poll_seconds)
    print("Drive E: detected.")


def sync_to_usb():
    if USB_DIST.exists():
        shutil.rmtree(USB_DIST)
    shutil.copytree(DIST, USB_DIST)


GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
FILE_SHARE_READ = 0x1
FILE_SHARE_WRITE = 0x2
OPEN_EXISTING = 3
INVALID_HANDLE_VALUE = wintypes.HANDLE(-1).value

FSCTL_LOCK_VOLUME = 0x00090018
FSCTL_DISMOUNT_VOLUME = 0x00090020
IOCTL_STORAGE_MEDIA_REMOVAL = 0x002D4804
IOCTL_STORAGE_EJECT_MEDIA = 0x002D4808

kernel32 = ctypes.windll.kernel32
kernel32.CreateFileW.restype = wintypes.HANDLE
kernel32.CreateFileW.argtypes = [
    wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD,
    wintypes.LPVOID, wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE,
]
kernel32.DeviceIoControl.restype = wintypes.BOOL
kernel32.DeviceIoControl.argtypes = [
    wintypes.HANDLE, wintypes.DWORD, wintypes.LPVOID, wintypes.DWORD,
    wintypes.LPVOID, wintypes.DWORD, ctypes.POINTER(wintypes.DWORD), wintypes.LPVOID,
]
kernel32.CloseHandle.argtypes = [wintypes.HANDLE]


def _ioctl(handle, code, in_buf=None, in_size=0):
    bytes_returned = wintypes.DWORD(0)
    ok = kernel32.DeviceIoControl(
        handle, code, in_buf, in_size, None, 0, ctypes.byref(bytes_returned), None
    )
    if not ok:
        raise ctypes.WinError(kernel32.GetLastError())


def eject_usb_drive():
    drive_letter = str(USB_DRIVE).rstrip("\\/").rstrip(":")
    volume_path = rf"\\.\{drive_letter}:"

    handle = kernel32.CreateFileW(
        volume_path,
        GENERIC_READ | GENERIC_WRITE,
        FILE_SHARE_READ | FILE_SHARE_WRITE,
        None,
        OPEN_EXISTING,
        0,
        None,
    )
    if handle in (0, INVALID_HANDLE_VALUE):
        raise ctypes.WinError(kernel32.GetLastError())

    try:
        _ioctl(handle, FSCTL_LOCK_VOLUME)
        _ioctl(handle, FSCTL_DISMOUNT_VOLUME)

        prevent_removal = wintypes.BYTE(0)
        _ioctl(
            handle,
            IOCTL_STORAGE_MEDIA_REMOVAL,
            ctypes.byref(prevent_removal),
            ctypes.sizeof(prevent_removal),
        )

        _ioctl(handle, IOCTL_STORAGE_EJECT_MEDIA)
    finally:
        kernel32.CloseHandle(handle)

    print(f"Drive {drive_letter}: ejected.")


def main():
    build()
    os.rename(DIST / "main.exe", DIST / "the_oregon_trail.exe")
    wait_for_usb_drive()
    sync_to_usb()
    eject_usb_drive()


if __name__ == "__main__":
    main()
