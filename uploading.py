'''
It must runned as Daemon, which is a background process and it never dies until force stopping it.
Refer :https://stackoverflow.com/questions/4797050/how-to-run-process-as-background-and-never-die
The watchdog module fires on_modified function which uploads the changes in the directory to dropbox

'''


import os
import contextlib
import dropbox
import time
import glob
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import datetime

#Place your Access token here
#https://blogs.dropbox.com/developers/2014/05/generate-an-access-token-for-your-own-account/
#create a folder  named sync
dbx = dropbox.Dropbox("LrDrirXl4MAAAAAAAAAAFd-9G2yDUHjTEdktZ2r5GhAtHOpRYJ9huMHN4-kA3RQb")

#The folder path which must be sync (Use complete path)
dirpath = ""


############################/***Dont not change anything below this line***/#################################

DROPBOX_SYNC_LOCATION='/sync'

@contextlib.contextmanager
def stopwatch(message):
    """Context manager to print how long a block of code took."""
    t0 = time.time()
    try:
        yield
    finally:
        t1 = time.time()
        print('Total elapsed time for %s: %.3f' % (message, t1 - t0))



def upload(dbx, fullname, folder, subfolder, name, overwrite=False):
    """Upload a file.
    Return the request response, or None in case of error.
    """
    path = '/%s/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'), name)
    while '//' in path:
        path = path.replace('//', '/')
    mode = (dropbox.files.WriteMode.overwrite
            if overwrite
            else dropbox.files.WriteMode.add)
    mtime = os.path.getmtime(fullname)
    with open(fullname, 'rb') as f:
        data = f.read()
    with stopwatch('upload %d bytes' % len(data)):
        try:
            res = dbx.files_upload(
                data, path, mode,
                client_modified=datetime.datetime(*time.gmtime(mtime)[:6]),
                mute=True)
        except dropbox.exceptions.ApiError as err:
            print('*** API error', err)
            return None
    print('uploaded as', res.name.encode('utf8'))
    return res



class MyHandler(FileSystemEventHandler):
    """
        Base file system event handler that you can override methods from.
    """
    def on_any_event(self, event):
        '''
        Called on any event like modify,create,delete

        '''

        dbx.files_delete_v2(DROPBOX_SYNC_LOCATION)

        for root, dirs, files in os.walk(dirpath):
            for filename in files:
                if filename.startswith('.'):
                    print('Skipping dot file:', filename)
                elif filename.startswith('@') or filename.endswith('~'):
                    print('Skipping temporary file:', filename)
                elif filename.endswith('.pyc') or filename.endswith('.pyo'):
                    print('Skipping generated file:', filename)
                else:
                    local_path = os.path.join(root, filename)
                    DROP_BOX_PATH = local_path.replace("/Users/sriniakhilgl/Desktop/test2", "")
                    toget_subfolder=DROP_BOX_PATH.split('/')
                    length=len(toget_subfolder)
                    DROP_BOX_PATH = DROPBOX_SYNC_LOCATION + DROP_BOX_PATH

                    mtime = os.path.getmtime(local_path)
                    mtime_dt = datetime.datetime(*time.gmtime(mtime)[:6])
                    #print(mtime_dt)
                    upload(dbx,local_path,DROPBOX_SYNC_LOCATION,toget_subfolder[length-2],filename,overwrite=True)




if __name__ == "__main__":
    '''
        main class 
    '''
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=dirpath, recursive=True)
    observer.start() #start thread
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
