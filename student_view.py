import streamlit as st
import student_controller  # Handles the logic
import constants
import auth
import pandas as pd
import base64
import os


def get_base64_img(file_path):
    """Encodes asset images to base64 for CSS injection."""
    try:
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                data = f.read()
            return base64.b64encode(data).decode()
    except Exception as e:
        print(f"Error loading asset: {e}")
    return None


def display_student_dashboard():
    # --- 1. INITIALIZE LOGIC ---
    student_controller.initialize_student_state()

    # --- 2. UI THEME & CSS ---
    grid_base64 = get_base64_img("grid.png")

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cedarville+Cursive&display=swap');

        /* Background Grid Pattern */
        .stApp {{
            background-image: url("data:image/png;base64,{grid_base64 if grid_base64 else ''}");
            background-repeat: repeat;
            background-size: 180px; 
            background-attachment: fixed;
        }}

        /* Sidebar Color Styling (#481F01) */
        [data-testid="stSidebar"] {{
            background-color: #481F01 !important; 
        }}

        /* Sidebar Typography */
        [data-testid="stSidebar"] *, [data-testid="stSidebar"] p, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h1 {{
            color: #FDF5E6 !important; 
        }}

        /* Main Header Styles */
        .dashboard-title {{
            color: #111;
            font-family: 'Courier New', monospace;
            text-align: left;
            font-size: 48px;
            font-weight: bold;
            letter-spacing: 8px;
            margin-bottom: -5px;
            padding-top: 10px;
        }}

        .dashboard-tagline {{
            font-family: 'Cedarville Cursive', cursive;
            color: #444;
            font-size: 24px;
            text-align: left;
            margin-top: -10px;
            margin-bottom: 20px;
        }}

        /* Content Card Styling */
        [data-testid="stVerticalBlockBorderWrapper"] {{
            background-color: rgba(255, 255, 255, 0.92);
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            border: 1px solid rgba(0,0,0,0.05);
        }}
        </style>

        <div class="dashboard-title">{constants.APP_NAME}</div>
        <div class="dashboard-tagline">{constants.TAGLINE}</div>
        """,
        unsafe_allow_html=True
    )
    st.divider()

    # --- 3. SIDEBAR UI ---
    with st.sidebar:
        st.markdown("## 🎓 **STUDENT**")
        st.divider()
        st.header("👤 Your Profile")

        st.write(f"**Username:** {st.session_state.get('username', 'N/A')}")
        st.write(f"**Name:** {st.session_state.get('student_name', 'New User')}")
        st.write(f"**Email:** {st.session_state.get('pdf_email', 'Upload Resume...')}")

        st.divider()
        st.subheader("⭐ Your Wishlist")
        if st.session_state['wishlist']:
            for item in st.session_state['wishlist']:
                with st.expander(f"📌 {item.get(constants.COL_ROLE)}"):
                    st.write(f"**Company:** {item.get(constants.COL_COMPANY)}")
                    st.write(f"**Match Score:** {item.get('match_score')}%")
        else:
            st.info("Your wishlist is empty.")

        st.divider()
        st.write("### 🛠️ Detected Skills")
        if st.session_state['detected_skills']:
            for skill in st.session_state['detected_skills']:
                st.info(f"✔ {skill}")
        else:
            st.caption("No skills detected yet.")

        if st.button("Logout 🔓", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    # --- 4. MAIN INTERFACE ---
    uploaded_file = st.file_uploader("Upload your Resume (PDF format)", type="pdf")

    # Call Controller to handle file processing
    if student_controller.handle_resume_upload(uploaded_file):
        st.rerun()

    # Display Recommendations UI
    if st.session_state['recommendations'] and uploaded_file is not None:
        st.subheader(f"🎯 Top 5 Recommendations")

        for job in st.session_state['recommendations']:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"### {job.get(constants.COL_ROLE, 'Not specified')}")
                    st.markdown(f"**🏢 {job.get(constants.COL_COMPANY, 'Not specified')}**")
                    st.markdown(f"📍 **Location:** {job.get(constants.COL_LOCATION, 'Not specified')}")
                    st.markdown(f"💰 **Stipend:** {job.get(constants.COL_STIPEND, 'Not specified')}")

                    matches = job.get('matched_keywords', [])
                    if matches:
                        st.caption(f"✨ Direct Matches: {', '.join(matches)}")

                with col2:
                    st.metric("Match Score", f"{job['match_score']}%")

                    job_id = job.get(constants.COL_ID)
                    is_saved = any(item.get(constants.COL_ID) == job_id for item in st.session_state['wishlist'])

                    if is_saved:
                        st.button("Saved ✅", key=f"s_{job_id}", disabled=True, use_container_width=True)
                    else:
                        if st.button("Wishlist ⭐", key=f"w_{job_id}", use_container_width=True):
                            st.session_state['wishlist'].append(job)
                            auth.save_wishlist(st.session_state.get('username'), st.session_state['wishlist'])
                            st.rerun()

                    link = job.get(constants.COL_LINK)
                    if pd.notna(link) and str(link).startswith("http"):
                        st.link_button("Apply 🔗", link, use_container_width=True)
                    else:
                        st.button("No Link 🚫", key=f"nl_{job_id}", disabled=True, use_container_width=True)