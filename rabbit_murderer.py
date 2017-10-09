"""
A simple program that is meant to monitor the system's processes to detect and
kill any fork bomb (rabit) malware processes (Continuously self-duplicating
processes that will inevitibly lead to the system failure).

Either runs for the specific user, or if run by root then can run full system.

@author: Derek S. Prijatelj
"""

import copy
from collections import Counter
import psutil

HARD_PROC_LIMIT = 63

# May need to split the check_if_bomb & other slow parts to ensure prog is fast
#   enough to kill the rabbit before the rabbit can make more without detection.
#from pathos.multiprocess import ProcessingPool

def monitor():
    """
    Monitors running processes looking for Fork Bombs. Kills them if found.
    """
    pname_count = Counter()
    tmp_count = None
    seen_pid = {} # stores pid : create time pairs
    name_to_pids = {} # name to set of pids that the name has applied to.

    # Loop through all processes checking if they are making children
    while True:
        tmp_seen_pid = set() #to find which pids are gone

        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=
                    ["pid", "name", "create_time", "username"]
                    )

                tmp_seen_pid.add(pinfo["pid"])

                # handle pid
                if pinfo["pid"] not in seen_pid.keys():
                    seen_pid[pinfo["pid"]] = pinfo

                    # if a new process, then increase count of name
                    pname_count[pinfo["name"]] += 1
                    # handle name
                    if pinfo["name"] not in name_to_pids.keys():
                        name_to_pids[pinfo["name"]] = set([pinfo["pid"]])
                    else:
                        if pinfo["pid"] not in name_to_pids[pinfo["name"]]:
                            name_to_pids[pinfo["name"]].add(pinfo["pid"])

                elif pinfo["create_time"] != seen_pid[pinfo["pid"]] \
                                                     ["create_time"]:
                    # pid has been seen, but new create time = different process
                    # decrement counter due to loss of process
                    pname_count[seen_pid[pinfo["pid"]]["name"]] -= 1
                    name_to_pids[seen_pid[pinfo["pid"]]["name"]] \
                        .remove(pinfo["pid"])
                    seen_pid[pinfo["pid"]] = pinfo

                    # if a new process, then increase count of name
                    pname_count[pinfo["name"]] += 1
                    # handle name
                    if pinfo["name"] not in name_to_pids.keys():
                        name_to_pids[pinfo["name"]] = set([pinfo["pid"]])
                    else:
                        if pinfo["pid"] not in name_to_pids[pinfo["name"]]:
                            name_to_pids[pinfo["name"]].add(pinfo["pid"])

                # remove pids that are no longer existing
                missing_pids = seen_pid.keys() - tmp_seen_pid
                for mpid in missing_pids:
                    tmp_name = seen_pid[mpid]["name"]
                    pname_count[tmp_name] -= 1
                    name_to_pids[tmp_name].remove(mpid)
                    seen_pid.pop(mpid)

            except psutil.NoSuchProcess:
                pass

        if tmp_count != None:
            check_if_bomb(pname_count, tmp_count, seen_pid, name_to_pids)
        tmp_count = copy.deepcopy(pname_count) # saves previous state of pids

def check_if_bomb(pname_count, tmp_count, seen_pid, name_to_pids):
    for name, count in pname_count.items():
        if (name in tmp_count.keys() \
                and tmp_count[name] >= 30 \
                and pname_count[name] >= tmp_count[name] * 2) \
                or pname_count[name] >= HARD_PROC_LIMIT:
            # get all parents and children, then kill all
            kill(name, seen_pid, name_to_pids)

def kill(name, seen_pid, name_to_pids):
    """
    Kills the given process and all of it's subprocesses.

    """
    for pid in name_to_pids[name]:
        proc = psutil.Process(pid) # TODO may cause race problem,
        #   may want to store proc, rather than pid.
        proc.kill()

    for proc in psutil.process_iter():
        try:
            if proc.name() == name or proc.exe() == name \
                    or proc.cmdline() == name:
                proc.kill()
        except psutil.NoSuchProcess:
            pass

def main():
    monitor()

if __name__ == "__main__":
    main()
