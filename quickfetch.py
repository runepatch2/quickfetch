import platform
import psutil # run 'pip3 install psutil' in VSC terminal.
import battery # run 'pip3 install battery' in VSC terminal.
import time


def byteToGB(bytes):
    return round(bytes / 1000000000, 2)

def byteToMB(bytes):
    return f"{round(bytes / 1000000, 2):,}"

def secondsToHHMMSS(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = round((seconds % 3600) % 60, 2)
    return {"hours": hours, "minutes": minutes, "seconds": seconds}

def chargeETA(timeETA, pluggedIn):
    startTime = time.time()
    if pluggedIn: 
        eta = battery.minutes_to_full()
    else:
        eta = battery.minutes_to_empty()
    try:
        timeETA = secondsToHHMMSS(eta * 60)
    except TypeError:
        if input("Not enough data to calculate ETA. Do you want to wait up to 30 seconds to calculate ETA? (y/n) ").strip().lower() == "y":
            while timeETA == None:
                if time.time() - startTime > 30:
                    timeETA = "TOOK TOO LONG. TERMINATING LOOP"
                    break
                try: timeETA = secondsToHHMMSS(eta * 60)
                except: 
                    time.sleep(1)
                    pass
    return timeETA
                

release = platform.release()
system = platform.system()
version = platform.version()

systemTime = secondsToHHMMSS(psutil.cpu_times().system)
userTime = secondsToHHMMSS(psutil.cpu_times().user)

totalSwapMB = byteToMB(psutil.swap_memory().total)
availableSwapMB = byteToMB(psutil.swap_memory().free)
usedSwapMB = byteToMB(psutil.swap_memory().used)

availableRAMGB = byteToGB(psutil.virtual_memory().available)
totalRAMGB = byteToGB(psutil.virtual_memory().total)
usedRAMGB = (totalRAMGB - availableRAMGB)

try:
    pluggedIn = psutil.sensors_battery().power_plugged
    device = "Laptop"
except AttributeError:
    device = "Desktop"
    pass
startPercent = 0
percentDelta = 0.00
timeUntilFull = None
timeUntilEmpty = None

print("----- CPU TIME INFO -----")
print(f"User time: {userTime}")
print(f"System time: {systemTime}\n")

print("----- MEMORY INFO -----")
print(f"RAM usage (GB): {round(usedRAMGB, 2)}/{round(totalRAMGB, 2)} ({round(100 * usedRAMGB/totalRAMGB, 2)}%)")
print(f"System swap (MB): {usedSwapMB}/{totalSwapMB} ({psutil.swap_memory().percent}%)")

print("----- BATTERY INFO -----")

if device == "Laptop":
    if pluggedIn:
        print(f"Status: charging ({battery.percent()}%). Will try to calculate ETA until full.")
        timeUntilFull = chargeETA(timeUntilFull, pluggedIn)
        if timeUntilFull != None: 
            print(timeUntilFull)
        else: print("Not enough data to calculate.")
    else:
        print(f"Status: discharging ({battery.percent()}%). Will try to calculate ETA until empty.")
        print(chargeETA(timeUntilEmpty, pluggedIn))

print("You're using a desktop so there's currently no battery information to give. Will add in the future.")