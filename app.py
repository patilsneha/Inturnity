import streamlit as st
import auth_view
import student_view
import constants


def main():
    # 1. Global Page Configuration
    st.set_page_config(
        page_title=constants.APP_NAME,
        page_icon="🚀",
        layout="wide"
    )

    # 2. Initialize Login State
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    # 3. Routing Logic
    if not st.session_state.logged_in:
        auth_view.show_auth_page()
    else:
        # Check user role and route accordingly
        role = st.session_state.get('role', 'student').lower()

        if role == 'admin':
            st.info("Admin Panel Placeholder")  # You can add admin_view here later
            student_view.display_student_dashboard()
        else:
            student_view.display_student_dashboard()


if __name__ == "__main__":
    main()