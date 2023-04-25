import ctypes
from typing import List
import random

delta = 0x9E3779B9
decrypt_sum = 0xC6EF3720
maximum_displayed_int_list_elements = 10

# Set the seed of random to 0, making all initialization vectors generation deterministic.
random.seed(0)

# 'int' in Python is a traditional 32 bit machine value which is automatically promoted to a 64 bit machine value, which is finally promoted to a "infinite" length value. This behavior is extremely different from the original C uint32_t value, making the original code incompatible without converting to a representation which replicates the original C value. ctypes.c_uint32 will convert a Python number into the corresponding c_uint32 (unsigned 32 bit integer), which allows for the replication of the original C behavior.
def uint32_cast(number : int):
	return ctypes.c_uint32(number).value

# Create a class which holds a number which will automatically cast to a ctypes uint32. Overrides many of the functions which support mathematical parameters, taken from: https://docs.python.org/3/library/operator.html
# TODO: Support all override functions to properly implement a true functional alternative to Python's 'int' type.
class UInt32:
	# A private static method which will grab either the number value from a UInt32 or the object itself otherwise.
	@staticmethod
	def __get_value(object : object):
		return object.number if isinstance(object, UInt32) else object

	def __init__(self, python_number):
		self.number = uint32_cast(python_number)

	def __add__(self, __value : object):
		value = UInt32.__get_value(__value)
		return self.__class__(self.number.__add__(value))

	def __sub__(self, __value : object):
		value = UInt32.__get_value(__value)
		return self.__class__(self.number.__sub__(value))

	def __mul__(self, __value : object):
		value = UInt32.__get_value(__value)
		return self.__class__(self.number.__mul__(value))

	def __radd__(self, __value : object):
		value = UInt32.__get_value(__value)
		return self.__class__(self.number.__add__(value))

	def __rsub__(self, __value : object):
		value = UInt32.__get_value(__value)
		return self.__class__(self.number.__sub__(value))

	def __rmul__(self, __value : object):
		value = UInt32.__get_value(__value)
		return self.__class__(self.number.__mul__(value))

	def __lshift__(self, __value : object):
		value = UInt32.__get_value(__value)
		return self.__class__(self.number.__lshift__(value))

	def __rshift__(self, __value : object):
		value = UInt32.__get_value(__value)
		return self.__class__(self.number.__rshift__(value))

	def __xor__(self, __value : object):
		value = UInt32.__get_value(__value)
		return self.__class__(self.number.__xor__(value))

	def __eq__(self, __value : object) -> bool:
		return self.number.__eq__(__value)
	
	def __str__(self) -> str:
		return self.number.__str__()

# Original C TEA Implementation taken from: https://en.wikipedia.org/wiki/Tiny_Encryption_Algorithm#Reference_code
def encrypt(v : List[int], k : List[int]):
	# Get variables for each of the values which will have mathematical operations applied to them as UInt32, which will automatically handle the conversion from the ctypes.uint32 to correctly handle the original C behavior.
	v0, v1 = UInt32(v[0]), UInt32(v[1])
	sum = UInt32(0)
	
	k0, k1, k2, k3 = k[0], k[1], k[2], k[3]

	for i in range(32):
		sum += delta
		v0 += ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1)
		v1 += ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3)

	# Return a new array with the Python-version of the numbers from the UInt32's.
	return [v0.number, v1.number]

def decrypt(v : List[int], k : List[int]):
	v0, v1 = UInt32(v[0]), UInt32(v[1])
	sum = UInt32(decrypt_sum)

	k0, k1, k2, k3 = k[0], k[1], k[2], k[3]

	for i in range(32):
		v1 -= ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3)
		v0 -= ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1)
		sum -= delta

	# Return a new array with the Python-version of the numbers from the UInt32's.
	return [v0.number, v1.number]

# Converts a string to an int list.
def string_to_int_list(string : str):
	int_list = []

	# Append the ordinal of each character in the string. This will be at-most 32 bits for a 4 byte Unicode character.
	for char in string:
		int_list.append(ord(char))

	return int_list

# Will take a string and encrypt the Unicode-chars bytes.
def encrypt_string(string : str, key : List[int]):
	return encrypt_int_list(int_list=string_to_int_list(string=string), key=key)

# Will take an int list and encrypt the values using the key parameter.
def encrypt_int_list(int_list : List[int], key : List[int]):
	encrypted_int_list = []

	for i in range(0, len(int_list), 2):
		# Iterate every int, only grabbing the second int if it is not our-of-bounds for the int list.
		first_int = int_list[i]
		second_int = 0

		if i + 1 < len(int_list):
			second_int = int_list[i + 1]

		# Encrypt the bytes using the key parameter.
		encrypted_int_tuple = encrypt([first_int, second_int], key)

		# Append the encrypted ints to the encrypted int list.
		encrypted_int_list.append(encrypted_int_tuple[0])
		encrypted_int_list.append(encrypted_int_tuple[1])

	return encrypted_int_list

def decrypt_int_list(int_list : List[int], key : List[int]):
	decrypted_int_list = []

	for i in range(0, len(int_list), 2):
		# Iterate every int, only grabbing the second int if it is not our-of-bounds for the int list.
		# TODO: Ensure that integers are 32 bits, as larger values will decode incorrectly.
		first_int = int_list[i]
		second_int = 0

		if i + 1 < len(int_list):
			second_int = int_list[i + 1]

		# Decrypt the ints using the key parameter.
		decrypted_int_tuple = decrypt([first_int, second_int], key)

		# Append the decrypted ints converted back to a char to the output string.
		decrypted_int_list.append(decrypted_int_tuple[0])
		decrypted_int_list.append(decrypted_int_tuple[1])

	return decrypted_int_list

def decrypt_int_list_string(int_list : List[int], key : List[int]):
	# TODO: Should use a StringBuilder-like object to speed this up. See https://stackoverflow.com/questions/10572624/mutable-strings-in-python/10572792#10572792
	output_string = ""

	decrypted_int_list = decrypt_int_list(int_list=int_list, key=key)

	for i in range(0, len(int_list), 2):
		# Iterate every int, only grabbing the second int if it is not our-of-bounds for the int list.
		# TODO: Ensure that integers are 32 bits, as larger values will decode incorrectly.
		first_int = decrypted_int_list[i]
		second_int = 0

		if i + 1 < len(decrypted_int_list):
			second_int = decrypted_int_list[i + 1]

		# Append the decrypted int(s) converted back to a char to the output string.
		output_string += chr(first_int)
		output_string += chr(second_int)

	return output_string

def generate_initialization_vector(input_list : List[int] | None = None):
	initialization_vector : List[int] = []

	for _ in range(len(input_list)):
		# Generate a random integer between 0 (inclusive) and 2^32 bits - 1 (inclusive, int32 maximum value).
		initialization_vector.append(random.randint(0, 2^32 - 1))

	return initialization_vector

# TODO: Implement Cipher Block Chaining, more information can be found here: https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_block_chaining_(CBC)
def encrypt_xor_vector(int_list : List[int], key : List[int], initialization_vector : List[int]):
	# Check that the input int_list and the initialization_vector have the same length.
	if len(int_list) != len(initialization_vector):
		raise ValueError("The int_list and initialization_vector parameters had differing lengths. " + str(len(int_list)) + " != " + str(len(initialization_vector)))

	xored_list : List[int] = []

	for i in range(len(int_list)):
		# ^ in Python is XOR, see https://docs.python.org/3/library/operator.html#mapping-operators-to-functions
		xored_list.append(int_list[i] ^ initialization_vector[i])
		# print(str(int_list[i]))
		# print(str(initialization_vector[i]))
		# print(str(int_list[i] ^ initialization_vector[i]))
	
	return encrypt_int_list(xored_list, key=key)

def decrypt_xor_vector(int_list : List[int], key : List[int], initialization_vector : List[int]):
	# Check that the input int_list and the initialization_vector have the same length.
	if len(int_list) != len(initialization_vector):
		raise ValueError("The int_list and initialization_vector parameters had differing lengths. " + str(len(int_list)) + " != " + str(len(initialization_vector)))

	xored_list : List[int] = []

	decrypted_int_list = decrypt_int_list(int_list, key=key)

	for i in range(len(decrypted_int_list)):
		# ^ in Python is XOR, see https://docs.python.org/3/library/operator.html#mapping-operators-to-functions
		xored_list.append(decrypted_int_list[i] ^ initialization_vector[i])
		# print(str(decrypted_int_list[i]))
		# print(str(initialization_vector[i]))
		# print(str(decrypted_int_list[i] ^ initialization_vector[i]))

	return xored_list

def test_string_encryption():
	key = [2194012, 1290311, 591021, 952112]

	string_to_encrypt = "Corrupti repudiandae sit consequatur voluptate accusamus sit fugiat. Vel perspiciatis quo rerum iure necessitatibus. Animi consequatur accusamus consequatur asperiores aut. Magnam ipsam sit error ducimus tempore quis. Aut dolorem modi voluptatem veritatis porro libero corrupti."

	encrypted_string = encrypt_string(string_to_encrypt, key)

	print("String to Encrypt: " + string_to_encrypt)
	print("Encrypted String Int Array: " + str(encrypted_string[:min(maximum_displayed_int_list_elements, len(encrypted_string))]) + ("" if len(encrypted_string) < maximum_displayed_int_list_elements else "..."))

	decrypted_string = decrypt_int_list_string(encrypted_string, key)

	print("Decrypted Int Array: " + decrypted_string)
	print("Is Encrypted String and Decrypted String Equal: " + str(string_to_encrypt == decrypted_string))

def test_value_key_encryption():
	value = [1839219, 1240194]
	key = [2194012, 1290311, 591021, 952112]

	print("Value: " + str(value))
	print("Key: " + str(key))
	print()

	encrypted_array = encrypt(value, key)
	print("Encrypted Value: " + str(encrypted_array))

	decrypted_array = decrypt(encrypted_array, key)
	print("Decrypted Value: " + str(decrypted_array))

def pad_list(list : List, multiple : int, pad_object):
	while len(list) % multiple != 0:
		list.append(pad_object)

	return list

def main():
	key = [2194012, 1290311, 591021, 952112]

	int_list = pad_list(string_to_int_list("this is a test."), 2, 0)
	print("Int List: " + str(int_list))

	initialization_vector = generate_initialization_vector(int_list)

	encrypted_xor_vector = encrypt_xor_vector(int_list, key, initialization_vector)
	print(str("Encrypted Xor Vector: " + str(encrypted_xor_vector)))

	decrypted_xor_vector = decrypt_xor_vector(encrypted_xor_vector, key, initialization_vector)
	print(str("Decrypted Xor Vector: " + str(decrypted_xor_vector)))

if __name__ == "__main__":
	main()
