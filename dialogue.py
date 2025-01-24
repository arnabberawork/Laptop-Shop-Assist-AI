from openai_api import initialize_conversation, get_chat_completions, get_chat_completions_tool, moderation_check, intent_confirmation_layer, initialize_conv_reco
from utils import compare_laptops_with_user, recommendation_validation
from schema.shopassist_schema import shopassist_custom_functions
from IPython.display import display
import logging

# Setup logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.StreamHandler(),
                        logging.FileHandler('app.log', encoding='utf-8', mode='a')  # Logs to app.log file
                    ])
logger = logging.getLogger(__name__)



def initialize_conversation_system():
    """
    Initializes the conversation system and retrieves the assistant's introduction.
    """
    conversation = initialize_conversation()
    introduction = get_chat_completions(conversation)
    return conversation, introduction


def handle_moderation_check(input_text):
    """
    Checks if the input text is flagged by the moderation system.
    """
    moderation = moderation_check(input_text)
    if moderation == 'Flagged':
        return False
    return True


def process_user_input(conversation, user_input):
    """
    Processes user input and updates the conversation.
    """
    conversation.append({"role": "user", "content": user_input})
    response_assistant = get_chat_completions(conversation)
    return response_assistant


def confirm_intent(response_tool):
    """
    Confirms the user's intent based on the response tool's output.
    """
    confirmation = intent_confirmation_layer(response_tool)
    return confirmation.get('result')


def fetch_recommendations(conversation_reco, response_tool):
    """
    Fetches laptop recommendations and updates the conversation.
    """
    logger.info("dialogue_info 1 - Fetching laptop recommendations. Response: %s and Type: %s", conversation_reco, type(conversation_reco))
    response = get_chat_completions_tool(response_tool, func_name=shopassist_custom_functions)
    logger.info("dialogue_info 2 - Fetching laptop recommendations. Response: %s and Type: %s", response, type(response))
    top_3_laptops = compare_laptops_with_user(response)
    validated_reco = recommendation_validation(top_3_laptops)
    conversation_reco = initialize_conv_reco(validated_reco)
    return top_3_laptops, conversation_reco


def generate_recommendation(conversation_reco, user_profile):
    """
    Generates recommendations based on the validated laptop list.
    """
    conversation_reco.append({"role": "user", "content": "This is my user profile" + str(user_profile)})
    recommendation = get_chat_completions(conversation_reco)
    return recommendation


def dialogue_mgmt_system():
    """
    Manages a conversational system between a user and an assistant to recommend laptops.

    This function initializes the conversation, retrieves the introduction, handles user input,
    performs moderation checks, and manages the recommendation process based on user interactions.

    Returns:
        None
    """

    conversation = initialize_conversation()

    introduction = get_chat_completions(conversation)

    display(introduction + '\n')

    top_3_laptops = None

    user_input = ''

    while(user_input != "exit"):

        user_input = input("")

        moderation = moderation_check(user_input)
        if moderation == 'Flagged':
            display("Sorry, this message has been flagged. Please restart your conversation.")
            break

        if top_3_laptops is None:

            conversation.append({"role": "user", "content": user_input})

            response_assistant = get_chat_completions(conversation)
            moderation = moderation_check(response_assistant)
            if moderation == 'Flagged':
                display("Sorry, this message has been flagged. Please restart your conversation.")
                break


            print(f"Input of intent confirmation : {response_assistant}")
            response_tool = get_chat_completions_tool(response_assistant,func_name=shopassist_custom_functions)
            confirmation = intent_confirmation_layer(response_tool)

            print("Intent Confirmation Yes/No:",confirmation.get('result'))

            if "No" in confirmation.get('result'):
                conversation.append({"role": "assistant", "content": str(response_assistant)})
                print("\n" + str(response_assistant) + "\n")

            else:
                print("\n" + str(response_assistant) + "\n")
                print('\n' + "Variables extracted!" + '\n')

                response = get_chat_completions_tool(response_assistant,func_name=shopassist_custom_functions)

                print("Thank you for providing all the information. Kindly wait, while I fetch the products: \n")
                top_3_laptops = compare_laptops_with_user(response)

                print("top 3 laptops are", top_3_laptops)

                validated_reco = recommendation_validation(top_3_laptops)

                conversation_reco = initialize_conv_reco(validated_reco)

                conversation_reco.append({"role": "user", "content": "This is my user profile" + str(response)})

                recommendation = get_chat_completions(conversation_reco)

                moderation = moderation_check(recommendation)
                if moderation == 'Flagged':
                    display("Sorry, this message has been flagged. Please restart your conversation.")
                    break

                conversation_reco.append({"role": "assistant", "content": str(recommendation)})

                print(str(recommendation) + '\n')
        else:
            conversation_reco.append({"role": "user", "content": user_input})

            response_asst_reco = get_chat_completions(conversation_reco)

            moderation = moderation_check(response_asst_reco)
            if moderation == 'Flagged':
                print("Sorry, this message has been flagged. Please restart your conversation.")
                break

            print('\n' + response_asst_reco + '\n')
            conversation.append({"role": "assistant", "content": response_asst_reco})

    return conversation        


if __name__ == "__main__":
    conversation = dialogue_mgmt_system()
    print(conversation)