from machine import SoftI2C, Pin
from qmc5883l import QMC5883L
from time import sleep

qmc_i2c = SoftI2C(scl=Pin(17), sda=Pin(16))
qmc = QMC5883L(qmc_i2c)

# from drv8833 import DRV8833
# ain1 = 
# drv = DRV8833()


print("starting calibration!")

# drv.throttle_a(1.0)
# drv.throttle_a(-1.0)

qmc.calibrate(5)

# drv.stop_a()
# drv.stop_b()

print("finished calibrating!")
print("calibration params: ", qmc.xs, qmc.xb, qmc.ys, qmc.yb)

for _ in range(9999):
    x, y, z = qmc.read_calib()
    # print(x, y, z, qmc.get_angle(x, y))
    print(qmc.get_angle(x, y))

    sleep(0.1)

