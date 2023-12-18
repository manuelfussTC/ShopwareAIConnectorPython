import sys
import threading
import sounddevice as sd
import wave
import numpy as np

from asr import ASR
from recorder import Recorder


class SpeechInput:
    def __init__(self, api_key):
        self.recorder = Recorder()  # Initialisiere die Audiorecorder-Komponente
        self.asr = ASR(api_key)  # Initialisiere die ASR-Komponente mit dem API-Key
        self.is_recording = False
        self.record_thread = None

    def reset(self):
        self.recording = False
        self.audio_data = []

    def callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        if self.recording:
            self.audio_data.append(indata.copy())

    def prompt_for_redo(self):
        user_input = input("Keine Audio-Daten aufgenommen. Möchtest du es erneut versuchen? (ja/nein): ")
        return user_input.lower() == 'ja'




    def record(self, filename):
        while True:  # Fügt eine Schleife hinzu, die die Aufnahme wiederholt, bis gültige Daten aufgenommen wurden
            self.reset()  # Setzt den Audio-Puffer zurück, bevor eine neue Aufnahme gestartet wird
            mic_device_id = 1  # Ersetzen Sie dies durch die ID Ihres Mikrofons
            with sd.InputStream(callback=self.callback, device=mic_device_id, channels=1, dtype='int16') as self.stream:
                self.samplerate = self.stream.samplerate
                print("Drücke Enter, um die Aufnahme zu starten und zu stoppen...")
                input()  # Warte auf Enter-Tastendruck, um die Aufnahme zu starten
                self.recording = True
                print("Aufnahme gestartet... Drücke Enter erneut, um die Aufnahme zu stoppen")
                input()  # Warte auf einen weiteren Enter-Tastendruck, um die Aufnahme zu stoppen
                self.recording = False
                print("Aufnahme gestoppt. Speichern...")
                if self.audio_data:
                    self.save(filename)
                    break  # Verlässt die Schleife, wenn Audio-Daten aufgenommen wurden
                elif not self.prompt_for_redo():
                    break  # Verlässt die Schleife, wenn der Benutzer die Aufnahme nicht erneut versuchen möchte

    def save(self, filename):
        print("In save method...")  # Debug-Ausgabe
        if not self.audio_data:
            print("Keine Audio-Daten aufgenommen.")
            return
        audio_data = np.concatenate(self.audio_data, axis=0)  # Vereinige alle Aufnahme-Chunks
        print(f"Audio data length: {len(audio_data)}")  # Debug-Ausgabe
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(audio_data.dtype.itemsize)  # Größe in Bytes
            wf.setframerate(self.samplerate)  # Verwenden der tatsächlichen Samplerate
            wf.writeframes(audio_data.tobytes())
        print(f"File saved as {filename}")  # Debug-Ausgabe

    def get_transcription(self):
        self.record('audio.wav')

        transcription = self.asr.transcribe('audio.wav')  # Transkribiere das Audio
        return transcription
