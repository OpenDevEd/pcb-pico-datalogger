import board
import busio

# Create I2C object
i2c = busio.I2C(board.GP3, board.GP2)

# Acquire lock
while not i2c.try_lock():
    pass

try:
    # Print out any addresses found
    devices = i2c.scan()

    if devices:
        for d in devices:
            print(hex(d))
finally:
    # Release the lock
    i2c.unlock()
