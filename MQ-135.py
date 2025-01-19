import RPi.GPIO as GPIO
import time

# Constants
SENSOR_PIN = 16  # GPIO pin connected to AO
WARMUP_TIME = 20  # Sensor needs warmup time
READING_INTERVAL = 1  # Time between readings in seconds
SAMPLE_WINDOW = 100  # Number of readings to take
READING_DELAY = 0.01  # 10ms between readings

def test_sensor_connection():
    print("Testing MQ-135 sensor connection...")
    print(f"GPIO Pin {SENSOR_PIN} configured for input")
    
    # Read initial value
    initial_value = GPIO.input(SENSOR_PIN)
    print(f"Initial reading: {initial_value}")
    
    # Test multiple readings
    print("Taking 10 test readings...")
    for i in range(10):
        reading = GPIO.input(SENSOR_PIN)
        print(f"Test reading {i+1}: {reading}")
        time.sleep(0.5)
    
    return True

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SENSOR_PIN, GPIO.IN)
    
    # Test connection before warmup
    if test_sensor_connection():
        print("Sensor connected successfully!")
        print("Warming up MQ-135 sensor...")
        time.sleep(WARMUP_TIME)
    else:
        raise Exception("Sensor connection failed!")

def get_sensor_readings():
    high_count = 0
    for _ in range(SAMPLE_WINDOW):
        if GPIO.input(SENSOR_PIN) == GPIO.HIGH:
            high_count += 1
        time.sleep(READING_DELAY)
    # Convert to percentage (0-1 range)
    return high_count / SAMPLE_WINDOW

def classify_air_quality(value):
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
            print("Air Quality Reading: " + str(format(value, '.2f')) + ", Classification: " + quality)
            time.sleep(READING_INTERVAL)
            
    except KeyboardInterrupt:
        print("\nProgram stopped by user")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()