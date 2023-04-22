import ctypes
from typing import List

delta = 0x9E3779B9

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
	sum = UInt32(0xC6EF3720)

	k0, k1, k2, k3 = k[0], k[1], k[2], k[3]

	for i in range(32):
		v1 -= ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3)
		v0 -= ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1)
		sum -= delta

	# Return a new array with the Python-version of the numbers from the UInt32's.
	return [v0.number, v1.number]

# TODO: Implement Cipher Block Chaining, more information can be found here: https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_block_chaining_(CBC)
def main():
	value = [1839219, 1240194]
	key = [2194012, 1290311, 591021, 952112]

	print("Value: " + str(value))
	print("Key: " + str(key))
	print()

	encrypted_array = encrypt(value, key)
	print("Encrypted Value: " + str(encrypted_array))

	decrypted_array = decrypt(encrypted_array, key)
	print("Decrypted Value: " + str(decrypted_array))

if __name__ == "__main__":
	main()
