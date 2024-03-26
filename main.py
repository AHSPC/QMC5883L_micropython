from machine import SoftI2C, PWM, Pin, soft_reset
from qmc5883l import QMC5883L
from time import sleep


qmc_i2c = SoftI2C(scl=Pin(17), sda=Pin(16))
print(qmc_i2c.scan())
qmc = QMC5883L(qmc_i2c)

from drv8833 import DRV8833

drv_freq = 100_000
ain1 = PWM(Pin(12), freq=drv_freq)
ain2 = PWM(Pin(13), freq=drv_freq)
bin1 = PWM(Pin(14), freq=drv_freq)
bin2 = PWM(Pin(15), freq=drv_freq)
drv = DRV8833(ain1, ain2, bin1, bin2)


print("starting calibration!")

drv.throttle_a(0.9)
drv.throttle_b(-0.9)

qmc.calibrate(5)

drv.stop_a()
drv.stop_b()

print("finished calibrating!")
print("calibration params: ", qmc.xs, qmc.xb, qmc.ys, qmc.yb)

drv.throttle_a(0.8)
drv.throttle_b(-0.8)
for _ in range(100):
    x, y, z, t = qmc.read_scaled()
    angle = qmc.get_angle(x, y)
    print(angle)

    # if abs(angle) < 1.0:
    #     print("found north!")
    #     break

    sleep(0.01)


drv.stop_a()
drv.stop_b()

soft_reset()
