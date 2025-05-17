# config.py
import os
import streamlit as st
from dotenv import load_dotenv

# Load local .env if running locally
load_dotenv()

def get_secret(key: str, default=None):
    return st.secrets.get(key) or os.getenv(key) or default

# Azure OpenAI
AZURE_OPENAI_ENDPOINT = get_secret("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = get_secret("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_API_VERSION = get_secret("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_DEPLOYMENT_NAME = get_secret("AZURE_OPENAI_DEPLOYMENT_NAME")

# Azure Document Intelligence (Form Recognizer)
AZURE_DOC_INTELLIGENCE_ENDPOINT = get_secret("AZURE_DOC_INTELLIGENCE_ENDPOINT")
AZURE_DOC_INTELLIGENCE_KEY = get_secret("AZURE_DOC_INTELLIGENCE_KEY")

# Azure AI Search
AZURE_SEARCH_ENDPOINT = get_secret("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = get_secret("AZURE_SEARCH_KEY")
AZURE_SEARCH_INDEX_NAME = get_secret("AZURE_SEARCH_INDEX_NAME")
