import psutil # type: ignore

'''
The psutil library can provide information about CPU usage, memory usage, and other system-related metrics, but it doesn't provide TDP directly.

'''

# Get CPU information
cpu_info = psutil.cpu_freq()
print(f"Current CPU Frequency: {cpu_info.current} MHz")
print(f"Max CPU Frequency: {cpu_info.max} MHz")