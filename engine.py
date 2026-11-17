import pandas as pd
import os
import pickle
import constants
from sentence_transformers import util
import streamlit as st
from processor import model_engine

@st.cache_data
def load_job_embeddings(data_path, embeddings_path):
    """
    Loads internship data and handles automatic vector synchronization.
    FUTURE SCOPE: Transition to ChromaDB for million-scale high-speed indexing.
    """
    if not os.path.exists(data_path):
        return pd.DataFrame(), None

    # DATA INTEGRITY CHECK: Re-index if CSV has been updated more recently than the cache
    csv_time = os.path.getmtime(data_path)
    pkl_time = os.path.getmtime(embeddings_path) if os.path.exists(embeddings_path) else 0
    force_reindex = csv_time > pkl_time

    df = pd.read_csv(data_path).fillna("Not specified")

    # Ensure mapped columns are treated as strings to prevent encoding errors
    for col in [constants.COL_ROLE, constants.COL_COMPANY, constants.COL_SKILLS]:
        df[col] = df[col].astype(str)

    if os.path.exists(embeddings_path) and not force_reindex:
        with open(embeddings_path, "rb") as f:
            job_embeddings = pickle.load(f)
    else:
        # Construct context strings for semantic analysis
        contexts = (
                df[constants.COL_ROLE] + " " +
                df[constants.COL_COMPANY] + " " +
                df[constants.COL_SKILLS]
        ).tolist()

        # Vectorization via the cached SLM (Small Language Model)
        job_embeddings = model_engine.encode(contexts, convert_to_tensor=True)

        # Persistence: Save vectors to disk to avoid expensive re-computation
        with open(embeddings_path, "wb") as f:
            pickle.dump(job_embeddings, f)

    return df, job_embeddings


def get_recommendations(resume_embedding, user_skills):
    """
    Core Logic: Matches users to internships using a Semantic-Keyword Hybrid approach.
    """
    if not os.path.exists(constants.DATA_PATH):
        return []

    df, job_embeddings = load_job_embeddings(constants.DATA_PATH, constants.EMBEDDINGS_PATH)

    if job_embeddings is None:
        return []

    # AI Semantic Match: Calculate Cosine Similarity between Resume and Job Vectors
    cosine_scores = util.cos_sim(resume_embedding, job_embeddings)[0]

    results = []
    for i, score in enumerate(cosine_scores):
        base_score = float(score)

        # Deterministic Keyword Overlap Detection
        job_skills_raw = str(df.iloc[i][constants.COL_SKILLS]).lower()
        matched_keywords = [skill for skill in user_skills if skill.lower() in job_skills_raw]

        # HYBRID SCORING SYSTEM WITH SAFETY NET
        # Penalize high AI scores if there is zero technical keyword overlap (Prevents Hallucinations)
        if base_score > 0.7 and len(matched_keywords) == 0:
            final_score = base_score * 0.8
        else:
            # Grant a 5% heuristic boost per direct keyword match
            final_score = min(1.0, base_score + (len(matched_keywords) * 0.05))

        # Compile detailed job data for the Presentation Layer
        job_data = df.iloc[i].to_dict()
        job_data['match_score'] = round(final_score * 100, 1)
        job_data['matched_keywords'] = matched_keywords
        results.append(job_data)

    # Sort by descending Match Score and return top results
    return sorted(results, key=lambda x: x['match_score'], reverse=True)[:constants.TOP_K_RESULTS]