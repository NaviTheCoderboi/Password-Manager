import hashlib
import random
import array

def generate_password(length):
	DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']  
	LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q','r', 's', 't', 'u', 'v', 'w', 'x', 'y','z']
	UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q','R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y','Z']
	SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>', '*', '(', ')', '<']
	COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS
	rand_digit = random.choice(DIGITS)
	rand_upper = random.choice(UPCASE_CHARACTERS)
	rand_lower = random.choice(LOCASE_CHARACTERS)
	rand_symbol = random.choice(SYMBOLS)
	temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol
	for x in range(length - 4):
		temp_pass = temp_pass + random.choice(COMBINED_LIST)
		temp_pass_list = array.array('u', temp_pass)
		random.shuffle(temp_pass_list)
	password = ""
	for x in temp_pass_list:
		password = password + x
	return password

def hash_password(password):
    password_bytes = password.encode('utf-8')
    hash_object = hashlib.sha256()
    hash_object.update(password_bytes)
    hash_hex = hash_object.hexdigest()
    return hash_hex

def verify_password(password, hash_hex):
    hashed_password = hash_password(password)
    if hashed_password == hash_hex:
        return True
    else:
        return False
