import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import random

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.1-70b-versatile"
        )

    def create_email(self, user_data, professor_data):
        # Define several email prompts for variability
        email_prompts = [
            PromptTemplate.from_template(
                """
                ### USER INFORMATION:
                Name: {name}
                Degree: {degree}
                Major: {major}
                University: {university}
                Rank: {rank}
                GPA: {gpa}
                Academic Year: {academic_year}
                Research Interests: {research_interests}
                Relevant Skills: {skills}
                Previous Institution/Company: {previous_institution}
                Relevant Experience/Project: {experience}

                ### PROFESSOR INFORMATION:
                {professor_data}

                ### INSTRUCTION:
                Write a professional inquiry email to the professor for a PhD position, using the provided details.

                ### EMAIL TEMPLATE:
                Subject: Inquiry About PhD Position in {research_interests} at {university}

                Dear Dr. [Professor's Last Name],

                I hope this email finds you well. My name is {name}, and I hold a {degree} in {major} from {university}, ranked {rank}, with a GPA of {gpa}. 
                I am writing to express my interest in joining your lab as a PhD student for {academic_year}.

                I recently read your paper on [Specific Recent Paper Title] and was particularly inspired by [specific finding or aspect]. 
                My academic background and research experience in {major} have equipped me with strong skills in {skills}, 
                which align closely with your current work on [Specific Project or Research Area].

                In my previous role at {previous_institution}, I {experience}. I am confident that my expertise in {skills} 
                would allow me to contribute meaningfully to your lab’s ongoing projects.

                Attached is my CV for your review. I would be grateful for the opportunity to discuss how my background and skills align with your research goals. 
                Thank you for your time, and I look forward to hearing from you.

                Best regards,
                {name}
                """
            ),
            PromptTemplate.from_template(
                """
                ### USER INFORMATION:
                Name: {name}
                Degree: {degree}
                Major: {major}
                University: {university}
                Rank: {rank}
                GPA: {gpa}
                Academic Year: {academic_year}
                Research Interests: {research_interests}
                Relevant Skills: {skills}
                Previous Institution/Company: {previous_institution}
                Relevant Experience/Project: {experience}

                ### PROFESSOR INFORMATION:
                {professor_data}

                ### INSTRUCTION:
                Write a concise and polite email to the professor asking for a PhD position, with personalized details from the user’s profile.

                ### EMAIL TEMPLATE:
                Subject: PhD Position Inquiry: {research_interests} at {university}

                Dear Dr. [Professor's Last Name],

                I hope you're doing well. My name is {name}, and I am a {degree} graduate in {major} from {university}. I have a GPA of {gpa} and would be thrilled to explore the possibility of joining your lab for a PhD position in {academic_year}.

                I’ve followed your work, particularly your recent paper on [Recent Paper Title], and I was particularly interested in [specific aspect]. My academic background, combined with my skills in {skills}, would make me a great fit for your ongoing research on [Research Area].

                In my previous role at {previous_institution}, I {experience}, and I believe I can contribute to the innovative projects in your lab.

                I’ve attached my CV for your review and would be grateful for the opportunity to discuss my candidacy further.

                Best regards,
                {name}
                """
            ),
        ]

        # Randomly choose one of the email templates
        chosen_email_prompt = random.choice(email_prompts)

        email_text = (chosen_email_prompt | self.llm).invoke(user_data | {"professor_data": professor_data}).content

        return email_text
