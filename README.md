# Laptop-Shop-Assist-AI

## Table of Contents
1. [Introduction](#introduction)
2. [Problem Statement](#problem-statement)
3. [Objectives](#objectives)
4. [Approach](#approach)
5. [Features](#features)
6. [Technologies/Libraries Used](#technologieslibraries-used)
7. [Installation](#installation)
8. [Usage](#usage)
9. [API Endpoints](#api-endpoints)
10. [Project Structure](#project-structure)
11. [Conclusions](#conclusions)
12. [Acknowledgements](#acknowledgements)
13. [Glossary](#glossary)
14. [Contributing](#contributing)
15. [License](#license)
16. [Author](#author)

## Introduction
Laptop-Shop-Assist-AI is an intelligent chatbot designed to assist users in finding the best laptop based on their needs. It leverages OpenAI's GPT models to interact with users, gather their requirements, and provide personalized laptop recommendations.

## Problem Statement
With the rapid growth of technology and the overwhelming variety of laptop models available, customers often find it difficult to choose a device that matches their requirements. The lack of expert guidance or personalized recommendations can lead to suboptimal purchases, resulting in customer dissatisfaction. 

Laptop-Shop-Assist-AI addresses this challenge by offering an interactive chatbot that understands customer needs and provides tailored laptop recommendations.

## Objectives
- To create an AI-powered chatbot that interacts with users to gather their laptop requirements.
- To analyze user preferences and provide personalized laptop recommendations.
- To ensure a safe and user-friendly interface for seamless interaction.

## Approach
1. Develop a user-friendly interface for chatbot interaction.
2. Use OpenAI's GPT models to understand and process user queries.
3. Employ moderation APIs to ensure safe and appropriate user interactions.
4. Provide real-time, personalized recommendations based on the user’s inputs.
5. Enable deployment as a web-based application using Flask and Streamlit.

## Features
- **Interactive Chatbot**: Engages users in a conversation to understand their laptop requirements.
- **Personalized Recommendations**: Provides top 3 laptop recommendations based on user inputs.
- **Moderation**: Ensures safe and appropriate interactions using OpenAI's moderation API.
- **Web Interface**: User-friendly web interface built with Flask and Streamlit.

## Technologies/Libraries Used
- Python 3.11 or higher
- Flask
- Streamlit
- OpenAI GPT API
- Pandas
- Scikit-learn
- NLTK
- SpaCy
- Matplotlib

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
    - Create a `.env` file in the root directory.
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
```plaintext
Laptop-Shop-Assist-AI/
├── Git_Repo/
│   ├── __pycache__/
│   ├── .env
│   ├── .gitignore
│   ├── .ipynb_checkpoints/
│   ├── app.log
│   ├── app.py
│   ├── chatbot_page.py
│   ├── data/
│   │   ├── updated_laptop.csv
│   ├── design/
│   ├── dialogue.py
│   ├── notebooks/
│   │   ├── ShopAssistAI-2.0.ipynb
│   ├── openai_api.py
│   ├── README.md
│   ├── requirements.txt
│   ├── schema/
│   │   ├── config.py
│   ├── static/
│   ├── templates/
│   │   ├── laptop-shop-assistant.html
│   └── utils.py
```
## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## Acknowledgements

- The project reference course materieals from upGrads curriculm .
- The project references from presentation in upGrads module given by [Alankar Gupta](https://www.linkedin.com/in/alankar-gupta-898a9659/)
- The project references insights and inferences from presentation in upGrads live class given by [Dr. Apurva Kulkarni] (https://www.linkedin.com/in/dr-apurva-kulkarni-33a074189/)
- The project references from presentation in upGrads live class given by [Amit Pandey](https://www.linkedin.com/in/amitpandeyprofile/)

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Author
* [Arnab Bera]( https://www.linkedin.com/in/arnabbera-tech/ )
