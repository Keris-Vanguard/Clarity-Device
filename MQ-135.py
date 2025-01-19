import spidev
import time

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

def read_adc(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

try:
    while True:
        sensor_value = read_adc(0)  # Read channel 0 (MQ-135 analog pin)
        voltage = sensor_value * (3.3 / 1023)  # Adjust for your ADC reference voltage
        print(f"Sensor Value: {sensor_value} | Voltage: {voltage:.2f}V")
        time.sleep(1)
except KeyboardInterrupt:
    spi.close()
