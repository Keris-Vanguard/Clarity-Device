import RPi.GPIO as GPIO
import time

SENSOR_PIN = 16
WARMUP_TIME = 20
READING_INTERVAL = 1
NUM_SAMPLES = 5
PULSE_TIMEOUT = 2.0  # Maximum time to wait for pulse

def get_pulse_duration():
    # Wait for sensor to go HIGH
    pulse_start = time.time()
    while GPIO.input(SENSOR_PIN) == GPIO.LOW:
        if time.time() - pulse_start > PULSE_TIMEOUT:
            return 0.0
    
    # Measure how long it stays HIGH
    pulse_start = time.time()
    while GPIO.input(SENSOR_PIN) == GPIO.HIGH:
        if time.time() - pulse_start > PULSE_TIMEOUT:
            return PULSE_TIMEOUT
    
    pulse_end = time.time()
    return pulse_end - pulse_start

def get_sensor_readings():
    readings = []
    for _ in range(NUM_SAMPLES):
        duration = get_pulse_duration()
        readings.append(duration)
        time.sleep(0.1)
    
    # Average the readings
    return sum(readings) / NUM_SAMPLES

def classify_air_quality(duration):
    # Classify based on pulse duration
    if duration < 0.1:  # Short pulses = clean air
        return "Good"
    elif duration < 0.5:  # Medium pulses = moderate
        return "Moderate"
    else:  # Long pulses = poor air
        return "Bad"

def main():
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SENSOR_PIN, GPIO.IN)
        print("Warming up sensor...")
        time.sleep(WARMUP_TIME)
        
        while True:
            duration = get_sensor_readings()
            quality = classify_air_quality(duration)
            print("Pulse Duration: " + str(format(duration, '.3f')) + "s, Air Quality: " + quality)
            time.sleep(READING_INTERVAL)
            
    except KeyboardInterrupt:
        print("\nProgram stopped")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()