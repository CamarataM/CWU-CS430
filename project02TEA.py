# Cipher Block Chaining information can be found here: https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_block_chaining_(CBC)
# Initial C TEA Implementation taken from: https://en.wikipedia.org/wiki/Tiny_Encryption_Algorithm#Reference_code
# import ctypes
import ctypes
from typing import List

# def encrypt(v : List[ctypes.c_uint32], k : List[ctypes.c_uint32]):
# 	v0, v1 = v[0], v[1]
# 	sum = ctypes.c_uint32(0)
	
# 	delta = ctypes.c_uint32(0x9E3779B9)
# 	k0, k1, k2, k3 = k[0], k[1], k[2], k[3]

# 	for i in range(32):
# 		# sum += delta
# 		v0 += ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1)
# 		v1 += ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3)
	
# 	v[0] = v0
# 	v[1] = v1

# print(str(encrypt([ctypes.c_uint32(2194012), ctypes.c_uint32(1290311)], [ctypes.c_uint32(2194012), ctypes.c_uint32(1290311), ctypes.c_uint32(591021), ctypes.c_uint32(952112)])))

delta = 0x9E3779B9

# 'int' in Python is a traditional 32 bit machine value which is automatically promoted to a 64 bit machine value, which is finally promoted to a "infinite" length value. There is a uint32_t alternative, which is ctypes.c_uint32, but it doesn't seem to play nice with the operators we need.
# def encrypt(v : List[int], k : List[int]):
# 	v0, v1 = v[0], v[1]
# 	sum = 0
	
# 	k0, k1, k2, k3 = k[0], k[1], k[2], k[3]

# 	for i in range(32):
# 		sum += delta
# 		v0 += ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1)
# 		v1 += ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3)

# 	# v[0] = v0
# 	# v[1] = v1
# 	# return v

# 	return [v0, v1]

# def decrypt(v : List[int], k : List[int]):
# 	v0, v1 = v[0], v[1]
# 	sum = 0xC6EF3720

# 	k0, k1, k2, k3 = k[0], k[1], k[2], k[3]

# 	for i in range(32):
# 		v1 -= ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3)
# 		v0 -= ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1)
# 		sum -= delta
	
# 	# v[0] = v0
# 	# v[1] = v1
# 	# return v

# 	return [v0, v1]

def uint32_cast(number : int):
	# return int(ctypes.c_uint32(number))
	return ctypes.c_uint32(number).value

def encrypt(v : List[int], k : List[int]):
	v0, v1 = uint32_cast(v[0]), uint32_cast(v[1])
	sum = 0
	
	k0, k1, k2, k3 = k[0], k[1], k[2], k[3]

	for i in range(32):
		sum += delta
		sum = uint32_cast(sum)
		v0 += ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1)
		v0 = uint32_cast(v0)
		v1 += ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3)
		v1 = uint32_cast(v1)

	return [v0, v1]

def decrypt(v : List[int], k : List[int]):
	v0, v1 = uint32_cast(v[0]), uint32_cast(v[1])
	sum = 0xC6EF3720

	k0, k1, k2, k3 = k[0], k[1], k[2], k[3]

	for i in range(32):
		v1 -= ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3)
		v1 = uint32_cast(v1)
		v0 -= ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1)
		v0 = uint32_cast(v0)
		sum -= delta
		uint32_cast(delta)

	return [v0, v1]

value = [1839219, 1240194]
key = [2194012, 1290311, 591021, 952112]

print("Value: " + str(value))
print("Key: " + str(key))

encrypted_array = encrypt(value, key)

print("Encrypted Value: " + str(encrypted_array))

decrypted_array = decrypt(encrypted_array, key)

print("Decrypted Value: " + str(decrypted_array))
# print("Decrypted Value Unsigned: " + str(decrypted_array[0] + 2**32) + ", " + str(decrypted_array[1] + 2**32))
# print("Decrypted Value Unsigned: " + str(ctypes.c_ulong(decrypted_array[0])) + ", " + str(ctypes.c_ulong(decrypted_array[1])))
