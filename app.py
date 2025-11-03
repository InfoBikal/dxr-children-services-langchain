import streamlit as st
import requests
import sys
import time
import json
from uuid import uuid4

# --- Page Configuration ---
st.set_page_config(
    page_title="DialogXR TASP Chatbot",
    page_icon="dialogXR_Icon.png",  # Make sure this image is in your GitHub repo
    layout="wide"
)

# --- API Configuration ---
# This public URL is correct and will be accessed from Streamlit Cloud
API_URL = "http://94.56.105.18:7898/children_services/chat"

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []  # Active conversation.
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []  # Archived conversations.
if "template_used" not in st.session_state:
    st.session_state["template_used"] = False
if "pending_input" not in st.session_state:
    st.session_state["pending_input"] = None
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid4())
# This new flag mimics the "working" logic
if "ran_from_button" not in st.session_state:
    st.session_state["ran_from_button"] = False


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
    # Make sure these images are in your GitHub repo
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
        st.session_state["session_id"] = str(uuid4())
        st.rerun()

# --- Main Chat Interface (Logic FIXED) ---

st.markdown("### Welcome to TASP Chatbot!")

# Function to set prompt from button
def set_prompt(question):
    st.session_state["pending_input"] = question
    st.session_state["template_used"] = True
    st.session_state["ran_from_button"] = True # Set the flag

# Show template questions
if not st.session_state["messages"] and not st.session_state["template_used"]:
    st.markdown("<div class='template-box'><strong>Suggested Questions:</strong></div>", unsafe_allow_html=True)
    
    cols = st.columns(len(template_questions) if len(template_questions) < 5 else 5)
    for i, question in enumerate(template_questions):
        cols[i].button(question, key=f"suggest_{i}", on_click=set_prompt, args=(question,), use_container_width=True)


# Display existing chat messages
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# THIS IS THE "WORKING" INPUT LOGIC
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# First, check for text input from the user
user_input = st.chat_input("Ask me anything...")

# NEXT, check if a button set the input
if pending_input := st.session_state.pop("pending_input", None):
    user_input = pending_input  # Overwrite user_input with button text
    # DO NOT RERUN. Let the script continue.

# NOW, process the input if we have any
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # --- Streaming Logic (This is the 'backend handling' part) ---
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            payload = {
                "question": user_input,
                "session_id": st.session_state["session_id"]
            }
            
            with requests.post(API_URL, json=payload, stream=True, timeout=90) as r:
                r.raise_for_status()
                
                # This is the "working" parsing logic from streamlit_app.py
                for line in r.iter_lines():
                    if line: # Filter out keep-alive newlines
                        decoded_line = line.decode('utf-8')
                        
                        if decoded_line.startswith("data:"):
                            try:
                                json_start_index = decoded_line.index('{')
                                data_str = decoded_line[json_start_index:]
                                data = json.loads(data_str)
                                
                                if data.get("event") == "new_token":
                                    chunk = data.get("data", "")
                                    full_response += chunk
                                    message_placeholder.markdown(full_response + "▌")
                                elif data.get("event") == "error":
                                    st.error(f"An error occurred: {data.get('data')}")
                                    break
                                elif data.get("event") == "end":
                                    break
                            
                            except (json.JSONDecodeError, ValueError) as e:
                                print(f"Warning: Could not parse line: {decoded_line}. Error: {e}")
                                pass 

            message_placeholder.markdown(full_response)
            st.session_state["messages"].append({"role": "assistant", "content": full_response})

            # Finally, if this was triggered by a button, rerun now
            if st.session_state.pop("ran_from_button", False):
                st.rerun()

        except requests.exceptions.RequestException as e:
            st.error(f"Failed to connect to the backend API. Please check the connection and try again. Error: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

