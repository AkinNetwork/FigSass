import psutil # type: ignore
import platform
import subprocess
import cpuinfo # type: ignore

def get_system_info():
    # Get basic system info
    uname = platform.uname()
    
    # Get CPU info
    cpu_info = cpuinfo.get_cpu_info()
    psutil_cpu_freq = psutil.cpu_freq()
    
    # Get detailed CPU info (Linux specific, you can add more for other OS)
    if platform.system() == 'Linux':
        result = subprocess.run(['lscpu'], stdout=subprocess.PIPE)
        lscpu_info = result.stdout.decode('utf-8')
    else:
        lscpu_info = "Detailed CPU info not available for this OS"
    
    return {
        'uname': uname,
        'cpu_info': cpu_info,
        'psutil_cpu_freq': psutil_cpu_freq,
        'lscpu_info': lscpu_info
    }

system_info = get_system_info()

print(f"System: {system_info['uname'].system}")
print(f"Node Name: {system_info['uname'].node}")
print(f"Release: {system_info['uname'].release}")
print(f"Version: {system_info['uname'].version}")
print(f"Machine: {system_info['uname'].machine}")
print(f"Processor: {system_info['uname'].processor}")

print(f"CPU Info: {system_info['cpu_info']}")
print(f"Current CPU Frequency: {system_info['psutil_cpu_freq'].current} MHz")
print(f"Max CPU Frequency: {system_info['psutil_cpu_freq'].max} MHz")

print(f"Detailed CPU Info: {system_info['lscpu_info']}")
