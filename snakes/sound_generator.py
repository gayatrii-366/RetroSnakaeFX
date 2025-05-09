import wave
import math
import struct

def generate_eat_sound():
    # Parameters for eat sound
    duration = 0.1  # seconds
    sample_rate = 44100  # Hz
    frequency = 880.0  # Hz (A5 note)
    
    samples = []
    num_samples = int(duration * sample_rate)
    
    for i in range(num_samples):
        t = float(i) / sample_rate
        # Create a short rising tone
        sample = math.sin(2.0 * math.pi * frequency * t * (1 + t * 10)) * 0.5
        # Apply fade out
        sample *= 1.0 - (float(i) / float(num_samples))
        samples.append(sample)
    
    # Save as WAV file
    with wave.open('sounds/eat.wav', 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        # Convert samples to bytes
        for sample in samples:
            packed_value = struct.pack('h', int(sample * 32767.0))
            wav_file.writeframes(packed_value)

def generate_crash_sound():
    # Parameters for crash sound
    duration = 0.2  # seconds
    sample_rate = 44100  # Hz
    base_frequency = 220.0  # Hz (A3 note)
    
    samples = []
    num_samples = int(duration * sample_rate)
    
    for i in range(num_samples):
        t = float(i) / sample_rate
        # Create a discordant sound with multiple frequencies
        sample = math.sin(2.0 * math.pi * base_frequency * t) * 0.3
        sample += math.sin(2.0 * math.pi * (base_frequency * 1.1) * t) * 0.3
        sample += math.sin(2.0 * math.pi * (base_frequency * 0.9) * t) * 0.3
        # Apply fade out
        sample *= 1.0 - (float(i) / float(num_samples))
        samples.append(sample)
    
    # Save as WAV file
    with wave.open('sounds/crash.wav', 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        # Convert samples to bytes
        for sample in samples:
            packed_value = struct.pack('h', int(sample * 32767.0))
            wav_file.writeframes(packed_value)

if __name__ == "__main__":
    generate_eat_sound()
    generate_crash_sound()
    print("Sound effects generated successfully!")