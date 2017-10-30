import psutil
import os

print("I AM THE LAW. ANYTHING THAT GETS IN MY WAY WILL BE TREATED AS AN ACCESSORY.")
print("YOU HAVE BEEN WARNED")

username = psutil.Process(os.getpid()).username()
judges = set()
#gets all starting processes and keeps them safe from the judges
law_abiding = set()
for starting in psutil.process_iter():
    if starting.username() == username:
        law_abiding.add(starting.pid)

#kills all processes that are not starting processes
while True:
    for target in psutil.process_iter():
        accessory = set()
        if target.pid not in law_abiding and target.username() == username and target.pid not in judges:
            target.suspend()
            accessory.add(target)
        for processes in accessory:
            try:
                processes.kill()
            except psutil.NoSuchProcess:
                pass
