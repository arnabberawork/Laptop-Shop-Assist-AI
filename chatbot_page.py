import streamlit as st
import requests  # To interact with the Flask API

# Title of the chatbot page
st.title("Laptop Shopping Assistant")

# Initialize session state variables if they don't exist
if "conversation_started" not in st.session_state:
    st.session_state.conversation_started = False
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "conversation_reco" not in st.session_state:
    st.session_state.conversation_reco = []
if "top_3_laptops" not in st.session_state:
    st.session_state.top_3_laptops = None
if "user_input_placeholder" not in st.session_state:
    st.session_state.user_input_placeholder = ""

# Function to start the conversation
def start_conversation():
    try:
        response = requests.post("http://127.0.0.1:5000/api/start_conversation")
        if response.status_code == 200:
            st.session_state.conversation_started = True
            st.session_state.conversation_history = response.json().get("conversation_history", [])
            st.session_state.conversation = response.json().get("conversation", [])
        else:
            st.error("Failed to start conversation. Please try again.")
    except Exception as e:
        st.error(f"Error calling the start conversation API: {str(e)}")

# Custom button styles
start_button_style = """
    <style>
        .start-button {
            background-color: #4CAF50;  /* Green color for start button */
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 16px;
            font-weight: bold;
            border: none;
            cursor: pointer;
        }
        .start-button:hover {
            background-color: #45a049;  /* Darker green on hover */
        }
    </style>
"""
send_button_style = """
    <style>
        .send-button {
            background-color: #0000FF;  /* Deep blue color */
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 16px;
            font-weight: bold;
            border: none;
            cursor: pointer;
        }
        .send-button:hover {
            background-color: #0000CC;  /* Darker blue on hover */
        }
    </style>
"""
end_button_style = """
    <style>
        .end-button {
            background-color: #FF6347;  /* Red color for end button */
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 16px;
            font-weight: bold;
            border: none;
            cursor: pointer;
        }
        .end-button:hover {
            background-color: #FF4500;  /* Darker red on hover */
        }
    </style>
"""

# Inject custom styles into the Streamlit app
st.markdown(start_button_style, unsafe_allow_html=True)
st.markdown(send_button_style, unsafe_allow_html=True)
st.markdown(end_button_style, unsafe_allow_html=True)

# Handle "Start Conversation"
if not st.session_state.conversation_started:
    # Render "Start Conversation" button with custom style using HTML
    if st.button('Start Conversation', key="start_button"):
        start_conversation()
else:
    # Once the conversation has started, render the conversation interface
    for msg in st.session_state.conversation_history:
        if msg["role"] == "bot":
            st.markdown(f"**Bot**: {msg['content']}")
        else:
            st.markdown(f"**User**: {msg['content']}")

    # User input box and submit icon
    user_input = st.text_input("You: ", key="user_input", placeholder="Type your message here...", value=st.session_state.user_input_placeholder)

    # Send button
    col1, col2 = st.columns([8, 1])
    with col2:
        send_button = st.button("➤")

    if send_button and user_input.strip():
        # Add user message to both conversation history and conversation
        user_message = {"role": "user", "content": user_input}
        st.session_state.conversation_history.append(user_message)
        st.session_state.conversation.append(user_message)

        # Define the API URL
        api_url = "http://127.0.0.1:5000/api/chat"

        # Define headers (if needed for JSON content type or authentication)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",  # Accept JSON response
            # "Authorization": "Bearer <Your-Token-Here>",  # If using authentication
        }

        # Prepare the payload with conversation data
        payload = {
            "user_input": user_input,
            "conversation": st.session_state.conversation,  # Current conversation context
            "conversation_history": st.session_state.conversation_history,  # Full conversation history
            "conversation_reco": st.session_state.conversation_reco,  # Recommendation data (if applicable)
            "top_3_laptops": st.session_state.top_3_laptops,  # Laptop recommendations (if any)
        }

        try:
            # Make the POST request to the API
            response = requests.post(api_url, json=payload, headers=headers)

            # Check if the response was successful (status code 200)
            if response.status_code == 200:
                response_data = response.json()

                # Get the bot's message from the response
                bot_message = {"role": "bot", "content": response_data.get("bot_response", "Sorry, I didn't understand.")}

                # Update both conversation history and conversation with bot's response
                st.session_state.conversation_history.append(bot_message)
                st.session_state.conversation.append(bot_message)

                # Additional data (if applicable)
                st.session_state.conversation_reco = response_data.get("conversation_reco", [])
                st.session_state.top_3_laptops = response_data.get("top_3_laptops", None)

            else:
                # Handle unexpected status codes from the server
                st.error(f"Error: Received unexpected status code {response.status_code} from the server.")
                st.error(response.text)

        except requests.exceptions.RequestException as e:
            # Handle any network-related errors or issues with the API request
            st.error(f"Error making the request: {str(e)}")

        # Clear the text input after sending the message
        st.session_state.user_input_placeholder = ""

    # Display the entire conversation history
    if st.session_state.conversation_history:
        for msg in st.session_state.conversation_history:
            if msg["role"] == "bot":
                st.markdown(f"**Bot**: {msg['content']}")
            else:
                st.markdown(f"**User**: {msg['content']}")

    # Center the "End Conversation" button with custom style
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button("End Conversation"):
        st.session_state.conversation_history = []
        st.session_state.conversation_started = False
        st.session_state.conversation_reco = []
        st.session_state.top_3_laptops = None
        st.session_state.conversation = []
    st.markdown("</div>", unsafe_allow_html=True)
