import streamlit as st
from ollama import Client
import ollama
from googlesearch import search
import requests
import pdftotext
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from langdetect import detect
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.hasher import Hasher
import yaml
from yaml.loader import SafeLoader

# Gotta be on top of the file
st.set_page_config(page_title="AI-Powered Web Search", layout="wide", page_icon="app/favicon.ico")

with open('app/secret.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
#    config['preauthorized']
)

name, authentication_status, username = authenticator.login(fields={'Form name':'Login', 'Password':'Password', 'Login':'Login'})

if authentication_status:

    # Streamlit UI
    st.title("AI-Powered Web Search Summarization with CGC")

    query = st.text_input("Enter your question to do a web search:", placeholder="What is the capital of France?")

    #Save user prompt and timestamp to a file. 
    def savePromptToFile(prompt):
        with open("user_prompt.txt", "a") as file:
            file.write(f'{now.strftime("%d-%m-%Y %H:%M:%S")} - {prompt}\n') 

    # PDF file upload
    uploaded_file = st.file_uploader('Or choose your .pdf file to answer on its basis', type="pdf")

    st.caption("Higher values make the output more accurate, but it may take longer to generate.")

    # Only show the number of search results slider if no PDF is uploaded
    if not uploaded_file:
        search_option = st.radio("Search option:", ["Automatic search", "Custom URLs"], index=0)
        if search_option == "Automatic search":
            num_results = st.slider("Number of search results:", min_value=1, max_value=5, value=3, step=1)
        else:
            custom_urls = st.text_area("Enter URLs (one per line, max 5):", height=100)
        word_limit = st.slider("Word limit per page:", min_value=1000, max_value=7000, value=3500, step=250)
    else:
        word_limit = st.slider("Word limit per PDF file:", min_value=1000, max_value=25000, value=10000, step=500)



    # Change timezone to Poland
    now = datetime.now()
    now = now + timedelta(hours=2)

    # Putting in single-line
    summary_focus, summary_length = st.columns(2)
    summary_length = summary_length.radio("Summary Length:", ["Short", "Medium", "Long"], index=1)
    focus_options = ["Main Points", "Details", "Examples", "Statistics", "Custom"]
    summary_focus = summary_focus.radio("Summary Focus:", focus_options)

    # Make sure that the user enters a custom focus if they select it
    if summary_focus == "Custom":
        custom_focus = st.text_area("Enter your custom focus:", height=100)
        if custom_focus:
            summary_focus = custom_focus
        else:
            st.warning("Please enter a custom focus or select one of the predefined options.")

    # Sidebar
    with st.sidebar:
        st.image("app/comtegra_logo.png")
        temperature = st.slider("AI Temperature:", min_value=0.0, max_value=1.0, value=0.2, step=0.1)
        st.caption("Higher temperature makes the output more random, lower temperature makes it more deterministic.")
        with st.expander("Prompt history: "):
            st.subheader("10 latest user prompts:")
            with open("user_prompt.txt", "r", encoding='utf-8', errors='ignore') as file: #Reads the file and displays the last 10 lines with a max of 150 characters
                lines = file.readlines()
                for line in reversed(lines[-10:]):
                    if len(line) > 150:
                        st.write("- " + line.strip()[:150] + "...")
                    else:
                        st.write("- " + line.strip())

        st.subheader("About")
        st.write("AI Search Engine is an innovative tool that combines the functionalities of a search engine and a conversational AI assistant. It allows users to ask questions in natural language and provides accurate, context-aware responses by leveraging advanced artificial intelligence and natural language processing technologies. Its ability to provide accurate and contextually relevant answers can save time and resources, making it a valuable asset in decision-making processes and operational efficiency.")
        st.write("Made with ❤️ by [Comtegra S.A.](https://cgc.comtegra.cloud)")
        st.subheader("Wsparcie")
        st.caption("Jeśli masz jakiekolwiek pytania, zapraszamy do kontaktu")
        st.write("[ai@comtegra.pl](mailto:ai@comtegra.pl)")

        # Add logout button
        authenticator.logout("Logout", "sidebar")

    # Initialize Ollama client
    client = Client(host="http://localhost:9001")
    default_model = "SpeakLeash/bielik-11b-v2.2-instruct:Q8_0" # Adjust the model as needed

    # Function to scrape content from a URL
    def scrape_content(url):
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['nav', 'header', 'footer', 'aside', 'script', 'style']):
                element.decompose()
        
            # Remove elements with common class names for non-content areas
            for element in soup(class_=['menu', 'sidebar', 'nav', 'footer', 'header', 'search']):
                element.decompose()
        
            # Get text and remove extra whitespace
            text = ' '.join(soup.stripped_strings)
            words = text.split()
            return ' '.join(words[:word_limit])  # Apply word_limit here
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching {url}: {e}")
            return ""
    

    # Function to generate summary
    def generate_summary(query):
        if summary_focus != "Custom":
            prompt = f"""Analyze and answer ONLY this question: '{query}'. Use only the following information sources: {combined_content}

            Instructions:
            1. Respond only in {query_language}.
            2. Provide a {summary_length_words[summary_length]}-word answer in clear paragraphs.
            3. Start with a direct, concise answer to the main question.
            4. {focus_prompt}
            5. Include relevant facts, figures, or examples from the sources.
            6. Acknowledge any information gaps or contradictions.
            7. Use objective, authoritative language similar to an expert in the field.
            8. Include step-by-step explanations or lists if needed.
            9. End with a brief summary or key takeaway.
            10. Do not repeat the question.

            Important: Remember answer ONLY this question: '{query}'.

            Only use the provided sources. If you can't answer based on this information, clearly state so."""
                
            response = ollama.chat(
                model=default_model,  # Adjust the model as needed
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                options={"temperature": temperature}
            )
            summary = response['message']['content']
            return summary
        elif summary_focus == "Custom":
            prompt = f"""Analyze and answer this question: '{query}'. Use only the following information sources: {combined_content}

            Instructions:
            {custom_focus}

            Important: Remember to answer ONLY this question: '{query}'.

            Only use the provided sources. If you can't answer based on this information, clearly state so."""

            response = ollama.chat(
                model=default_model, # Adjust the model as needed
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                options={"temperature": temperature}
            )
            summary = response['message']['content']
            return summary
        elif uploaded_file:
            prompt = f"""Analyze and answer ONLY this question: '{query}'. Use only the following information sources: {combined_content}

            Instructions:
            1. Respond only in {query_language}.
            2. Provide a {summary_length_words[summary_length]}-word answer in clear paragraphs.
            3. Start with a direct, concise answer to the main question.
            4. {focus_prompt}
            5. Include relevant facts, figures, or examples from the sources.
            6. Acknowledge any information gaps or contradictions.
            7. Use objective, authoritative language similar to an expert in the field.
            8. Include step-by-step explanations or lists if needed.
            9. End with a brief summary or key takeaway.
            10. Do not repeat the question.

            Important: Remember answer ONLY this question: '{query}'.

            Only use the provided sources. If you can't answer based on this information, clearly state so."""
            
            response = ollama.chat(
                model=default_model, # Adjust the model as needed
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                options={"temperature": temperature}
            )
            summary = response['message']['content']
            return summary

    # Function to generate related questions
    def generate_related_questions(query, summary, num_questions=3):
        prompt = f"""Based on the following query and summary, generate {num_questions} related questions in the same language as the original query ({query_language}):

        Original query: {query}
        Summary: {summary}

        Instructions:
        1. Generate {num_questions} concise, relevant questions that explore related topics or dive deeper into aspects of the original query.
        2. Each question should be on a new line and start with a number and a period (e.g., "1. ").
        3. Use ONLY the language of the original query ({query_language}). Do not use any other language.
        4. Do not include any introductory or concluding text, only the numbered questions.

        Remember: All questions MUST be in {query_language}.
        """

        response = ollama.chat(
            model=default_model,  # Adjust the model as needed
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={"temperature": temperature}
        )
        related_questions = response['message']['content']
        return related_questions



    # Function to convert PDF to text
    def pdf_to_text(uploaded_file):
        try:
            pdf = pdftotext.PDF(uploaded_file)
            text = ""
            for page in pdf:
                words = page.split()
                text += ' '.join(words)
                if len(text.split()) >= word_limit:
                    break
            return ' '.join(text.split()[:word_limit])
        except:
            st.error("Error processing PDF file. Please try again with a different file.")
            return ""

    if st.button("Search") or query:
        if query and not uploaded_file:
            with st.spinner("Thinking..."):
                # Perform Google search or use custom URLs
                if search_option == "Automatic search":
                    search_results = list(search(query, num_results=num_results))
                else:
                    custom_url_list = [url.strip() for url in custom_urls.split('\n') if url.strip()]
                    if len(custom_url_list) > 5:
                        st.warning("Limit of 5 URLs exceeded. Only the first 5 URLs will be used.")
                    search_results = custom_url_list[:5]
                
                #Save user prompt to a file
                savePromptToFile(query)
                
                # Scrape content from search results
                contents = []
                for url in search_results:
                    content = scrape_content(url)
                    contents.append(content)
                
                # Combine contents and create a prompt for the LLM
                combined_content = "\n\n".join(contents)

                # Detect language in which you should respond
                query_language = "pl"


                # Modify the prompt to include customizable summarization
                summary_length_words = {"Short": "100-150", "Medium": "200-250", "Long": "300-350"}
                focus_instructions = {
                    "Main Points": "Focus on the main points and key information.",
                    "Details": "Include more details and additional information.",
                    "Examples": "Provide specific examples, if available.",
                    "Statistics": "Include relevant statistics and figures, if available."
                }

                # summary_focus twice because it's the default value returned
                focus_prompt = focus_instructions.get(summary_focus, summary_focus) 
                
                # Generate summary using Llama 3.1
                summary = generate_summary(query)
                
                # Display results
                st.subheader("Summary")
                st.write(summary)
                
                # Generate related questions
                st.subheader("Related Questions")
                related_questions = generate_related_questions(query, summary)
                st.write(related_questions)
                
                # Display sources
                st.subheader("Sources:")
                for url in search_results:
                    st.write(url)
        elif uploaded_file and query: #Answers based on a PDF file
            with st.spinner("Processing file..."):
                
                combined_content = pdf_to_text(uploaded_file)

                if not combined_content:
                    pass
                else:
                    #Save user prompt to a file
                    savePromptToFile(query)

                # Detect language in which you should respond
                query_language = "pl"

                # Modify the prompt to include customizable summarization
                summary_length_words = {"Short": "100-150", "Medium": "200-250", "Long": "300-350"}
                focus_instructions = {
                    "Main Points": "Focus on the main points and key information.",
                    "Details": "Include more details and additional information.",
                    "Examples": "Provide specific examples, if available.",
                    "Statistics": "Include relevant statistics and figures, if available."
                }

                focus_prompt = focus_instructions.get(summary_focus, summary_focus)

                # Generate summary using Llama 3.1
                summary = generate_summary(query) # combined_content here is the PDF text

                # Display results
                st.subheader("Summary")
                st.write(summary)

                # Generate related questions
                st.subheader("Related Questions")
                related_questions = generate_related_questions(query, summary)
                st.write(related_questions)

                # Display source
                st.subheader("Source:")
                st.write(uploaded_file.name)
                
        else:
            st.warning("Please enter a question/file")

elif authentication_status == False:
    st.error("Username or password is incorrect")
elif authentication_status == None:
    st.warning("Please enter username and password")