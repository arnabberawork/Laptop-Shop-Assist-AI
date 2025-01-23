import pandas as pd
import os, ast, json

def iterate_llm_response(funct, debug_response, num=10, *params):
    """
    Calls a specified function repeatedly and prints the results.

    This function is designed to test the consistency of a response from a given function.
    It calls the function multiple times (default is 10) and prints out the iteration count,
    the function's response(s).

    Args:
        funct (function): The function to be tested. This function should accept a single argument
                          and return the response value(s).
        debug_response (dict): The input argument to be passed to 'funct' on each call.
        num (int, optional): The number of times 'funct' will be called. Defaults to 10.
        *params: Additional parameters that may be passed to 'funct'.

    Returns:
        This function only returns the results to the console.

    Example usage:
        Test the consistency of responses from 'intent_confirmation_layer' function
        iterate_llm_response(get_chat_completions, messages)
    """
    print(f"Input Prompt : \n{debug_response} ")
    print("===" * 30)
    i = 0  # Initialize counter
    while i < num:
        print(f" Start Execution - Iteration Number : {i + 1} ")
        # Call the function with debug_response and params if any
        response = funct(debug_response, *params)
        print(response)
        print("===" * 30)
        
        # Increment the counter
        i += 1


def extract_user_info(GPU_intensity, Display_quality, Portability, Multitasking, Processing_speed, Budget):
    """

    Parameters:
    GPU_intensity (str): GPU intensity required by the user.
    Display_quality (str): Display quality required by the user.
    Portability (str): Portability required by the user.
    Multitasking (str): Multitasking capability required by the user.
    Processing_speed (str): Processing speed required by the user.
    Budget (int): Budget of the user.

    Returns:
    dict: A dictionary containing the extracted information.
    """
    return {
        "GPU intensity": GPU_intensity,
        "Display quality": Display_quality,
        "Portability": Portability,
        "Multitasking": Multitasking,
        "Processing speed": Processing_speed,
        "Budget": Budget
    }


def find_match_score(input1, input2, debug=False):
    match_score = 0  # Initialize match score to 0
     # Check if input1 is a string and convert it to a dictionary if needed
    if isinstance(input1, str):
        input1_dict = ast.literal_eval(input1)
    else:
        input1_dict = input1  # If already a dictionary, use it directly
    
    # Check if input2 is a string and convert it to a dictionary if needed
    if isinstance(input2, str):
        input2_dict = ast.literal_eval(input2)
    else:
        input2_dict = input2  # If already a dictionary, use it directly
    
    # Define the hierarchy of the values (None will be treated as -1, and 'low', 'medium', 'high' will have respective values)
    hierarchy = {None: -1, 'low': 1, 'medium': 2, 'high': 3}
    
    # Iterate through each key-value pair in the first dictionary
    for key, value in input1_dict.items():
        if key != 'Budget':  # Skip the 'Budget' key for this match scoring logic
            # Calculate the difference between the values in input1_dict and input2_dict based on hierarchy
            if (hierarchy.get(input2_dict.get(key, None), -1) - hierarchy.get(value, -1)) >= 0:
                match_score += 1  # If input2 value is higher in the hierarchy, increment match score
                if debug:
                    # If debugging, print the status of the match and corresponding values
                    print(f"Pass")
                    print(f"Asked {key} : {hierarchy.get(value, -1)} - {value} ; Laptop's {key}: {hierarchy.get(input2_dict.get(key, None))} - {input2_dict.get(key, None)}")
            else:
                if debug:
                    # If the condition fails, print debug information
                    print("Fail")
                    print(f"Asked {key} : {hierarchy.get(value, -1)} - {value} ; Laptop's {key}: {hierarchy.get(input2_dict.get(key, None))} - {input2_dict.get(key, None)}")
        else:
            if debug:
                # If 'Budget' is encountered, print debug info
                print("Fail")
                print(f"Asked {key} : {hierarchy.get(value, -1)} - {value}")
        
        # If debugging is enabled, print the total match score after each iteration
        if debug:
            print(f"Total Match Score : {match_score}")
    
    return match_score  # Return the final match score

def compare_laptops_with_user(user_req_string):
    """
    Compares laptops based on user requirements and returns the top 3 matching laptops in JSON format.

    Parameters:
    - user_req_string (str): A string representing user requirements in JSON format.
    - {{{'GPU intensity': 'high',
         'Display quality': 'high',
         'Portability': 'low',
         'Multitasking': 'high',
         'Processing speed': 'medium',
         'Budget': 80000}}}

    Returns:
    - str: A JSON string containing information about the top 3 matching laptops based on user requirements.
    """
    
    script_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(script_dir, "data/updated_laptop.csv")
    user_laptop_df = pd.read_csv(file_path)
    
    # Format price column
    user_laptop_df['Price']=user_laptop_df['Price'].str.replace(',','').astype('float64')
    user_laptop_df=user_laptop_df[ user_laptop_df['Price']<=user_req_string['Budget'] ]
    user_laptop_df = user_laptop_df.reset_index(drop=True)

    # Extracting user requirements from the input string (assuming it's a dictionary)
    # Create a scoring mechanism for comparing the laptops in the laptop descriptions against the user_req_string containing the user's persona
    user_laptop_df['Score'] = user_laptop_df['laptop_feature'].apply(lambda x : find_match_score(user_req_string, x, debug=False))    
    # Sorting laptops by score in descending order and selecting the top 3 products
    top_laptops=user_laptop_df.sort_values(by=['Score','Price'],ascending=[False,True]).head(3)
    # top_laptops
    top_laptops_json=top_laptops.to_json(orient='records') # Converting the top laptops DataFrame to JSON string
    
    return top_laptops_json


def recommendation_validation(laptop_recommendation):
    """
    Validate a list of laptop recommendations based on a score threshold.

    Parameters:
    - laptop_recommendation (str): JSON string containing a list of laptop recommendations,
      each with a 'Score' key representing its rating.

    Returns:
    - list: A filtered list of laptop recommendations where each item has a 'Score' greater than 2.
    """
    #laptop_recommendation=top_3_laptops
    laptop_data=json.loads(laptop_recommendation) # convert JSON string to Python objects
    validated_data=[]
    for product in laptop_data :
        if product['Score']>2 :
            validated_data.append(product)

    return validated_data