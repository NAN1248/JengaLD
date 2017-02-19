# Dependencies: pywin32, boto3
# https://sourceforge.net/projects/pywin32/files/pywin32/
# pip install boto3

import os
import datetime
import win32file
import win32event
import win32con
import boto3

savefilepath = os.path.abspath('.')
savefilename = 'jengastate.sav'
s3 = boto3.resource('s3')
bucket = 'jengalongdistance'
gameidkey = 'game1'

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
    data = open(savefilename, 'rb')
    s3.Bucket(bucket).put_object(Key=gameidkey, Body=data)
    print(savefilename, ' in ', os.listdir(savefilepath), ' uploaded at ', datetime.datetime.now())
      
main()