import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# --- Page Config ---
st.set_page_config(
    page_title="Savour Restaurant Assistant",
    page_icon="🍽️",
    layout="centered"
)

# --- Styling ---
st.markdown("""
<style>
    .main { background-color: #0f0f0f; }
    .stChatMessage { border-radius: 12px; }
    .restaurant-header {
        text-align: center;
        padding: 1rem 0;
        border-bottom: 1px solid #2a2a2a;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="restaurant-header">
    <h2>🍽️ Savour Restaurant</h2>
    <p style="color: #888; font-size: 14px;">AI-powered customer assistant — ask me anything!</p>
</div>
""", unsafe_allow_html=True)

# --- System Prompt ---
SYSTEM_PROMPT = """You are a friendly, helpful AI assistant for Savour, a Pakistani-fusion restaurant in DHA Phase 5, Karachi.

Restaurant Information:
- Name: Savour Restaurant
- Location: DHA Phase 5, Karachi, Pakistan
- Hours: Monday–Thursday 12pm–11pm | Friday–Sunday 12pm–12am
- Phone/WhatsApp for reservations: 0300-1234567
- Parking: Available on-site

Menu Highlights:
- Desi BBQ Platter (PKR 1,800)
- Karahi Chicken (PKR 1,200)
- Biryani Bowl — Chicken or Beef (PKR 900)
- Pakistani-Italian Fusion Pasta (PKR 1,100)
- Paneer Karahi — vegetarian (PKR 1,000)
- Daal Makhani — vegetarian (PKR 750)
- Veggie Pasta — vegetarian (PKR 950)
- Soft drinks & juices: PKR 200–350
- Specialty chai & desserts: PKR 150–500

Dietary Options:
- Vegetarian: Yes (paneer karahi, daal makhani, veggie pasta)
- Halal: Yes, fully halal certified

Delivery:
- Available via foodpanda and Cheetah

Events & Private Dining:
- Private dining room available for up to 30 guests
- Contact via WhatsApp: 0300-1234567

Rules:
- Only answer questions about Savour Restaurant
- If asked something unrelated, politely redirect
- Keep responses friendly, concise, and helpful
- Always encourage reservations for groups of 6 or more"""

# --- Initialize Groq Client ---
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("⚠️ GROQ_API_KEY not found. Add it to your Streamlit secrets.")
    st.stop()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=api_key,
    temperature=0.0
)

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Suggested Questions ---
if not st.session_state.messages:
    st.markdown("**Quick questions:**")
    cols = st.columns(2)
    suggestions = [
        "What are your opening hours?",
        "Do you have vegetarian options?",
        "How do I make a reservation?",
        "Show me your menu"
    ]
    for i, suggestion in enumerate(suggestions):
        with cols[i % 2]:
            if st.button(suggestion, key=f"sug_{i}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": suggestion})
                st.rerun()

# --- Display Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Handle Input ---
if prompt := st.chat_input("Ask anything about Savour..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(""):
            # Build LangChain message history
            langchain_messages = [SystemMessage(content=SYSTEM_PROMPT)]
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    langchain_messages.append(HumanMessage(content=msg["content"]))
                else:
                    langchain_messages.append(AIMessage(content=msg["content"]))

            response = llm.invoke(langchain_messages)
            reply = response.content
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
