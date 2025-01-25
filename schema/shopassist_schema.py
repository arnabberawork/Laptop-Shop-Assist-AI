# `shopassist_custom_functions` - OpenAI Function Calling Configuration
'''
This code defines a custom function for leveraging OpenAI's function calling feature.
The function, named 'extract_user_info', is designed to extract structured information from user input 
regarding their laptop preferences to guide personalized recommendations.

The 'parameters' section defines the expected input structure, which includes the following keys:
  - 'GPU_intensity': Indicates the importance of the laptop's GPU capability, with possible values of 'low', 'medium', or 'high'.
  - 'Display_quality': Represents the preferred display quality, with possible values of 'low', 'medium', or 'high'.
  - 'Portability': Specifies the required portability level of the laptop, with possible values of 'low', 'medium', or 'high'.
  - 'Multitasking': Describes the importance of multitasking capabilities, with values 'low', 'medium', or 'high'.
  - 'Processing_speed': Represents the desired processing speed of the laptop, with values 'low', 'medium', or 'high'.
  - 'Budget': Specifies the user's budget as an integer.

This function can be used to extract and interpret structured user preferences to guide AI models in providing laptop recommendations.
'''

shopassist_custom_functions = [
    {
        'name': 'extract_user_info',
        'description': 'Get the user laptop information from the body of the input text',
        'parameters': {
            'type': 'object',
            'properties': {
                'GPU_intensity': {
                    'type': 'string',
                    'description': 'GPU intensity of the user requested laptop. The values  are ''low'', ''medium'', or ''high'' based on the importance of the corresponding keys, as stated by user'
                },
                'Display_quality': {
                    'type': 'string',
                    'description': 'Display quality of the user requested laptop. The values  are ''low'', ''medium'', or ''high'' based on the importance of the corresponding keys, as stated by user'
                },
                'Portability': {
                    'type': 'string',
                    'description': 'The portability of the user requested laptop. The values  are ''low'', ''medium'', or ''high'' based on the importance of the corresponding keys, as stated by user'
                },
                'Multitasking': {
                    'type': 'string',
                    'description': 'The multitasking abiliy of the user requested laptop. The values  are ''low'', ''medium'', or ''high'' based on the importance of the corresponding keys, as stated by user'
                },
                'Processing_speed': {
                    'type': 'string',
                    'description': 'The processing speed of the user requested laptop.  The values  are ''low'', ''medium'', or ''high'' based on the importance of the corresponding keys, as stated by user'
                },
                'Budget': {
                    'type': 'integer',
                    'description': 'The budget of the user requested laptop. The values are integers.'
                }
            }
        }
    }
]
