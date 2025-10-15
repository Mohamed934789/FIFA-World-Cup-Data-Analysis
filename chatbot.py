import streamlit as st
import pandas as pd
import os, base64
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents.agent_types import AgentType  # Import necessary for template

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Football Data Chatbot ⚽",
    page_icon="⚽",
    layout="centered"
)

# --- BACKGROUND IMAGE (BASE64) + GLASS-BLUR UI ---
img_path = "images/ChatGPT_Image_Oct_12_2025_10_49_10_PM.png"
if os.path.exists(img_path):
    with open(img_path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        /* Background */
        .stApp {{
            background-image: url("data:image/png;base64,{data}");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }}

        /* Dark translucent overlay with blur for readability */
        .stApp::before {{
            content: "";
            position: fixed;
            inset: 0;
            background: rgba(4,12,20,0.45);
            backdrop-filter: blur(6px);
            z-index: 0;
            pointer-events: none;
        }}

        /* Container adjustments so content sits above overlay */
        .appview-container .main, .stApp > .main {{
            position: relative;
            z-index: 1;
        }}

        /* Glass-style chat bubbles (best-effort selectors) */
        /* These selectors target Streamlit's chat/message containers */
        div[data-testid="stMarkdownContainer"] > div[role="listitem"] > div {{
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 14px;
            padding: 10px 12px;
            margin-bottom: 8px;
            backdrop-filter: blur(4px) saturate(120%);
            box-shadow: 0 4px 18px rgba(2,6,23,0.35);
            color: #e7eef8;
        }}

        /* Slight color tint for user vs assistant messages using attribute role text */
        div[aria-label="User"] div[role="listitem"] > div,
        div[aria-label="user"] div[role="listitem"] > div {{
            background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
            border: 1px solid rgba(255,255,255,0.06);
        }}
        div[aria-label="Assistant"] div[role="listitem"] > div,
        div[aria-label="assistant"] div[role="listitem"] > div {{
            background: linear-gradient(180deg, rgba(10,90,130,0.08), rgba(10,90,130,0.03));
            border: 1px solid rgba(10,90,130,0.14);
        }}

        /* Input box styling */
        div[data-baseweb="input"] input {{
            border-radius: 12px !important;
            padding: 12px !important;
            font-size: 15px !important;
            background: rgba(255,255,255,0.03) !important;
            color: #e7eef8 !important;
            border: 1px solid rgba(255,255,255,0.06) !important;
        }}

        /* Header text colors */
        .stHeader, .stMarkdown {{
            color: #ffd60a;
        }}

        /* Make error/warning text clearer on dark bg */
        .stError, .stWarning {{
            color: #ffd6a3;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    st.error(f"Background image not found at: {img_path}")

# --- HEADER ---
st.title("⚽ Football Data Chatbot")
st.write("Ask me anything about the football match data!")

# --- LOAD DATA AND INITIALIZE AGENT ---

@st.cache_resource
def get_data_agent():
    """
    Loads all CSV files from the 'data' directory into a list of pandas DataFrames
    and initializes the LangChain Pandas DataFrame agent.
    """
    data_folder = 'data'
    if not os.path.exists(data_folder):
        st.error(f"Error: The directory '{data_folder}' was not found. Please create it and add your CSV files.")
        return None

    files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]
    if not files:
        st.error(f"No CSV files (.csv) found in the '{data_folder}' directory.")
        return None

    try:
        df_list = [pd.read_csv(os.path.join(data_folder, file), encoding='latin1') for file in files]

        # --- 1. CORRECTED MODEL NAME ---
        # Use the official name for the fast and capable Gemini Flash model.
        # This will improve speed and reduce errors.
        llm = ChatGoogleGenerativeAI(
            model="models/gemini-2.5-flash",
            google_api_key=st.secrets["GOOGLE_API_KEY"],
            convert_system_message_to_human=True,
        )

        # --- 2. NEW PROMPT TEMPLATE FOR MULTILINGUAL SUPPORT ---
        # This template adds a crucial instruction for the agent.
        agent_instructions = """
        Thought: The user wants me to answer a question about their data. I need to use the tools available to me to find the correct information and provide a final answer.
        My final answer must be in the same language as the user's original question.
        """

        # --- 3. CREATE THE AGENT WITH THE NEW INSTRUCTIONS ---
        agent = create_pandas_dataframe_agent(
            llm=llm,
            df=df_list,
            verbose=True,
            handle_parsing_errors=True, # This is still useful as a backup
            allow_dangerous_code=True,
            # Apply the new instructions to the agent's thinking process
            agent_executor_kwargs={"handle_parsing_errors": True},
            agent_kwargs={
                "suffix": agent_instructions,
            }
        )
        return agent

    except Exception as e:
        st.error(f"An error occurred while loading data or setting up the agent: {e}")
        return None

# Get the agent from the cached function
agent = get_data_agent()

# --- CHAT INTERFACE ---

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("E.g., Who scored the most goals in the 2014 world cup?"):
    if agent is not None:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = agent.invoke(prompt)
                    answer = response.get('output', "Sorry, I couldn't find an answer.")
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    error_message = f"An error occurred: {e}"
                    st.error(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": error_message})
    else:
        st.warning("The agent is not available due to an error. Please check the setup.")
