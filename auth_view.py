import streamlit as st
import auth
import constants
import base64
import os
import pandas as pd
import json


def get_image_as_base64(file):
    """
    Converts your typewriter.png into a base64 string
    for seamless CSS injection.
    """
    if os.path.exists(file):
        with open(file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None


def show_auth_page():
    # 1. FETCH THE ASSET
    typewriter_base64 = get_image_as_base64("typewriter.png")
    typewriter_css = f"url('data:image/png;base64,{typewriter_base64}')" if typewriter_base64 else "none"

    # 2. INJECT FINAL REFINED CSS
    st.markdown(f"""
        <style>
        /* THE MAIN APP CONTAINER */
        .stApp {{
            background-image: {typewriter_css} !important;
            background-size: cover !important; 
            background-position: center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
        }}

        [data-testid="stHeader"] {{ background: transparent !important; }}
        [data-testid="stAppViewContainer"]::before {{ content: none !important; }}

        /* THE MAIN APP TITLE */
        .auth-header {{ 
            color: #111; 
            font-family: 'Courier New', monospace; 
            text-align: center; 
            font-size: 42px; 
            font-weight: bold;
            letter-spacing: 6px;
            margin-top: 5px !important; 
            margin-bottom: -10px !important;
        }}

        /* THE TABS */
        .stTabs {{
            background: transparent !important; 
            border: none !important;
            max-width: 320px; 
            margin: 98px auto 0px auto !important; 
            position: relative;
            z-index: 10;
        }}

        [data-baseweb="tab-list"] {{ justify-content: center !important; }}

        button[data-baseweb="tab"] {{ 
            color: #670626 !important; 
            font-family: 'Courier New', monospace !important; 
            font-weight: bold !important;
        }}

        /* INPUT BLOCKS */
        .stTextInput input {{
            background-color: rgba(255, 255, 255, 0.3) !important;
            border: none !important;
            border-bottom: 1px dashed rgba(0,0,0,0.3) !important;
            font-family: 'Courier New', monospace !important;
            text-align: center;
            font-size: 14px !important;
            margin-top: 8px !important; 
            margin-left: 22px !important; 
            width: 240px !important;
            color: #111 !important;
        }}

        /* THE ACTION BUTTON */
        .stButton>button {{
            background-color: #111 !important;
            color: white !important;
            font-family: 'Courier New', monospace !important;
            border-radius: 2px !important;
            letter-spacing: 2px !important;
            position: fixed;
            bottom: 15%; 
            left: 50%;
            transform: translateX(-50%);
            width: 240px !important;
            z-index: 100;
            border: none !important;
        }}

        .stAlert {{
            margin-top: 10px !important;
            margin-left: 22px !important;
            width: 240px !important;
        }}
        </style>
        <div class="auth-header">{constants.APP_NAME}</div>
    """, unsafe_allow_html=True)

    # 3. INTERFACE TABS & AUTH LOGIC
    tab1, tab2 = st.tabs([" LOGIN ", " REGISTER "])

    with tab1:
        u = st.text_input("ID", placeholder="USERNAME", key="l_user", label_visibility="collapsed")
        p = st.text_input("PW", type="password", placeholder="PASSWORD", key="l_pass", label_visibility="collapsed")

        if st.button("LOGIN", use_container_width=False, key="login_btn"):
            user_data = auth.verify_user(u, p)
            if user_data:
                st.session_state.logged_in = True
                st.session_state.username = u  # Correct Username mapping
                st.session_state.full_name = user_data.get('full_name', 'User')
                st.session_state.role = user_data.get('role', 'student')

                # Load Wishlist
                saved_wish = user_data.get('wishlist')
                if pd.notna(saved_wish) and str(saved_wish).strip() != "":
                    try:
                        st.session_state['wishlist'] = json.loads(saved_wish)
                    except:
                        st.session_state['wishlist'] = []
                else:
                    st.session_state['wishlist'] = []

                st.rerun()
            else:
                st.error("ACCESS DENIED")

    with tab2:
        new_u = st.text_input("NEW_ID", placeholder="CHOOSE USERNAME", key="r_user", label_visibility="collapsed")
        new_p = st.text_input("NEW_PW", type="password", placeholder="PASSWORD", key="r_p",
                              label_visibility="collapsed")
        conf_p = st.text_input("CONF_PW", type="password", placeholder="CONFIRM PASSWORD", key="r_cp",
                               label_visibility="collapsed")
        admin_code = st.text_input("ADMIN CODE", placeholder="ADMIN CODE (OPTIONAL)", type="password", key="r_admin",
                                   label_visibility="collapsed")

        if st.button("CREATE ACCOUNT", use_container_width=False, key="reg_btn"):
            if not new_u or not new_p:
                st.warning("All fields required.")
            elif new_p != conf_p:
                st.warning("Passwords do not match.")
            else:
                assigned_role = 'admin' if admin_code == constants.ADMIN_PASSCODE else 'student'
                if auth.add_user(new_u, new_p, role=assigned_role):
                    st.success("ACCOUNT CREATED")
                else:
                    st.error("USERNAME TAKEN")