import streamlit as st
import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

GROQ_API_KEY = "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"


# Custom CSS loading functions
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)


def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)


class MentalHealthChatbot:
    def __init__(self, groq_api_key: str, model_name: str):
        self.groq_api_key = groq_api_key
        self.model_name = model_name

        # Set the API key in the environment
        os.environ["GROQ_API_KEY"] = self.groq_api_key

        # Initialize the language model
        self.llm = ChatGroq(temperature=0.2, model_name=self.model_name, groq_api_key=self.groq_api_key)

        # Set up the chatbot chain with a mental health focus and memory
        self.memory = ConversationBufferMemory()
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            prompt=ChatPromptTemplate.from_template(
                """You are Marin, a compassionate mental health assistant developed by S Khavin under TextFusion.AI. Your role is to provide supportive and informative responses based on reliable mental health information. Always prioritize the user's well-being and give advice for the same. Remember to use the conversation history to provide context-aware responses. 
                Current conversation:
                {history}

                Human: {input}

                AI Assistant:"""
            ),
            output_parser=StrOutputParser(),
        )

    def respond(self, query: str) -> str:
        try:
            response = self.conversation.predict(input=query)
            return response
        except Exception as e:
            return f"I apologize, but I encountered an error while processing your request: {str(e)}. Please try rephrasing your question or ask something else."
        


# Streamlit app
def main():
    st.set_page_config(
        page_title="Mental Health Assistant",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    # Custom CSS to hide Streamlit's default elements and set custom fonts
    hide_streamlit_style = """

        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap');
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        .viewerBadge_link__1S137, .viewerBadge_container__1QSob { 
        visibility: hidden;
        display: none;
        }

        .stApp {
            font-family: 'DM Serif Display', serif;
        }
        .stTitle, .stSubheader {
            font-family: 'DM Serif Display', serif;
        }
        .stChat {
            border-radius: 10px;
            padding: 10px;
        }
        .stChatMessage {
            background-color: #d9faf6;
            border-radius: 15px;
            padding: 10px;
            margin-bottom: 10px;
        }
        .stChatMessage.user {
            background-color: #d9faf6;
        }
        .stChatMessage.assistant {
            background-color: #d9faf6;
        }
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # Load custom fonts
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

    # Load Material Icons
    st.markdown("""
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    """, unsafe_allow_html=True)

    st.title("Marin 🧠💚")
    st.subheader("-Your personal mental health assistant-")

    # Initialize MentalHealthChatbot
    GROQ_API_KEY = "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"

    if not GROQ_API_KEY:
        st.error("API key is missing. Please set the GROQ_API_KEY environment variable.")
    else:
        # Initialize chatbot in session state if it doesn't exist
        if 'chatbot' not in st.session_state:
            st.session_state.chatbot = MentalHealthChatbot(
                groq_api_key=GROQ_API_KEY,
                model_name="mixtral-8x7b-32768"
            )

        # Chat interface
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🤖"):
                st.markdown(message["content"])

        if prompt := st.chat_input("How are you feeling today?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user", avatar="👤"):
                st.markdown(prompt)

            with st.chat_message("assistant", avatar="👱🏼‍♀"):
                with st.spinner("Thinking..."):
                    response = st.session_state.chatbot.respond(prompt)
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    with st.sidebar:
        st.header("🧠 Mental Health Resources")
        st.markdown("""
        - <i class="material-icons">call</i> [Talk to Someone](https://findahelpline.com)
        - <i class="material-icons">person_search</i> [Find a Psychologist](https://www.therapyroute.com/)
        - <i class="material-icons">psychology</i> [Mental Health Topics](https://www.apa.org/topics)
        """, unsafe_allow_html=True)
        st.write("Copyright © TextFusion.AI")
        st.markdown('<i class="material-icons">photo_camera</i> [Instagram](https://instagram.com/im.your.nemesis)',
                    unsafe_allow_html=True)
        st.write("For issues, please contact us on Instagram")

        if st.button("Clear Conversation", key="clear_button"):
            st.session_state.messages = []
            st.session_state.chatbot.memory.clear()
            st.experimental_rerun()


if __name__ == "__main__":
    main()
