def route_question(question: str, explanation_agent, quiz_master, exam_coach, context: str = ""):
    question_lower = question.lower()
    
    if any(keyword in question_lower for keyword in ["explain", "what is", "how does", "understand"]):
        return explanation_agent.explain_topic(question, context)
    elif any(keyword in question_lower for keyword in ["quiz", "test me", "questions", "mcq"]):
        num_q = 5  
        if "5 question" in question_lower:
            num_q = 5
        elif "10 question" in question_lower:
            num_q = 10
        quiz = quiz_master.generate_quiz(question, num_q, context)
        return format_quiz(quiz)
    elif any(keyword in question_lower for keyword in ["study plan", "revise", "prepare", "exam strategy"]):
        days = 7  
        if "5 day" in question_lower:
            days = 5
        elif "3 day" in question_lower:
            days = 3
        return exam_coach.create_study_plan(question, days)
    else:
        return explanation_agent.explain_topic(question, context)

def format_quiz(quiz: dict) -> str:
    formatted = f"## Quiz on {quiz['topic']}\n\n"
    for i, q in enumerate(quiz['questions']):
        formatted += f"{i+1}. {q['question']}\n"
        for j, option in enumerate(q['options']):
            formatted += f"   {chr(97+j)}. {option}\n"
        formatted += "\n"
    return formatted