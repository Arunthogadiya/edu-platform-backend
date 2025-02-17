from app.v1.repository.ChatbotConversationsRepository import ChatbotConversationsRepository

class ChatbotService:
    def __init__(self, llm_service):
        self.llm_service = llm_service
        self.repository = ChatbotConversationsRepository()
    
    def process_query(self, query, child_id):
        """
        Process a text query and return response
        """
        # Get context for the child
        context = self.get_context(child_id)
        
        # Generate response using LLM
        response = self.llm_service.generate_response(query, context)
        
        # Save conversation to database
        self.repository.save_conversation(child_id, query, response)
        
        return {
            'response': response['text'],
            'resources': response['resources']
        }
    
    def process_voice_query(self, audio_data, child_id):
        """
        Process a voice query and return response
        """
        # Transcribe audio to text
        transcript = self.llm_service.transcribe_audio(audio_data)
        
        # Process the transcribed text
        response = self.process_query(transcript, child_id)
        
        return {
            'transcript': transcript,
            **response
        }
    
    def get_history(self, user_id):
        """
        Retrieve chat history for a user
        """
        return self.repository.get_conversations_by_user(user_id)
    
    def get_context(self, child_id):
        """
        Get context information for a child
        """
        # Implement context gathering logic here
        # This could include academic records, behavior records, etc.
        pass