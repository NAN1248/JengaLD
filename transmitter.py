# Dependencies: pywin32, requests
# https://sourceforge.net/projects/pywin32/files/pywin32/
# pip install requests
import os
import datetime

import win32file
import win32event
import win32con

savefilepath = os.path.abspath('.')

def main():
    change_handle = win32file.FindFirstChangeNotification(savefilepath, 0, win32con.FILE_NOTIFY_CHANGE_LAST_WRITE)

    try:
        while True:
            # 500 ms timeout
            result = win32event.WaitForSingleObject(change_handle, 500)
            
            if result == win32con.WAIT_OBJECT_0:
                uploadsave()
                win32file.FindNextChangeNotification(change_handle)
    finally:
        win32file.FindCloseChangeNotification(change_handle)
      
def uploadsave():
    print(os.listdir(savefilepath), ' updated at ', datetime.datetime.now())
      
main()