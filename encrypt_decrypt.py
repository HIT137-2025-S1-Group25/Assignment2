#!/bin/python3
"""
This program was interpreted and has capabilities of:
-fully decryption method without using the original text.
-it can take any integers or characters as user inputs
Two user inputs are taken which is used to encrypt the file into a new file called "encrypted_text.txt".
"""


original_file= '/home/jo/Documents/Engineering/HIT137/testing/raw_text-assign.txt'
encrypted_file='/home/jo/Documents/Engineering/HIT137/testing/encrypted_text.txt'

input_keyn=int(ord(input("Please enter one character for user input n: ")))
input_keym=int(ord(input("Please enter one character for user input m: ")))

#open file
def open_file(file_location):
    try:
        with open(file_location, 'r') as file:
            content = file.readlines()
        return content
    except FileNotFoundError:
        print(f"Error: The file '{file_location}' was not found.")
        return None
	
#checkpoints of encryption
def file2encrypt(efile,ofile,int_keyn,int_keym):
	raw_encrypt_message=''
	for char in ofile:
		# ASCII values: A-Z (65-90), a-z (97-122)
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

	#Write encryption to file
	with open(efile, "w") as wfile:
		wfile.write(encryptedmessage)
	
	return

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
				raw_encrypt_char = char_no - int_keym^2
				while raw_encrypt_char <= 77:
					#calculate overshift
					raw_encrypt_char -= 77 
					raw_encrypt_char += 90
					
				encrypt_char = chr(raw_encrypt_char)

				raw_decrypt_message += str(encrypt_char)

		if not char.isalpha():
			raw_decrypt_message += str(char)

	return raw_decrypt_message

def decrypt2original(dfile, ofile):
	index_decryptedcontents_counter=0
	for i in decrypt_message:
		index_decryptedcontents_counter += 1

	counter_check=0
	for i in range(index_decryptedcontents_counter):
		if dfile[counter_check] == ofile[counter_check]:
			counter_check +=1
		else:
			return "File not correctly decrypted"
	return "Decrypted file checked for correctness"


original_contents=str(open_file(original_file))
encryption=file2encrypt(encrypted_file, original_contents, input_keyn, input_keym)

encrypted_contents=str(open_file(encrypted_file))
decrypt_message=decryption(encrypted_contents, input_keyn, input_keym)
print("The decoded message is", str(decrypt_message))

original_contents=str(open_file(original_file))
decryption_checked= decrypt2original(decrypt_message, original_contents)
print(decryption_checked)
