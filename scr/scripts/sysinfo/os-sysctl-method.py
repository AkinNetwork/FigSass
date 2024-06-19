import subprocess

# On macOS, you can use sysctl to get detailed system information

def get_sysctl_info():
    result = subprocess.run(['sysctl', '-a'], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')

sysctl_info = get_sysctl_info()
print(sysctl_info)
