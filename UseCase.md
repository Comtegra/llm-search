# Guide to Using the AI-Powered Web Search Summarization Tool on CGC

This tutorial will guide you through using the AI-Powered Web Search Summarization tool deployed on the [Comtegra GPU Cloud (CGC)](https://cgc.comtegra.cloud/).

## Brief Introduction

The AI-Powered Web Search Summarization tool on CGC enhances online research by integrating advanced web scraping techniques with state-of-the-art AI analysis. This application simplifies the process of gathering, synthesizing, and summarizing information from various web sources. It converts complex search queries into concise, actionable summaries, saving researchers time and providing a clear overview of any topic. The tool also supports PDF summarization, enabling users to extract key information from uploaded documents.

## AI Models Used

This tool can utilize any AI model compatible with Ollama. For this specific application, we use:

1. SpeakLeash/bielik-11b-v2.2-instruct:Q8_0:
   - 11 billion parameters
   - 32,768 token context window
   - Enhanced NLP capabilities
   - Improved training data
   - Flexible deployment options

While this app is configured to use SpeakLeash/bielik-11b-v2.2-instruct:Q8_0, users can easily configure other compatible models based on their specific needs.


## Understanding the Platform

The [Comtegra GPU Cloud (CGC)](https://cgc.comtegra.cloud/) is a powerful cloud computing platform designed for AI and data science workloads. It offers:

1. **GPU-accelerated computing**: Access to high-performance GPUs for accelerated computations in AI, machine learning, and data processing tasks.

2. **Versatile resource management**: Manage resources using the CGC CLI (Command Line Interface) to create, list, and delete compute, storage, and network resources.

3. **Web-accessible resources**: Secure web-accessible URLs for each compute resource.

4. **File management**: Access storage resources via a user-friendly file browser.

5. **Diverse compute options**:
   - Jupyter notebooks with pre-installed TensorFlow or PyTorch
   - Triton inferencing server for large-scale inference
   - Label Studio for data annotation tasks
   - RAPIDS suite for accelerated data processing

6. **Database engines**: PostgreSQL and Weaviate, accessible within your namespace.

7. **CUDA-ready environment**: Notebooks include CUDA libraries and GPU drivers for seamless GPU utilization.

CGC combines the power of GPU computing with the flexibility of cloud resources, making it an ideal platform for AI-powered applications like the Web Search Summarization Tool.

## Prerequisites

- Access to the [Comtegra GPU Cloud (CGC)](https://cgc.comtegra.cloud/) platform (use the data provided in the welcome e-mail)
- Login credentials (username and password)
   - These can be set in the `secret.yaml` file for secure storage and easy configuration
- PDF files for summarization (optional)

## Step-by-Step Guide

### 1. [Setting up CGC Environment](https://docs.cgc.comtegra.cloud/Getting%20Started/installation)
a. Create a volume:
```
cgc volume create <my_volume> -s 30
```
b. Create a compute instance:
```
cgc compute create --name <my_instance> -c 6 -m 24 -g 1 -gt A5000 -v <my_volume> nvidia-pytorch
```
### 2. Installing dependencies
a. Access the Jupyter notebook environment provided by CGC.

b. Open and run the "softstack.ipynb" file to install all necessary dependencies.

### 3. Setting up Ollama
a. Start the Ollama service:
```
ollama serve
```
b. Pull the required models:
```
ollama pull SpeakLeash/bielik-11b-v2.2-instruct:Q8_0
```
> **Note**: Run `ollama serve` in one terminal window and pull models in a separate terminal window to avoid conflicts.

### 4. Starting the Application
a. Start the Streamlit app:
```
streamlit run app/app.py --server.port <your_open_port> --server.baseUrlPath=/<your_base_path>
```
> **Note**: If you're unsure how to open a port or configure your network settings, please refer to the CGC documentation at [https://docs.cgc.comtegra.cloud/](https://docs.cgc.comtegra.cloud/Network-management/custom-ports). The documentation provides detailed instructions on managing network resources and configuring ports for your compute instances. For information on custom port configuration, check the Network Management category.


### 5. Accessing the Application

Navigate to the application URL in your web browser:

https://resource-name.namespace.region.comtegra.cloud/<your_base_path>

### 6. Authentication

Log in using your provided credentials:
- Username: `test`
- Password: `test`

### 7. Formulating Your Query

In the main input field, enter your research question. For example:

`"What are the most promising advancements in solar panel efficiency in the last year?"`

### 8. PDF Summarization

To summarize a PDF instead of performing a web search:

1. **Upload your PDF**: Click on "Drag and drop file here" and select your file.
2. **Ask your question**: Enter your query about the PDF content in the main input field.
3. **Customize settings**: Adjust the summarization parameters to fit your needs.
4. **Generate summary**: Click the "Search" button to analyze the PDF and create a summary.
5. **Review results**: Examine the AI-generated summary based on your PDF's content.

> **Tip**: This feature is perfect for quickly extracting key information from lengthy documents or research papers.

### 9. Customizing the Search

Adjust the search parameters to fit your needs:

- **Number of search results**: 4 (for a broader range of sources)
- **Word limit per page**: 3500 (to capture more detailed information)
- **Summary length**: Medium
- **Summary focus**: Main Points
- **AI model**: SpeakLeash/bielik-11b-v2.2-instruct:Q8_0
- **Temperature**: 0.2 (adjusts the level of creativity in the AI's output; lower values produce more precise and predictable results)

> **Tip**: Experiment with these settings to find the best combination for your research needs.

### 10. Initiating the Search

Click the "Search" button to start the process. The application will:
1. Perform a Google search based on your query
2. Scrape content from the user-selected number of top results
3. Analyze and summarize the information using the selected AI model
4. Provide a list of related questions for further exploration

> **Note**: For PDF summarization, the summary will be based on the content of the uploaded document rather than web search results.

### 11. Reviewing the Results

Examine the generated summary, which will include content based on the options selected:
- A concise answer to your main question
- Key points related to your query
- Relevant statistics and examples from the sources
- Any other details as chosen in the search customization

### 12. Exploring Related Questions

Below the summary, you'll find a list of AI-generated related questions. Use these to:
- Gain new perspectives on your topic
- Identify areas for further research

### 13. Verifying Sources

At the bottom of the page, you'll find a list of source URLs. Always check these to:
- Verify the credibility of the information
- Access the original articles for more in-depth reading

### 14. Viewing Query History

The application keeps track of your search queries along with timestamps. This feature allows you to:
- Review your past searches
- Track the progression of your research
- Easily revisit previous topics

You can find your query history in two places:

1. In the "user_prompt.txt" file, which logs all queries with their respective timestamps.
2. On the sidebar of the application in an expandable section, where the 10 latest user prompts are displayed for quick reference.

The sidebar display provides a convenient way to see your most recent queries at a glance, while the full history in the text file allows for more comprehensive review of your search patterns over time.


### 15. Iterative Research

Use the tool for iterative research:
1. Start with a broad query
2. Use the results and related questions to refine your focus
3. Conduct follow-up searches on specific aspects of your topic

## Troubleshooting

1. **CGC CLI Issues**:
   - If you encounter "Command not found" errors, ensure the CGC CLI is properly installed and added to your system PATH.
   - For authentication issues, verify your login credentials and try logging in again using `cgc register`.

2. **Resource Creation Problems**:
   - If volume or compute instance creation fails, check your account quotas and available resources in the CGC dashboard using `cgc status`.
   - Ensure you have the necessary permissions to create resources in your namespace.

3. **Ollama Service Errors**:
   - Missing Installation: Ollama might not start if it hasn't been downloaded or installed properly. Verify that the Ollama software is installed and accessible on your system.
   - If Ollama fails to start, check if the service is already running in another terminal.

4. **Model Download Issues**:
   - If model pulling fails, check your internet connection.
   - Ensure you have enough storage space in your volume for the models.

5. **Streamlit App Launch Problems**:
   - If the app doesn't start, verify that all dependencies are correctly installed.
   - Check if the specified port is already in use by another application.

6. **Application Access Issues**:
   - If you can't access the app URL, ensure your compute instance is running and the correct port is open.
   - Verify that you're using the correct base path in the URL.
   - If the app crashes frequently:
     - Check system logs for error messages.
     - Ensure you have sufficient resources (CPU, RAM, GPU memory) to run the selected AI model. For example, SpeakLeash/bielik-11b-v2.2-instruct:Q8_0 requires at least 16GB of GPU memory.

7. **Authentication Failures**:
   - Double-check the provided username and password.
   - Change username and password in the `secret.yaml` file and restart the app.

8. **Search Functionality Issues**:
   - If searches fail, check your internet connection and make sure Ollama is running.
   - Verify that the selected AI model is properly loaded and functioning.

9. **Performance Problems**:
   - If the application is slow, try reducing the number of search results or word limit per page.
   - Consider using a more powerful compute instance if consistent performance issues occur.

10. **Result Quality Issues**:
    - If summaries are irrelevant or low-quality, try adjusting the AI model, temperature, or summary focus settings.
    - Ensure your input query is clear and specific.

11. **PDF Upload Issues**:
    - Ensure your PDF file is not corrupted and is in a standard format.
    - Check that the file size doesn't exceed any limits set by the application.

If you encounter persistent issues not covered here, contact CGC support for further assistance.


## Best Practices

- Begin with clear, specific questions for the best results
- Adjust the search parameters based on the complexity of your topic
- Always verify information from the original sources
- For PDF summarization, use clear and specific questions related to the document's content
- Regularly review your query history to track your research progress and identify patterns in your inquiries

By following this tutorial, you can efficiently gather and summarize information on complex topics, accelerating your research process and identifying key areas for further investigation.