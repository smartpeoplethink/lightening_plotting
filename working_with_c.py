import ctypes

# Load the DLL
lib = ctypes.CDLL("./mylib.dll")

# Call the function
lib.hello()