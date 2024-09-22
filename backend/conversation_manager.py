# services/conversation_manager.py
class ConversationManager:
    def __init__(self):
        self.history = []

    def generate_initial_prompt(self, topic):
        return f"Let's have a conversation about {topic}. Please start by introducing the topic and asking me a question about it."

    def update_history(self, user_input, ai_response):
        self.history.append({"user": user_input, "ai": ai_response})

    def get_history(self):
        return self.history