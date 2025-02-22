import chromadb
import os
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings, HuggingFaceInferenceAPIEmbeddings
import json

# Load API keys from api_key.json
with open("api_key.json", "r") as api_file:
    api = json.load(api_file)

HUGGINGFACE_API_KEY = api["HUGGINGFACE_API_KEY"]

if HUGGINGFACE_API_KEY:
    print("Using Hugging Face API for embeddings...")
    embedding_function = HuggingFaceInferenceAPIEmbeddings(
        api_key=HUGGINGFACE_API_KEY,
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
else:
    print("Using local embeddings...")
    embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Initialize ChromaDB with persistent storage
vector_store = Chroma(persist_directory="../chroma_db", embedding_function=embedding_function)

# Knowledge base to store in ChromaDB
documents = [
    "### Personal Information\n"
    "Full Name: Ankit Rijal\n"
    "Current Location: Dallas, Texas\n"
    "Date of Birth: September 20, 1997\n"
    "Place of Birth: Nepal\n"
    "Phone: (817) 703-8670\n"
    "Email: ankitrijal2054@gmail.com\n"
    "LinkedIn: https://www.linkedin.com/in/ankitrjl2054/\n"
    "GitHub: https://github.com/ankitrijal2054\n"
    "Portfolio: https://ankitrijal2054.github.io/portfolio_website/\n"
    "Instagram: https://www.instagram.com/ankit_rjl/\n",

    "### Professional Summary\n"
    "Ankit Rijal is an aspiring Machine Learning Engineer with a software development background. "
    "He has experience in building scalable applications, is proficient in Python, C#, PostgreSQL, and ReactJS, "
    "and has expertise in ML frameworks like TensorFlow, Keras, PyTorch, and scikit-learn. "
    "He is skilled in data processing, system optimization, and developing data-driven solutions to enhance efficiency and innovation.\n",

    "### Technical Skills\n"
    "Machine Learning & AI: TensorFlow, Keras, PyTorch, scikit-learn, Hugging Face Transformers, Generative AI, "
    "Transformer Architecture, CNN, RNN, LSTM, Attention Mechanisms, Autoencoders, GANs, Reinforcement Learning, "
    "Streamlit, LangChain, RAG, ChromaDB.\n"
    "Programming Languages: Python, C#, JavaScript, TypeScript.\n"
    "Database & Cloud Technologies: PostgreSQL, SQL, AWS (S3, Lambda, Amplify), Render.\n"
    "Frameworks & Development: .NET, ReactJS, React Native, Flask, HTML, CSS.\n"
    "Version Control & DevOps: Git, GitHub, Docker, CI/CD (GitHub Actions).\n",

    "### Certifications\n"
    "Gen AI Language Modeling with Transformers – IBM, Feb 2025\n"
    "Advanced Deep Learning Specialist – IBM, Jan 2025\n"
    "Machine Learning with Python (V2) – Coursera, Dec 2024\n",

    "### Professional Experience\n"
    "Software Developer | The Reynolds and Reynolds | Jan 2022 – July 2024\n"
    "Led development & maintenance of KeyTrak applications (Desktop, Web, Mobile), impacting over 5,000+ businesses.\n"
    "Spearheaded 20+ feature rollouts, improving deployment efficiency by 30% through a robust CI/CD pipeline.\n"
    "Developed & optimized 30+ RESTful APIs, ensuring scalability & maintainability with SOLID principles.\n"
    "Achieved over 95 percent unit test coverage with Jest, reducing production defects significantly.\n"
    "Worked cross-functionally with teams of 10+ developers, ensuring timely delivery of software solutions.\n"
    "Tools & Technologies Used: PostgreSQL, PowerShell, C#, .NET, ReactJS, TypeScript, React Native, Jest, "
    "pgAdmin, Tortoise SVN, Visual Studio, VS Code, Phabricator, Jenkins, Slack, GitHub Actions.\n",

    "### Notable Work Projects\n"
    "SVN to GitHub Repository Migration: Successfully migrated a large SVN repository to GitHub, improving developer collaboration by 20%.\n"
    "Reduced deployment time by 30% by automating processes using custom scripts & GitHub Actions.\n"
    "Migrated 50+ build processes from Jenkins to GitHub Actions, enhancing automation & reliability.\n"
    "Database Update Automation: Developed a PowerShell script & console app to automate database updates, reducing manual intervention by 90%.\n"
    "Integrated automation into the CI/CD pipeline, decreasing update time by 50%.\n"
    "Improved efficiency, ensuring 99 percent uptime and eliminating critical errors during database updates.\n",

    "### Personal Projects\n"
    "Sentiment Analysis Web App (https://sentiment-analysis-app-33hz.onrender.com/)\n"
    "Technologies: Python, Flask, ReactJS, Hugging Face Transformers, Flask-CORS, SciPy.\n"
    "Built a responsive web app using ReactJS & Flask to analyze user text sentiment with a pre-trained RoBERTa model.\n"
    "Designed a real-time interactive UI with seamless backend integration using Flask-CORS.\n"
    "Housing Price Predictor Web App (https://github.com/ankitrijal2054/House_Price_Prediction)\n"
    "Technologies: Python, Streamlit, Scikit-learn, Pandas.\n"
    "Built a housing price prediction app using a Random Forest model with real-time user input.\n"
    "Created robust preprocessing pipelines for categorical & numerical data handling.\n"
    "Weather App (https://weather-app-3jmk.onrender.com/)\n"
    "Technologies: Python, Flask, ReactJS, OpenWeatherMap API, Render.\n"
    "Developed a fully responsive web app with real-time weather data fetching & display.\n"
    "Conducted extensive testing for cross-platform compatibility.\n",

    "### Education\n"
    "Master’s in Artificial Intelligence – University of the Cumberlands, KY (Ongoing).\n"
    "Bachelor's in Computer Science – East Central University, Ada, OK (Graduated in 2021).\n",

    "### Personal Life\n"
    "Hobbies & Interests: Watching movies that spark curiosity, playing soccer, hiking, traveling, and DIY projects.\n"
    "Movies: Sci-Fi & Mind-Bending (Interstellar, Inception), Psychological Thriller & Action (The Dark Knight), "
    "Inspirational & Drama (The Pursuit of Happyness).\n"
    "Music: Country, Nepali Folk, and Rap.\n"
    "Sports & Fitness: Soccer, Cricket, Hiking, Running, Gym.\n"
    "Cooking & Cuisine: Nepali, Indian, and Mexican food.\n"
    "Languages: English, Nepali, Hindi.\n"
    "Life Philosophy: Simple living, high thinking.\n"
    "Challenges & Personal Growth: Views challenges as opportunities for growth and learning.\n"
    "Travel & Cultural Experiences: Passionate about traveling, exploring new places, and learning about different cultures.\n",

    "### Goals & Aspirations\n"
    "Transition into a Machine Learning Engineer role.\n"
    "Work on AI-driven projects that impact real-world applications.\n"
    "Contribute to open-source projects in AI & software development.\n"
    "Earn AWS certification and gain expertise in cloud-based ML deployment.\n"
]

# Insert documents into ChromaDB
vector_store.add_texts(documents)
vector_store.persist()  # Save the database
print("Knowledge base successfully added to ChromaDB!")

