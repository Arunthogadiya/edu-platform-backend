from flask import Blueprint, request, jsonify
from app.config.logger_config import LogConfig
from app.v1.service.ChatbotService import ChatbotService
from app.v1.service.LLMService import LLMService
from werkzeug.utils import secure_filename
from functools import wraps
import time
import os

chatbot_bp = Blueprint('chatbot', __name__)
logger = LogConfig.setup_logger(__name__)

# Initialize services
llm_service = LLMService()
chatbot_service = ChatbotService(llm_service)

# Rate limiting configuration
RATE_LIMITS = {
    'query': {'requests': 60, 'per_minutes': 1},
    'voice': {'requests': 30, 'per_minutes': 1},
    'document': {'requests': 30, 'per_minutes': 1},
    'history': {'requests': 120, 'per_minutes': 1}
}

def rate_limit(limit_type):
    def decorator(f):
        requests = {}
        @wraps(f)
        def wrapper(*args, **kwargs):
            now = time.time()
            window_start = now - (RATE_LIMITS[limit_type]['per_minutes'] * 60)
            
            # Clean old requests
            requests = {ts: count for ts, count in requests.items() if ts > window_start}
            
            # Count requests in window
            if sum(requests.values()) >= RATE_LIMITS[limit_type]['requests']:
                return jsonify({'error': 'Rate limit exceeded'}), 429
                
            requests[now] = requests.get(now, 0) + 1
            return f(*args, **kwargs)
        return wrapper
    return decorator

@chatbot_bp.route('/api/chatbot/query', methods=['POST'])
@rate_limit('query')
def handle_text_query():
    """
    Handle text-based queries to the chatbot
    """
    try:
        data = request.get_json()
        query = data.get('query')
        child_id = data.get('child_id')
        context = data.get('context')
        
        if not query or not child_id:
            return jsonify({'error': 'Missing required fields'}), 400
            
        response = chatbot_service.process_query(query, child_id, context)
        
        return jsonify({
            'response': response['response'],
            'resources': response.get('resources', []),
            'suggestions': response.get('suggestions', []),
            'confidence_score': response.get('confidence_score', 1.0)
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing chatbot query: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@chatbot_bp.route('/api/chatbot/voice-query', methods=['POST'])
@rate_limit('voice')
def handle_voice_query():
    """
    Handle voice-based queries to the chatbot
    """
    try:
        data = request.get_json()
        audio_data = data.get('audio_data')
        child_id = data.get('child_id')
        
        if not audio_data or not child_id:
            return jsonify({
                'error': 'Missing required fields'
            }), 400
            
        response = chatbot_service.process_voice_query(audio_data, child_id)
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error processing voice query: {str(e)}")
        return jsonify({
            'error': 'Internal server error'
        }), 500

@chatbot_bp.route('/api/chatbot/image-query', methods=['POST'])
def handle_image_query():
    """
    Handle image-based queries to the chatbot
    """
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
            
        image_file = request.files['image']
        query = request.form.get('query')
        child_id = request.form.get('child_id')
        
        if not query or not child_id:
            return jsonify({
                'error': 'Missing required fields'
            }), 400
            
        image_data = image_file.read()
        response = chatbot_service.process_image_query(query, image_data, child_id)
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error processing image query: {str(e)}")
        return jsonify({
            'error': 'Internal server error'
        }), 500

@chatbot_bp.route('/api/chatbot/history', methods=['GET'])
@rate_limit('history')
def get_chat_history():
    """
    Retrieve chat history for a user
    """
    try:
        user_id = request.args.get('user_id')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        if not user_id:
            return jsonify({
                'error': 'Missing user_id parameter'
            }), 400
            
        history, total_pages = chatbot_service.get_history(user_id, page, per_page)
        
        return jsonify({
            'history': history,
            'total_pages': total_pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        logger.error(f"Error retrieving chat history: {str(e)}")
        return jsonify({
            'error': 'Internal server error'
        }), 500

@chatbot_bp.route('/api/chatbot/upload-document', methods=['POST'])
@rate_limit('document')
def upload_document():
    """
    Handle document upload for RAG context
    """
    try:
        if 'document' not in request.files:
            return jsonify({'error': 'No document file provided'}), 400
            
        file = request.files['document']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
            
        # Save file temporarily
        filename = secure_filename(file.filename)
        temp_path = os.path.join('/tmp', filename)
        file.save(temp_path)
        
        # Process document
        success = chatbot_service.process_document(temp_path)
        
        # Clean up
        os.remove(temp_path)
        
        if success:
            return jsonify({'message': 'Document processed successfully'}), 200
        else:
            return jsonify({'error': 'Failed to process document'}), 500
            
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@chatbot_bp.route('/api/chatbot/analyze-document', methods=['POST'])
@rate_limit('document')
def analyze_document():
    """
    Analyze a document for RAG context
    """
    try:
        if 'document' not in request.files:
            return jsonify({'error': 'No document file provided'}), 400
            
        file = request.files['document']
        child_id = request.form.get('child_id')
        context = request.form.get('context')
        
        if not file or not child_id:
            return jsonify({'error': 'Missing required fields'}), 400
            
        # Validate file size (5MB limit)
        if len(file.read()) > 5 * 1024 * 1024:
            return jsonify({'error': 'File size too large'}), 413
        file.seek(0)
        
        # Validate file type
        allowed_extensions = {'.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png'}
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in allowed_extensions:
            return jsonify({'error': 'Unsupported file type'}), 400
            
        analysis = chatbot_service.analyze_document(file, child_id, context)
        
        return jsonify(analysis), 200
        
    except Exception as e:
        logger.error(f"Error analyzing document: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500