# Report

#### Why i choose dropbox?
None of Drives has good REST APIs. On searching, found Dropbox has released REST API v2 (version 2 ) recently. So i choosed Dropbox for this problem.

#### Approach

I found 3 types of approach to given problem:  
First one, I thought to hash the files and folders and when ever i find a change in their hashes then I could upload file into dropbox and same with download.  
The second was to use SSH instead of Drive as my server.  
Lastly, I found the easy way where i can use Metadata of file/directory i.e last modified date and time and upload or download accordingly.  
( If file in local folder is recently modified comapred to the same file in dropbox, then i will upload the file and download for vice versa.)  

##### Note:
The sync happens as per time u choose in deploying Cron job.  
Time complexity: O(n*m) ( for both upload and download n = files in dropbox m = files in local folder ) . 




