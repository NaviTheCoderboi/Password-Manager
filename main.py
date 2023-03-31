import sqlite3
from getpass import getpass
from cryptography.fernet import Fernet
from utilis import generate_password,verify_password,hash_password

conn = sqlite3.connect("passwords.db")
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS passwords(service STRING, password INTEGER)""")
verified = False

print("welcome to password manager!")
while True:
	_master_password = cur.execute("""SELECT * FROM passwords WHERE service = ?""",("master",))
	master_password = _master_password.fetchone()
	key_fetch = cur.execute("""SELECT * FROM passwords WHERE service = ?""",("key",))
	_key = key_fetch.fetchone()
	if not _key:
		_key = Fernet.generate_key()
		cur.execute("""INSERT INTO passwords(service,password) VALUES(?,?)""",("key",_key,))
		conn.commit()
		key = Fernet(_key)
	else:
		key = Fernet(_key[1])
	if verified==False:
		if not master_password:
			set_master_password = getpass("Set a master password: ",stream=None)
			if len(set_master_password) <=5 or " " in set_master_password:
				print("your password must have more than 5 characters and no spaces")
				continue
			else:
				main_pass_hash = hash_password(set_master_password)
				cur.execute("""INSERT INTO passwords(service,password) VALUES(?,?)""",("master",main_pass_hash,))
				conn.commit()
				print("Master password successfully set!")
				continue
		else:
			master_pass = getpass("Please enter the master password: ",stream=None)
			if verify_password(master_pass,master_password[1]) == False:
				print("wrong password!")
				conn.close()
				break
			else:
				verified = True
				continue
	else:
		print("""
------------------------
g to generate a password
a to add new password
l to list all passwords
d to delete a password
q to quit
------------------------
 """)
		inp = input(": ")
		if inp.lower() == "q":
			conn.close()
			break
		elif inp.lower() == "g":
			size = input("How long should your password be: ")
			try:
				size = int(size)
                                if size<5:
                                        print("Please enter password length greater than 5!")
                                else:
				        print(f"Here is your random password:\n    {generate_password(size)}")
			except ValueError:
				print("Enter a number next time!")
		elif inp.lower() == "a":
			service = input("For which service is your password for: ")
			password = getpass("Enter the password: ",stream=None)
			passw = key.encrypt(password.encode('utf-8'))
			cur.execute("""INSERT INTO passwords(service, password) VALUES(?,?)""",(service,passw,))
			conn.commit()
			print("Password successfully added!")
		elif inp.lower() == "l":
			_passwords = cur.execute("""SELECT * FROM passwords WHERE service NOT IN (?, ?)""",("key","master",))
			passwords_fetch = _passwords.fetchall()
			for i in passwords_fetch:
				print("{:<5} -> {:<5}".format(i[0],key.decrypt(i[1].decode("utf-8")).decode("utf-8")))
		elif inp.lower() == "d":
			service = input("Enter the service: ")
			try_service = cur.execute("""SELECT * FROM passwords WHERE service NOT IN (?, ?) AND service = ?""",("key","master",service,))
			fetch_service = try_service.fetchone()
			if not fetch_service:
				print("No such password saved for this service!")
			else:
				cur.execute("""DELETE FROM passwords WHERE service = ? AND service not in (?,?)""",(service,"key","master",))
				conn.commit()
				print("Successfully deleted password!")
		else:
			print("Invalid input!")

print("Thanks for using my password manager\nMade with ❤️  by NaviTheCoderboi")
