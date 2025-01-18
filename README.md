# Shopy: An AI-Powered Shopping Agent

[![Project Status](https://img.shields.io/badge/Status-In%20Development-yellow)](https://github.com/your-username/shopy-agent)
[![License](https://img.shields.io/badge/License-MIT-blue)](https://opensource.org/licenses/MIT)

**Shopy** is an AI-powered shopping agent designed to provide users with a streamlined and decisive online shopping experience. By leveraging web search, data parsing, product comparison, and content creation, Shopy delivers tailored recommendations based on user queries.

## Key Features

*   **Intelligent Web Search:** Utilizes Tavily API for robust and comprehensive product searches.
*   **Data Parsing & Structuring:** Employs AI models (Gemini) to structure and analyze product data.
*   **Product Comparison:** Compares products based on specs and reviews to provide recommendations.
*   **YouTube Review Integration:** Includes relevant YouTube review links for enhanced product insights.
*   **Personalized Recommendations:** Delivers tailored product recommendations based on user queries.
*   **Email Delivery:** Optional email delivery of personalized recommendations (planned).

## Architecture

Shopy is built as a multi-agent system using LangGraph, which enables a modular, scalable, and robust workflow. The main components are:

*   **Tavily Search Agent:** Responsible for searching product information online.
*   **Data Structuring Agent:** Maps the search results to a structured format.
*   **Product Comparison Agent:** Compares products based on extracted data and available reviews.
*   **YouTube Review Agent:** Fetches relevant video reviews from YouTube.
*   **Email Agent:** (Planned) Sends personalized recommendations to users.

## Technologies Used

*   **LangChain:** For multi-agent orchestration and tooling.
*   **LangGraph:** For defining the agent workflow.
*   **Gemini API:** For natural language processing and data structuring.
*   **Tavily API:** For robust web search.
*   **YouTube API:** For video review retrieval. (planned)
*   **Python:** As the primary programming language.
*   **Pydantic:** For data validation.
*   **python-dotenv:** For managing environment variables.
*   **Rich:** For formatted console output.

## Getting Started

### Prerequisites

*   Python 3.10 or higher
*   Git
*   A Google Cloud Platform project with the Gemini API enabled and a valid API key.
*   A Tavily API key
*  A YouTube API Key
*  A Gmail account with an App Password for email sending.

### Setup

1.  **Clone the repository:**
    ```bash
    git clone [repository URL]
    cd shopy-agent
    ```
2.  **Set up a virtual environment (optional but recommended):**
    ```bash
    python -m venv langenv
    source langenv/bin/activate # On macOS/Linux
    langenv\Scripts\activate # On Windows
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure environment variables:**
    * Create a `.env` file in the root directory.
    * Add your API keys, Gmail username and app password:
       ```
        GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
        TAVILY_API_KEY=YOUR_TAVILY_API_KEY
        YOUTUBE_API_KEY=YOUR_YOUTUBE_API_KEY
        GMAIL_USER=YOUR_GMAIL_USER_NAME
        GMAIL_PASS=YOUR_GMAIL_APP_PASSWORD
       ```

### Running the Application

1.  Navigate to the `shopy` directory.
    ```bash
    cd shopy
    ```
2.  Run the application:
    ```bash
    python -m shopy.main
    ```
3.  Follow the prompts to enter your product query and email.

Shopy/
├── shopy/
│ ├── pycache/
│ ├── configs/
│ │ └── config.py
│ ├── utils/
│ │ ├── init.py
│ │ └── rich_utils.py
│ ├── init.py
│ ├── agent.py
│ ├── llm.py
│ ├── main.py
│ ├── models.py
│ └── prompts.py
├── .env
├── README.md
└── requirements.txt


## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue to discuss improvements or bug fixes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For any questions or inquiries, please reach out to [my GitHub profile][def].

[def]: https://github.com/SBDI