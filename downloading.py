import os
import sys
import dropbox
import time
import unicodedata
import  datetime

#Place your Access token here
#https://blogs.dropbox.com/developers/2014/05/generate-an-access-token-for-your-own-account/
#create a folder  named sync
dbx = dropbox.Dropbox("LrDrirXl4MAAAAAAAAAAFd-9G2yDUHjTEdktZ2r5GhAtHOpRYJ9huMHN4-kA3RQb")

#The folder path which must be sync (Use complete path)
dirpath = ""



############################/***Dont not change anything below this line***/#################################



DROPBOX_SYNC_LOCATION='/sync'



Totallist=dbx.files_list_folder(DROPBOX_SYNC_LOCATION,recursive=True)
Actual_list=Totallist.entries
listall_in_drive=list()

for files in Actual_list:

    if isinstance(files, dropbox.files.FileMetadata):
        file_path=files.path_display


        file_path_desktop = file_path.replace(DROPBOX_SYNC_LOCATION, dirpath)
        print(file_path_desktop)
        filetempname=file_path.replace(DROPBOX_SYNC_LOCATION, '')
        listall_in_drive.append(file_path_desktop)

        if os.path.exists(file_path_desktop) :
            '''
            if folder/file already exists
            '''
            mtime = os.path.getmtime(file_path_desktop)
            mtime_dt = datetime.datetime(*time.gmtime(mtime)[:6])
            if files.client_modified!=mtime_dt:
                dbx.files_download_to_file(file_path_desktop,file_path)


        else:
            '''
            if file doesnot exist
            '''
            temp=file_path_desktop.split('/')
            newpath="/"
            for each in range(0,len(temp)-1):
                newpath=newpath+temp[each]+'/'

            if not os.path.exists(newpath):
                os.makedirs(newpath)
                dbx.files_download_to_file(file_path_desktop, file_path)


            else:
                dbx.files_download_to_file(file_path_desktop, file_path)

#print(listall_in_drive)
for root, dirs, files in os.walk(dirpath):
    for filename in files:

        path = os.path.join(root, filename)
        if filename.startswith('.'):
            print('Skipping dot file:', filename)

        elif path not in listall_in_drive :
            print(path)
            os.remove(os.path.join(root,filename))
        if len(os.listdir(root)) == 0:
            #print(root)# check whether the directory is now empty after deletions, and if so, remove it
            os.removedirs(root)
#removeEmptyFolders(dirpath)





