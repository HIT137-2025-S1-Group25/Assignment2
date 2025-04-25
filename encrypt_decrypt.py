#!/bin/python3
"""
This program is a solution to Assignment 2, question 1, for unit HIT137.
The program was interpreted to have the capabilities of:
-fully decryption method without using the original text.
-taking any or many inputs from user for key m and n

Instructions:
To use this program, please do the following steps:
1. Add in the file path and name of the file that is to be encrypted in the variable "original_file"
2. Add in the file path and name of the file that is to contain the encrypted message in the variable "encrypted_file"

"""

import os

#Variable that contains the message to be encrypted
ORIGINAL_FILENAME= 'raw_text.txt'

#Variable that contains the message to be encrypted
ENCRYPTED_FILENAME='encrypted_text.txt'

#File paths
SCRIPT_FILE= __file__
DIR_FILE = os.path.dirname(os.path.abspath(SCRIPT_FILE))
ORIGINAL_FILE= DIR_FILE + "/" + ORIGINAL_FILENAME
ENCRYPTED_FILE=DIR_FILE + "/" + ENCRYPTED_FILENAME

n=input("Please enter any input for n: ")
m=input("Please enter any input for m: ")

if n.isalpha or not n.isnumeric:
	if len(n) == 1:
		input_keyn = int(ord(n))
	else:
		input_keyn = 0
		for nchar in n:
			input_keyn = input_keyn + int(ord(nchar))
else:
	input_keyn = n

if m.isalpha or not m.isnumeric:
	if len(m) == 1:
		input_keym = int(ord(m))
	else:
		input_keym = 0
		for mchar in m:
			input_keym = input_keym + int(ord(mchar))
else:
	input_keym = m

#open file
def open_file(file_location):
	if not os.path.isfile(file_location):
		print("Files not found.  Please read instructions")
		return False
	else:
		with open(file_location, 'r') as file:
			content = file.readlines()
			return content, True
	
#checkpoints of encryption
def file2encrypt(efile,ofile,int_keyn,int_keym):
	raw_encrypt_message=''
	for char in ofile:
		#ASCII values: A-Z (65-90), a-z (97-122)
		#check lower case 
		char_no=int(ord(char))
		if 97 <= char_no <= 122:
			if 97 <= char_no <= 109:
				# check first half (97-112 ) and encrypt char by +n*m
				raw_encrypt_char=char_no + (int_keyn * int_keym)
				
				while raw_encrypt_char > 109:
					raw_encrypt_char -= 109 +1
					raw_encrypt_char += 97
			
				encrypt_char = chr(raw_encrypt_char)
				raw_encrypt_message += str(encrypt_char)

			else:
				#check second half and encrypt char by -n*m
				raw_encrypt_char=char_no - (int_keyn * int_keym)
				while 110 > raw_encrypt_char:
				
					#calculate overshift
					raw_encrypt_char += 122
					raw_encrypt_char -= 110 -1
			
				encrypt_char = chr(raw_encrypt_char)
				raw_encrypt_message += str(encrypt_char)

		if 65 <= char_no <= 90:
			if 65 <= char_no <= 77:
				raw_encrypt_char = char_no - int_keyn
				
				while raw_encrypt_char < 65:
					#calculate overshift
					raw_encrypt_char += 77 
					raw_encrypt_char -= 65 -1

				encrypt_char = chr(raw_encrypt_char)
				raw_encrypt_message += str(encrypt_char)

			else:
				raw_encrypt_char = char_no + (int_keym^2)
				while 90 < raw_encrypt_char :
					#calculate overshift
					raw_encrypt_char += 77 
					raw_encrypt_char -= 90
					
				encrypt_char = chr(raw_encrypt_char)

				raw_encrypt_message += str(encrypt_char)

		if not char.isalpha():
			raw_encrypt_message += str(char)
		encryptedmessage = raw_encrypt_message[2:-2]

	if os.path.isfile(efile):
	#Write encryption to file
		with open(efile, "w") as wfile:
			wfile.write(encryptedmessage)
		print("Successfully encrypted the original message")
		return True
	else:
		print("Missing file to write encryption")
		return False

def decryption(contents, int_keyn,int_keym) :
	raw_decrypt_message=''
	string_contents=str(contents)
	for char in string_contents:
		char_no=ord(char)
		if 97 <= char_no <= 122:
			if 97 <= char_no <= 109:
				raw_encrypt_char=char_no - (int_keyn * int_keym)
				
				while raw_encrypt_char < 97:
					raw_encrypt_char += 109
					raw_encrypt_char -= 97 -1
			
				encrypt_char = chr(raw_encrypt_char)
				raw_decrypt_message += str(chr(raw_encrypt_char))

			else:
				#check second half and encrypt char by -n*m
				raw_encrypt_char=char_no + (int_keyn * int_keym)

				while 123 <= raw_encrypt_char:
					#calculate overshift
					raw_encrypt_char -= 122
					raw_encrypt_char += 110 -1
			
				encrypt_char = chr(raw_encrypt_char)

				raw_decrypt_message += str(encrypt_char)

		if 65 <= char_no <= 90:
			if 65 <= char_no <= 77:
				raw_encrypt_char = char_no + int_keyn
				
				while raw_encrypt_char > 77:
					#calculate overshift
					raw_encrypt_char -= 77 
					raw_encrypt_char += 65
				encrypt_char = chr(raw_encrypt_char)

				raw_decrypt_message += str(encrypt_char)

			else:
				raw_encrypt_char = char_no - (int_keym^2)
				while raw_encrypt_char <= 77:
					#calculate overshift
					raw_encrypt_char -= 77 
					raw_encrypt_char += 90
					
				encrypt_char = chr(raw_encrypt_char)

				raw_decrypt_message += str(encrypt_char)

		if not char.isalpha():
			raw_decrypt_message += str(char)
	print(raw_decrypt_message)
	return raw_decrypt_message

def decrypt2original(dfile, ofile):
	index_decryptedcontents_counter=0
	for i in dfile:
		index_decryptedcontents_counter += 1

	counter_check=0
	for i in range(index_decryptedcontents_counter):
		if dfile[counter_check] == ofile[counter_check]:
			counter_check +=1
		else:
			return "File not correctly decrypted"
	print("Decrypted file checked for correctness")

#Encryption of original message
original_contents=str(open_file(ORIGINAL_FILE))
file2encrypt(ENCRYPTED_FILE, original_contents, input_keyn, input_keym)

#Decryption of the encrypted message
encrypted_contents=str(open_file(ENCRYPTED_FILE))
decrypt_message=decryption(encrypted_contents, input_keyn, input_keym)
print(decrypt_message)
decrypt2original(decrypt_message, ORIGINAL_FILE)

