import subprocess

'''
Using External Tools with Subprocess:
For more detailed hardware information, you can use external tools and parse their output. For example, lscpu on Linux can provide detailed CPU information.
'''

def get_lscpu_info():
    result = subprocess.run(['lscpu'], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')

lscpu_info = get_lscpu_info()
print(lscpu_info)