import google.generativeai as genai
import streamlit as st
import json
from prompt import prompt_template

def initialize_session_state() -> None:
    """
    Initialize session state for the Streamlit application.
    
    Returns:
        None
    """
    return st.session_state.setdefault('api_key', None)

def text_page() -> None:
    """
    Main function for the Streamlit app to perform grammar correction using Gemini.

    Returns:
        None
    """
    st.title("Grammar correction using Gemini")

    # Initialize session state
    initialize_session_state()

    # Input for API key in the sidebar
    api_key = st.sidebar.text_input("Enter your API key:", value=st.session_state.api_key)

    # Check if the API key is provided
    if not api_key:
        st.sidebar.error("Please enter your API key.")
        st.stop()
    else:
        # Store the API key in session state
        st.session_state.api_key = api_key

    # Configure the genai library with the provided API key
    genai.configure(api_key=api_key)

    # Model configuration options in the sidebar
    temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.9, 0.1)
    top_p = st.sidebar.number_input("Top P", 0.0, 1.0, 1.0, 0.1)
    top_k = st.sidebar.number_input("Top K", 1, 100, 1)
    max_output_tokens = st.sidebar.number_input("Max Output Tokens", 1, 10000, 2048)
    language = st.sidebar.selectbox("Language", ["en"])

    # Set up the model generation configuration
    generation_config = {
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "max_output_tokens": max_output_tokens,
    }

    # Default safety settings (currently as an empty dictionary)
    safety_settings = "{}"
    safety_settings = json.loads(safety_settings)

    # Input for user's query
    text = st.text_input("Enter your Query:")
    print(text)
    
    # Check if the query is provided
    if not text:
        st.error("Please enter your query.")
        st.stop()

    # Initialize the Gemini model
    gemini = genai.GenerativeModel(
        model_name="gemini-pro",
        generation_config=generation_config,
        safety_settings=safety_settings
    )

    # Generate the prompt using the template
    prompt = prompt_template[language].format(text=text)
    prompt_parts = [prompt]
    print(prompt_parts)

    # Generate content using the Gemini model
    try:
        response = gemini.generate_content(prompt_parts)
        print(response.text)
        st.subheader("Gemini:")
        if response.text:
            st.write(response.text)
        else:
            st.write("No output from Gemini.")
    except Exception as e:
        st.write(f"An error occurred: {str(e)}")
        # Check candidate safety ratings
        if hasattr(response, 'candidates'):
            for candidate in response.candidates:
                if hasattr(candidate, 'safety_ratings'):
                    print("Safety ratings:", candidate.safety_ratings)
                else:
                    print("No safety ratings available.")
        else:
            print("No candidates available in the response.")

# Run the Streamlit app
if __name__ == "__main__":
    text_page()
