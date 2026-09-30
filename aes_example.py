# Versión interactiva de AES_example.py: pide el mensaje al usuario
# Requiere: pip install pycryptodome

from Crypto.Cipher import AES
import base64, os

def generate_secret_key_for_AES_cipher():
	# AES key length must be either 16, 24, or 32 bytes long
	AES_key_length = 16 # use larger value in production
	# generate a random secret key with the decided key length
	secret_key = os.urandom(AES_key_length)
	# encode this secret key for storing safely in database
	encoded_secret_key = base64.b64encode(secret_key)
	return encoded_secret_key

def encrypt_message(private_msg, encoded_secret_key, padding_character):
	# decode the encoded secret key
	secret_key = base64.b64decode(encoded_secret_key)
	# use the decoded secret key to create a AES cipher
	cipher = AES.new(secret_key, AES.MODE_ECB)
	# convert the message to bytes first (so accents and ñ are counted correctly)
	private_msg = private_msg.encode("utf-8")
	# pad the private_msg to a multiple of 16 bytes
	padded_private_msg = private_msg + (padding_character * ((16-len(private_msg)) % 16))
	# use the cipher to encrypt the padded message
	encrypted_msg = cipher.encrypt(padded_private_msg)
	# encode the encrypted msg for storing safely in the database
	return base64.b64encode(encrypted_msg)

def decrypt_message(encoded_encrypted_msg, encoded_secret_key, padding_character):
	# decode the encoded encrypted message and encoded secret key
	secret_key = base64.b64decode(encoded_secret_key)
	encrypted_msg = base64.b64decode(encoded_encrypted_msg)
	# use the decoded secret key to create a AES cipher
	cipher = AES.new(secret_key, AES.MODE_ECB)
	# decrypt, remove the padding and convert back to text
	decrypted_msg = cipher.decrypt(encrypted_msg)
	unpadded_private_msg = decrypted_msg.rstrip(padding_character)
	return unpadded_private_msg.decode("utf-8")


####### BEGIN HERE #######

padding_character = b"{"

private_msg = input("Escribe el mensaje que quieres cifrar: ")

secret_key = generate_secret_key_for_AES_cipher()
encrypted_msg = encrypt_message(private_msg, secret_key, padding_character)
decrypted_msg = decrypt_message(encrypted_msg, secret_key, padding_character)

print()
print("  Original Msg: %s - (%d)" % (private_msg, len(private_msg)))
print("   Secret Key: %s - (%d)" % (secret_key.decode(), len(secret_key)))
print("Encrypted Msg: %s - (%d)" % (encrypted_msg.decode(), len(encrypted_msg)))
print("Decrypted Msg: %s - (%d)" % (decrypted_msg, len(decrypted_msg)))
print()
print("¿El descifrado coincide con el original? ->", decrypted_msg == private_msg)