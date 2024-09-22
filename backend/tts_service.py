# services/tts_service.py
from TTS.api import TTS
import io

class TTSService:
    def __init__(self, model_name="tts_models/en/ljspeech/tacotron2-DDC"):
        self.tts = TTS(model_name=model_name)

    def synthesize_speech(self, text):
        try:
            # Synthesize speech and get the wav data
            wav = self.tts.tts(text)
            
            # Convert the wav data to bytes
            buffer = io.BytesIO()
            self.tts.synthesizer.save_wav(wav, buffer)
            return buffer.getvalue()
        except Exception as e:
            print(f"Error in TTS: {e}")
            return None