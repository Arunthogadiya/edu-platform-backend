from app.v1.repository.ChatbotConversationsRepository import ChatbotConversationsRepository
from app.utils.document_utils import load_documents

class ChatbotService:
    def __init__(self, llm_service):
        self.llm_service = llm_service
        self.repository = ChatbotConversationsRepository()
    
    def process_query(self, query, child_id, context=None):
        """Process a text query with enhanced response"""
        context_data = self.get_context(child_id)
        if context:
            context_data['additional_context'] = context
            
        response = self.llm_service.generate_response(query, context_data)
        
        return {
            'response': response['text'],
            'resources': response.get('resources', []),
            'suggestions': response.get('suggestions', []),
            'confidence_score': response.get('confidence_score', 1.0)
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
    
    def process_image_query(self, query, image_data, child_id):
        """
        Process a query with image and return response
        """
        # Get context for the child
        context = self.get_context(child_id)
        
        # Generate response using LLM with image
        response = self.llm_service.generate_response(
            query, 
            context,
            use_rag=False,
            image_data=image_data
        )
        
        # Save conversation to database
        self.repository.save_conversation(child_id, query, response)
        
        return {
            'response': response['text'],
            'resources': response['resources']
        }

    def get_history(self, user_id, limit=None, cursor=None):
        """Get paginated chat history"""
        history = self.repository.get_conversations_by_user(
            user_id, 
            limit=limit, 
            cursor=cursor
        )
        
        return {
            'history': [
                {
                    'id': str(item['id']),
                    'query': item['query'],
                    'response': item['response'],
                    'timestamp': item['timestamp'].isoformat(),
                    'resources': item.get('resources', []),
                    'type': item.get('type', 'text')
                }
                for item in history['items']
            ],
            'has_more': history['has_more'],
            'next_cursor': history.get('next_cursor')
        }
    
    def get_context(self, child_id):
        """
        Get context information for a child
        """
        # Implement context gathering logic here
        # This could include academic records, behavior records, etc.
        pass

    def process_document(self, file_path):
        """
        Process uploaded document and initialize LLM service with it
        """
        try:
            # Load documents using utility function
            documents = load_documents(file_path)
            
            # Initialize vector store with documents
            self.llm_service.initialize_vector_store(documents)
            
            return True
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            return False

    def analyze_document(self, file, child_id, context=None):
        """Analyze uploaded document"""
        try:
            temp_path = f"/tmp/{file.filename}"
            file.save(temp_path)
            
            # Process document
            documents = load_documents(temp_path)
            
            # Initialize vector store
            self.llm_service.initialize_vector_store(documents)
            
            # Generate analysis
            analysis = self.llm_service.analyze_document(documents)
            
            os.remove(temp_path)
            
            return {
                'analysis': analysis['summary'],
                'extracted_text': analysis.get('extracted_text'),
                'topic_summary': analysis.get('topic_summary'),
                'suggested_questions': analysis.get('suggested_questions', []),
                'resources': analysis.get('resources', [])
            }
        except Exception as e:
            logger.error(f"Document analysis error: {str(e)}")
            raise