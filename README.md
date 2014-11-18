#idaStrTrans.py
Translate any language in IDA Pro.

##Background
Sometime we do reverse engineering, cannot understand strings in other language.

So I make this python script to do the auto translate by using Google Translate.

It can auto detect any source language. And translate it to any other language.

If the string is too short, you should manually given the source language.


##Usage
You should install python with easy_install, to install this two library..

* easy_install goslate
* easy_install chardet

Then load the script in IDA Pro, you will see:

    Use F3 translate ANSI/UTF-8 to Chinese
    Use F4 translate ANSI/UTF-8 to English
    Use Ctrl-F3 translate Korea to Chinese
    Use Ctrl-F4 translate Korea to English
    Use Shift-F3 translate Unicode to Chinese 
    Use Shift-F4 translate Unicode to English
Enjoy it!!
