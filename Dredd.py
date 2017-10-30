import psutil
import os
print("I AM THE LAW. ANYTHING THAT GETS IN MY WAY WILL BE TREATED AS AN ACCESSORY.")
print("YOU HAVE BEEN WARNED")

#get the name of this userspace
username = psutil.Process(os.getpid()).username()
#now take every starting process and do not hurt them. The are law-abiding
law_abiding = set()
for starting in psutil.process_iter():
    if starting.username() == username:
        law_abiding.add(starting.pid)
for citizens in law_abiding:
        print(citizens)
#will kill any process that starts 
while True:
    for target in psutil.process_iter():
        if target.pid not in law_abiding and target.username() == username:
            print(target)
            target.kill()
