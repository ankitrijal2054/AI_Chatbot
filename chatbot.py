import requests
import json

# Load API keys from api_key.json
with open("api_key.json", "r") as api_file:
    api = json.load(api_file)

OPENROUTER_API_KEY = api["OPENROUTER_API_KEY"]

if not OPENROUTER_API_KEY:
    raise ValueError("Missing OpenRouter API Key. Set OPENROUTER_API_KEY in environment variables.")

def chat_with_ai(query):
    """Send query to DeepSeek model via OpenRouter API and return response"""
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }
        
        context = '''Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

Ankit Rijal
Dallas, Texas | (817) 703-8670 | ankitrijal2054@gmail.com | LinkedIn | GitHub |Portfolio

PROFILE
Aspiring Machine Learning Engineer with a strong software development background and
experience in building scalable applications across desktop, web, and mobile platforms.
Proficient in Python, C#, PostgreSQL, and React JS, with growing expertise in machine learning
frameworks like TensorFlow, Keras, and scikit-learn. Skilled in data processing, system
optimization, and delivering solutions that enhance user engagement and efficiency. Passionate
about leveraging data-driven models to drive innovation and performance.

SKILLS & ABILITIES
Programming Languages: Python, C#, JavaScript, TypeScript
Machine Learning: TensorFlow, Keras, scikit-learn, streamlit,  Hugging Face Transformers
Web Development: ReactJS, HTML, CSS
Database: PostgreSQL, SQL
Frameworks: .NET, React Native, Flask
Cloud Platforms: AWS, Render
Version Control: Git, GitHub

CERTIFICATES
•DEEP LEARNING WITH KERAS AND TENSORFLOW, COURSERA
•MACHINE LEARNING WITH PYTHON (V2), COURSERA
•REACT - THE COMPLETE GUIDE (HOOKS, REACT ROUTER, REDUX), UDEMY


PROFESSIONAL EXPERIENCE
SOFTWARE DEVELOPER | THE REYNOLDS AND REYNOLDS | Jan 2022 – July 2024
• Led and collaborated on the development and maintenance of KeyTrak applications
(Desktop, Web, Mobile) using PostgreSQL, C#, .Net, React, TypeScript, and React Native.
• Drove seamless feature rollouts through Agile practices and a robust CI/CD pipeline.
• Built RESTful APIs and applied SOLID principles for scalable, maintainable solutions.
• Ensured software reliability with Jest-based unit testing and efficient version control via Git.
• Boosted performance and reduced downtime by optimizing databases and resolving critical
production issues.

Tools and Technologies: PostgreSQL, PowerShell, C#, .Net, React JS, TypeScript, React Native,
RESTful APIs, pgAdmin, Tortoise SVN, Visual Studio, Jenkins, Slack, Git, Github Actions.

NOTABLE WORK PROJECTS
SVN to GitHub Repository Migration
• Successfully migrated SVN repository to GitHub, enhancing collaboration and version control.
• Utilized Git, GitHub, and custom scripts for efficient data migration.
• Streamlined CI/CD by migrating build processes from Jenkins to GitHub Actions.
• Enhanced deployment speed and reliability with automated GitHub Actions pipelines.

Database Update Automation
• Developed a PowerShell script and console application to automate the database update process.
• Seamlessly integrated the automation solution with the CI/CD pipeline.
• Achieved improved efficiency and reliability in database updates, reducing manual intervention.

PERSONAL PROJECTS
SENTIMENT ANALYSIS WEB APP
Technologies: Python, Flask, ReactJS, Hugging Face Transformers, Flask-CORS, SciPy
• Developed a responsive web app with ReactJS and Flask to analyze sentiment of user-input
text using a pre-trained RoBERTa model from Hugging Face Transformers.
• Created a user-friendly UI with real-time updates and ensured seamless cross-origin
communication using Flask-CORS.
• Optimized performance and accuracy with SoftMax and robust backend design.

HOUSING PRICE PREDICTOR WEB APP
Technologies: Python, Streamlit, Scikit-learn, Pandas
• Developed a web app to predict housing prices using a Random Forest model, with real-time
user inputs and visualizations via Streamlit.
• Built robust preprocessing pipelines to handle categorical, numeric, and non-numeric data,
ensuring accurate predictions.
• Visualized model performance metrics (RMSE, R²) and results, providing clear insights into model
accuracy and predictions.

WEATHER APP
Technologies: Python, Flask, ReactJS, OpenWeatherMap API, Render
• Developed a fully responsive web application using Flask as the backend, with a ReactJS
frontend for an interactive user experience.
• Integrated the OpenWeatherMap API for real-time weather data, including temperature, humidity,
sunrise-sunset times, and other weather conditions.
• Conducted extensive testing for functionality and cross-platform compatibility.

EDUCATION
MASTER’S IN ARTIFICIAL INTELLIGENCE, UNIVERSITY OF THE CUMBERLANDS, KY | CURRENT
BACHELOR'S IN COMPUTER SCIENCE, EAST CENTRAL UNIVERSITY, ADA, OK

Note 1: If the context provided does not contain information relevant to the question, then reply as a normal chatbot.
Note 2: If the context provided contains information relevant to the question, then reply as a first person based on the context.
Note 3: When answering the question, make sure to provide a clear and concise response. And do not say that you are replying based on context.

Question: '''
        full_query = context + query
        
        # Send request to OpenRouter
        response = requests.post(
            url=url,
            headers=headers,
            data=json.dumps({
                "model": "deepseek/deepseek-chat:free",
                "messages": [{"role": "user", "content": full_query}]
            })
        )

        # Parse response
        print(response)
        response_json = response.json()
        if "choices" in response_json and len(response_json["choices"]) > 0:
            return response_json["choices"][0]["message"]["content"]
        else:
            return "Error: No valid response from AI."

    except Exception as e:
        return f"Error processing request: {str(e)}"
