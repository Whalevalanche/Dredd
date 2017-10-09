"""
A simple program that is meant to monitor the system's processes to detect and
kill any fork bomb (rabit) malware processes (Continuously self-duplicating
processes that will inevitibly lead to the system failure).

Either runs for the specific user, or if run by root then can run full system.

@author: Derek S. Prijatelj
"""

import os
from collections import Counter
import psutil

HARD_PROC_LIMIT = 64 # mimics the upper limit of ulimit in unix, where user's
#   are limited a certain number of processes.
this_pid = psutil.Process(os.getpid())
this_ppid = this_pid.ppid()
known_rabbit = set()

# May need to split the check_if_bomb & other slow parts to ensure prog is fast
#   enough to kill the rabbit before the rabbit can make more without detection.
#from pathos.multiprocess import ProcessingPool

def monitor():
    """
    Monitors running processes looking for Fork Bombs. Kills them if found.
    """
    set()

    # Loop through all processes checking if they are making children
    while True:
        nc_count = Counter()
        nc_to_proc = {}

        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=
                    ["pid", "name", "cmdline", "create_time", "username"]
                    )
                nc_tup = (pinfo["name"], tuple(pinfo["cmdline"]))

                nc_count[nc_tup] += 1

                if nc_tup not in nc_to_proc.keys():
                    nc_to_proc[nc_tup] = set([proc])
                else:
                    nc_to_proc[nc_tup].add(proc)

            except psutil.NoSuchProcess:
                pass

        check_if_bomb(nc_count, nc_to_proc)

def check_if_bomb(nc_count, nc_to_proc):
    for (name, cmd), count in nc_count.most_common():
        if count >= HARD_PROC_LIMIT or (name, cmd) in known_rabbit:
            kill(name, cmd, nc_to_proc)
            known_rabbit.add((name, cmd))

def kill(name, cmd, nc_to_proc):
    """
    First, sedate, then kill the processes by name.

    """
    # Sedate and gather
    p_set = set()
    for proc in psutil.process_iter():
        try:
            #if proc.name() == name \
            if proc.name() == name and tuple(proc.cmdline()) == cmd \
                    and proc.pid != this_ppid and proc.pid != os.getpid():
                proc.suspend()
                p_set.add(proc)
        except psutil.NoSuchProcess:
            pass

    # Kill
    for proc in p_set:
        try:
            proc.kill()
        except psutil.NoSuchProcess:
            pass

def main():
    monitor()

if __name__ == "__main__":
    main()
