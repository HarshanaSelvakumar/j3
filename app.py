import streamlit as st
import pandas as pd
import os

# File paths
USER_FILE = "users.csv"

# Initialize users file
if not os.path.exists(USER_FILE):
    df = pd.DataFrame(columns=["username", "password", "role"])
    df.to_csv(USER_FILE, index=False)

jobs = []
applications = []

if 'user' not in st.session_state:
    st.session_state.user = None

def load_users():
    return pd.read_csv(USER_FILE)

def save_user(username, password, role):
    df = load_users()
    if username in df['username'].values:
        return False
    df_new = pd.DataFrame([{"username": username, "password": password, "role": role}])
    df = pd.concat([df, df_new], ignore_index=True)
    df.to_csv(USER_FILE, index=False)
    return True

def validate_login(username, password):
    df = load_users()
    user = df[df['username'] == username]
    if not user.empty and user.iloc[0]['password'] == password:
        return user.iloc[0]['role']
    return None

def register():
    st.title("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["job_seeker"])
    if st.button("Register"):
        if save_user(username, password, role):
            st.success("Registered successfully. Please login.")
        else:
            st.error("Username already exists.")

def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        role = validate_login(username, password)
        if role:
            st.session_state.user = {"username": username, "role": role}
            st.success("Login successful!")
        else:
            st.error("Invalid credentials.")

def admin_dashboard():
    st.title("Admin Dashboard")
    st.subheader("Post a Job")
    title = st.text_input("Job Title")
    description = st.text_area("Job Description")
    if st.button("Post Job"):
        jobs.append({"title": title, "description": description})
        st.success("Job posted.")

    st.subheader("Applications")
    for app in applications:
        st.markdown(f"**{app['username']}** applied for **{app['job']}** - Status: {app['status']}")
        if st.button(f"Approve {app['username']} - {app['job']}"):
            app['status'] = "Approved"
        if st.button(f"Reject {app['username']} - {app['job']}"):
            app['status'] = "Rejected"

def job_seeker_dashboard():
    st.title("Job Seeker Dashboard")
    st.subheader("Available Jobs")
    for i, job in enumerate(jobs):
        st.markdown(f"**{job['title']}**: {job['description']}")
        if st.button(f"Apply for {job['title']} - {i}"):
            applications.append({
                "username": st.session_state.user["username"],
                "job": job["title"],
                "status": "Pending"
            })
            st.success("Application submitted.")

    st.subheader("My Applications")
    for app in applications:
        if app["username"] == st.session_state.user["username"]:
            st.markdown(f"Applied for **{app['job']}** - Status: {app['status']}")

def main():
    menu = ["Login", "Register"]
    if st.session_state.user:
        if st.session_state.user["role"] == "admin":
            admin_dashboard()
        else:
            job_seeker_dashboard()
        if st.button("Logout"):
            st.session_state.user = None
    else:
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "Login":
            login()
        else:
            register()

if __name__ == "__main__":
    main()
