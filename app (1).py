import validators
import streamlit as st

from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import (
    YoutubeLoader,
    UnstructuredURLLoader
)

st.set_page_config(page_title="YouTube / Website Summarizer")
st.title("Summarize YouTube or Website")

with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", type="password")

url = st.text_input("Enter URL")

if st.button("Summarize"):
    if not groq_api_key or not url:
        st.error("Provide API key and URL")

    elif not validators.url(url):
        st.error("Invalid URL")

    else:
        with st.spinner("Summarizing..."):

            if "youtube.com" in url or "youtu.be" in url:
                loader = YoutubeLoader.from_youtube_url(url)
            else:
                loader = UnstructuredURLLoader(urls=[url])

            docs = loader.load()

            llm = ChatGroq(
                groq_api_key=groq_api_key,
                model_name="llama-3.1-70b-versatile"
            )

            prompt = PromptTemplate(
                template="Summarize the following content in 300 words:\n{text}",
                input_variables=["text"]
            )

            chain = load_summarize_chain(
                llm,
                chain_type="stuff",
                prompt=prompt
            )

            result = chain.invoke({"input_documents": docs})
            st.success(result["output_text"])
