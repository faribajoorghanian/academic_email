import streamlit as st
from chains import Chain
from utils import fetch_google_scholar_data

def create_streamlit_app(llm):
    st.title("📚 Academic Email Generator")

    # User inputs
    st.header("Input Your Information")
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    degree = st.text_input("Highest Degree (e.g., MSc in Computer Science)")
    university = st.text_input("University")
    gpa = st.text_input("GPA")
    research_interests = st.text_area("Research Interests")
    major = st.text_area("Major")
    rank = st.text_area("University Rank")
    academic_year = st.text_area("Academic Year")
    skills = st.text_area("Relevant Skills (comma-separated)")
    previous_institution = st.text_area("Previous Institution/Company")
    experience = st.text_area("Relevant Experience/Projects")
    scholar_url = st.text_input("Professor's Google Scholar URL or Research Area")
    upload_cv = st.file_uploader("Upload Your Existing CV (optional)", type=["tex", "pdf", "docx"])

    submit_button = st.button("Generate Email")

    if submit_button:
        # Handle missing required fields
        if not name or not email or not degree or not university:
            st.warning("Please fill in all required fields (Full Name, Email, Degree, University).")
            return
        if not scholar_url:
            st.warning("Please provide a Professor's Google Scholar URL or Research Area.")
            return

        try:
            # Handle user data
            user_data = {
                "name": name,
                "email": email,
                "degree": degree,
                "university": university,
                "gpa": gpa,
                "research_interests": research_interests,
                "major": major,
                "rank": rank,
                "academic_year": academic_year,
                "skills": skills,
                "previous_institution": previous_institution,
                "experience": experience,
            }

            # Fetch professor's details
            professor_data = fetch_google_scholar_data(scholar_url)
            
            # Handle missing professor data
            if "error" in professor_data:
                st.error(f"Failed to fetch professor details: {professor_data['error']}")
                return

            # Generate email
            email_text = llm.create_email(user_data, professor_data)

            # Display email
            st.header("Generated Email")
            st.markdown(email_text)
        except Exception as e:
            st.error(f"An Error Occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    st.set_page_config(layout="wide", page_title="Academic Email Creator", page_icon="📚")
    create_streamlit_app(chain)

