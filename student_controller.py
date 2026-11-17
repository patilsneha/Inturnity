import streamlit as st
import processor
import engine


def initialize_student_state():
    """
    Ensures all required session keys exist for a persistent user context.
    Adds 'profile_score' for backend analytics.
    """
    keys = {
        'wishlist': [],
        'detected_skills': [],
        'recommendations': [],
        'profile_score': 0
    }
    for key, default in keys.items():
        if key not in st.session_state:
            st.session_state[key] = default


def calculate_profile_strength(text, skills):
    """
    BACKEND ANALYTICS: Logic to evaluate the quality of the uploaded resume.
    """
    score = 0
    # content depth check
    if len(text.split()) > 150: score += 40
    # contactability check
    if st.session_state.get('pdf_email') != "Not specified": score += 20
    # technical density check
    if len(skills) >= 4: score += 40

    st.session_state['profile_score'] = score
    return score


def handle_resume_upload(uploaded_file):
    """
    Orchestrates the data flow from raw PDF to AI-ranked recommendations.
    Implements redundancy prevention logic to save computational resources.
    """
    if uploaded_file is not None:
        # Generate a unique hash-like key for the current upload
        file_key = f"processed_{uploaded_file.name}_{uploaded_file.size}"

        # Logic: Only execute heavy AI pipeline if the file is new
        if st.session_state.get('last_processed_key') != file_key:
            with st.spinner("AI Engine is executing semantic mapping..."):
                # 1. Extraction Phase
                raw_text = processor.extract_text_from_pdf(uploaded_file)
                processor.extract_name(raw_text)
                processor.extract_email(raw_text)

                # 2. Level 1: Keyword Analysis
                skills = processor.get_detected_skills(raw_text)
                st.session_state['detected_skills'] = skills

                # 3. Backend Analytics: Profile Strength
                calculate_profile_strength(raw_text, skills)

                # 4. Level 2: Semantic Analysis & Ranking
                resume_emb = processor.get_embedding(raw_text)
                st.session_state['recommendations'] = engine.get_recommendations(
                    resume_emb, skills
                )

                # Update key to prevent re-processing
                st.session_state['last_processed_key'] = file_key
                return True
    return False