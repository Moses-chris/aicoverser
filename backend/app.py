# app.py
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.llama_service import LlamaService
from services.stt_service import STTService
from services.tts_service import TTSService
from services.conversation_manager import ConversationManager
from services.performance_analyzer import PerformanceAnalyzer

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize services
llama_service = LlamaService()
stt_service = STTService()
tts_service = TTSService()
conversation_manager = ConversationManager()
performance_analyzer = PerformanceAnalyzer()

class ConversationRequest(BaseModel):
    topic: str

@app.post("/start_conversation")
async def start_conversation(request: ConversationRequest):
    initial_prompt = conversation_manager.generate_initial_prompt(request.topic)
    ai_response = llama_service.generate_response(initial_prompt)
    audio_response = tts_service.synthesize_speech(ai_response)
    
    return {
        "text_response": ai_response,
        "audio_response": audio_response
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            audio_data = await websocket.receive_bytes()
            
            # Process the audio data
            text = stt_service.transcribe(audio_data)
            
            # Generate AI response
            ai_response = llama_service.generate_response(text)
            
            # Synthesize speech
            audio_response = tts_service.synthesize_speech(ai_response)
            
            # Send response back to the client
            await websocket.send_text(ai_response)
            await websocket.send_bytes(audio_response)
            
            # Update conversation history
            conversation_manager.update_history(text, ai_response)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        # Analyze performance when the conversation ends
        performance_summary = performance_analyzer.analyze(conversation_manager.get_history())
        await websocket.send_json(performance_summary)
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)