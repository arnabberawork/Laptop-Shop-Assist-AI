import os,logging
from flask import Flask, request, jsonify, render_template, session
from openai_api import get_chat_completions, get_chat_completions_tool
from dialogue import initialize_conversation_system, handle_moderation_check, process_user_input, confirm_intent, fetch_recommendations,generate_recommendation
from schema.shopassist_schema import shopassist_custom_functions
from schema.config import Config
from datetime import timedelta

# Setup logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.StreamHandler(),
                        logging.FileHandler('app.log', encoding='utf-8', mode='a')  # Logs to app.log file
                    ])
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='templates', static_folder='static')
#app.config.from_object(Config)

# Secret key for session management (use a secure key in production)
app.secret_key = os.urandom(24)  # Generates a random 24-byte secret key

# Set the session lifetime (optional)
app.permanent_session_lifetime = timedelta(days=1)  # Session expires in 1 days

@app.route('/')
def home():
    logger.debug("Rendering the home page.")
    return render_template('laptop-shop-assistant.html')

@app.route('/api/start_conversation', methods=['GET'])
def start_conversation():
    logger.info("Starting a new conversation.")
    try:
        # Initialize conversation and introduction
        conversation, introduction = initialize_conversation_system()
        session['conversation'] = conversation
        logger.debug("Conversation initialized: %s", conversation)
        return jsonify({"introduction": introduction}), 200
    except Exception as e:
        logger.error("Error starting conversation: %s", str(e))
        return jsonify({"error": "Failed to start conversation."}), 500

@app.route('/api/process_input', methods=['POST'])
def process_input():
    user_input = request.json.get('message')
    logger.info("app_info 1 - Processing user input: %s", user_input)
    
    try:
        conversation = session.get('conversation', [])
        top_3_laptops = session.get('top_3_laptops', None)
        
        # Moderation check for user input
        if not handle_moderation_check(user_input):
            logger.warning("User input flagged by moderation: %s", user_input)
            return jsonify({"error": "Message flagged by moderation."}), 400
        
        if top_3_laptops is None:
            logger.debug("No recommendations in session. Processing input.")
            # Process user input
            response_assistant = process_user_input(conversation, user_input)
            logger.debug("app_info 2 - Assistant response: %s", response_assistant)
            
            # Moderation check for assistant response
            if not handle_moderation_check(response_assistant):
                logger.warning("Assistant response flagged by moderation: %s", response_assistant)
                return jsonify({"error": "Assistant response flagged by moderation."}), 400
            
            # Confirm intent
            response_tool = get_chat_completions_tool(response_assistant, func_name=shopassist_custom_functions)
            logger.debug("Tool response for confirmation: %s", response_tool)
            confirmation = confirm_intent(response_tool)
            logger.info("app_info 3 - Intent confirmation result: %s", confirmation)
            
            if "no" in confirmation.strip().lower():
                conversation.append({"role": "user", "content": user_input})
                conversation.append({"role": "assistant", "content": response_assistant})
                session['conversation'] = conversation
                logger.info("app_info 4 - User declined further recommendations.")
                return jsonify({"response": response_assistant}), 200
            else:
                # Fetch recommendations
                top_3_laptops, conversation_reco = fetch_recommendations(str(conversation), response_assistant)
                logger.info("app_info 5 - Fetched recommendations: %s", top_3_laptops)
                logger.info("app_info 5-1 - Fetched recommendations: %s", conversation_reco)
                session['top_3_laptops'] = "Fetched recommendations"
                recommendation=generate_recommendation(conversation_reco, response_assistant)
                conversation_reco.append({"role": "user", "content": user_input})
                conversation_reco.append({"role": "assistant", "content": recommendation})
                session['conversation'] = conversation_reco
                return jsonify({"response": recommendation }), 200
        else:
            logger.info("app_info 6 - Continuing conversation with existing recommendations.")
            # Continue conversation with recommendations
            conversation.append({"role": "user", "content": user_input})
            logger.debug("Updated conversation with user input: %s", conversation)
            response_asst_reco = get_chat_completions(conversation)
            logger.info("app_info 7 - Assistant response with recommendations: %s", response_asst_reco)
            
            if not handle_moderation_check(response_asst_reco):
                logger.warning("Recommendation response flagged by moderation: %s", response_asst_reco)
                return jsonify({"error": "Recommendation response flagged by moderation."}), 400
            
            conversation.append({"role": "user", "content": user_input})
            conversation.append({"role": "assistant", "content": response_asst_reco})
            session['conversation'] = conversation
            return jsonify({"response": response_asst_reco}), 200
    except Exception as e:
        logger.error("Error processing input: %s", str(e))
        return jsonify({"error": "Failed to process input."}), 500
    
@app.route('/api/end_conversation', methods=['POST'])
def end_conversation():
    logger.info("Ending the conversation.")
    try:
        # Check if session exists before clearing
        if 'conversation' in session or 'top_3_laptops' in session:
            session.clear()
            logger.debug("Session data cleared successfully.")
        else:
            logger.debug("Session already empty.")

        return jsonify({"status": "conversation ended", "content": "The conversation has been ended."}), 200
    except Exception as e:
        # Log full stack trace for debugging
        logger.error("Error ending conversation: %s", str(e), exc_info=True)
        return jsonify({
            "error": "Failed to end conversation.",
            "details": str(e)  
        }), 500

if __name__ == '__main__':
    logger.info("Starting the Flask application.")
    app.run(debug=True)
