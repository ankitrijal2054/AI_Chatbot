import os
import hashlib
from datetime import datetime, timezone

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# =========================================
# Embeddings (local to avoid dim mismatch)
# =========================================
print("💻 Using local Hugging Face embeddings...")
embedding_function = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"  # 384-dim
)

# =========================================
# Vector store (auto-persist in v0.4+)
# =========================================
COLLECTION_NAME = "ankit_rijal_kb"
PERSIST_DIR = "../chroma_db"

vector_store = Chroma(
    collection_name=COLLECTION_NAME,
    persist_directory=PERSIST_DIR,
    embedding_function=embedding_function,
)

# =========================================
# Knowledge base (merged + expanded)
# Store as sectioned blocks so we can chunk with metadata
# =========================================
KB_VERSION = "2025-10-07"
UPDATED_AT = datetime.now(timezone.utc).isoformat()

sections = [
    {
        "section": "Personal Information",
        "category": "personal",
        "keywords": "name, phone, email, location, contact, linkedin, github, portfolio, social",
        "content": """
Full Name: Ankit Rijal
Date of Birth: September 20, 1997
Place of Birth: Nepal
Current Location: Dallas, Texas, USA
Phone: (817) 703-8670
Email: ankitrijal2054@gmail.com
LinkedIn: https://www.linkedin.com/in/ankitrjl2054/
GitHub: https://github.com/ankitrijal2054
Portfolio: https://ankitrijal2054.github.io/portfolio_website/
Instagram: https://www.instagram.com/ankit_rjl/
"""
    },
    {
        "section": "Professional Summary",
        "category": "career",
        "keywords": "summary, software engineer, AI engineer, full stack, cloud, LLM, RAG, CI/CD, AWS",
        "content": """
Ankit Rijal is a full-stack software engineer and aspiring AI engineer with 2.5+ years of experience building scalable, cloud-ready applications and RESTful APIs. He is proficient in Python, C#, TypeScript/JavaScript, ReactJS, SQL, and AWS, and has hands-on experience integrating generative AI features (LLMs, LangChain, RAG) into production-grade apps. He focuses on backend optimization, CI/CD automation, containerized deployment, and end-to-end MLOps workflows. He enjoys bridging AI and software engineering to ship practical, reliable, and human-centric products.
"""
    },
    {
        "section": "Education",
        "category": "education",
        "keywords": "masters, bachelors, university of the cumberlands, east central university, graduation",
        "content": """
Master’s in Artificial Intelligence — University of the Cumberlands, KY (Expected Aug 2025)
Bachelor’s in Computer Science — East Central University, Ada, OK (May 2021)
"""
    },
    {
        "section": "Professional Experience",
        "category": "experience",
        "keywords": "reynolds and reynolds, keytrak, c#, .net, apis, ci/cd, git migration, jenkins to github actions",
        "content": """
Software Developer — The Reynolds and Reynolds Company (College Station, TX) — Jan 2022 to July 2024
• Developed and maintained C#/.NET-based full-stack KeyTrak applications (desktop, web, mobile) used by 5,000+ enterprise customers.
• Designed 30+ RESTful APIs in C# using ASP.NET Core and SOLID principles, improving modularity and performance.
• Migrated legacy Jenkins CI/CD pipelines to GitHub Actions, reducing deployment time by ~30%.
• Led version control migration from SVN to Git across an Agile team, improving collaboration and release efficiency.
• Partnered with QA and Product to resolve production issues with clear documentation and timely updates.
Tech: PostgreSQL, C#, .NET, ReactJS, TypeScript, PowerShell, Jenkins, GitHub Actions, Visual Studio, VS Code, Phabricator, Slack.
"""
    },
    {
        "section": "Projects",
        "category": "projects",
        "keywords": "guide2smart ai, adaptive quiz, generative ai chatbot, rag, chromadb, mlops, ai image assistant, streamlit, sentiment app, weather app",
        "content": """
Guide2Smart AI — Adaptive Quiz Generator
Tech: Python, FastAPI, React, Google Gemini APIs
• Generates MCQs, explanations, and summaries from uploaded study files using LLMs and a modular FastAPI backend.

Generative AI Chatbot (RAG)
Tech: Python, Flask, LangChain, ChromaDB, Hugging Face
• Retrieval-Augmented Generation chatbot with text + voice interfaces, persistent memory, and contextual responses.

MLOps Pipeline — Housing Price Prediction
Tech: DVC, MLflow, Docker, AWS EC2, Prometheus, Grafana, Apache Airflow, Evidently AI
• End-to-end workflow with data/model versioning, CI/CD, containerized deployment, monitoring, and automated retraining.

AI Image Assistant
Tech: Python, Streamlit, Google Gemini 1.5 Flash
• Vision-language assistant for captioning and visual Q&A; deployed on Streamlit Community Cloud.

Sentiment Analysis Web App
Tech: Python, Flask, React, Hugging Face Transformers
• RoBERTa-based text sentiment analysis with responsive React UI and Flask API (CORS-enabled).

Weather App
Tech: Python, Flask, React, OpenWeatherMap API, Render
• Real-time weather retrieval and display with cross-platform testing.
"""
    },
    {
        "section": "Technical Skills",
        "category": "skills",
        "keywords": "python, c#, typescript, react, fastapi, asp.net core, flask, postgres, redis, aws, docker, github actions, tdd, langchain, transformers",
        "content": """
Languages & Frameworks: Python, C#, JavaScript, TypeScript, ASP.NET Core, FastAPI, Flask, ReactJS, React Native
Databases & Cloud: PostgreSQL, Redis, AWS (EC2, S3), GCP
DevOps & Automation: GitHub Actions, Jenkins, Docker, Agile/Scrum, Unit Testing
AI & ML: TensorFlow, Keras, PyTorch, scikit-learn, Hugging Face Transformers, LangChain, RAG, Gemini APIs, Amazon Bedrock
MLOps: DVC, MLflow, Prometheus, Grafana, Apache Airflow, Evidently AI
Assistants & Tools: GitHub Copilot, Amazon Q Developer, Cursor, Lovable
Practices: TDD, OOP, SOLID Principles
"""
    },
    {
        "section": "Certifications",
        "category": "certifications",
        "keywords": "aws, ibm, google cloud, transformers, deep learning, machine learning with python",
        "content": """
AWS Generative AI for Developers — AWS
Generative AI and LLMs: Architecture & Data Preparation — IBM
Fundamentals of AI Agents using RAG and LangChain — IBM
Production Machine Learning Systems — Google Cloud
Advanced Deep Learning Specialist — IBM (Jan 2025)
GenAI Language Modeling with Transformers — IBM (Feb 2025)
Machine Learning with Python (V2) — Coursera (Dec 2024)
"""
    },
    {
        "section": "Notable Achievements",
        "category": "achievements",
        "keywords": "ci/cd, uptime, unit tests, performance, automation, reliability",
        "content": """
• Migrated 50+ build pipelines from Jenkins to GitHub Actions, boosting reliability and automation.
• Achieved ~95% unit test coverage across KeyTrak modules, lowering production defects.
• Reduced deployment time by ~30% through optimized CI/CD processes and custom scripts.
• Improved system uptime to ~99% via automated database update processes and robust monitoring.
"""
    },
    {
        "section": "Personal Life & Interests",
        "category": "personal",
        "keywords": "movies, hiking, soccer, cricket, music, cuisine, languages, values",
        "content": """
Hobbies & Interests: Movies that spark curiosity, soccer, hiking, DIY projects, travel.
Favorite Movies: Interstellar, Inception, The Dark Knight, The Pursuit of Happyness.
Music: Country, Nepali Folk, Rap.
Sports & Fitness: Soccer, Cricket, Running, Gym.
Cuisine: Nepali, Indian, Mexican.
Languages: English, Nepali, Hindi.
Philosophy: “Simple living, high thinking.”
Core Values: Integrity, growth mindset, empathy.
"""
    },
    {
        "section": "Goals & Aspirations",
        "category": "goals",
        "keywords": "ai engineer, ml engineer, open source, certifications, cloud, llm, rag, mlops",
        "content": """
• Transition into an AI/Machine Learning Engineer role.
• Build AI products with real-world impact and ethical best practices.
• Contribute to open-source AI and ML tooling.
• Earn advanced AWS certifications; deepen cloud-based ML deployment.
• Continue mastery of LLMs, RAG systems, and MLOps at production scale.
"""
    },
    {
        "section": "Aliases & Variants",
        "category": "personal",
        "keywords": "aliases, username, misspellings",
        "content": """
Common Name Variants & Usernames:
• Ankit, Ankit R., Ankit Rijal
• ankitrijal2054, ankitrjl2054
Common misspelling: “Ankit Rajil”
"""
    },
]

# =========================================
# Chunking with metadata
# =========================================
splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,           # ~200–300 words per chunk
    chunk_overlap=120,
    separators=["\n\n", "\n", ". ", " "]
)

docs: list[Document] = []
ids: list[str] = []

def make_id(section: str, idx: int, text: str) -> str:
    h = hashlib.md5(text.strip().encode("utf-8")).hexdigest()[:12]
    return f"{section.lower().replace(' ','_')}-{idx}-{h}"

for block in sections:
    raw_text = block["content"].strip()
    if not raw_text:
        continue

    chunks = splitter.split_text(raw_text)
    for i, chunk in enumerate(chunks):
        meta = {
            "source": "self_kb",
            "version": KB_VERSION,
            "updated_at": UPDATED_AT,
            "section": block["section"],
            "category": block["category"],
            "keywords": block["keywords"],
        }
        docs.append(Document(page_content=chunk, metadata=meta))
        ids.append(make_id(block["section"], i, chunk))

# =========================================
# Upsert into Chroma (add or dedupe by ID)
# =========================================
if docs:
    # Optional: delete any existing docs with same IDs to avoid duplicates
    try:
        # Chroma wrapper supports delete by ids on underlying collection
        vector_store._collection.delete(ids=ids)  # safe to attempt; ignore if not present
    except Exception:
        pass

    vector_store.add_documents(documents=docs, ids=ids)
    print(f"✅ Inserted {len(docs)} chunks into collection '{COLLECTION_NAME}'.")
    print(f"💾 Chroma automatically persisted to: {PERSIST_DIR}")
else:
    print("⚠️ No documents to insert.")
