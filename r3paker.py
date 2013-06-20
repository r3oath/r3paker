# ----------------------------------------------------------------------------
# R3PAKER - Secure File and Document Storage System.
# ----------------------------------------------------------------------------
# Copyright (C) 2013 Tristan Strathearn.
# Email: r3oath@gmail.com
# Website: www.r3oath.com
# ----------------------------------------------------------------------------

import sys
import os
import time
import bz2
import base64
import hashlib

from argparse import ArgumentParser
from Crypto.Cipher import AES
from Crypto import Random

R3PACK_SIGNATURE = '_r3pak'

# ----------------------------------------------------------------------------

class r3walker():
    """Walks the Data directory and provides a list of all available files."""
    def __init__(self, base_dir='Data'):
        self.base_dir = base_dir

    def getFiles(self, only_packed=False):
        """Generator object, will return a list of files for each directory
        in the base_dir.

        Keyword Arguments:
        only_packed -- Return only packed files. (Defualt False)

        """
        for root, dirs, files in os.walk(self.base_dir):
            files_ = []
            for file_ in files:
                if only_packed is False:
                    if file_.count(R3PACK_SIGNATURE) is 0:
                        files_.append(os.path.join(root, file_))
                else:
                    if file_.count(R3PACK_SIGNATURE) > 0:
                        files_.append(os.path.join(root, file_))
            yield files_

# ----------------------------------------------------------------------------

class r3crypter():
    """Handles Encryption/Decrpytion/Compression/Decompression."""
    def __init__(self, key):
        self.key = hashlib.sha256(key).digest()

    def encrypt(self, data):
        """Returns encrypted data using AES and bz2 compression.

        Keyword Arguments:
        data -- The data to encrypt.

        """
        iv      = Random.new().read(AES.block_size)
        cipher  = AES.new(self.key, AES.MODE_CFB, iv)
        data    = cipher.encrypt(data)

        return bz2.compress(iv + data)

    def decrypt(self, data):
        """Returns decrypted data using AES and bz2 decompression.

        Keyword Arguments:
        data -- The data to decrypt.

        """
        data    = bz2.decompress(data)
        iv      = data[0:16] # Get only the IV from the data.
        data    = data[16:len(data)] # Get all the data apart from the IV.
        cipher  = AES.new(self.key, AES.MODE_CFB, iv)

        return cipher.decrypt(data)

# ----------------------------------------------------------------------------

class r3paker():
    """The engine of R3PAKER."""
    def __init__(self):
        pass

    def pack(self, key, base_dir='Data'):
        """Recursively packs and encrypts the <base_dir>.

        Keyword Arguments:
        key -- The encryption key to use with AES.
        base_dir -- The base data directory. (Defualt 'Data')

        """
        start_time = time.time()
        total_file_count = 0

        newLine()

        walker      = r3walker(base_dir=base_dir)
        crypter     = r3crypter(key)

        for files in walker.getFiles():
            for file_ in files:
                print_('Packing: %s' % getNicePath(file_))
                try:
                    # Get the file data.
                    fd = open(file_, 'rb')
                    data = fd.read()
                    fd.close()

                    try:
                        # Compress/Encrpyt the data and save.
                        fd = open(file_ + R3PACK_SIGNATURE, 'wb')
                        fd.write(crypter.encrypt(data))
                        fd.close()

                        try:
                            # Remove the original file.
                            os.remove(file_)
                        except:
                            print_('Could not remove: %s' %
                                   getNicePath(file_), highlight=True)
                    except:
                        print_('Encrpytion Failed: %s' % getNicePath(file_),
                              highlight=True)
                except:
                    print_('Failed to open: %s' % getNicePath(file_),
                          highlight=True)

                total_file_count += 1
        return (total_file_count, time.time() - start_time)

    def unpack(self, key, base_dir='Data'):
        """Recursively unpacks and decrypts the <base_dir>

        Keyword Arguments:
        key -- The encryption key to use with AES.
        base_dir -- The base data directory. (Defualt 'Data')

        """
        start_time = time.time()
        total_file_count = 0

        newLine()

        walker      = r3walker(base_dir=base_dir)
        crypter     = r3crypter(key)

        for files in walker.getFiles(only_packed=True):
            for file_ in files:
                print_('Unpacking: %s' % getNicePath(file_))
                try:
                    # Get the file data.
                    fd = open(file_, 'rb')
                    data = fd.read()
                    fd.close()

                    try:
                        # Decompress/Decrpyt the data and save.
                        fd = open(file_.replace(R3PACK_SIGNATURE, ''), 'wb')
                        fd.write(crypter.decrypt(data))
                        fd.close()

                        try:
                            # Remove the original file.
                            os.remove(file_)
                        except:
                            print_('Could not remove: %s' %
                                   getNicePath(file_), highlight=True)
                    except:
                        print_('Decrpytion Failed: %s' % getNicePath(file_),
                              highlight=True)
                except:
                    print_('Failed to open: %s' % getNicePath(file_),
                          highlight=True)

                total_file_count += 1
        return (total_file_count, time.time() - start_time)

# ----------------------------------------------------------------------------
# HELPER FUNCTIONS

def print_(text, symbol='', highlight=False):
    """Prints the specified text with special formatting options.

    Keyword Arguments:
    text -- The text to print out.
    symbol -- The symbol/text to prepend to the text. (Defualt '')
    highlight -- Should the line be highlighted? (Defualt False)

    """
    if highlight == False:
        print symbol + text
    else:
        newLine()
        print '/' * (len(text) + len(symbol))
        print symbol + text
        print '/' * (len(text) + len(symbol))
        newLine()

def newLine():
    """Creates a new line, for spacing out printed text etc."""
    print ''

def getNicePath(path, length=50):
    """Returns a formatted string based on the specified path if the path
    is more than <length> characters in length.

    Example:
    Turns: Data/Some/Directory/Structure/File.text
    Into: Data/.../Structure/File.text

    Keyword Arguments:
    path -- The path string to format.
    length -- The max path length before formatting begins. (Defualt 50)

    """
    if len(path) > length:
        start = path.find(os.sep) + 1 # Add 1 so we include the seperator.
        end = 0
        if path.count(os.sep) > 2:
            end = path[0:path.rfind(os.sep)].rfind(os.sep)
            return path[0:start] + '...' + path[end:]
        else:
            end = path.rfind(os.sep)
            return '...' + path[end:]
    else:
        return path

def printEndStatus(files_affected, runtime):
    """Prints out how many files were affected.

    Keyword Arguments:
    files_affected -- The number of files affected.

    """
    if files_affected == 1:
        print_('1 File was processed in %s!' % getRunTime(runtime),
               highlight=True)
    elif files_affected > 1:
        print_('%d Files were processed in %s!' %
               (files_affected, getRunTime(runtime)), highlight=True)
    else:
        print_('No files were processed!', highlight=True)

def getRunTime(runtime):
    """Return a string formatted to display the mins and/or seconds it
    took to run a function/command.

    Keyword Arguments:
    runtime -- The total time in seconds to format.

    """
    if int(runtime / 60) > 0:
        return '%d mins and %0.2f seconds' % (runtime / 60, runtime % 60)
    else:
        return '%0.2f seconds' % runtime

def userInput(text, default_answer=''):
    """Grab input from the user and offer the choice of a defualt answer.

    Keyword Arguments:
    text -- The text to display to the user.
    default_answer -- The default answer to use if no input is given.

    """
    input_ = ''
    if len(default_answer) != 0:
        input_ = raw_input('%s [%s]: ' % (text, default_answer))
    else:
        input_ = raw_input('%s: ' % text)
    if len(input_) == 0:
        input_ = default_answer
    return input_

def generateKeyCheck(key, base_dir='Data'):
    """Generates a new 'keycheck' file to verify secret keys.

    Keyword Arguments:
    key -- The key to use for encryption.
    base_dir -- The directory to store the 'keycheck' file in.

    """
    try:
        crypter = r3crypter(key)
        fd = open(base_dir + os.sep + 'keycheck' + R3PACK_SIGNATURE, 'wb')
        fd.write(crypter.encrypt(R3PACK_SIGNATURE))
        fd.close()
        return True
    except:
        return False

def verifyKeyCheck(key, base_dir='Data'):
    """Decrpyts the signature inside of a 'keycheck' file to determine if
    the key provided is valid.

    Keyword Arguments:
    key -- The key to use for decryption.
    base_dir -- The directory in which the 'keycheck' file is located.

    """
    try:
        crypter = r3crypter(key)
        fd = open(base_dir + os.sep + 'keycheck' + R3PACK_SIGNATURE, 'rb')
        check = crypter.decrypt(fd.read())
        fd.close()
        if check == R3PACK_SIGNATURE:
            return True
        else:
            return False
    except:
        return False

# ----------------------------------------------------------------------------
# ENTRY POINT...

def main(args):
    # Script name and Author information.
    print_('R3PAKER - Secure File and Document Storage System.')
    print_('Created by Tristan Strathearn (www.r3oath.com)')
    newLine()

    # Get the security key.
    key = ''
    if args.k == None:
        key = userInput('Please enter the secret key', '')
    else:
        key = args.k

    # Get the working directory.
    base_dir = ''
    if args.d == None:
        base_dir = userInput('Which directory are you working with?', 'Data')
    else:
        base_dir = args.d

    # Get the pak command.
    pak_command = ''
    if args.a == None:
        pak_command = userInput('Action: (P)ack or (U)npack the data?',
                            'P').lower()
    else:
        pak_command = args.a.lower()

    # ---------------------------------------
    # Start the packing or unpacking process.

    if pak_command == 'p':
        if generateKeyCheck(key, base_dir=base_dir) is True:
            paker = r3paker()
            files_affected, runtime = paker.pack(key, base_dir=base_dir)
            printEndStatus(files_affected, runtime)
        else:
            print_('Could not write Key Check file!', highlight=True)

    if pak_command == 'u':
        if verifyKeyCheck(key, base_dir=base_dir) is False:
            print_('Key check file could not be verified!', highlight=True)
            ans = userInput('Damages could occur, type YES to continue',
                            'No')
            if ans == 'YES':
                paker = r3paker()
                files_affected, runtime = paker.unpack(key, base_dir=base_dir)
                printEndStatus(files_affected, runtime)
        else:
            paker = r3paker()
            files_affected, runtime = paker.unpack(key, base_dir=base_dir)
            printEndStatus(files_affected, runtime)

    print_('R3PAKER has finished successfully.')

if __name__ == "__main__":
    # Command line arguments handler.
    arg_parser = ArgumentParser(description=
                                'Secure File and Document Storage System.')
    arg_parser.add_argument('-k', metavar='Key', type=str,
                            help='The secret key.')
    arg_parser.add_argument('-d', metavar='Directory', type=str,
                            help='The directory to work with.')
    arg_parser.add_argument('-a', metavar='Action', type=str,
                            help='The action to take. (P)ack or (U)npack.')
    args = arg_parser.parse_args()

    # Start the script.
    main(args)
