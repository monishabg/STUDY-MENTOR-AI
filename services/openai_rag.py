from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import Vector
from dotenv import load_dotenv
import os

load_dotenv()

class OpenAIRAG:
    def __init__(self):
        self.openai_client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        self.search_client = SearchClient(
            endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
            index_name=os.getenv("AZURE_SEARCH_INDEX_NAME"),
            credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_KEY"))
        )
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    
    def get_embedding(self, text: str) -> list:
        response = self.openai_client.embeddings.create(
            input=text,
            model="text-embedding-ada-002"
        )
        return response.data[0].embedding
    
    def search_documents(self, query: str, top_k: int = 3) -> list:
        # Vectorize the query
        vector = Vector(
            value=self.get_embedding(query),
            k=top_k,
            fields="contentVector"
        )
        
        # Perform vector search
        results = self.search_client.search(
            search_text=query,
            vectors=[vector],
            top=top_k
        )
        
        return [{"content": result["content"], "score": result["@search.score"]} for result in results]
    
    def augmented_generation(self, query: str, context: str = "") -> str:
        if not context:
            search_results = self.search_documents(query)
            context = "\n\n".join([res["content"] for res in search_results])
        
        prompt = f"""
        Use the following context to answer the question. If you don't know the answer, say you don't know.
        
        Context:
        {context}
        
        Question: {query}
        
        Answer:
        """
        
        response = self.openai_client.chat.completions.create(
            model=self.deployment_name,
            messages=[
                {"role": "system", "content": "You answer questions using the provided context."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        return response.choices[0].message.content