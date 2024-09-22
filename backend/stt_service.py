# services/stt_service.py
import whisper

class STTService:
    def __init__(self, model_name="base"):
        self.model = whisper.load_model(model_name)

    def transcribe(self, audio_data):
        try:
            # Whisper expects a path to an audio file, so we need to temporarily save the audio data
            with open("temp_audio.wav", "wb") as f:
                f.write(audio_data)
            
            # Perform the transcription
            result = self.model.transcribe("temp_audio.wav")
            return result["text"]
        except Exception as e:
            print(f"Error in STT: {e}")
            return "Sorry, I couldn't understand the audio."
        finally:
            # Clean up the temporary file
            import os
            os.remove("temp_audio.wav")