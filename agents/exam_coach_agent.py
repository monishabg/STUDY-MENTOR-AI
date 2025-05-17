from openai import AzureOpenAI
from dotenv import load_dotenv
import os
from typing import List, Dict

load_dotenv()

class ExamCoachAgent:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    
    def create_study_plan(self, subject: str, days: int, current_level: str = "beginner") -> str:
        prompt = f"""
        Create a simple {days}-day study plan for {subject} (level: {current_level}).
        Present it in this exact format without additional explanations:
    
        Day 1: [Main Topic 1] - [Subtopic A], [Subtopic B]
        Day 2: [Main Topic 2] - [Subtopic C], [Subtopic D]
        ...
        Final Day: Revision and Practice
    
        Important:
        - Each day must be on a new line
        - Keep it concise with 1-3 topics per day
        - Include exactly {days} days
        - Add a blank line between each day for better readability
        """
    
        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[
                {"role": "system", "content": "You create simple, direct study plans with clear daily topics. Always put each day on a new line."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
    
        return self._clean_response(response.choices[0].message.content)
    
    def _clean_response(self, text: str) -> str:
        """Clean and format the response with proper line breaks"""
        lines = []
        for line in text.split('\n'):
            line = line.strip()
            if line.startswith(("Day ", "Final Day:")):
                lines.append(line)
    
        formatted_response = "\n\n".join(lines)
    
        return formatted_response if formatted_response else "Could not generate study plan"
    
    def suggest_revision_strategy(self, topic: str, weak_areas: List[str] = []) -> Dict:
        prompt = f"""
        In 3-5 bullet points, suggest a revision strategy for {topic}.
        Weak areas: {weak_areas if weak_areas else 'None specified'}
        Focus on practical techniques only.
        """
        
        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[
                {"role": "system", "content": "You provide concise revision strategies without fluff."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=300
        )
        
        return {
            "topic": topic,
            "strategy": response.choices[0].message.content,
            "weak_areas_focus": weak_areas
        }