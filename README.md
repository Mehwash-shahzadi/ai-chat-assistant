# AI Chat Assistant

A modern AI-powered chat application that lets you have intelligent conversations with multiple language models. Built with Python, Streamlit, and FastAPI.

## About

AI Chat Assistant is a full-stack conversational AI platform where users can chat with different AI models through a clean web interface. The project includes user authentication, multiple AI model support, and a REST API backend.

Whether you're learning AI development, building a chatbot, or just exploring language models, this project provides a solid foundation with production-ready features like secure authentication and scalable architecture.

## Features

- **Multiple AI Models** - Choose between Mistral, Zephyr, and Llama models
- **Secure Authentication** - Password protection with bcrypt encryption
- **Real-time Chat** - Get instant responses from AI models
- **Adjustable Responses** - Control how long or short AI answers should be
- **Clean Interface** - Simple and intuitive user interface
- **REST API** - Backend API for easy integration
- **Session Management** - Keeps you logged in securely
- **Chat History** - See your conversation history
- **Quick Actions** - Pre-made buttons for common questions

## Tech Stack

- **Frontend:** Streamlit
- **Backend:** FastAPI
- **AI Models:** HuggingFace (Mistral, Zephyr, Llama)
- **Security:** Bcrypt password hashing
- **Language:** Python 3.8+

## Prerequisites

Before you start, make sure you have:

- Python 3.8 or higher installed
- pip package manager
- A HuggingFace account (free to create)

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/Mehwash-Shahzadi/ai-chat-assistant.git
cd ai-chat-assistant
```

2. **Create a virtual environment**

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the root directory and add your HuggingFace token:

```
HUGGINGFACE_API_TOKEN=your_token_here
```

You can get a free token from [HuggingFace Settings](https://huggingface.co/settings/tokens).

5. **Run the application**

Open two terminal windows:

**Terminal 1 - Start the backend:**

```bash
uvicorn backend.main:app --reload
```

**Terminal 2 - Start the frontend:**

```bash
streamlit run frontend/app.py
```

6. **Open your browser**

- Frontend: http://localhost:8501
- Backend API: http://localhost:8000

## Usage

### Getting Started

1. Open the app in your browser
2. Log in with username `demo` and password `demo123`
3. Start chatting with the AI!

### Switching Models

- Click the model dropdown in the sidebar
- Choose between Mistral, Zephyr, or Llama
- Your conversation continues with the new model

### Adjusting Responses

- Use the response length slider in the sidebar
- Choose between 50-300 tokens
- Shorter responses are faster, longer ones are more detailed

### Quick Actions

Click any of the quick action buttons for instant responses:

- Get a tech fact
- Hear a programming joke
- Learn a coding tip
- Understand an AI concept

## Project Structure

```
ai-chat-assistant/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── llm_service.py       # AI model integration
│   ├── auth.py              # Authentication logic
│   └── requirements.txt
├── frontend/
│   ├── app.py               # Main Streamlit app
│   ├── auth_ui.py           # Login page
│   └── requirements.txt
├── .env                      # Your API keys (create this)
├── .gitignore
├── README.md
└── requirements.txt
```

## Available Models

**Mistral** - Fast and smart, best for general questions
**Zephyr** - Conversational and friendly, great for chatting  
**Llama** - Advanced reasoning, good for complex topics

## API Documentation

Once the backend is running, visit http://localhost:8000/docs to see the interactive API documentation.

### Main Endpoints

- `GET /models` - Get list of available AI models
- `POST /query` - Send a message and get AI response
- `POST /login` - User authentication
- `POST /logout` - End session
- `POST /switch-model` - Change AI model

## Security

- Passwords are encrypted using bcrypt
- Session tokens for authentication
- Automatic logout after 24 hours
- No passwords stored in plain text

## Future Plans

- Save chat history to database
- Add voice input support
- Support multiple languages
- Docker deployment
- Deploy to cloud platforms

## Demo Accounts

For testing, you can use these accounts:

- Username: `demo` | Password: `demo123`
- Username: `admin` | Password: `admin123`

## Troubleshooting

**Backend not starting?**

- Make sure Python 3.8+ is installed
- Check that port 8000 is not in use
- Verify your HuggingFace token in .env file

**Frontend not loading?**

- Ensure backend is running first
- Check that port 8501 is available
- Try refreshing the browser

**Authentication errors?**

- Make sure backend is running
- Check your username and password
- Clear browser cache and try again

## Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

---
