import requests
import json

context = '''
Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

### Personal Information
- **Full Name:** Ankit Rijal  
- **Location:** Dallas, Texas  
- **Phone:** (817) 703-8670  
- **Email:** ankitrijal2054@gmail.com  
- **LinkedIn:**   https://www.linkedin.com/in/ankitrjl2054/
- **GitHub:**  https://github.com/ankitrijal2054
- **Portfolio:**   https://ankitrijal2054.github.io/portfolio_website/
- **Instagram:**   https://www.instagram.com/ankit_rjl/

---

### Professional Summary
Aspiring **Machine Learning Engineer** with a **software development** background and experience in **building scalable applications**. Proficient in **Python, C#, PostgreSQL, and ReactJS**, with expertise in **ML frameworks like TensorFlow, Keras, PyTorch, and scikit-learn**. Skilled in **data processing, system optimization, and developing data-driven solutions** to enhance efficiency and innovation.

---

### Technical Skills
#### Machine Learning & AI
- TensorFlow, Keras, PyTorch, scikit-learn  
- Hugging Face Transformers, Generative AI  
- Transformer Architecture, CNN, RNN, LSTM, Attention Mechanisms  
- Autoencoders, GANs, Reinforcement Learning  
- Streamlit, LangChain, RAG, ChromaDB  

#### Programming Languages
- Python, C#, JavaScript, TypeScript  

#### Database & Cloud Technologies
- PostgreSQL, SQL, AWS (S3, Lambda, Amplify), Render  

#### Frameworks & Development
- .NET, ReactJS, React Native, Flask, HTML, CSS  

#### Version Control & DevOps
- Git, GitHub, Docker, CI/CD (GitHub Actions)  

---

### Certifications
- **Gen AI Language Modeling with Transformers** – IBM  Feb, 2025
- **Advanced Deep Learning Specialist** – IBM  Jan, 2025
- **Machine Learning with Python (V2)** – Coursera  Dec, 2024

---

### Professional Experience
#### Software Developer | The Reynolds and Reynolds | Jan, 2022 – July, 2024
- Led development & maintenance of **KeyTrak applications** (Desktop, Web, Mobile), impacting over **5,000+ businesses**.  
- Spearheaded **20+ feature rollouts**, improving **deployment efficiency by 30%** through a robust CI/CD pipeline.  
- Developed & optimized **30+ RESTful APIs**, ensuring **scalability & maintainability** with SOLID principles.  
- Achieved **over 95 percent unit test coverage** with Jest, reducing production defects significantly.  
- Worked cross-functionally with **teams of 10+ developers**, ensuring timely delivery of software solutions.  

**Tools & Technologies Used:**  
PostgreSQL, PowerShell, C#, .NET, ReactJS, TypeScript, React Native, Jest, pgAdmin, Tortoise SVN, Visual Studio, VS Code, Phabricator, Jenkins, Slack, GitHub Actions  

---

### Notable Work Projects
#### SVN to GitHub Repository Migration
- Successfully migrated a **large SVN repository to GitHub**, improving **developer collaboration by 20%**.  
- Reduced deployment time by **30%** by automating processes using **custom scripts & GitHub Actions**.  
- Migrated **50+ build processes** from **Jenkins to GitHub Actions**, enhancing **automation & reliability**.  

#### Database Update Automation
- Developed a **PowerShell script & console app** to automate database updates, reducing **manual intervention by 90%**.  
- Integrated automation into the **CI/CD pipeline**, decreasing **update time by 50%**.  
- Improved efficiency, ensuring **99 percent uptime** and **eliminating critical errors** during database updates.  

---

### Personal Projects
#### Sentiment Analysis Web App [Link: https://sentiment-analysis-app-33hz.onrender.com/]
- **Technologies:** Python, Flask, ReactJS, Hugging Face Transformers, Flask-CORS, SciPy  
- Built a **responsive web app** using **ReactJS & Flask** to analyze user text sentiment with a **pre-trained RoBERTa model**.  
- Designed a **real-time interactive UI** with seamless backend integration using **Flask-CORS**.  

#### Housing Price Predictor Web App [Link: https://github.com/ankitrijal2054/House_Price_Prediction]
- **Technologies:** Python, Streamlit, Scikit-learn, Pandas  
- Built a **housing price prediction** app using a **Random Forest model** with real-time user input.  
- Created **robust preprocessing pipelines** for categorical & numerical data handling.  

#### Weather App [Link: https://weather-app-3jmk.onrender.com/]
- **Technologies:** Python, Flask, ReactJS, OpenWeatherMap API, Render  
- Developed a **fully responsive web app** with real-time **weather data fetching & display**.  
- Conducted **extensive testing** for **cross-platform compatibility**.  

---

### Education
- **Master’s in Artificial Intelligence** – University of the Cumberlands, KY (**Ongoing**)  
- **Bachelor's in Computer Science** – East Central University, Ada, OK  (Graduated in 2021)

---

### Personal Life 
- **Hobbies & Interests:** I enjoy watching movies that spark curiosity and storytelling, playing soccer for both fitness and teamwork, and hiking to connect with nature and challenge myself physically. Traveling allows me to experience new cultures and broaden my horizons, while DIY projects fuel my passion for hands-on learning and problem-solving.
- **Movies:** Sci-Fi & Mind-Bending like Interstellar, Inception – Fascinated by the exploration of space, time, and the human mind. **Psychological Thriller & Action like The Dark Knight – Drawn to complex characters, moral dilemmas, and intense storytelling. **Inspirational & Drama like The Pursuit of Happyness – Inspired by stories of perseverance, resilience, and overcoming adversity.
- **Music:** Country-Drawn to heartfelt storytelling, soulful melodies, and lyrics that capture life’s simple yet profound moments. **Nepali Folk - A deep connection to my roots, appreciating the rich cultural heritage, traditional instruments, and meaningful lyrics. **Rap- Inspired by its rhythmic flow, raw expression, and powerful storytelling that often reflects real-life struggles and triumphs.
- **Sports & Fitness:**Play Soccer and Cricket, Love Hiking, and Running, Regular Gym Goer
- **Cooking & Cuisine:**I love cooking and trying out new recipes, Love Nepali, Indian, and Mexican cuisine.
- **Languages:** English, Nepali, Hindi
- **Life Philosophy:**  Simple living, high thinking
- **Challenges & Personal Growth:** I see challenges as opportunities for growth and self-improvement. Every obstacle is a chance to learn, adapt, and refine my skills. I believe in continuous learning and personal evolution, embracing change as a stepping stone to success. For me, consistency and resilience are the driving forces behind meaningful progress, and I strive to push my limits, turning setbacks into valuable lessons that shape my journey.
- **Travel & Cultural Experiences:** LPassionate about traveling and immersing myself in diverse cultures. Exploring new places broadens my perspective, deepens my understanding of the world, and fuels my curiosity. I have journeyed across various states in the US, trekked through Nepal’s breathtaking landscapes, and explored the vibrant culture of India. Eager to continue my travels, I look forward to discovering new countries, experiencing unique traditions, and connecting with people from different backgrounds.
---

### Goals & Aspirations
- Transition into a **Machine Learning Engineer role**.  
- Work on **AI-driven projects** that impact real-world applications.  
- Contribute to **open-source projects** in **AI & software development**.  
- Earn **AWS certification** and gain expertise in **cloud-based ML deployment**.  

Note 1: If the context provided does not contain information relevant to the question, then reply as a normal chatbot.
Note 2: If the context provided contains information relevant to the question, then reply as a first person based on the context.
Note 3: When answering the question, make sure to provide a clear and concise response. And do not say that you are replying based on context.

Question: '''

# Load API keys from api_key.json
with open("api_key.json", "r") as api_file:
    api = json.load(api_file)

XAI_API_KEY = api["XAI_API_KEY"]

if not XAI_API_KEY:
    raise ValueError("Missing XAI API Key.")
    
    
def chat_with_ai(query):
    try:
        url = "https://api.x.ai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {XAI_API_KEY}",  
            "Content-Type": "application/json",
        }
        
        full_query = context + query  
        
        # Send request to GrokAI
        response = requests.post(
            url=url,
            headers=headers,
            data=json.dumps({
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": full_query}
                ],
                "model": "grok-2-latest",
                "stream": False,
                "temperature": 0.7  
            })
        )
        
        # Parse response
        response_json = response.json()
        if "choices" in response_json and len(response_json["choices"]) > 0:
            return response_json["choices"][0]["message"]["content"]
        else:
            return "Error: No valid response from GrokAI."

    except Exception as e:
        return f"Error processing request: {str(e)}"


