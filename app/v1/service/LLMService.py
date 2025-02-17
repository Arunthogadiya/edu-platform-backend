from langchain.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from app.config.llm_config import LLM_CONFIG, BASIC_PROMPT_TEMPLATE, RAG_TEMPLATE
from app.utils.image_utils import convert_to_base64
from app.utils.document_utils import format_docs
from app.v1.service.BhashiniService import BhashiniService

class LLMService:
    def __init__(self):
        # Initialize embeddings and LLMs
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.vector_store = None
        self.ollama_llm = OllamaLLM(model=LLM_CONFIG["ollama"]["model"])
        self.multimodal_llm = OllamaLLM(model="bakllava")
        
        # Initialize prompts and chains
        self.basic_prompt = ChatPromptTemplate.from_template(BASIC_PROMPT_TEMPLATE)
        self.rag_prompt = ChatPromptTemplate.from_template(RAG_TEMPLATE)
        self.basic_chain = self.basic_prompt | self.ollama_llm | StrOutputParser()
        
        # Initialize RAG chain
        self.rag_chain = (
            RunnablePassthrough.assign(context=lambda input: format_docs(input["context"]))
            | self.rag_prompt
            | self.ollama_llm
            | StrOutputParser()
        )
        
        self.bhashini_service = BhashiniService()
    
    def initialize_vector_store(self, documents):
        """Initialize or update vector store with documents"""
        self.vector_store = Chroma.from_documents(
            documents=documents, 
            embedding=self.embeddings
        )
    
    def generate_response(self, query, context, use_rag=True, image_data=None, target_language=None):
        """Generate response with optional translation"""
        # Get response in English
        response = self._generate_base_response(query, context, use_rag, image_data)
        
        # Translate if needed
        if target_language and target_language != 'en':
            try:
                response['text'] = self.bhashini_service.translate_text(
                    response['text'],
                    'en',
                    target_language
                )
            except Exception as e:
                logger.warning(f"Translation failed: {str(e)}")
        
        return response
    
    def _generate_base_response(self, query, context, use_rag, image_data):
        """Generate base response in English"""
        if image_data:
            # Handle multimodal query
            image_b64 = convert_to_base64(image_data)
            llm_with_image = self.multimodal_llm.bind(images=[image_b64])
            response_text = llm_with_image.invoke(query)
        elif use_rag and self.vector_store:
            # Get relevant documents and generate response using RAG
            docs = self.vector_store.similarity_search(query)
            response_text = self.rag_chain.invoke({
                "context": docs,
                "question": query
            })
        else:
            # Generate response using basic LLM
            response_text = self.basic_chain.invoke({"question": query})

        resources = self.get_relevant_resources(query, response_text)
        return {
            "text": response_text,
            "resources": resources
        }
    
    def transcribe_audio(self, audio_data, source_language=None):
        """Transcribe audio using Bhashini"""
        return self.bhashini_service.transcribe_audio(audio_data, source_language)
    
    def get_relevant_resources(self, query, response):
        """
        Get relevant educational resources based on query and response
        """
        # Implement resource retrieval logic here
        # Could include YouTube EDU links, etc.
        return []

    def analyze_document(self, documents):
        """Analyze document content"""
        combined_text = format_docs(documents)
        
        # Generate document summary
        summary_response = self.basic_chain.invoke({
            "question": f"Summarize the following document: {combined_text}"
        })
        
        # Generate topic summary
        topic_response = self.basic_chain.invoke({
            "question": f"What are the main topics in this document: {combined_text}"
        })
        
        # Generate suggested questions
        questions_response = self.basic_chain.invoke({
            "question": f"Generate 3 relevant questions about this document: {combined_text}"
        })
        
        return {
            'summary': summary_response,
            'extracted_text': combined_text,
            'topic_summary': topic_response,
            'suggested_questions': questions_response.split('\n'),
            'resources': self.get_relevant_resources(combined_text, summary_response)
        }