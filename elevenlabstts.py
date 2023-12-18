from elevenlabs import generate, play


class ElevenLabsTTS:
    def __init__(self, api_key=None):
        if api_key:
            from elevenlabs import set_api_key
            set_api_key(api_key)

    def synthesize(self, text):
        audio = generate(
            text=text,
            voice="Adam",
            model="eleven_multilingual_v2",
        )
        play(audio)  # Übergeben des use_ffmpeg Parameters an die


tts = ElevenLabsTTS('1fffb49270eaf8702047a9330d841fab')
