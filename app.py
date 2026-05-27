import streamlit as st
import requests
import uuid
from bs4 import BeautifulSoup
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Support AI Agent",
    page_icon="🤖",
    layout="centered",
)

# ─────────────────────────────────────────────
# FORCE LIGHT THEME & WHITE BACKGROUND
# ─────────────────────────────────────────────
st.markdown("""
    <style>
        /* Force white background everywhere */
        .stApp, .stApp > div, [data-testid="stAppViewContainer"] {
            background-color: #ffffff !important;
            color: #111111 !important;
        }
        [data-testid="stHeader"] {
            background-color: #ffffff !important;
        }
        section[data-testid="stSidebar"] {
            background-color: #f5f5f5 !important;
        }
        /* Chat input area */
        [data-testid="stBottom"] {
            background-color: #ffffff !important;
        }
    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.title("🤖 Support AI Agent")
st.caption(
    "Ask me anything about Zerodha — charges, account setup, Varsity lessons, "
    "TradingQnA discussions, and more. I remember our conversation!"
)
st.divider()

# ─────────────────────────────────────────────
# SIDEBAR — API KEY
# ─────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    google_api_key = st.text_input(
        "Google Gemini API Key",
        type="password",
        placeholder="Paste your key here…",
    )
    st.markdown(
        "🔑 [Get a free API Key](https://aistudio.google.com/app/apikey)",
        unsafe_allow_html=True,
    )
    st.divider()

    # Clear conversation button
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.memory = MemorySaver()
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

    st.markdown("**Sources searched:**")
    st.markdown(
        "- zerodha.com/support\n"
        "- zerodha.com/varsity\n"
        "- tradingqna.com\n"
        "- zerodha.com/z-connect"
    )

# ─────────────────────────────────────────────
# TOOLS
# ─────────────────────────────────────────────
@tool
def search_zerodha_ecosystem(query: str) -> str:
    """
    Search the Zerodha ecosystem for answers.
    Covers Zerodha Support, Varsity, Z-Connect blog, and TradingQnA.
    Use this for any question about Zerodha products, charges, account,
    trading rules, or investment concepts.
    """
    search = DuckDuckGoSearchResults(num_results=5)
    scoped_query = f"site:zerodha.com OR site:tradingqna.com {query}"
    return search.invoke(scoped_query)


@tool
def read_webpage(url: str) -> str:
    """
    Fetch and read the full text content of a webpage URL.
    Use this after searching to get detailed information from a specific page.
    Returns up to 6000 characters of cleaned text.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; ZerodhaBot/1.0)"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove noise
        for tag in soup(["script", "style", "header", "footer", "nav", "aside"]):
            tag.extract()

        text = soup.get_text(separator=" ", strip=True)
        return text[:6000]

    except requests.exceptions.Timeout:
        return "Error: The webpage took too long to respond."
    except requests.exceptions.HTTPError as e:
        return f"Error: Received HTTP {e.response.status_code} from the server."
    except Exception as e:
        return f"Error reading webpage: {str(e)}"


tools = [search_zerodha_ecosystem, read_webpage]

# ─────────────────────────────────────────────
# SESSION STATE — Memory & Chat History
# ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "memory" not in st.session_state:
    st.session_state.memory = MemorySaver()

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# ─────────────────────────────────────────────
# RENDER CHAT HISTORY
# ─────────────────────────────────────────────
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ─────────────────────────────────────────────
# AGENT SYSTEM PROMPT
# ─────────────────────────────────────────────
SYSTEM_PROMPT = """
You are a highly professional and helpful Zerodha Ecosystem Expert.

Your goal is to help users with accurate, concise, and well-formatted answers
about anything related to Zerodha — including brokerage charges, account opening,
trading platforms (Kite, Console, Coin), Varsity learning modules, and
TradingQnA community discussions.

Guidelines:
1. Always search before answering — never guess charges or policies.
2. Format responses clearly using **bold text**, bullet points, and tables where helpful.
3. If a question is a follow-up, use the conversation history for context.
4. Cite the source URL when referencing specific pages.
5. If you genuinely cannot find an answer, politely advise the user to email
   support@zerodha.com or visit https://support.zerodha.com.
6. Keep responses focused and avoid unnecessary padding.
"""

# ─────────────────────────────────────────────
# CHAT INPUT & AGENT INVOCATION
# ─────────────────────────────────────────────
if prompt := st.chat_input("Ask about Zerodha… e.g. What are the delivery brokerage charges?"):

    if not google_api_key:
        st.warning("⚠️ Please enter your Google Gemini API Key in the sidebar to continue.")
        st.stop()

    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Run agent
    with st.chat_message("assistant"):
        with st.spinner("🔍 Searching Zerodha ecosystem…"):
            try:
                # Build LLM
                llm = ChatGoogleGenerativeAI(
                    model="gemini-2.5-flash",
                    temperature=0,
                    google_api_key=google_api_key,
                )

                # Build agent with memory
                agent = create_react_agent(
                    llm,
                    tools,
                    prompt=SYSTEM_PROMPT,
                    checkpointer=st.session_state.memory,
                )

                config = {
                    "configurable": {
                        "thread_id": st.session_state.thread_id
                    }
                }

                response = agent.invoke(
                    {"messages": [("user", prompt)]},
                    config=config,
                )

                final_answer = response["messages"][-1].content

                # Handle Gemini returning a list of blocks instead of a string
                if isinstance(final_answer, list):
                    final_answer = "".join(
                        block["text"]
                        for block in final_answer
                        if isinstance(block, dict) and "text" in block
                    )

                st.markdown(final_answer)
                st.session_state.messages.append(
                    {"role": "assistant", "content": final_answer}
                )

            except Exception as e:
                error_msg = str(e)
                if "API_KEY" in error_msg.upper() or "401" in error_msg:
                    st.error("❌ Invalid API Key. Please check your Gemini API Key in the sidebar.")
                elif "quota" in error_msg.lower():
                    st.error("❌ API quota exceeded. Please check your Google AI Studio usage limits.")
                else:
                    st.error(f"❌ Something went wrong: {error_msg}")
