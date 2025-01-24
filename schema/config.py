import os

# Set the dummy environment variable in the code
os.environ['FLASK_SECRET_KEY'] = 'dummy_secret_key_for_testing'

class Config:
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')  # Will get the value from the environment
