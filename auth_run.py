import streamlit as st
import auth_view

# 1. SET PAGE CONFIG
st.set_page_config(page_title="INTURNITY", layout="wide")


def main():
    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "role" not in st.session_state:
        st.session_state.role = None

    # 2. CHECK LOGIN STATUS
    if not st.session_state.logged_in:
        auth_view.show_auth_page()
    else:
        # 3. TEMP PLACEHOLDER (No imports needed)
        st.balloons()
        with st.sidebar:
            st.title("INTURNITY")
            st.write(f"Logged in as: **{st.session_state.full_name}**")
            st.write(f"Role: **{st.session_state.role.upper()}**")
            if st.button("LOGOUT"):
                st.session_state.logged_in = False
                st.rerun()

        if st.session_state.role == 'admin':
            st.header("🛠️ Admin Dashboard Placeholder")
            st.success("Authentication successful! You are recognized as an Admin.")
        else:
            st.header("🎓 Student Dashboard Placeholder")
            st.success("Authentication successful! You are recognized as a Student.")

        st.info("To see your actual dashboard, we will link student_view.py next!")


if __name__ == "__main__":
    main()