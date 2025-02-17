from app.config.llm_config import BHASHINI_CONFIG
import requests
import json
import base64

class BhashiniService:
    def __init__(self):
        self.config = BHASHINI_CONFIG
        self.client = self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Bhashini client"""
        from app.utils.bhashini_client import BhashiniClient
        return BhashiniClient(
            user_id=self.config['user_id'],
            api_key=self.config['api_key'],
            pipeline_id=self.config['pipeline_id']
        )
    
    def transcribe_audio(self, audio_data, source_language=None):
        """Transcribe audio using Bhashini ASR"""
        try:
            return self.client.asr(audio_data, source_language=source_language)
        except Exception as e:
            logger.error(f"ASR error: {str(e)}")
            raise
    
    def text_to_speech(self, text, language, gender='female'):
        """Convert text to speech using Bhashini TTS"""
        try:
            return self.client.tts(text, language, gender=gender)
        except Exception as e:
            logger.error(f"TTS error: {str(e)}")
            raise
    
    def translate_text(self, text, source_lang, target_lang):
        """Translate text using Bhashini translation"""
        try:
            return self.client.translate(text, source_lang, target_lang)
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            raise
