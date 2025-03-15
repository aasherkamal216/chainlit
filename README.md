# Chainlit Chatbot

## Description

This project is a simple chatbot application built using Chainlit and Litellm. It allows users to send text and images to the chatbot, which then processes the input and generates a response using the Gemini 2.0 Flash model.

## Features

-   **Text Input:** Users can send text messages to the chatbot.
-   **Image Input:** Users can send images to the chatbot, which are processed and included in the message context.
-   **Streaming Responses:** The chatbot provides streaming responses, displaying the output as it's generated.
-   **Chat History:** The chatbot maintains a chat history, allowing for contextual conversations.

## Prerequisites

- Python 3.11+
- UV package manager
- Google Gemini API Key

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create and Activate Virtual Environment**

    ```bash
    uv venv
    .venv\Scripts\activate  # On Windows
    ```

3.  **Install the dependencies:**

    ```bash
    uv sync
    ```

4. **Set up environment variables:**
    ```bash
    cp .env.example .env
    ```
    Then add your API Keys in `.env`

## Usage

Run the chatbot using this command:

```bash
chainlit run src/chatbot/app.py -w
```

This command starts the Chainlit application, which will open in your web browser on http://localhost:8000/. You can then start interacting with the chatbot by sending text messages and images.
