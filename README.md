Snipt Sync
=====

Creates a context menu in Sublime Text 2 that allows you to insert your snippets from Snipt.net directly in Snipt.

Installation
====
1. Open Sublime Text 2 and click on Preferences -> Browse Packages   
2. Clone or download the files into this directory and rename it to "SniptSync"   
3. Restart Sublime Text 2   
4. Go to Preferences->Package Settings->Settings-User and paste in the following ```{   
    "snipt_api_key":"YOUR KEY HERE",   
    "snipt_username":"YOUR USERNAME HERE"   
   }```  
5. After inserting your information save the file  
   


Usage
====
**Sync Snipts** - This will sync all of your snipts and organize them in a context menu. When the syncing is done you should see an update in the status bar with how many snipts were added.

To sync your snipts go to Tools->Snipt Sync->Sync Snipts

**Insert Snipt** - To insert a snippet just right click in your file and go to the context menu item labeled "Snipts." Then just select the snipt you'd like to insert and it will be fetched from Snipt and inserted at your cursors position.

Future Functionality
====
- [ ] Allow you to create snipts from within Sublime
- [ ] Edit snipts from within Sublime Text
- [ ] Allow offline mode which would create Sublime snippets from snipt snippets.
- [ ] Expand comment list to ease users inserting of snippets
- [ ] Add threading so that the application doesn't freeze up while creating the context menu (basically the parsing of the JSON)
