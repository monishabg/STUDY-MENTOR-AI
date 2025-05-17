from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class ExplanationAgent:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    
    def explain_topic(self, topic: str, context: str = "") -> str:
        prompt = f"""
        You are an Explanation Guru AI that helps students understand complex topics in simple terms.
        The student has asked: "{topic}"
        
        Context from their materials: {context[:2000] if context else "No additional context provided"}
        
        Provide a clear, concise explanation suitable for a high school student.
        Use analogies and examples where helpful.
        Keep the explanation under 200 words.
        """
        
        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[
                {"role": "system", "content": "You are a helpful tutor that explains concepts clearly and simply."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        
        return response.choices[0].message.content