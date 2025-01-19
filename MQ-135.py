import RPi.GPIO as GPIO
import time
import statistics

# Constants
SENSOR_PIN = 16  # GPIO pin connected to AO
WARMUP_TIME = 20  # Sensor needs warmup time
READING_INTERVAL = 1  # Time between readings in seconds
NUM_SAMPLES = 10  # Number of samples to average

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SENSOR_PIN, GPIO.IN)
    print("Warming up MQ-135 sensor...")
    time.sleep(WARMUP_TIME)

def get_sensor_readings():
    readings = []
    for _ in range(NUM_SAMPLES):
        # Read digital value (0 or 1)
        reading = GPIO.input(SENSOR_PIN)
        readings.append(reading)
        time.sleep(0.1)
    return statistics.mean(readings)

def classify_air_quality(value):
    # These thresholds should be calibrated based on your specific needs
    if value < 0.3:
        return "Good"
    elif value < 0.6:
        return "Moderate"
    else:
        return "Bad"

def main():
    try:
        setup()
        while True:
            value = get_sensor_readings()
            quality = classify_air_quality(value)
            print(f"Air Quality Reading: {value:.2f}, Classification: {quality}")
            time.sleep(READING_INTERVAL)
            
    except KeyboardInterrupt:
        print("\nProgram stopped by user")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()