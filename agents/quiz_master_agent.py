from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class QuizMasterAgent:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    
    def generate_quiz(self, topic: str, num_questions: int = 5, context: str = "") -> dict:
        prompt = f"""
        You are a Quiz Master AI that creates educational quizzes for students.
        Generate {num_questions} multiple-choice questions about: "{topic}"
        
        Context from their materials: {context[:2000] if context else "No additional context provided"}
        
        Return the questions in this JSON format:
        {{
            "topic": "the quiz topic",
            "questions": [
                {{
                    "question": "question text",
                    "options": ["option1", "option2", "option3", "option4"],
                    "correct_answer": "index of correct option (0-3)"
                }}
            ]
        }}
        """
        
        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[
                {"role": "system", "content": "You are a quiz generator that creates clear, educational multiple-choice questions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1000,
            response_format={"type": "json_object"}
        )
        
        return eval(response.choices[0].message.content)
    
    def evaluate_quiz(self, answers: dict, quiz: dict) -> dict:
        correct = 0
        results = []
        
        for i, question in enumerate(quiz['questions']):
            is_correct = answers.get(str(i)) == question['correct_answer']
            if is_correct:
                correct += 1
            
            results.append({
                "question": question['question'],
                "user_answer": question['options'][int(answers.get(str(i), -1))] if answers.get(str(i)) else "No answer",
                "correct_answer": question['options'][question['correct_answer']],
                "is_correct": is_correct,
                "explanation": f"Explanation for why {question['options'][question['correct_answer']]} is correct"
            })
        
        return {
            "score": f"{correct}/{len(quiz['questions'])}",
            "percentage": f"{(correct/len(quiz['questions']))*100}%",
            "results": results
        }