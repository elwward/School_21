import psutil
import sys
import os

def generator(path):
    with open(path, 'r') as f:
        for line in f:
            yield line

def main():
    data=generator(sys.argv[1])
    for i in data:
        pass

    pid = os.getpid()
    process = psutil.Process(pid)

    memory = process.memory_info().rss / (1024 ** 3)
    cpu_times = process.cpu_times()
    total_time = cpu_times.user + cpu_times.system

    print(f"Peak Memory Usage = {memory:.3f} GB")
    print(f"User Mode Time + System Mode Time = {total_time:.2f}s")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Enter 2 arguments")
        exit()
    try:
        main()
    except Exception as error:
        print(error)