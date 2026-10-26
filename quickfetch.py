import platform
import psutil # run 'pip install psutil' in VSC terminal.
import battery # run 'pip install battery' in VSC terminal.
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

pluggedIn = psutil.sensors_battery().power_plugged
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

# Pseudo-code
# Detect whether device is plugged in or not
# If so, try to calculate time until full, except if TypeError. In which case ask the user if they want to wait 1 minute to calculate. If they don't pass
#If not plugged in, again try to calculate time until empty, except TypeError. In which case ask if they want to wait 1 minute. If not, pass.

if pluggedIn:
    print("Seems like your device is plugged in. Will try to calculate time until full.")
    timeUntilFull = chargeETA(timeUntilFull, pluggedIn)
    if timeUntilFull != None: 
        print(timeUntilFull)
    else: print("Not enough data to calculate.")
else:
    print("Seems like your device is unplugged! Will try to calculate ETA: ")
    print(chargeETA(timeUntilEmpty, pluggedIn))