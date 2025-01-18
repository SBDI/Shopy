# Shopy: AI-Powered Shopping Agent
Shopy is an intelligent, multi-agent system designed to provide enhanced online shopping experiences. By combining web search, data parsing, product comparison, and content creation, Shopy delivers decisive recommendations tailored to each user's needs.

## Key Components:

*   **Tavily**: For robust web searches.
*   **Llama-3.1-70B**: For analyzing and structuring data.
*   **YouTube API**: To provide relevant video reviews.
*   **SMTP**: To facilitate email delivery of tailored recommendations.
*   **LangGraph**: For managing agent workflows and state.

## Getting Started

1.  **Clone the repository:**
    ```bash
    git clone [repository URL]
    cd shopy-rpos
    ```
2.  **Setup Environment:**

    *   Create a `.env` file in the root directory and add the necessary API keys:
       ```
        GROQ_API_KEY=YOUR_GROQ_API_KEY
        TAVILY_API_KEY=YOUR_TAVILY_API_KEY
        YOUTUBE_API_KEY=YOUR_YOUTUBE_API_KEY
        GMAIL_USER=YOUR_GMAIL_USER_NAME
        GMAIL_PASS=YOUR_GMAIL_APP_PASSWORD
       ```
    *   Install the dependencies
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the Application:**
    ```bash
    python shopy/main.py
    ```

   * By default, a mock LLM is used. To use a real LLM provider, please set the environment variable`GROQ_API_KEY` following the instuctions in the notebook.

4.  **Follow Prompt:**
    *   When prompted, enter your product query and email to begin the process.

    Note:
    - The Graphviz visualizaiton has been disabled by default for local use.