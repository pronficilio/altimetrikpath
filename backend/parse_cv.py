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
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
from positions import positions

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
        model="gpt-4o",
        max_tokens=2500,
        temperature=0.666
    )
    return response.choices[0].message.content

def determine_user_levels(tools_matches, languages_matches, skills_matches, positions):
    user_levels = {}
    missing_tools = {}
    missing_languages = {}
    missing_skills = {}
    for position in positions:
        area = position['area']
        level = position['level']
        total_items = 0
        total_score = 0
        if area not in missing_tools:
            missing_tools[area] = {}
            missing_languages[area] = {}
            missing_skills[area] = {}

        # For toolsTechnologiesFrameworks
        for item in position['toolsTechnologiesFrameworks']:
            if "Optional" not in item:
                total_items += 1
            if area in tools_matches and item in tools_matches[area]['Explicit Matches']:
                total_score += 1
            elif area in tools_matches and item in tools_matches[area]['Implicit Matches']:
                total_score += 0.8
            elif area in tools_matches and item in tools_matches[area]['Probable Matches']:
                total_score += 0.5
            else:
                if level not in missing_tools[area]:
                    missing_tools[area][level] = []
                missing_tools[area][level].append(item)

        # For programmingLanguages
        for item in position['programmingLanguages']:
            if "Optional" not in item:
                total_items += 1
            if area in languages_matches and item in languages_matches[area]['Explicit Matches']:
                total_score += 1
            elif area in languages_matches and item in languages_matches[area]['Implicit Matches']:
                total_score += 0.8
            elif area in languages_matches and item in languages_matches[area]['Probable Matches']:
                total_score += 0.5
            else:
                if level not in missing_languages[area]:
                    missing_languages[area][level] = []
                missing_languages[area][level].append(item)

        # For skillsResponsibilities
        for item in position['skillsResponsibilities']:
            if "Optional" not in item:
                total_items += 1
            if area in skills_matches and item in skills_matches[area]['Explicit Matches']:
                total_score += 1
            elif area in skills_matches and item in skills_matches[area]['Implicit Matches']:
                total_score += 0.8
            elif area in skills_matches and item in skills_matches[area]['Probable Matches']:
                total_score += 0.5
            else:
                if level not in missing_skills[area]:
                    missing_skills[area][level] = []
                missing_skills[area][level].append(item)

        match_percentage = (total_score / total_items) * 100 if total_items > 0 else 0

        # Save the percentage score per area and per level
        if area not in user_levels:
            user_levels[area] = {}
        user_levels[area][level] = match_percentage

    return {
        "current": user_levels,
        "missing_tools": missing_tools,
        "missing_languages": missing_languages,
        "missing_skills": missing_skills
    }

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
        },
        {
            "role": "system",
            "content": (
                "Based on the CV text provided, identify which **Tools, Technologies, and Frameworks**, **Programming Languages** and **Skills and Responsibilities**  the candidate is familiar or proficient in based on the CV text.\n\n"
                "Consider both explicit mentions and implicit knowledge based on the context, including projects, work experience, and years of experience in each role.\n\n"
                "For each technology or framework, decompose it into its underlying sub-technologies or components to better infer skills.\n\n"
                "Make reasonable assumptions about tool proficiency based on years of experience - e.g., a developer with 5+ years likely knows common tools even if not explicitly mentioned.\n\n"
                "For each area, provide three categorized lists:\n"
                "1. **Explicit Matches** (100% confidence - directly mentioned)\n"
                "2. **Implicit Matches** (80% confidence - strongly implied by role/project/technology)\n"
                "3. **Probable Matches** (60% confidence - reasonably assumed from context and experience)\n\n"
                "Please provide the results in JSON format with the following structure:\n\n"
                "```json\n"
                "{\n"
                '  "tools": {\n'
                '    "area1": {\n'
                '      "Explicit Matches": [],\n'
                '      "Implicit Matches": [],\n'
                '      "Probable Matches": []\n'
                '    },\n'
                '    "area2": {\n'
                '      "Explicit Matches": [],\n'
                '      "Implicit Matches": [],\n'
                '      "Probable Matches": []\n'
                '    }\n'
                '  },\n'
                '  "languages": {\n'
                '    "area1": {\n'
                '      "Explicit Matches": [],\n'
                '      "Implicit Matches": [],\n'
                '      "Probable Matches": []\n'
                '    },\n'
                '    "area2": {\n'
                '      "Explicit Matches": [],\n'
                '      "Implicit Matches": [],\n'
                '      "Probable Matches": []\n'
                '    }\n'
                '  },\n'
                '  "skills": {\n'
                '    "area1": {\n'
                '      "Explicit Matches": [],\n'
                '      "Implicit Matches": [],\n'
                '      "Probable Matches": []\n'
                '    },\n'
                '    "area2": {\n'
                '      "Explicit Matches": [],\n'
                '      "Implicit Matches": [],\n'
                '      "Probable Matches": []\n'
                '    }\n'
                '  }\n'
                '}\n'
                "```"
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
        area_tools[area] = list(set(tools))
    prompt = (
        "The predefined Tools, Technologies, and Frameworks for each area and level are:\n"
        f"{json.dumps(area_tools, indent=2)}\n\n"
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
        area_languages[area] = list(set(languages))
    prompt = (
        "The predefined Programming Languages for each area and level are:\n"
        f"{json.dumps(area_languages, indent=2)}\n\n"
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
        predefined_skills[area] = list(set(skills))
    prompt = (
        "The predefined Skills and Responsibilities for each area and level are:\n"
        f"{json.dumps(predefined_skills, indent=2)}\n\n"
    )
    return prompt


load_dotenv()
clientOpenAI = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
)

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

# Verificar si el modelo 'en_core_web_sm' está instalado
try:
    spacy.load('en_core_web_sm')
except OSError:
    download('en_core_web_sm', quiet=True)

def main():
    file_path = sys.argv[1]
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
        "gpt_response": None
    }

    # Initialize the conversation
    messages = initialize_chatgpt_conversation(text, user_data)

    # Prompt 1: Tools, Technologies, and Frameworks
    tools_prompt = get_tools_prompt(positions)
    messages.append({"role": "user", "content": tools_prompt})
    # tools_response = get_chatgpt_response(clientOpenAI, messages)
    # tools_response = tools_response.replace("```json", '').replace("```", '').strip()

    # Prompt 2: Programming Languages
    languages_prompt = get_languages_prompt(positions)
    messages.append({"role": "user", "content": languages_prompt})
    # languages_response = get_chatgpt_response(clientOpenAI, messages)
    # languages_response = languages_response.replace("```json", '').replace("```", '').strip()

    # Prompt 3: Skills and Responsibilities
    skills_prompt = get_skills_prompt(positions)
    messages.append({"role": "user", "content": skills_prompt})
    # skills_response = get_chatgpt_response(clientOpenAI, messages)
    # skills_response = skills_response.replace("```json", '').replace("```", '').strip()

    response = get_chatgpt_response(clientOpenAI, messages)
    response = response.replace("```json", '').replace("```", '').strip()

    # guarda el mensaje y respuesta en archivos logs
    with open("logs.txt", "w") as f:
        f.write(response)
    with open("messages.txt", "w") as f:
        f.write(json.dumps(messages, indent=2))

    # Parsea la respuesta en formato JSON
    response_dict = json.loads(response)

    tools_matches = response_dict['tools']
    languages_matches = response_dict['languages']
    skills_matches = response_dict['skills']

    user_levels = determine_user_levels(tools_matches, languages_matches, skills_matches, positions)

    user_data["career_path"] = user_levels
    # Imprime en formato JSON
    print(json.dumps(user_data, indent=2))

    exit()

if __name__ == "__main__":
    main()
