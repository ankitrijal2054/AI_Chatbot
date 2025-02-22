import chromadb
import os
from langchain_postgres.vectorstores import PGVector
from langchain.embeddings import HuggingFaceEmbeddings, HuggingFaceInferenceAPIEmbeddings
from langchain.schema import Document
import json

# Load API keys from api_key.json
with open("api_key.json", "r") as api_file:
    api = json.load(api_file)

HUGGINGFACE_API_KEY = api["HUGGINGFACE_API_KEY"]
PG_CONNECTION_STRING = api["PG_CONNECTION_STRING"]

if HUGGINGFACE_API_KEY:
    print("Using Hugging Face API for embeddings...")
    embedding_function = HuggingFaceInferenceAPIEmbeddings(
        api_key=HUGGINGFACE_API_KEY,
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
else:
    print("Using local embeddings...")
    embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Knowledge base to store in PostgreSQL
documents = [
    Document(page_content="""### Personal Information
Full Name: Ankit Rijal
Current Location: Dallas, Texas
Date of Birth: September 20, 1997
Place of Birth: Nepal
Phone: (817) 703-8670
Email: ankitrijal2054@gmail.com
LinkedIn: https://www.linkedin.com/in/ankitrjl2054/
GitHub: https://github.com/ankitrijal2054
Portfolio: https://ankitrijal2054.github.io/portfolio_website/
Instagram: https://www.instagram.com/ankit_rjl/
""", metadata={"category": "personal_info"}),

    Document(page_content="""### Professional Summary
Ankit Rijal is an aspiring Machine Learning Engineer with a software development background.
He has experience in building scalable applications, is proficient in Python, C#, PostgreSQL, and ReactJS,
and has expertise in ML frameworks like TensorFlow, Keras, PyTorch, and scikit-learn.
He is skilled in data processing, system optimization, and developing data-driven solutions to enhance efficiency and innovation.
""", metadata={"category": "professional_summary"}),

    Document(page_content="""### Technical Skills
Machine Learning & AI: TensorFlow, Keras, PyTorch, scikit-learn, Hugging Face Transformers, Generative AI,
Transformer Architecture, CNN, RNN, LSTM, Attention Mechanisms, Autoencoders, GANs, Reinforcement Learning,
Streamlit, LangChain, RAG, ChromaDB.
Programming Languages: Python, C#, JavaScript, TypeScript.
Database & Cloud Technologies: PostgreSQL, SQL, AWS (S3, Lambda, Amplify), Render.
Frameworks & Development: .NET, ReactJS, React Native, Flask, HTML, CSS.
Version Control & DevOps: Git, GitHub, Docker, CI/CD (GitHub Actions).
""", metadata={"category": "technical_skills"}),

    Document(page_content="""### Certifications
Gen AI Language Modeling with Transformers – IBM, Feb 2025
Advanced Deep Learning Specialist – IBM, Jan 2025
Machine Learning with Python (V2) – Coursera, Dec 2024
""", metadata={"category": "certifications"}),

    Document(page_content="""### Professional Experience
Software Developer | The Reynolds and Reynolds | Jan 2022 – July 2024
Led development & maintenance of KeyTrak applications (Desktop, Web, Mobile), impacting over 5,000+ businesses.
Spearheaded 20+ feature rollouts, improving deployment efficiency by 30% through a robust CI/CD pipeline.
Developed & optimized 30+ RESTful APIs, ensuring scalability & maintainability with SOLID principles.
Achieved over 95 percent unit test coverage with Jest, reducing production defects significantly.
Worked cross-functionally with teams of 10+ developers, ensuring timely delivery of software solutions.
Tools & Technologies Used: PostgreSQL, PowerShell, C#, .NET, ReactJS, TypeScript, React Native, Jest,
pgAdmin, Tortoise SVN, Visual Studio, VS Code, Phabricator, Jenkins, Slack, GitHub Actions.
""", metadata={"category": "professional_experience"}),

    Document(page_content="""### Notable Work Projects
SVN to GitHub Repository Migration: Successfully migrated a large SVN repository to GitHub, improving developer collaboration by 20%.
Reduced deployment time by 30% by automating processes using custom scripts & GitHub Actions.
Migrated 50+ build processes from Jenkins to GitHub Actions, enhancing automation & reliability.
Database Update Automation: Developed a PowerShell script & console app to automate database updates, reducing manual intervention by 90%.
Integrated automation into the CI/CD pipeline, decreasing update time by 50%.
Improved efficiency, ensuring 99 percent uptime and eliminating critical errors during database updates.
""", metadata={"category": "notable_projects"}),

    Document(page_content="""### Personal Projects
Sentiment Analysis Web App (https://sentiment-analysis-app-33hz.onrender.com/)
Technologies: Python, Flask, ReactJS, Hugging Face Transformers, Flask-CORS, SciPy.
Built a responsive web app using ReactJS & Flask to analyze user text sentiment with a pre-trained RoBERTa model.
Designed a real-time interactive UI with seamless backend integration using Flask-CORS.
Housing Price Predictor Web App (https://github.com/ankitrijal2054/House_Price_Prediction)
Technologies: Python, Streamlit, Scikit-learn, Pandas.
Built a housing price prediction app using a Random Forest model with real-time user input.
Created robust preprocessing pipelines for categorical & numerical data handling.
Weather App (https://weather-app-3jmk.onrender.com/)
Technologies: Python, Flask, ReactJS, OpenWeatherMap API, Render.
Developed a fully responsive web app with real-time weather data fetching & display.
Conducted extensive testing for cross-platform compatibility.
""", metadata={"category": "personal_projects"}),

    Document(page_content="""### Education
Master’s in Artificial Intelligence – University of the Cumberlands, KY (Ongoing).
Bachelor's in Computer Science – East Central University, Ada, OK (Graduated in 2021).
""", metadata={"category": "education"}),

    Document(page_content="""### Personal Life
Hobbies & Interests: Watching movies that spark curiosity, playing soccer, hiking, traveling, and DIY projects.
Movies: Sci-Fi & Mind-Bending (Interstellar, Inception), Psychological Thriller & Action (The Dark Knight),
Inspirational & Drama (The Pursuit of Happyness).
Music: Country, Nepali Folk, and Rap.
Sports & Fitness: Soccer, Cricket, Hiking, Running, Gym.
Cooking & Cuisine: Nepali, Indian, and Mexican food.
Languages: English, Nepali, Hindi.
Life Philosophy: Simple living, high thinking.
Challenges & Personal Growth: Views challenges as opportunities for growth and learning.
Travel & Cultural Experiences: Passionate about traveling, exploring new places, and learning about different cultures.
""", metadata={"category": "personal_life"}),

    Document(page_content="""### Goals & Aspirations
Transition into a Machine Learning Engineer role.
Work on AI-driven projects that impact real-world applications.
Contribute to open-source projects in AI & software development.
Earn AWS certification and gain expertise in cloud-based ML deployment.
""", metadata={"category": "goals"})
]

# Create vector store in PostgreSQL
vector_store = PGVector.from_documents(
    documents=documents,
    embedding=embedding_function,
    connection=PG_CONNECTION_STRING,
    collection_name="vector_store"
)

print("Knowledge base successfully added to ChromaDB!")
