import serial.tools.list_ports as sl

availableSerials = sl.comports()

for com in availableSerials:

    print(f"-{com.name}: {com.description}")