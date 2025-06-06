# 📚 STUDY-MENTOR-AI

STUDY-MENTOR-AI is a multi-agent AI assistant designed to help students learn better using intelligent automation. It provides interactive concept explanations, quizzes, and exam support, powered by Azure OpenAI, AI Search, and Document Intelligence.

## 🚀 Features

- **Explanation Agent**: Provides topic-wise concept breakdowns.
- **Quiz Master Agent**: Creates customizable quizzes for practice.
- **Exam Coach Agent**: Offers strategic revision plans and mock questions.
- **Document Parsing**: Extracts data from NCERT textbooks.
- **Search Engine**: Finds relevant content from indexed knowledge base.
- **Streamlit UI**: Clean, interactive user interface.

## 🏗️ Tech Stack

- **Backend**: Python
- **LLM**: Azure OpenAI (GPT-3.5)
- **Search**: Azure AI Search
- **Document Parsing**: Azure Document Intelligence
- **Framework**: Autogen Agents
- **Frontend**: Streamlit

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/STUDY-MENTOR-AI.git
cd STUDY-MENTOR-AI
```

2. **Create a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Add Your API Keys**
Update config.py or set environment variables for:

-AZURE_OPENAI_API_KEY
-AZURE_SEARCH_KEY
-DOCUMENT_INTELLIGENCE_KEY
-Corresponding endpoint URLs and deployment names

5. **Run the Application**
```bash
streamlit run app.py
```

## 🧩 Implementation Details

The STUDY-MENTOR-AI system is built around modular AI agents, each with specific roles, working together to support student learning through:

### 🔹 1. Explanation Agent

- Uses GPT-3.5 from Azure OpenAI to explain concepts from NCERT textbooks.
- Fetches topic-relevant content using Azure AI Search.
- Formats explanations in a student-friendly tone.

### 🔹 2. Quiz Master Agent

- Generates multiple-choice questions or short quizzes using LLM prompting.
- Can take a topic or uploaded document as input context.
- Evaluates student responses and provides feedback.

### 🔹 3. Exam Coach Agent

- Acts like a mentor for revision planning.
- Provides last-minute tips, and topic prioritization.

### 🔹 4. Document Ingestion Pipeline

- NCERT PDFs are parsed using Azure Document Intelligence.
- Extracted data is converted into clean text and chunked into semantic blocks.

### 🔹 5. Vector Store & Retrieval

- Processed text chunks are embedded using `text-embedding-ada-002`.
- Stored in Azure AI Search for fast retrieval based on user queries.
- Enables RAG (Retrieval-Augmented Generation) workflows.

### 🔹 6. User Interface (Streamlit)

- Frontend built with Streamlit to select agent, input topic, and view results.
- Options to upload syllabus, ask questions, or generate quizzes.

### 🔹 7. Config Management

- Keys and endpoints stored securely in `config.py` or `.env`.
- Modular service integration through the `services/` folder.

---

## 🔁 Workflow Summary

1. User selects an agent (e.g., Quiz Master).
2. Inputs a topic or uploads a document.
3. System performs:
   - Retrieval from Azure Search
   - Response generation using GPT-3.5
   - Result display via Streamlit
4. User interacts with and iterates on the output.
