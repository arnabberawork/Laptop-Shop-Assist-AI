# Laptop-Shop-Assist-AI

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [API Endpoints](#api-endpoints)
6. [Project Structure](#project-structure)
7. [Contributing](#contributing)
8. [License](#license)

## Introduction
Laptop-Shop-Assist-AI is an intelligent chatbot designed to assist users in finding the best laptop based on their needs. It leverages OpenAI's GPT models to interact with users, gather their requirements, and provide personalized laptop recommendations.

## Features
- **Interactive Chatbot**: Engages users in a conversation to understand their laptop requirements.
- **Personalized Recommendations**: Provides top 3 laptop recommendations based on user inputs.
- **Moderation**: Ensures safe and appropriate interactions using OpenAI's moderation API.
- **Web Interface**: User-friendly web interface built with Flask and Streamlit.

## Installation
### Prerequisites
- Python 3.11 or higher
- pip (Python package installer)

### Steps
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/Laptop-Shop-Assist-AI.git
    cd Laptop-Shop-Assist-AI
    ```

2. Create a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    - Create a [.env](http://_vscodecontentref_/1) file in the root directory.
    - Add your OpenAI API key:
        ```
        OPENAI_API_KEY=your_openai_api_key
        ```

## Usage
### Running the Flask Application
1. Start the Flask server:
    ```sh
    python app.py
    ```

2. Open your web browser and navigate to `http://127.0.0.1:5000`.

### Running the Streamlit Application
1. Start the Streamlit app:
    ```sh
    streamlit run chatbot_page.py
    ```

2. Open your web browser and navigate to the URL provided by Streamlit.

## API Endpoints
- **`GET /api/start_conversation`**: Initializes a new conversation.
- **`POST /api/process_input`**: Processes user input and returns the assistant's response.
- **`POST /api/end_conversation`**: Ends the current conversation.

## Project Structure
Laptop-Shop-Assist-AI/
├── Git_Repo/
│   ├── __pycache__/
│   ├── .env
│   ├── .gitignore
│   ├── .ipynb_checkpoints/
│   ├── [app.log](http://_vscodecontentref_/2)
│   ├── [app.py](http://_vscodecontentref_/3)
│   ├── [chatbot_page.py](http://_vscodecontentref_/4)
│   ├── data/
│   │   ├── updated_laptop.csv
│   ├── design/
│   ├── [dialogue.py](http://_vscodecontentref_/5)
│   ├── notebooks/
│   │   ├── ShopAssistAI-2.0.ipynb
│   ├── [openai_api.py](http://_vscodecontentref_/6)
│   ├── [README.md](http://_vscodecontentref_/7)
│   ├── [requirements.txt](http://_vscodecontentref_/8)
│   ├── schema/
│   │   ├── config.py
│   ├── static/
│   ├── templates/
│   │   ├── laptop-shop-assistant.html
│   └── [utils.py](http://_vscodecontentref_/9)

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
