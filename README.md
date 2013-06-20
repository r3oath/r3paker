R3PAKER
=======

#####Secure File and Document Storage System for Linux, Windows and Mac OS.

R3PAKER processes any directory, AES encrypting its contents and compressing each file using BZ2. These packed files can be stored safely on remote servers, USB keys, etc without anyone being able to use them or view their contents. Only someone who knows the security key will be able to unpack the directory. This is similar to using a program like TrueCrypt although not nearly advanced. What R3PAKER does offer is a single script to quickly encrypt and decrypt any directory on the fly without having to install a program to do so.

Copyright (C) 2013 Tristan Strathearn (r3oath@gmail.com)

####Requirements

R3PAKER makes use of the [Crypto Python Module](https://www.dlitz.net/software/pycrypto/). Please make sure you have this installed before using.

##Usage

####Commandline Arguments.

You have two options when using R3PAKER. One is to call the script with command line arugments when you do not require user input. The other way is to run the script without any arguments and it will interactively prompt you for the required fields.

![Usage](http://www.r3oath.com/images/r3paker/win-usage2.jpg)

####Packing a directory.

By defualt R3PAKER looks for a directory call `Data` in the same location as itself. This is the directory containing the files you'll like to pack. If you want to use another directory, please specify it.

![Usage](http://www.r3oath.com/images/r3paker/win-pack.jpg)

####Invalid Keys.

If you've packed a directory, you would have specified a security key. Only the exact same security key can properly unpack the data. If you were to enter the incorrect key, you data will become scrambled and unsuable. So to help avoid this R3PAKER creates a `keycheck` file in the packed data directory. Before unpacking R3PAKER tests the supplied key against this file to verify it. If it fails, you will be notified. Say for some reason you purposely deleted the `keycheck` file you'll be asked if you still want to unpack the data, just make sure it's the right key!

![Usage](http://www.r3oath.com/images/r3paker/win-badkey.jpg)

####Unpacking a directory.

Similar to packing, R3PAKER uses the `Data` directory by default when looking for packed files. Packed files have a trailing `_r3pak` signature on the end of the file extension/name. Once unpacked all the original data will be available for use again.

![Usage](http://www.r3oath.com/images/r3paker/win-unpack.jpg)
