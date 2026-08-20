import requests
import streamlit as st

GENERATE_API_USING_AWS_URL="http://127.0.0.1:8000/generate_using_aws"
GENERATE_API_USING_GCP_URL="http://127.0.0.1:8000/generate_using_gcp"

def generate_response(prompt:str) -> str:
    resp=requests.post(
        GENERATE_API_USING_GCP_URL,
        json={
            "query":prompt
        }
    )
    resp=resp.json()["answer"]
    return resp



st.set_page_config(
    page_title="Twin LLM",
    page_icon="🤖",
    layout="wide"
)

if "messages" not in st.session_state:
    st.session_state.messages=[]


st.html(
    """
    <style>

    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        max-width: 100%;
    }

    /* Hide Streamlit default header */
    header {
        visibility: hidden;
    }

    /* Hide Streamlit footer */
    footer {
        visibility: hidden;
    }

    /* Hide hamburger menu */
    #MainMenu {
        visibility: hidden;
    }


   
    .landing-container {
        height: 65vh;

        display: flex;
        flex-direction: column;

        justify-content: center;
        align-items: center;

        text-align: center;
    }

    .landing-title {
        font-size: 4rem;
        font-weight: 700;

        margin-bottom: 0.8rem;
    }

    .landing-subtitle {
        font-size: 1.15rem;

        color: #888;

        max-width: 750px;

        line-height: 1.6;
    }


    

    .chat-header {
        width: 100%;

        padding-top: 1rem;
        padding-bottom: 1rem;

        margin-bottom: 1rem;

        border-bottom: 1px solid rgba(128, 128, 128, 0.2);
    }

    .chat-title {
        font-size: 1.8rem;
        font-weight: 700;
    }


   
    [data-testid="stChatMessage"] {
        max-width: 850px;
        margin-left: auto;
        margin-right: auto;
    }


    

    [data-testid="stChatInput"] {
        max-width: 850px;
        margin-left: auto;
        margin-right: auto;
    }

    </style>
    """
)


if not st.session_state.messages:
    st.html(
        """
        <div class="landing-container">

            <div class="landing-title">
                Twin LLM
            </div>

            <div class="landing-subtitle">
                A LLM to imitate your writing style and generate
                posts, articles, tweets, code the way you do.
            </div>

        </div>
        """
    )

    col1,col2,col3=st.columns([1,2,1])

    with col2:
        prompt = st.text_input(
            "Prompt",
            placeholder="What would you like your Twin to write?",
            label_visibility="collapsed",
            key="initial_prompt"
        )

        st.write()
        st.write()
        st.write()

        generate_button=st.button(
            "Generate",
            type="primary",
            use_container_width=True
        )

    prompt=str(prompt)
    if generate_button and prompt.strip():
        st.session_state.messages.append(
            {
                "role":"user",
                "content":prompt
            }
        )

        response=generate_response(prompt=prompt)

        st.session_state.messages.append(
            {
                "role":"assistant",
                "content":response
            }
        )

        st.rerun()

else:
    st.html(
        """
        <div class="chat-header">
            <div class="chat-title">
                Twin LLM
            </div>
        </div>
        """
    )

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(
                message["content"]
            )


    prompt=st.chat_input(
        "What would you like your Twin to write?"
    )
    

    if prompt:
        prompt = str(prompt)
        prompt = prompt.strip()

        with st.chat_message("user"):
            st.markdown(prompt)


        st.session_state.messages.append(
            {
                "role":"user",
                "content":prompt
            }
        )

        response=generate_response(prompt=prompt)

        with st.chat_message("assistant"):
            st.markdown(response)


        st.session_state.messages.append(
            {
                "role":"assistant",
                "content":response
            }
        )



