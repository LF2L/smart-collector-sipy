import machine
import ubinascii

print(machine.unique_id())
print(ubinascii.hexlify(machine.unique_id(),':').decode())