# For handling file operations, JSON, and string manipulations
import json
from utils import extract_user_info
from schema.shopassist_schema import shopassist_custom_functions

# For interacting with the OpenAI API
import openai

# For retrying failed requests with exponential backoff
from tenacity import retry, wait_random_exponential, stop_after_attempt

# For loading environment variables from a .env file
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def initialize_conversation():
    '''
    Returns a list [{"role": "system", "content": system_message}]
    '''
    delimiter = "####"

    example_user_dict = {'GPU intensity': "high",
                        'Display quality':"high",
                        'Portability': "low",
                        'Multitasking': "high",
                        'Processing speed': "high",
                        'Budget': "150000"}

    example_user_req = {'GPU intensity': "_",
                        'Display quality': "_",
                        'Portability': "_",
                        'Multitasking': "_",
                        'Processing speed': "_",
                        'Budget': "_"}

    system_message = f"""
    You are an intelligent laptop gadget expert and your goal is to find the best laptop for a user.
    You need to ask relevant questions and understand the user profile by analysing the user's responses.
    You final objective is to fill the values for the different keys ('GPU intensity','Display quality','Portability','Multitasking','Processing speed','Budget') in the python dictionary and be confident of the values.
    These key value pairs define the user's profile.
    The python dictionary looks like this
    {{'GPU intensity': 'values','Display quality': 'values','Portability': 'values','Multitasking': 'values','Processing speed': 'values','Budget': 'values'}}
    The value for 'Budget' should contain a numerical value extracted from the user's response. Ignore any non-numerical characters and extract only the numerical portion.
    The values for all keys, except 'Budget', should be 'low', 'medium', or 'high' based on the importance of the corresponding keys, as stated by user.
    All the values in the example dictionary are only representative values.
    {delimiter}
    Here are some instructions around the values for the different keys. If you do not follow this, you'll be heavily penalised:
    - The values for all keys, except 'Budget', should strictly be either 'low', 'medium', or 'high' based on the importance of the corresponding keys, as stated by user.
    - The value for 'Budget' should always be extracted as a numerical value (integer or float), even if the user's input contains:
        - Numerical values as interger or float (e.g., 35000, , 77356.80 )
        - Numerical values as strings (e.g., "50000", "70,000", '1,40,000')
        - Currency symbols (e.g., "$50000", "40000 ₹", "€ 90000") or Currency words (e.g., "INR 40000", "56,000 USD", "50000 EURO")
    - Steps to handle the Budget value:
        - Extract the numerical portion from the input.
        - Ignore any non-numeric characters like currency symbols, commas, or words.
        - Convert the extracted number into a proper numerical type (e.g., integer or float).
    - 'Budget' value needs to be greater than or equal to 25000 INR. If the user says less than that, please mention that there are no laptops in that range.
    - Do not randomly assign values to any of the keys.
    - The values need to be inferred from the user's response.
    {delimiter}

    To fill the dictionary, you need to have the following chain of thoughts:
    Follow the chain-of-thoughts below and only output the final updated python dictionary for the keys as described in {example_user_req}. \n
    {delimiter}
    Thought 1: Ask a question to understand the user's profile and requirements. \n
    If their primary use for the laptop is unclear. Ask followup questions to understand their needs.
    You are trying to fill the values of all the keys {{'GPU intensity','Display quality','Portability','Multitasking','Processing speed','Budget'}} in the python dictionary by understanding the user requirements.
    Identify the keys for which you can fill the values confidently using the understanding. \n
    Remember the instructions around the values for the different keys.
    If the necessary information has been extracted, only then proceed to the next step. \n
    Otherwise, rephrase the question to capture their profile clearly. \n

    {delimiter}
    Thought 2: Now, you are trying to fill the values for the rest of the keys which you couldn't in the previous step.
    Remember the instructions around the values for the different keys.
    Ask questions you might have for all the keys to strengthen your understanding of the user's profile.
    If yes, move to the next Thought. If no, ask question on the keys whose values you are unsure of. \n
    It is a good practice to ask question with a sound logic as opposed to directly citing the key you want to understand value for.
    {delimiter}

    {delimiter}
    Thought 3: Check if you have correctly updated the values for the different keys in the python dictionary.
    If you are not confident about any of the values, ask clarifying questions.
    {delimiter}

    {delimiter}
    Here is a sample conversation between the user and assistant:
    User: "Hi, I am an editor."
    Assistant: "Great! As an editor, you likely require a laptop that can handle demanding tasks. Hence, the laptop should have high multitasking capability. You would also need a high end display for better visuals and editing. May I know what kind of work do you primarily focus on? Are you more involved in video editing, photo editing, or both? Understanding the specific type of editing work will help me tailor my recommendations accordingly. Let me know if my understanding is correct until now."
    User: "I primarily work with After Effects."
    Assistant: "Thank you for providing that information. Working with After Effects involves working with graphics, animations, and rendering, which will require high GPU. Do you work with high-resolution media files, such as 4K videos or RAW photos? Understanding your file sizes will help determine the storage capacity and processing power needed."
    User: "Yes, sometimes I work with 4K videos as well."
    Assistant: "Thank you for the information. Processing 4K vidoes will require a good processor and high GPU. I think we have already determined earlier that you need a high GPU. To ensure I have a complete understanding of your needs, I have one more question: Are you frequently on the go and require a laptop that is lightweight and easy to carry, or do you primarily work from a stationary location?"
    User: "Yes, sometimes I travel but do not carry my laptop."
    Assistant:"Could you kindly let me know your budget for the laptop? This will help me find options that fit within your price range while meeting the specified requirements."
    User: "my max budget is 1.5lakh inr"
    Assistant: "{example_user_dict}"
    {delimiter}

    Start with a short welcome message and encourage the user to share their requirements.
    """
    
    conversation = [{"role": "system", "content": system_message}]

    return conversation


@retry(
    wait=wait_random_exponential(min=1, max=10),  # Retry interval - max wait time to 10 seconds
    stop=stop_after_attempt(2)  # Limit retries to 2 attempts
)
def get_chat_completions(input, json_format=False):
    """
    This function defines a Chat Completions API call using OpenAI's GPT-4o-mini model.

    Parameters:
    - input (list): A list of dictionaries representing the chat messages provided to the model. 
      Each dictionary typically includes keys like "role" (e.g., 'system', 'user', or 'assistant') and "content" (the actual message).
    - json_format (bool): A flag to specify whether the output should be in JSON format. Default is False.

    Functionality:
    1. Uses the GPT-4o-mini model to generate chat completions based on the input.
    2. If `json_format` is True:
        - Appends a system instruction to the input to ensure the output is formatted as a JSON object.
        - Calls the OpenAI API with the response format set to `json_object`.
        - Attempts to parse the API response into a Python dictionary using `json.loads()`. 
        - Handles any `JSONDecodeError` gracefully by printing an error message if the parsing fails.
    3. If `json_format` is False:
        - Calls the OpenAI API without enforcing JSON output.
        - Directly returns the raw text content of the model's response.
    
    API Call Parameters:
    - `model`: Specifies the GPT-4o-mini model to use for chat completion.
    - `seed`: Sets a deterministic random seed for reproducibility.
    - `max_completion_tokens`: Specifies the maximum number of tokens in the output to control the response length.
    - `temperature`: Controls the randomness of the response (lower values like 0.3 produce more deterministic results).
    - `tools`: Can include specific functions or tools for more specialized responses, such as extracting preferences.

    Returns:
    - If `json_format` is True: Returns a Python dictionary parsed from the model's JSON output.
    - If `json_format` is False: Returns the raw text content from the model's response.

    Example usage:
    - To get a formatted JSON response: `get_chat_completions(input, json_format=True)`
    - To get raw text: `get_chat_completions(input, json_format=False)`
    """
    
    model = "gpt-4o-mini"
    system_message_json_output = """ \n Output format : <<. Return the final result or output in JSON format. Return only the extracted Python dictionary.>> """
    
    if json_format:
        # Append system instruction for JSON output format
        input[0]["content"] += system_message_json_output
        # API call with json_object response format
        chat_completion_json = openai.chat.completions.create(
            model=model,
            messages=input,
            response_format={"type": "json_object"},
            n=1,
            seed=1234,
            max_completion_tokens=500,
            temperature=0.3
        )
        try:
            # Parse the JSON output from the response
            output = json.loads(chat_completion_json.choices[0].message.content)
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
    else:
        # API call without enforcing JSON output
        chat_completion_json = openai.chat.completions.create(
            model=model,
            messages=input,
            n=1,
            seed=2345,
            max_completion_tokens=500,
            temperature=0.3
        )
        # Extract raw text content from the response
        output = chat_completion_json.choices[0].message.content

    return output



@retry(
    wait=wait_random_exponential(min=1, max=10),  # Retry interval - max wait time to 10 seconds
    stop=stop_after_attempt(2)  # Limit retries to 2 attempts
)
def get_chat_completions_tool(input,func_name=shopassist_custom_functions):
    """
    Generate chat completions using OpenAI's GPT-4o-mini model and return the result in JSON format.

    Parameters:
    - input (list): A list of dictionaries representing the chat messages for the model prompt, typically containing keys such as "role" and "content".
    - tool_func (callable): A function or set of functions that are passed for tool handling, which can be used by the model. Default is 'shopassist_custom_functions'.

    Returns:
    - dict: If a function call is detected in the response, a dictionary with the function name and arguments is returned.
    - dict: If no function call is detected, an error message is returned in the form of a dictionary.
    - None: If there is an error during the API call, such as JSON decoding failure, None is returned.
    """

    system_message = """
    You are a helpful assistant for a shopping recommendation system. Based on the user's input, you need to extract their preferences regarding laptops and suggest the best options based on the criteria provided. Your tasks include:
    
    1. Extracting key preferences from the user's input for GPU intensity, display quality, portability, multitasking, and processing speed.
    2. If the user opts to include a budget, you will also extract and consider the budget to narrow down the options.
    3. Use the provided 'shopassist_custom_functions' to guide your recommendations, ensuring the response is tailored to the user's needs.
    4. You will return the preferences extracted from the user's input, including the budget if provided.
    
    Do not make any assumptions about the user’s preferences; only extract and return the exact information they provide.
    """
    model = "gpt-4o-mini"
    final_message = [{ "role": "system", "content": system_message },{ "role": "user", "content": input }]
    tools = [{
        'type':'function',
        "function":{
            'name': func_name[0]['name'],
            'description': func_name[0]['description'],
            'parameters': func_name[0]['parameters']
        }
    }]
    try:
        chat_completion_json = openai.chat.completions.create(
            model=model,
            messages=final_message,
            n=1,
            seed=1234,
            max_completion_tokens=500,
            temperature=0.3,
            tools=tools,
            tool_choice="auto"
        )
        response = chat_completion_json.choices[0].message
        tool_call = response.tool_calls[0]
        tool_name = tool_call.function.name
        arguments_str = tool_call.function.arguments
        # Parse the arguments string into a dictionary
        arguments = json.loads(arguments_str)
        if tool_name == tool_name:
            # Pass the extracted arguments to the function dynamically
            output = extract_user_info(
                arguments.get('GPU_intensity', ''),
                arguments.get('Display_quality', ''),
                arguments.get('Portability', ''),
                arguments.get('Multitasking', ''),
                arguments.get('Processing_speed', ''),
                arguments.get('Budget', 0)
            )
            return output
        else:
            return {"error": f"Unexpected tool call: {tool_name}"}
            
    except Exception as e:
        print(f"Error during API call: {e}")
        return None


# Define a function called moderation_check that takes user_input as a parameter.
def moderation_check(user_input):
    """
    Perform moderation check on user input using the OpenAI API.

    Parameters:
    - user_input (str): The text input to be checked for moderation.

    Returns:
    - str: "Flagged" if the input is flagged by the moderation system,
           "Not Flagged" otherwise.
    """
    # Call the OpenAI API to perform moderation on the user's input.
    model= "omni-moderation-latest"
    response=openai.moderations.create(
        model=model,
        input=user_input
    )  
    # Extract the moderation result from the API response.
    moderation_output=response.results[0].flagged
    # Check if the input was flagged by the moderation system. If flagged, return "Flagged" else return "Not Flagged"
    if moderation_output :
        return "Flagged"
    else :
        return "Not Flagged"


def intent_confirmation_layer(response_assistant):
    """
    This function takes in a response from an AI assistant and evaluates it based on specific criteria.

    Args:
    - response_assistant (str): The input text containing user requirements captured through 6 keys:
      'GPU intensity', 'Display quality', 'Portability', 'Multitasking', 'Processing speed', and 'Budget'.

    Returns:
    - dict: A JSON-formatted dictionary with keys 'result' and, if applicable, 'reason'.
      - 'result' (str): Either 'Yes' or 'No', indicating if the input meets the criteria.
      - 'reason' (str, optional): If 'result' is 'No', this key provides a reason for the evaluation.

    Key Instructions:
    1. The input should include values for the specified keys.
    2. Allowed values for 'GPU intensity', 'Display quality', 'Portability', 'Multitasking', and 'Processing speed'
       are 'low', 'medium', and 'high'.
    3. 'Budget' should only have a numerical value.
    4. Only a one-word string in JSON format ('Yes' or 'No') should be output at the key 'result'.
    5. If 'result' is 'No', include the reason in the key 'reason'.
    6. Use the AI model 'GPT-4o-mini' to process the evaluation.

    Example:
    >>> input_text = "{'GPU intensity': 'high', 'Display quality': 'medium', 'Portability': 'low',
                      'Multitasking': 'medium', 'Processing speed': 'high', 'Budget': 1200}"
    >>> intent_confirmation_layer(input_text)
    {'result': 'Yes'}

    Note: Modify the input text to match the expected format before passing it to this function.
    """
    delimiter = "####"

    allowed_values = {"low","medium","high"}
    system_message = f"""
        You are a senior evaluator who has an eye for detail. The input text will contain a user requirement captured through 6 keys.
        You are provided an input. You need to evaluate step by step if the input text has the following keys:
        {{
        "GPU intensity" : "values",
        "Display quality" : "values",
        "Portability" : "values",
        "Multitasking" : "values",
        "Processing speed" : "values",
        "Budget" : "number"
        }}
        You need to evaluate the input step by step to ensure it adheres to the following criteria:
        
        {delimiter} 
        Step 1 - Budget:
        1. Extract the value of 'Budget' from the input text.
        2. If the budget contains non-numeric characters (e.g., currency symbols, spaces, commas, or words), clean it by:
        - Removing all non-numeric characters, such as ₹, $, commas, spaces, or text like 'INR' or 'USD'.
        - Converting the cleaned number into a numerical format (integer or float).
        3. Validate the numerical value:
        - Ensure the budget is greater than or equal to 25000 (default currency is INR).
        - If the budget is less than 25000, return: "There are no laptops in that price range below 25000 INR."
        4. If the budget is valid, proceed to the next step.
        
        {delimiter}
        Step 2 - 'GPU intensity', 'Display quality', 'Portability' :
        - The keys 'GPU intensity', 'Display quality', 'Portability' must have values from this set: {allowed_values}.
        - Ensure case-insensitive matching for these values (e.g., 'Low', 'low', 'LOW' are all valid).
        - If any value is outside this set, output: `{{"result": "No", "reason": "The values for <key> are outside the allowed set."}}`.

        {delimiter}
        Step 3 - 'Multitasking', and 'Processing speed' :
        - The keys 'Multitasking', and 'Processing speed' must have values from this set: {allowed_values}.
        - Ensure case-insensitive matching for these values (e.g., 'Low', 'low', 'LOW' are all valid).
        - If any value is outside this set, output: `{{"result": "No", "reason": "The values for <key> are outside the allowed set."}}`.
        
        {delimiter} 
        Output Rules:
        1. If all keys are valid and the budget is >= 25000, output: `{{"result": "Yes"}}`.
        2. If any key is invalid or the budget is less than 25000, output: 
        - `{{"result": "No", "reason": "<explanation>"}}`.
        {delimiter}
        Only output a one-word string ('Yes' or 'No') at the key 'result' in JSON format, with an optional 'reason' if the result is 'No'.
        """
    
    model="gpt-4o-mini"
    messages=[
        { "role" : "system", "content" : system_message },
        { "role" : "user", "content" : f"""Here is the input: {response_assistant}"""  }
    ]
    chat_completion_json=openai.chat.completions.create(
        model=model,
        messages=messages,
        n=1,
        seed=3456,
        response_format={"type": "json_object"},
        max_completion_tokens=500,
        temperature=0
    )
    response=chat_completion_json.choices[0].message.content
    try :
        json_output=json.loads(response)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:",e)

    return json_output
        
    

def initialize_conv_reco(products):
    """
    Initializes a conversation recommendation system for a laptop gadget expert.

    Parameters:
    - products (list): A list of products to be included in the user's profile.

    Returns:
    - conversation (list): A list containing initial system and user messages for the conversation.

    Description:
    This function sets up a conversation recommendation system for an intelligent laptop gadget expert.
    The system message provides guidance on how to respond to user queries based on the product catalog.
    It instructs to summarize each laptop's major specifications and price, starting with the most expensive.
    The user message confirms the list of products included in the user's profile.

    Example:
    >>> products = ['Laptop A', 'Laptop B', 'Laptop C']
    >>> initialize_conv_reco(products)
    [{'role': 'system', 'content': 'You are an intelligent laptop gadget expert and you are tasked with the objective to solve the user queries about any product from the catalogue in the user message. You should keep the user profile in mind while answering the questions.\n\nStart with a brief summary of each laptop in the following format, in decreasing order of price of laptops:\n1. <Laptop Name> : <Major specifications of the laptop>, <Price in Rs>\n2. <Laptop Name> : <Major specifications of the laptop>, <Price in Rs>\n\n'},
    {'role': 'user', 'content': " These are the user's products: ['Laptop A', 'Laptop B', 'Laptop C']"}]
    """
    system_message = f"""
    You are an intelligent laptop gadget expert and you are tasked with the objective to \
    solve the user queries about any product from the catalogue in the user message \
    You should keep the user profile in mind while answering the questions.\

    Start with a brief summary of each laptop in the following format, in decreasing order of price of laptops:
    1. <Laptop Name> : <Major specifications of the laptop>, <Price in Rs>
    2. <Laptop Name> : <Major specifications of the laptop>, <Price in Rs>

    """
    user_message = f""" These are the user's products: {products}"""
    conversation = [{"role": "system", "content": system_message },
                    {"role":"user","content":user_message}]
    return conversation


