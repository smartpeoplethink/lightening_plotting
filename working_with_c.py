import ctypes

# Load the shared library into c types.
libc = ctypes.CDLL("./calculations.exe")
counter = libc.add()

print(counter)