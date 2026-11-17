import pdfplumber
import re
import constants
import streamlit as st
from sentence_transformers import SentenceTransformer


# --- MODEL LOADING (PREVENTS HANGING) ---
@st.cache_resource
def load_processor_model():
    """
    Loads the SLM model once and caches it.
    Moving this here prevents circular imports between engine and processor.
    """
    return SentenceTransformer(constants.SLM_MODEL)


# Initialize the model engine
model_engine = load_processor_model()


def extract_text_from_pdf(file):
    """Extracts raw text from an uploaded PDF file."""
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                content = page.extract_text()
                if content:
                    text += content + "\n"
    except Exception as e:
        print(f"Error during PDF extraction: {e}")
    return text


def extract_name(text):
    """
    Extracts the candidate's name from the top of the resume.
    Updates session state for the sidebar.
    """
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    name = "Candidate"

    if lines:
        # Check first 3 lines, skipping common document headers
        for line in lines[:3]:
            if len(line) > 2 and line.lower() not in ['resume', 'cv', 'curriculum vitae', 'contact']:
                name = line
                break

    st.session_state['student_name'] = name
    return name


def extract_email(text):
    """
    Uses Regex to find an email address in the text.
    Updates session state for the 3rd point in the sidebar profile.
    """
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(pattern, text)
    email = match.group(0) if match else "Not specified"

    st.session_state['pdf_email'] = email
    return email


def get_detected_skills(text):
    """
    Level 1 Extraction: Keyword matching against the Master Skill Library.
    Uses regex word boundaries to avoid partial matches.
    """
    detected = []
    text_lower = text.lower()

    for skill in constants.SKILL_LIBRARY:
        # \b ensures we match 'c' but not 'canva'
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower):
            detected.append(skill)

    unique_skills = sorted(list(set(detected)))
    st.session_state['detected_skills'] = unique_skills
    return unique_skills


def get_embedding(text):
    """
    Passes text to the SLM model to get AI vectors.
    Used for semantic matching.
    """
    return model_engine.encode(text, convert_to_tensor=True)