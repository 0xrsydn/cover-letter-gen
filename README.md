# Cover Letter Generator

Tired of making personalized cover letter for specific company everytime you applying job? Also tired of applying hundred of jobs with different cover letters just to be rejected later? Well, let's just make it more efficient and less time consuming while keeping cover letter quality as good as possible with LLM powered app.

Cover Letter Generator is an AI-powered application that crafts personalized cover letters on the fly. Built with LangChain and Gradio library, it harnesses the power of ChatGPT to generate contextually relevant and engaging cover letters. Simply input your job role, target company's name & brief details, and your profile details (work experience, academic background, etc.) and let the magic happen!

![Application Interface](img/Screenshot_53.png)

## Getting Started

These instructions will help you set up the project locally on your machine.

### Prerequisites

To run this application, you will need to have:

- A Python environment running Python 3.6 or newer.
- An OpenAI API Key (stored in local environment).
- Required libraries (LangChain, Gradio, etc.).

### Installation

1. Clone this repository with the command:

    ```bash
    git clone https://github.com/0xrsydn/cover-letter-gen.git
    ```

2. Install the required libraries with the command:

    ```bash
    pip install -r requirements.txt
    ```
   
3. Run the application with the command:

    ```bash
    python app.py
    ```

Your application should now be running on local URL, `http://127.0.0.1:7860`.

## Usage

Fill in the required fields:

1. Input your target job role, e.g., `Software Engineer`.
2. Input the company's name, e.g., `Google Inc.`
3. Provide a brief detail about the target company, e.g., `A multinational tech company specializing in internet-related products and services.`
4. Describe your profile (work experiences, academic background, etc.), e.g., `Graduated with a Computer Science degree and have 4 years of experience as a backend engineer.`

Click the "Generate" button and behold! Your tailor-made cover letter is crafted instantly.

## Live Demo

You can check my live demo hosted on [Hugging Face Spaces](https://huggingface.co/spaces/0xrsydn/cover-letter-gen).
![Huggingface Image](img/hf-logo.svg)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### Note

As with all AI outputs, generated cover letters should be reviewed and thoroughly checked before use. The developer holds no liability for any inaccuracies or issues arising from the use of generated content.

Constructive criticisms and suggestions are always welcome.
