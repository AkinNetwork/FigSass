import cpuinfo # type: ignore

cpu_info = cpuinfo.get_cpu_info()
print(cpu_info)