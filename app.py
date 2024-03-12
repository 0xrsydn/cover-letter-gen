import gradio as gr
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import LLMChain

#Get the OpenAI API key from the environment
openai_api_key = os.environ.get("OPENAI_API_KEY")

# Define the chain and LLM first
model = ChatOpenAI()
prompt = PromptTemplate.from_template("""
So, I am applying for {job_role} at {company_name}
=================
{company_context}
=================
{candidate_profile}
=================
From the company profile and my profile, please create a cover letter for the {job_role} position. Ensure that it is well-crafted and engaging for recruiters and hiring managers. Also, verify that my recent work experience and academic background align with the role I am applying for.
""")
output_parser = StrOutputParser()
chain = LLMChain(llm=model, prompt=prompt)

# Create Gradio interface function with topic as input
def generate_cover_letter(job_role, company_name, company_context, candidate_profile):
    output = chain.run(job_role=job_role, company_name=company_name, company_context=company_context, candidate_profile=candidate_profile)
    return output

# Create Gradio interface
gr.Interface(
    fn=generate_cover_letter,
    inputs=[
        gr.Textbox(label="Job Role", placeholder="Ex: Data Scientist, Fullstack Developer, etc."),
        gr.Textbox(label="Company Name", placeholder="Enter a company name you applying"),
        gr.Textbox(label="Company Context", placeholder="Enter a brief description of the company"),
        gr.Textbox(label="Candidate Profile", placeholder="Describe your professional background, key skills, and relevant experiences")
    ],
    outputs=gr.Textbox(label="Generated Cover Letter"),
    title="Cover Letter Generator",
    description="Generate a cover letter based on your job role, company, context, and profile."
).launch()
