# 🍽️ Savour Restaurant AI Assistant

An AI-powered customer service chatbot for a Pakistani-fusion restaurant, built using Claude API and Streamlit. Demonstrates how small businesses can automate customer queries with a conversational AI assistant.

## 🚀 Live Demo
[👉 Try it here](https://your-streamlit-link-here) *(deploy to Streamlit Cloud and update this link)*

## 💡 Features
- 💬 Multi-turn conversation with memory across the session
- 🍛 Answers questions about menu, hours, reservations, delivery, and events
- ⚡ Quick-reply suggestion buttons for common questions
- 🔒 System prompt knowledge base — stays on-topic, never hallucinates outside scope
- 📱 Clean, mobile-friendly UI

## 🛠 Tech Stack
| Component | Technology |
|-----------|------------|
| LLM | Claude Sonnet (Anthropic API) |
| Framework | Streamlit |
| Language | Python |

## ⚙️ How It Works
1. Restaurant info (menu, hours, policies) is embedded in a structured system prompt
2. User sends a message → passed to Claude API with full conversation history
3. Claude responds in context, staying strictly within the restaurant's knowledge base
4. Conversation memory maintained via Streamlit session state

## 🏃 Setup & Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/mutahir-ahmed-ai/savour-restaurant-chatbot
cd savour-restaurant-chatbot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your API key
Create `.streamlit/secrets.toml`:
```toml
ANTHROPIC_API_KEY = "your-anthropic-api-key-here"
```

### 4. Run
```bash
streamlit run app.py
```

## 🚀 Deploy to Streamlit Cloud
1. Push repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repo → set `ANTHROPIC_API_KEY` in secrets
4. Deploy

## 💼 Business Use Case
This chatbot template can be adapted for any business — restaurants, clinics, salons, retail stores — replacing the system prompt knowledge base with their specific information. Typical setup time: under 2 hours per client.

## 📬 Contact
Built by [Mutahir Ahmed](https://www.linkedin.com/in/mutahir-ahmed-8229341b5) — open to freelance AI projects.
