import streamlit as st
import requests
import sys
import time
import json  # Import json for parsing the stream
from uuid import uuid4  # Added for session ID generation

# --- Page Configuration ---
# All your branding and layout are preserved
st.set_page_config(
    page_title="DialogXR TASP Chatbot",
    page_icon="dialogXR_Icon.png",
    layout="wide"
)

# --- API Configuration ---
# This is your new public URL, pointing to the FastAPI server
# that is running on your cluster.
API_URL = "http://94.56.105.18:7898/children_services/chat"

# --- Session State ---
# This is from your old app, with the session_id added for the new backend
if "messages" not in st.session_state:
    st.session_state["messages"] = []  # Active conversation.
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []  # Archived conversations.
if "template_used" not in st.session_state:
    st.session_state["template_used"] = False
if "pending_input" not in st.session_state:
    st.session_state["pending_input"] = None
# ADDED: Your new backend requires a session_id for memory
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid4())

# --- UI Elements (Unchanged) ---
template_questions = [
    "Can you provide examples of cases that have successful interventions and strategies that have prevented harm.",
    "What are the signs and indicators of different types of child abuse and neglect?",
    "What are the key learnings for local authorities in addressing child neglect?",
    "What are the acts of Parents or Parent that can be considered as disguised compliance?",
    "​How can safeguarding partners effectively share information to protect children at risk?"
]

st.markdown("""
    <style>
    .template-box {
        background-color: #018926;
        padding: 12px;
        border-radius: 8px;
        font-size: 16px;
        font-style: italic;
        color: #FFFFFF;
        text-align: center;
        font-weight: bold;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.title("🤖 The Association of Safeguarding Partners Chatbot")
    
    st.markdown("### Powered by:")
    st.image("dialogXR_Typography.png", width=300)
    
    st.markdown(
        """<p style="margin-top:1rem; margin-bottom:0.5rem; font-size: 1.1rem; font-weight: bold;">AI powered by</p>""",
        unsafe_allow_html=True
    )
    st.image("intel_lenovo_cropped.png", width=250)
    
    st.markdown(
        """<p style="margin-top:1rem; margin-bottom:0.5rem; font-size: 1.1rem; font-weight: bold;">Designed by</p>""",
        unsafe_allow_html=True
    )
    st.image("Bikal_logo.svg", width=120)
    
    st.markdown("### Conversation History")
    if st.session_state["chat_history"]:
        for idx, conv in enumerate(st.session_state["chat_history"], 1):
            with st.expander(f"Conversation {idx}", expanded=False):
                preview = conv[-2:] if len(conv) >= 2 else conv
                preview_html = "<div style='font-size:12px; max-width:200px;'>"
                for msg in preview:
                    preview_html += f"<p><strong>{msg['role'].capitalize()}:</strong> {msg['content']}</p>"
                preview_html += "</div>"
                st.markdown(preview_html, unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Load", key=f"load_{idx}"):
                        st.session_state["messages"] = conv.copy()
                        # Give a new session ID when loading old chat
                        st.session_state["session_id"] = str(uuid4())
                with col2:
                    if st.button("Delete", key=f"delete_{idx}"):
                        st.session_state["chat_history"].pop(idx - 1)
                        st.rerun()
    else:
        st.info("No previous conversations stored.")
    
    if st.button("🆕 New Chat"):
        if st.session_state["messages"]:
            st.session_state["chat_history"].append(st.session_state["messages"].copy())
        st.session_state["messages"] = []
        st.session_state["template_used"] = False
        # Generate a new session ID
        st.session_state["session_id"] = str(uuid4())
        st.rerun()

# --- Main Chat Interface (Logic Updated) ---

st.markdown("### Welcome to TASP Chatbot!")

# Function to set prompt from button
def set_prompt(question):
    st.session_state["pending_input"] = question
    st.session_state["template_used"] = True

# Show template questions
if not st.session_state["messages"] and not st.session_state["template_used"]:
    st.markdown("<div class='template-box'><strong>Suggested Questions:</strong></div>", unsafe_allow_html=True)
    
    cols = st.columns(len(template_questions) if len(template_questions) < 5 else 5)
    for i, question in enumerate(template_questions):
        # FIXED: Added a unique key to prevent Streamlit error
        cols[i].button(question, key=f"suggest_{i}", on_click=set_prompt, args=(question,), use_container_width=True)

# Display existing chat messages
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Check for pending input from buttons
if prompt_from_button := st.session_state.pop("pending_input", None):
    user_input = prompt_from_button
    st.rerun() # Rerun to process the input immediately
else:
    user_input = st.chat_input("Ask me anything...")

# Process user input
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # --- NEW: Streaming Logic ---
    # This replaces your old threading logic to work with the new FastAPI server
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Prepare the JSON payload for the new backend
            payload = {
                "question": user_input,
                "session_id": st.session_state["session_id"]
            }
            
            # Connect to the streaming endpoint
            with requests.post(API_URL, json=payload, stream=True, timeout=90) as r:
                r.raise_for_status() # Check for HTTP errors
                
                for line in r.iter_lines():
                    if line:
                        # Find the start of the JSON
                        try:
                            # Clean the line: remove 'data: ' prefix
                            json_str = line.decode('utf-8')
                            if json_str.startswith('data: '):
                                json_str = json_str[len('data: '):]
                            
                            # Skip empty keep-alive pings
                            if not json_str.strip():
                                continue

                            data = json.loads(json_str)
                            
                            if data.get("event") == "new_token":
                                chunk = data.get("data", "")
                                full_response += chunk
                                message_placeholder.markdown(full_response + "▌")
                            elif data.get("event") == "error":
                                st.error(f"An error occurred: {data.get('data')}")
                                break
                            elif data.get("event") == "end":
                                break

                        except json.JSONDecodeError as e:
                            # This catches parsing errors from junk lines/pings
                            print(f"Warning: Could not decode JSON line: {line.decode('utf-8')}. Error: {e}")
            
            message_placeholder.markdown(full_response)
            st.session_state["messages"].append({"role": "assistant", "content": full_response})

        except requests.exceptions.RequestException as e:
            st.error(f"Failed to connect to the backend API: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
