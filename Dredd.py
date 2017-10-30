import psutil
import os
from collections import Counter
print("I AM THE LAW. ANYTHING THAT GETS IN MY WAY WILL BE TREATED AS AN ACCESSORY.")
print("YOU HAVE BEEN WARNED")

#starting processes include
SOFT_PROC_LIMIT = 20
HARD_PROC_LIMIT = 100
known_rabbit = set()
judges = set() #exchange between judges
#get the name of this userspace
username = psutil.Process(os.getpid()).username()
#now take every starting process and do not hurt them. They are law-abiding
law_abiding = set()
for starting in psutil.process_iter():
    if starting.username() == username:
        law_abiding.add(starting.pid)

def check_if_bomb(nc_count, nc_to_proc):
    for (name, cmd), count in nc_count.most_common():
        if count >= HARD_PROC_LIMIT or (name, cmd) in known_rabbit:
            kill(name, cmd, nc_to_proc)
            known_rabbit.add((name, cmd))
while True:
    #get the number of current processes
    num_proc = 0
    for proc in psutil.process_iter():
        if proc.pid not in law_abiding and proc.username() == username:
            print(proc)
            num_proc = num_proc + 1
    # Loop through all processes checking if they are making children
    if num_proc < SOFT_PROC_LIMIT:
        nc_count = Counter()
        nc_to_proc = {}
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=["pid", "name", "cmdline", "create_time", "username"])
                nc_tup = (pinfo["name"], tuple(pinfo["cmdline"]))
                nc_count[nc_tup] += 1
                if nc_tup not in nc_to_proc.keys():
                    nc_to_proc[nc_tup] = set([proc])
                else:
                    nc_to_proc[nc_tup].add(proc)
            except psutil.NoSuchProcess:
                pass
        check_if_bomb(nc_count, nc_to_proc)

    #will kill all process that starts, when process_limit exceeds its limit
    else:
        accessory = set()
        for target in psutil.process_iter():
            if target.pid not in law_abiding and target.username() == username and target.pid not in judges:
                print(target)
                target.suspend()
                accessory.add(target)
        for processes in accessory:
            try:
                target.kill()
            except psutil.NoSuchProcess:
                pass
        num_proc = 0 #reset the number of processes counted and loop
