#!/usr/bin/python
#
#
# Simple tool to take an arbitrary binary (DLL, exe, etc.) 
# and convert it to a XOR encrypted char array for embedding
# in loaders that decrypt the data in memory and do something
# useful with it. 
#
# Drew Kirkpatrick
# drew.kirkpatrick@gmail.com
# @hoodoer
#
# Various bits borrowed and stolen from Shawn https://github.com/ShawnDEvans


import argparse
import subprocess
import sys
import os


# Oh so half arsed
TEMP_OUTPUT_BLOB_FILE = "./EncodedBinaryData"
OUTPUT_FILE_H         = "./encodedOutput.h"



def generateCharEncoding(filename):
	outputEncoding = subprocess.check_output(['xxd', '-i', filename])

	return outputEncoding





def xorcrypt(data, key):
    result = ''
    pad = key*(len(data)/len(key)) + key[:(len(data)%len(key))]

    for i in range(len(data)):
      result += chr (ord(data[i]) ^ ord(pad[i]))    

    return result






def encryptBinaryBlob(clearTextBlob, password):
	cipherTextBlob = xorcrypt(clearTextBlob, password)

	return cipherTextBlob






if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("--filename", help="the file to encode (DLL, exe, etc) as a char array")
	parser.add_argument("--password", default="NULL", help="XOR encrypt payload with PASSWORD (OPTIONAL)")
	args = parser.parse_args()

	if len(sys.argv) < 3:
		parser.print_help()
		sys.exit()


	# Read in the clear text source blob
	fileHandle = open(args.filename, "r")
	clearTextBlob = fileHandle.read()
	fileHandle.close()

	outputBlobHandle = open(TEMP_OUTPUT_BLOB_FILE, "w")

	if args.password is not "NULL":
		print "Encryption turned on"
		print " -- Password is: " + args.password

		# If we're using encryption, create the encrypted binary blob
		cipherTextBlob = encryptBinaryBlob(clearTextBlob, args.password)

		# write it out so we can easily use xxd to format it
		outputBlobHandle.write(cipherTextBlob)
	else:
		print "No encryption"
		
		# write it out so we can easily use xxd to format it
		outputBlobHandle.write(clearTextBlob)

	# Close our temporary output blob file
	outputBlobHandle.close()


	# Create the source code for embedding the binary blob
		# Create the source code for embedding the binary blob
	outputEncoding = ""
	outputEncoding += "#ifndef ENCODEDDATA_H"
	outputEncoding += "\n"
	outputEncoding += "#define ENCODEDDATA_H"
	outputEncoding += "\n"
	outputEncoding += "\n"

	outputEncoding += generateCharEncoding(TEMP_OUTPUT_BLOB_FILE)
	outputEncoding += "\n"


	# Add on the password into the output if we're encrypted. 
	# Don't want to lose that, will need it to decrypt the data
	# Note: If you actually compile this password into the binary
	# some AV's will discover it, decrypt your shellcode on static 
	# analysis, and bust you. So remove/comment that if you're 
	# trying to be sneaky
	if args.password is not "NULL":
		outputEncoding += 'unsigned char __cipherTextPassphrase[] = "' + args.password + '";'
	
	outputEncoding += "\n"
	outputEncoding += "\n"
	outputEncoding += "#endif //ENCODEDDATA_H"
	outputEncoding += "\n"


	outputFileHandle = open(OUTPUT_FILE_H, "w")
	outputFileHandle.write(outputEncoding)
	outputFileHandle.close()

	# Ever so minor efforts at cleaning up. 
	os.remove(TEMP_OUTPUT_BLOB_FILE)

	print "Source code saved in: " + OUTPUT_FILE_H

