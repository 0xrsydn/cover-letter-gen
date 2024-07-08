import gradio as gr
import os
import fitz  # PyMuPDF
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Set the API key as an environment variable
os.environ["GROQ_API_KEY"] #if using Open AI change to "OPENAI_API_KEY"

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text("text")
    return text

# Function to split text into chunks
def split_text_into_chunks(text, chunk_size=1000, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    chunks = text_splitter.split_text(text)
    return chunks

# Function to create vector store
def create_vector_store(chunks):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.from_texts(chunks, embeddings)
    return vector_store

# Function to perform RAG
def perform_rag(vector_store, query):
    retriever = vector_store.as_retriever()
    docs = retriever.get_relevant_documents(query)
    context = " ".join([doc.page_content for doc in docs])
    return context

# Function to parse output
def parse_output(output):
    # Directly access the content of the AIMessage object
    output_content = output.content
    start_index = output_content.find('content="') + len('content="')
    end_index = output_content.rfind('"')
    parsed_content = output_content[start_index:end_index]
    parsed_content = parsed_content.replace('\\n', '\n')
    return parsed_content

# Create Gradio interface function with topic as input
def generate_cover_letter(pdf_path, job_role, company_name, company_context):
    # Extract text from PDF
    text = extract_text_from_pdf(pdf_path)
    # Split text into chunks
    chunks = split_text_into_chunks(text)
    # Create vector store
    vector_store = create_vector_store(chunks)
    # Perform RAG
    candidate_profile = perform_rag(vector_store, job_role)

    # Load the Groq model
    chat = ChatGroq(
        temperature=0.5,
        model="llama3-70b-8192", #define model available on Groq
        api_key=os.getenv("GROQ_API_KEY")
    )

    # Define the prompt
    system = "You are expert career coach and consultant. You will generate well made and proper cover letetr based on user profile and user input."
    human = """
    So, I am applying for {job_role} at {company_name}
    =================
    {company_context}
    =================
    {candidate_profile}
    =================
    From the company profile and my profile, please create a cover letter for the {job_role} position. Ensure that it is well-crafted and engaging for recruiters and hiring managers. Also, verify that my recent work experience and academic background align with the role I am applying for.
    """
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

    # Define LangChain
    chain = prompt | chat
    output = chain.invoke({"job_role": job_role, "company_name": company_name, "company_context": company_context, "candidate_profile": candidate_profile})
    # Parse output
    parsed_output = parse_output(output)
    
    return parsed_output

# Create Gradio interface
gr.Interface(
    fn=generate_cover_letter,
    inputs=[
        gr.File(label="Upload ATS Resume (PDF)", file_types=[".pdf"]),
        gr.Textbox(label="Job Role", placeholder="Ex: Data Scientist, Fullstack Developer, etc."),
        gr.Textbox(label="Company Name", placeholder="Enter a company name you applying"),
        gr.Textbox(label="Company Context", placeholder="Enter a brief description of the company")
    ],
    outputs=gr.Textbox(label="Generated Cover Letter", show_copy_button=True),
    title="Cover Letter Generator",
    description="Generate a cover letter based on your job role, company, context, and profile."
).launch()
