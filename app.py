import os
import streamlit as st
from anthropic import Anthropic

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

# --- System Prompt (Restaurant Knowledge Base) ---
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
- Vegan options: Limited — ask staff
- Halal: Yes, fully halal certified

Delivery:
- Available via foodpanda and Cheetah
- No direct delivery

Events & Private Dining:
- Private dining room available for up to 30 guests
- Corporate dinners, family gatherings, birthday events
- Contact via WhatsApp to book: 0300-1234567

Rules:
- Only answer questions about Savour Restaurant
- If asked something unrelated, politely redirect
- Keep responses friendly, concise, and helpful
- Always encourage reservations for groups of 6 or more
- If unsure about something specific, suggest calling on WhatsApp"""

# --- Initialize Anthropic Client ---
api_key = st.secrets.get("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    st.error("⚠️ ANTHROPIC_API_KEY not found. Add it to your Streamlit secrets or environment variables.")
    st.stop()

client = Anthropic(api_key=api_key)

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Helper: generate assistant reply ---
def generate_reply():
    """Call the API and append the assistant reply to session state."""
    with st.chat_message("assistant"):
        with st.spinner(""):
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1000,
                system=SYSTEM_PROMPT,
                messages=st.session_state.messages
            )
            reply = response.content[0].text
            st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})

# --- Suggested Questions (only shown before any conversation) ---
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
                # Don't rerun — fall through so we generate a reply this render cycle
                break  # only one button can be clicked per render

# --- Display Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Generate reply if last message is from user (handles both button clicks and chat input) ---
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    # Check we haven't already rendered the last message above (avoid double display)
    generate_reply()
    st.rerun()  # refresh so the input box is clean and history is in sync

# --- Chat Input ---
if prompt := st.chat_input("Ask anything about Savour..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    generate_reply()
