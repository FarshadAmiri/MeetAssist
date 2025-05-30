# recorder.py

import sounddevice as sd
import soundfile as sf
import threading
import time

def record_audio(duration, output_path, samplerate=16000, channels=1):
    print(f"Recording audio for {duration} seconds...")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels, dtype='int16')
    sd.wait()
    sf.write(output_path, recording, samplerate)
    print(f"Audio saved to {output_path}")

def record_continuous(output_path, stop_event, samplerate=16000, channels=1):
    print("Starting continuous audio recording...")
    with sf.SoundFile(output_path, mode='w', samplerate=samplerate, channels=channels, subtype='PCM_16') as file:
        with sd.InputStream(samplerate=samplerate, channels=channels, dtype='int16') as stream:
            while not stop_event.is_set():
                data = stream.read(1024)[0]
                file.write(data)
