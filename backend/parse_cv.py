import sys
import json
from pyresparser import ResumeParser
import spacy
import nltk
from spacy.cli import download
from openai import OpenAI
from dotenv import load_dotenv
import os
from pdfminer.high_level import extract_text as extract_pdf_text
from docx import Document
import tiktoken

# positions_data = {
positions = [
    {
        "area": "Frontend Engineering",
        "level": "Junior",
        "toolsTechnologiesFrameworks": ["HTML/CSS", "JavaScript", "Git"],
        "programmingLanguages": ["HTML", "CSS", "JavaScript"],
        "skillsResponsibilities": [
            "Basic frontend structure",
            "Responsive design",
            "Basic Git usage"
        ]
    },
    {
        "area": "Frontend Engineering",
        "level": "Mid",
        "toolsTechnologiesFrameworks": ["React", "Vue.js", "Sass", "DevTools"],
        "programmingLanguages": ["HTML", "CSS", "JavaScript", "TypeScript"],
        "skillsResponsibilities": [
            "Component libraries",
            "State management",
            "Code optimization"
        ]
    },
    {
        "area": "Frontend Engineering",
        "level": "Senior",
        "toolsTechnologiesFrameworks": ["Redux", "Webpack", "GraphQL", "CI/CD tools", "Advanced CSS"],
        "programmingLanguages": ["JavaScript", "TypeScript"],
        "skillsResponsibilities": [
            "Architecture implementation",
            "Performance optimization",
            "Mentoring juniors",
            "Code reviews"
        ]
    },
    {
        "area": "Frontend Engineering",
        "level": "Lead",
        "toolsTechnologiesFrameworks": ["Next.js", "Tailwind", "Jest", "Cypress", "Design tools integration"],
        "programmingLanguages": ["TypeScript", "JavaScript", "Optional: Rust"],
        "skillsResponsibilities": [
            "Team leadership",
            "Technical direction",
            "Design/backend integration",
            "Project planning",
            "High-level problem-solving"
        ]
    },
    {
        "area": "Frontend Engineering",
        "level": "Architect",
        "toolsTechnologiesFrameworks": ["Angular", "Micro-frontends", "WebAssembly", "Architecture patterns"],
        "programmingLanguages": ["TypeScript", "JavaScript", "Optional: WebAssembly"],
        "skillsResponsibilities": [
            "Design frontend architecture",
            "Coordinate teams",
            "Ensure scalability"
        ]
    },
    {
        "area": "Backend Engineering",
        "level": "Junior",
        "toolsTechnologiesFrameworks": ["Node.js", "Basic REST APIs", "Git"],
        "programmingLanguages": ["JavaScript", "Python", "Java"],
        "skillsResponsibilities": [
            "Basic API development",
            "CRUD operations",
            "Version control"
        ]
    },
    {
        "area": "Backend Engineering",
        "level": "Mid",
        "toolsTechnologiesFrameworks": ["Express", "Django", "Flask", "ORM (e.g., SQLAlchemy)"],
        "programmingLanguages": ["JavaScript", "Python", "Java", "SQL"],
        "skillsResponsibilities": [
            "API integration",
            "Data modeling",
            "Intermediate DB management",
            "Error handling"
        ]
    },
    {
        "area": "Backend Engineering",
        "level": "Senior",
        "toolsTechnologiesFrameworks": ["Microservices", "Docker", "gRPC", "RabbitMQ", "CI/CD tools", "SQL optimization"],
        "programmingLanguages": ["Python", "Java", "Golang", "SQL"],
        "skillsResponsibilities": [
            "Microservices design",
            "DB performance tuning",
            "Mentorship",
            "Technical leadership"
        ]
    },
    {
        "area": "Backend Engineering",
        "level": "Lead",
        "toolsTechnologiesFrameworks": ["Kubernetes", "Redis", "Kafka", "Advanced CI/CD"],
        "programmingLanguages": ["Python", "Java", "Golang", "Optional: Rust"],
        "skillsResponsibilities": [
            "Architectural planning",
            "Infrastructure considerations",
            "High-level problem-solving",
            "Team management"
        ]
    },
    {
        "area": "Backend Engineering",
        "level": "Architect",
        "toolsTechnologiesFrameworks": ["Distributed systems", "Serverless architecture", "Advanced API design patterns"],
        "programmingLanguages": ["Go", "Java", "Python", "Scala"],
        "skillsResponsibilities": [
            "Design scalable systems",
            "Enforce best practices",
            "Integrate with DevOps and frontend"
        ]
    },
    {
        "area": "Fullstack Engineering",
        "level": "Junior",
        "toolsTechnologiesFrameworks": ["HTML", "CSS", "JavaScript", "Basic Node.js"],
        "programmingLanguages": ["JavaScript", "TypeScript"],
        "skillsResponsibilities": [
            "Basic full-stack knowledge",
            "CRUD operations",
            "Client-server interaction"
        ]
    },
    {
        "area": "Fullstack Engineering",
        "level": "Mid",
        "toolsTechnologiesFrameworks": ["React", "Express", "Redux", "REST API", "SQL"],
        "programmingLanguages": ["JavaScript", "TypeScript", "Python", "SQL"],
        "skillsResponsibilities": [
            "Intermediate full-stack skills",
            "Frontend-backend connection",
            "Data handling",
            "State management"
        ]
    },
    {
        "area": "Fullstack Engineering",
        "level": "Senior",
        "toolsTechnologiesFrameworks": ["Next.js", "Microservices", "Docker", "NoSQL (MongoDB)", "Authentication"],
        "programmingLanguages": ["JavaScript", "TypeScript", "Python"],
        "skillsResponsibilities": [
            "Advanced full-stack design",
            "API security",
            "Performance tuning",
            "Cross-functional collaboration"
        ]
    },
    {
        "area": "Fullstack Engineering",
        "level": "Lead",
        "toolsTechnologiesFrameworks": ["Advanced API Integration", "Kubernetes", "Server-side rendering", "CI/CD"],
        "programmingLanguages": ["JavaScript", "TypeScript", "Python", "Go"],
        "skillsResponsibilities": [
            "Full-stack architecture leadership",
            "Optimize performance across layers",
            "Manage cross-team dependencies"
        ]
    },
    {
        "area": "Fullstack Engineering",
        "level": "Architect",
        "toolsTechnologiesFrameworks": ["Design patterns", "Hybrid cloud", "Distributed architecture"],
        "programmingLanguages": ["Go", "JavaScript", "TypeScript", "Optional: Rust"],
        "skillsResponsibilities": [
            "Define scalable architectures",
            "Ensure reliability",
            "Improve security"
        ]
    },
    {
        "area": "Manual Testing",
        "level": "Junior",
        "toolsTechnologiesFrameworks": ["TestRail", "Basic testing documentation"],
        "programmingLanguages": ["N/A"],
        "skillsResponsibilities": [
            "Execute test cases",
            "Log issues",
            "Assist in bug tracking"
        ]
    },
    {
        "area": "Manual Testing",
        "level": "Mid",
        "toolsTechnologiesFrameworks": ["Jira", "Exploratory Testing", "Basic scripting (Python, JavaScript)"],
        "programmingLanguages": ["Python", "JavaScript"],
        "skillsResponsibilities": [
            "Develop test cases",
            "Execute regression testing",
            "Enhance QA processes"
        ]
    },
    {
        "area": "Manual Testing",
        "level": "Senior",
        "toolsTechnologiesFrameworks": ["Postman", "SoapUI", "SQL for data validation", "User Acceptance Testing"],
        "programmingLanguages": ["Python", "SQL"],
        "skillsResponsibilities": [
            "Lead test planning",
            "Design complex test cases",
            "Manage bug prioritization"
        ]
    },
    {
        "area": "Manual Testing",
        "level": "Lead",
        "toolsTechnologiesFrameworks": ["Test strategy creation", "Advanced API testing", "Cross-browser testing", "CI/CD"],
        "programmingLanguages": ["Python", "SQL"],
        "skillsResponsibilities": [
            "Define test strategy",
            "Coordinate QA/Dev teams",
            "Lead UAT",
            "Mentor team members"
        ]
    },
    {
        "area": "Manual Testing",
        "level": "Architect",
        "toolsTechnologiesFrameworks": ["Zephyr", "qTest", "QA automation pipelines"],
        "programmingLanguages": ["Python", "SQL"],
        "skillsResponsibilities": [
            "Oversee testing lifecycle",
            "Design automation strategies",
            "Ensure QA best practices"
        ]
    },
    {
        "area": "DevOps/SRE/Infra",
        "level": "Junior",
        "toolsTechnologiesFrameworks": ["Basic Linux", "Bash scripting", "Docker", "Git"],
        "programmingLanguages": ["Shell", "Python"],
        "skillsResponsibilities": [
            "Manage CI/CD pipelines",
            "Understand containerization",
            "Write basic deployment scripts"
        ]
    },
    {
        "area": "DevOps/SRE/Infra",
        "level": "Mid",
        "toolsTechnologiesFrameworks": ["Docker", "Jenkins", "Ansible", "Kubernetes"],
        "programmingLanguages": ["Shell", "Python", "Go"],
        "skillsResponsibilities": [
            "CI/CD management",
            "Container orchestration",
            "Infrastructure as code",
            "System monitoring"
        ]
    },
    {
        "area": "DevOps/SRE/Infra",
        "level": "Senior",
        "toolsTechnologiesFrameworks": ["Terraform", "AWS/Azure/GCP", "Advanced Kubernetes", "Prometheus", "Grafana"],
        "programmingLanguages": ["Shell", "Go", "Python"],
        "skillsResponsibilities": [
            "Scale infrastructure",
            "Advanced monitoring",
            "SRE practices"
        ]
    },
    {
        "area": "DevOps/SRE/Infra",
        "level": "Lead",
        "toolsTechnologiesFrameworks": ["Cross-region cloud infra", "Advanced CI/CD", "Service mesh (Istio)"],
        "programmingLanguages": ["Go", "Python", "Shell"],
        "skillsResponsibilities": [
            "Lead SRE practices",
            "Plan cloud architecture",
            "Collaborate with developers on infra"
        ]
    },
    {
        "area": "DevOps/SRE/Infra",
        "level": "Architect",
        "toolsTechnologiesFrameworks": ["Hybrid cloud", "Disaster recovery", "Observability"],
        "programmingLanguages": ["Go", "Python"],
        "skillsResponsibilities": [
            "Design resilient infrastructure",
            "Implement cloud-native strategies",
            "Oversee DevOps best practices"
        ]
    },
    {
        "area": "UX/UI Design",
        "level": "Junior",
        "toolsTechnologiesFrameworks": ["Figma", "Adobe XD", "Basic HTML/CSS", "Design principles"],
        "programmingLanguages": ["N/A"],
        "skillsResponsibilities": [
            "Basic design tasks",
            "Support senior designers",
            "Maintain visual consistency"
        ]
    },
    {
        "area": "UX/UI Design",
        "level": "Mid",
        "toolsTechnologiesFrameworks": ["Figma", "InVision", "Usability testing tools"],
        "programmingLanguages": ["N/A"],
        "skillsResponsibilities": [
            "Conduct user research",
            "Intermediate UI/UX design",
            "Test designs and collect feedback"
        ]
    },
    {
        "area": "UX/UI Design",
        "level": "Senior",
        "toolsTechnologiesFrameworks": ["Advanced prototyping", "Interaction design", "Accessibility standards"],
        "programmingLanguages": ["N/A"],
        "skillsResponsibilities": [
            "Lead design reviews",
            "Create high-fidelity prototypes",
            "Define UX/UI standards"
        ]
    },
    {
        "area": "UX/UI Design",
        "level": "Lead",
        "toolsTechnologiesFrameworks": ["Advanced design systems", "User testing strategies", "Accessibility standards"],
        "programmingLanguages": ["N/A"],
        "skillsResponsibilities": [
            "Lead design projects",
            "Ensure design consistency",
            "Collaborate across teams"
        ]
    },
    {
        "area": "UX/UI Design",
        "level": "Architect",
        "toolsTechnologiesFrameworks": ["Design system architecture", "UX strategy for scalable systems"],
        "programmingLanguages": ["N/A"],
        "skillsResponsibilities": [
            "Oversee user experience",
            "Define scalable design systems",
            "Collaborate with frontend architects"
        ]
    },
    {
        "area": "Data Engineering",
        "level": "Junior",
        "toolsTechnologiesFrameworks": ["SQL", "ETL tools (e.g., Talend)", "Basic Python or R", "Git"],
        "programmingLanguages": ["SQL", "Python"],
        "skillsResponsibilities": [
            "Data extraction and processing",
            "Support data pipelines",
            "Maintain ETL scripts"
        ]
    },
    {
        "area": "Data Engineering",
        "level": "Mid",
        "toolsTechnologiesFrameworks": ["Apache Spark", "SQL", "Airflow"],
        "programmingLanguages": ["SQL", "Python", "Optional: Scala"],
        "skillsResponsibilities": [
            "Build ETL pipelines",
            "Data modeling",
            "Optimize data storage"
        ]
    },
    {
        "area": "Data Engineering",
        "level": "Senior",
        "toolsTechnologiesFrameworks": ["Advanced Spark", "Data Lake architecture", "Kafka", "Cloud data services (e.g., BigQuery)"],
        "programmingLanguages": ["Python", "SQL", "Scala"],
        "skillsResponsibilities": [
            "Lead data architecture",
            "Optimize and scale pipelines",
            "Mentor team members"
        ]
    },
    {
        "area": "Data Engineering",
        "level": "Lead",
        "toolsTechnologiesFrameworks": ["Distributed data systems", "DataOps", "Cloud architectures"],
        "programmingLanguages": ["Python", "SQL", "Scala"],
        "skillsResponsibilities": [
            "Oversee data projects",
            "Ensure scalability",
            "Maintain data quality"
        ]
    },
    {
        "area": "Data Engineering",
        "level": "Architect",
        "toolsTechnologiesFrameworks": ["Data architecture design", "Hybrid data cloud", "Compliance (GDPR, CCPA)"],
        "programmingLanguages": ["SQL", "Python"],
        "skillsResponsibilities": [
            "Define data strategies",
            "Manage compliance",
            "Design scalable architecture"
        ]
    },
    {
        "area": "Data Science",
        "level": "Junior",
        "toolsTechnologiesFrameworks": ["Jupyter", "Pandas", "Numpy"],
        "programmingLanguages": ["Python", "R"],
        "skillsResponsibilities": [
            "Exploratory data analysis",
            "Basic ML algorithms",
            "Data cleaning"
        ]
    },
    {
        "area": "Data Science",
        "level": "Mid",
        "toolsTechnologiesFrameworks": ["Scikit-learn", "SQL", "Feature engineering"],
        "programmingLanguages": ["Python", "SQL"],
        "skillsResponsibilities": [
            "Develop ML models",
            "Statistical analysis",
            "Communicate findings"
        ]
    },
    {
        "area": "Data Science",
        "level": "Senior",
        "toolsTechnologiesFrameworks": ["TensorFlow", "Deep Learning", "Docker", "Data wrangling"],
        "programmingLanguages": ["Python", "R"],
        "skillsResponsibilities": [
            "Lead model development",
            "Integrate data pipelines",
            "Advanced statistical techniques"
        ]
    },
    {
        "area": "Data Science",
        "level": "Lead",
        "toolsTechnologiesFrameworks": ["MLFlow", "Hyperparameter tuning", "Model monitoring"],
        "programmingLanguages": ["Python", "R"],
        "skillsResponsibilities": [
            "Oversee DS projects",
            "Ensure reproducibility",
            "Manage model lifecycles",
            "Lead A/B testing"
        ]
    },
    {
        "area": "Data Science",
        "level": "Architect",
        "toolsTechnologiesFrameworks": ["Model scaling", "AI Ethics and Bias", "Cross-functional collaboration"],
        "programmingLanguages": ["Python", "Optional: Julia"],
        "skillsResponsibilities": [
            "Define AI/ML strategy",
            "Oversee collaboration",
            "Set DS standards"
        ]
    },
    {
        "area": "AI Engineering",
        "level": "Junior",
        "toolsTechnologiesFrameworks": ["TensorFlow", "Keras", "PyTorch", "Jupyter", "Basic ML"],
        "programmingLanguages": ["Python", "Optional: Julia"],
        "skillsResponsibilities": [
            "Support AI model development",
            "Perform data wrangling for AI models"
        ]
    },
    {
        "area": "AI Engineering",
        "level": "Mid",
        "toolsTechnologiesFrameworks": ["Model optimization", "NLP (spaCy)", "CNN/RNN models"],
        "programmingLanguages": ["Python", "R", "Julia"],
        "skillsResponsibilities": [
            "Develop AI models",
            "Implement deep learning algorithms",
            "Collaborate on AI projects"
        ]
    },
    {
        "area": "AI Engineering",
        "level": "Senior",
        "toolsTechnologiesFrameworks": ["Deep Learning frameworks", "GANs", "Transformer models", "Reinforcement Learning", "ONNX"],
        "programmingLanguages": ["Python", "Optional: C++"],
        "skillsResponsibilities": [
            "Lead AI projects",
            "Design advanced model architectures",
            "Hyperparameter tuning",
            "Scale AI models"
        ]
    },
    {
        "area": "AI Engineering",
        "level": "Lead",
        "toolsTechnologiesFrameworks": ["Advanced NLP", "MLOps (TensorFlow Serving)", "AI deployment at scale"],
        "programmingLanguages": ["Python", "Optional: Julia", "Rust"],
        "skillsResponsibilities": [
            "Oversee AI deployments",
            "Set AI standards and frameworks",
            "Ensure scalability and performance"
        ]
    },
    {
        "area": "AI Engineering",
        "level": "Architect",
        "toolsTechnologiesFrameworks": ["AI ethics", "Responsible AI", "Distributed ML", "Federated Learning"],
        "programmingLanguages": ["Python", "Optional: Julia"],
        "skillsResponsibilities": [
            "Define AI architecture and governance",
            "Oversee AI ethics and compliance",
            "Set strategic direction for AI initiatives"
        ]
    }
]

def count_tokens(prompt):
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(prompt)
    return len(tokens)

def extract_text(file_path):
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == '.pdf':
        text = extract_pdf_text(file_path)
    elif file_extension.lower() == '.docx' or file_extension.lower() == '.doc':
        text = extract_docx_text(file_path)
    else:
        raise ValueError('Formato de archivo no soportado.')
    return text

def extract_docx_text(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def get_chatgpt_response(client, prompt):
    response = client.chat.completions.create(
        messages=prompt,
        model="gpt-3.5-turbo",
        max_tokens=2500,
        temperature=0.5
    )
    return response.choices[0].message.content

def determine_user_levels(tools_matches, languages_matches, skills_matches, positions):
    user_levels = {}
    for position in positions:
        area = position['area']
        level = position['level']
        total_items = 0
        total_score = 0

        # For toolsTechnologiesFrameworks
        for item in position['toolsTechnologiesFrameworks']:
            if "Optional" not in item:
                total_items += 1
            if item in tools_matches[area]['Explicit Matches']:
                total_score += 1
            elif item in tools_matches[area]['Implicit Matches']:
                total_score += 0.8
            elif item in tools_matches[area]['Probable Matches']:
                total_score += 0.5

        # For programmingLanguages
        for item in position['programmingLanguages']:
            if "Optional" not in item:
                total_items += 1
            if item in languages_matches[area]['Explicit Matches']:
                total_score += 1
            elif item in languages_matches[area]['Implicit Matches']:
                total_score += 0.8
            elif item in languages_matches[area]['Probable Matches']:
                total_score += 0.5

        # For skillsResponsibilities
        for item in position['skillsResponsibilities']:
            if "Optional" not in item:
                total_items += 1
            if item in skills_matches[area]['Explicit Matches']:
                total_score += 1
            elif item in skills_matches[area]['Implicit Matches']:
                total_score += 0.8
            elif item in skills_matches[area]['Probable Matches']:
                total_score += 0.5

        match_percentage = (total_score / total_items) * 100 if total_items > 0 else 0

        # Save the percentage score per area and per level
        if area not in user_levels:
            user_levels[area] = {}
        user_levels[area][level] = match_percentage

    return user_levels

def initialize_chatgpt_conversation(cv_text, user_data):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an AI assistant that helps analyze resumes to aid in career path planning. "
                "Your task is to extract relevant information from the candidate's CV and map it to predefined career paths and levels."
                "Answer only in json, please."
            )
        },
        {
            "role": "user",
            "content": (
                f"Here is the text extracted from a candidate's CV:\n\n{cv_text}\n\n"
                "We have also attempted to parse the CV automatically, but the extracted data may be incomplete or contain errors. "
                f"The parsed data is:\n{json.dumps(user_data, indent=2)}\n\n"
                "Please use this information as a reference, but rely primarily on the CV text for accurate information."
            )
        }
    ]
    return messages

def get_tools_prompt(positions):
    # Crear un diccionario para almacenar las herramientas por área
    area_tools = {}
    for position in positions:
        area = position['area']
        tools = position['toolsTechnologiesFrameworks']
        if area in area_tools:
            area_tools[area].extend(tools)
        else:
            area_tools[area] = tools.copy()
    for area, tools in area_tools.items():
        area_tools[area] = list(set(tools)).sort()
    prompt = (
        "Based on the CV text provided, identify which **Tools, Technologies, and Frameworks** the candidate is familiar with.\n\n"
        "Consider both explicit mentions and implicit knowledge based on the context, including projects or work experience.\n\n"
        "For each technology or framework, decompose it into its underlying sub-technologies or components to better infer skills.\n\n"

        "The predefined Tools, Technologies, and Frameworks for each area and level are:\n"
        f"{json.dumps(area_tools, indent=2)}\n\n"
        
        "For each area, provide three categorized lists:\n"
        "1. **Explicit Matches** (100% confidence - directly mentioned)\n"
        "2. **Implicit Matches** (80% confidence - strongly implied by role/project/technology)\n"
        "3. **Probable Matches** (60% confidence - reasonably assumed from context)\n\n"
        "Output the results in JSON format."
    )
    return prompt

def get_languages_prompt(positions):
    # Crear un diccionario para almacenar los lenguajes de programación por área
    area_languages = {}
    for position in positions:
        area = position['area']
        languages = position['programmingLanguages']
        if area in area_languages:
            area_languages[area].extend(languages)
        else:
            area_languages[area] = languages.copy()
    for area, languages in area_languages.items():
        area_languages[area] = list(set(languages)).sort()
    prompt = (
        "Based on the CV text provided, identify the **Programming Languages** the candidate is proficient in based on the CV text.\n\n"
        "Consider both explicit mentions and implicit knowledge based on the context, including projects or work experience.\n\n"
        "For each technology or framework, decompose it into its underlying sub-technologies or components to better infer skills.\n\n"

        "The predefined Programming Languages for each area and level are:\n"
        f"{json.dumps(area_languages, indent=2)}\n\n"
        
        "For each area, provide three categorized lists:\n"
        "1. **Explicit Matches** (100% confidence - directly mentioned)\n"
        "2. **Implicit Matches** (80% confidence - strongly implied by role/project/technology)\n"
        "3. **Probable Matches** (60% confidence - reasonably assumed from context)\n\n"
        "Output the results in JSON format."
    )
    return prompt

def get_skills_prompt(positions):
    # Crear un diccionario para almacenar las habilidades y responsabilidades por área
    predefined_skills = {}
    for position in positions:
        area = position['area']
        skills = position['skillsResponsibilities']
        if area in predefined_skills:
            predefined_skills[area].extend(skills)
        else:
            predefined_skills[area] = skills.copy()
    for area, skills in predefined_skills.items():
        predefined_skills[area] = list(set(skills)).sort()
    prompt = (
        "Based on the CV text provided, identify the user's **Skills and Responsibilities** based on the CV text.\n\n"
        "Consider both explicit mentions and implicit knowledge based on the context, including projects or work experience.\n\n"
        "For each technology or framework, decompose it into its underlying sub-technologies or components to better infer skills.\n\n"

        "The predefined Skills and Responsibilities for each area and level are:\n"
        f"{json.dumps(predefined_skills, indent=2)}\n\n"
        
        "For each area, provide three categorized lists:\n"
        "1. **Explicit Matches** (100% confidence - directly mentioned)\n"
        "2. **Implicit Matches** (80% confidence - strongly implied by role/project/technologie)\n"
        "3. **Probable Matches** (60% confidence - reasonably assumed from context)\n\n"
        "Output the results in JSON format."
    )
    return prompt


load_dotenv()
clientOpenAI = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
)

nltk.download('stopwords')
nltk.download('punkt')

# Verificar si el modelo 'en_core_web_sm' está instalado
try:
    spacy.load('en_core_web_sm')
except OSError:
    download('en_core_web_sm')

def main():
    file_path = sys.argv[1]
    print("Procesando archivo: ", file_path)
    # Extrae el texto del archivo
    text = extract_text(file_path)
    data = ResumeParser(file_path).get_extracted_data()
    user_data = {
        "name": data.get("name"),
        "email": data.get("email"),
        "mobile_number": data.get("mobile_number"),
        "skills": data.get("skills"),
        "college_name": data.get("college_name"),
        "designation": data.get("designation"),
        "education": data.get("degree"),
        "experience": data.get("experience"),
        "company_names": data.get("company_names"),
        "no_of_pages": data.get("no_of_pages"),
        "total_experience": data.get("total_experience"),
        "text": text
    }
    print("\n\n\n")
    print("Archivo Procesado.")

    # Initialize the conversation
    messages = initialize_chatgpt_conversation(text, user_data)
    # Prompt 1: Tools, Technologies, and Frameworks
    tools_prompt = get_tools_prompt(positions)
    messages.append({"role": "user", "content": tools_prompt})
    tools_response = get_chatgpt_response(clientOpenAI, messages)
    tools_response = tools_response.replace("```json", '').replace("```", '').strip()
    

    # Guarda el mensaje en un archivo plano
    with open("tools_response.txt", "w") as f:
        f.write(json.dumps(messages, indent=2))
        f.write(tools_response)
    messages.pop()
    print("prompt 1 finalizado")

    # Prompt 2: Programming Languages
    languages_prompt = get_languages_prompt(positions)
    messages.append({"role": "user", "content": languages_prompt})
    languages_response = get_chatgpt_response(clientOpenAI, messages)
    languages_response = languages_response.replace("```json", '').replace("```", '').strip()

    with open("languages_response.txt", "w") as f:
        f.write(json.dumps(messages, indent=2))
        f.write(languages_response)
    messages.pop()
    print("prompt 2 finalizado")


    # Prompt 3: Skills and Responsibilities
    skills_prompt = get_skills_prompt(positions)
    messages.append({"role": "user", "content": skills_prompt})
    skills_response = get_chatgpt_response(clientOpenAI, messages)
    skills_response = skills_response.replace("```json", '').replace("```", '').strip()

    with open("skills_response.txt", "w") as f:
        f.write(json.dumps(messages, indent=2))
        f.write(skills_response)
    messages.pop()
    print("prompt 3 finalizado")

    # print(f"tools_response: {tools_response}")
    # print(f"languages_response: {languages_response}")
    # print(f"skills_response: {skills_response}")


    tools_matches = json.loads(tools_response)
    languages_matches = json.loads(languages_response)
    skills_matches = json.loads(skills_response)

    user_levels = determine_user_levels(tools_matches, languages_matches, skills_matches, positions)
    for area, info in user_levels.items():
        print(f"Area: {area}")
        print(f"  Level: {info['level']}")
        print(f"  Confidence Score: {info['score']:.2f}%")

    print("\n\n\n")
    print("Tools Matches:")
    print(tools_matches)
    print("\n\n\n")
    print("Languages Matches:")
    print(languages_matches)
    print("\n\n\n")
    print("Skills Matches:")
    print(skills_matches)
    print("\n\n\n")


    exit()

if __name__ == "__main__":
    main()
