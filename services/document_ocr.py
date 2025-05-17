from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os
from PIL import Image
import PyPDF2
import io

load_dotenv()

def process_uploaded_file(file):
    if file.type == "application/pdf":
        return extract_text_from_pdf(file)
    elif file.type.startswith('image/'):
        return extract_text_from_image(file)
    else:
        raise ValueError("Unsupported file type")

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_image(file):
    client = DocumentAnalysisClient(
        endpoint=os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"),
        credential=AzureKeyCredential(os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY"))
    )

    image = Image.open(file)
    byte_stream = io.BytesIO()
    image.save(byte_stream, format=image.format)
    byte_stream.seek(0)

    poller = client.begin_analyze_document(
        "prebuilt-read", 
        document=byte_stream
    )
    result = poller.result()

    text = ""
    for page in result.pages:
        for line in page.lines:
            text += line.content + "\n"
    
    return text