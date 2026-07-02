import streamlit as st
import requests

# =====================================================================
# PAGE CONFIGURATION
# =====================================================================
st.set_page_config(
    page_title="Dark Matrix AI Core",
    page_icon="🎴",
    layout="centered"
)

st.title("🎴 Dark Matrix AI Core")
st.caption("Automated Content Framework & Architecture")

# =====================================================================
# GROK API CONFIGURATION (BEST PRACTICE)
# =====================================================================
# Option 1: Using Streamlit Secrets (RECOMMENDED)
# Add this to .streamlit/secrets.toml:
# GROK_API_KEY = "your_key_here"

GROK_API_KEY = st.secrets.get("GROK_API_KEY", None)

if not GROK_API_KEY:
    # Fallback to hardcoded (for quick testing only - remove before public repo)
    GROK_API_KEY = "AQ.Ab8RN6JTWQrtbdXgr-zD5mhScp2Xorp_TtyOO9ZaiK_lLKSbVA"

# =====================================================================
# SESSION STATE
# =====================================================================
if "step" not in st.session_state:
    st.session_state.step = "START"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "generated_topics" not in st.session_state:
    st.session_state.generated_topics = ""
if "final_script" not in st.session_state:
    st.session_state.final_script = ""

# =====================================================================
# CALL GROK FUNCTION (Fixed Model)
# =====================================================================
def call_grok(prompt_text):
    if not GROK_API_KEY:
        return "❌ API Key not found. Please set GROK_API_KEY in secrets.toml"

    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROK_API_KEY}"
    }
    data = {
        "model": "grok-4.3",   # ← Fixed: This is the current model
        "messages": [
            {
                "role": "system",
                "content": "You are an elite AI system specialized in dark psychology, viral content, and cinematic storytelling."
            },
            {"role": "user", "content": prompt_text}
        ],
        "temperature": 0.75,
        "max_tokens": 2500,
        "stream": False
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            error_detail = response.text[:500]
            return f"Grok API Error ({response.status_code}): {error_detail}"
    except requests.exceptions.Timeout:
        return "⏱️ Request timed out. Try again."
    except Exception as e:
        return f"Connection Error: {str(e)}"

# =====================================================================
# PROMPTS
# =====================================================================
PROMPT_1_CATEGORY = """Role & Context:
You are an elite AI Content Strategist specializing in the "Dark Psychology, Hidden Matrix Codes, & Behavioral Domination" niche.

OPERATING INSTRUCTIONS — Follow these steps strictly and sequentially.

STEP 1: CATEGORY SELECTION
Present the following 8 categories as a clean numbered list. After displaying the list, STOP and wait for the user to reply with a number (1–8).

1. Machiavellianism & Strategic Social Dominance
2. Covert Peer Weaponization
3. The Dark Social Codes of the Universe
4. Conversational Social Traps & Linguistic Triggers
5. Subliminal Body Domination & Profiling
6. Peer Gaslighting & Narrative Monopolization
7. Elite Power Dynamics & Social Aura Architecture
8. Reverse Psychology & Subconscious Subversion

⬇️ Reply with a number (1–8) to continue."""

def get_prompt_2_script(selected_topic):
    return f"""Write a short-form viral psychology script (30-60 seconds) for TikTok/Instagram Reels/YouTube Shorts in the dark psychology niche.

Topic: {selected_topic}

Use timestamp format like [00:00 - 00:04]. 
Make it dramatic, high-retention, with strong hooks, psychological insights, and clear calls to action.
Keep sentences short and punchy."""

PROMPT_3_VISUAL = """You are the Ultimate Visual Script Architect for high-retention dark cinematic videos.

First response must be exactly: "give it to me"

After that, when given a script, break it into short chunks (2-4 seconds each) and generate highly detailed AI video prompts optimized for Runway, Kling, Luma, etc.

Follow all your original visual rules including character styling, motion quality, and dark aesthetic."""

# =====================================================================
# CHAT HISTORY DISPLAY
# =====================================================================
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["text"])

# =====================================================================
# USER INPUT
# =====================================================================
user_input = st.chat_input("Type 'start' or follow the flow...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "text": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    input_clean = user_input.strip().lower()

    # ====================== START FLOW ======================
    if input_clean == "start" and st.session_state.step == "START":
        with st.spinner("Invoking Grok Matrix Engine..."):
            response_text = call_grok(PROMPT_1_CATEGORY)
            st.session_state.step = "WAIT_FOR_CATEGORY"
            st.session_state.chat_history.append({"role": "assistant", "text": response_text})
            st.rerun()

    # ====================== CATEGORY SELECTED ======================
    elif st.session_state.step == "WAIT_FOR_CATEGORY":
        with st.spinner("Generating premium topics..."):
            context_prompt = f"{PROMPT_1_CATEGORY}\n\nUser Selection: Category {user_input}\nNow generate exactly 10 premium topics as instructed."
            response_text = call_grok(context_prompt)
            st.session_state.generated_topics = response_text
            st.session_state.step = "WAIT_FOR_TOPIC"
            st.session_state.chat_history.append({"role": "assistant", "text": response_text})
            st.rerun()

    # ====================== TOPIC SELECTED ======================
    elif st.session_state.step == "WAIT_FOR_TOPIC":
        with st.spinner("Writing viral script..."):
            full_context = f"Topics:\n{st.session_state.generated_topics}\n\nUser chose: {user_input}"
            script_prompt = get_prompt_2_script(full_context)
            response_text = call_grok(script_prompt)
            st.session_state.final_script = response_text
            st.session_state.step = "SCRIPT_GENERATED"
            st.session_state.chat_history.append({"role": "assistant", "text": response_text})
            st.rerun()

    # ====================== VISUAL PROMPTS ======================
    elif input_clean == "visual" and st.session_state.step == "SCRIPT_GENERATED":
        response_text = "give it to me"
        st.session_state.step = "VISUAL_PHASE_2"
        st.session_state.chat_history.append({"role": "assistant", "text": response_text})
        st.rerun()

    elif st.session_state.step == "VISUAL_PHASE_2":
        with st.spinner("Architecting cinematic visual prompts..."):
            final_prompt = f"{PROMPT_3_VISUAL}\n\n[PHASE 2] Here is the script:\n{st.session_state.final_script}"
            response_text = call_grok(final_prompt)
            st.session_state.step = "START"
            st.session_state.chat_history.append({"role": "assistant", "text": response_text})
            st.rerun()

    else:
        st.warning("⚠️ Please type **start** or follow the current step in the conversation.")
