import timeit

# Simple assignment
print(timeit.timeit('a = 1 + 2', number=1000000))  # Fast, typically in nanoseconds

# Function call
def simple_function():
    return 1 + 2

print(timeit.timeit('simple_function()', globals=globals(), number=1000000))  # Slightly slower due to function overhead

# I/O operation
with open('test_file.txt', 'w') as f:
    f.write('This is a test.')

print(timeit.timeit("open('test_file.txt').read()", number=1000))  # Much slower due to I/O

# Complex computation
print(timeit.timeit('sorted([i for i in range(1000)])', number=1000))  # Depends on input size and complexity
