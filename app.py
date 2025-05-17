import streamlit as st
from dotenv import load_dotenv
import os
import uuid
from agents.explanation_agent import ExplanationAgent
from agents.quiz_master_agent import QuizMasterAgent
from agents.exam_coach_agent import ExamCoachAgent
from services.document_ocr import process_uploaded_file

load_dotenv()
def set_custom_style():
    st.markdown("""
    <style>
    .main {
        background-color: #1a1a1a;
    }
    .stChatMessage {
        color: white !important;
    }
    
    .study-day {
        background-color: #2d2d2d;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .study-day h4 {
        color: #4a90e2 !important;
        margin-top: 0;
    }
    .study-activity {
        margin-left: 1rem;
    }
    
    .quiz-container {
        margin: 1rem 0;
    }
    .quiz-option {
        padding: 0.75rem;
        margin: 0.5rem 0;
        border-radius: 0.5rem;
        border: 1px solid #444;
        background-color: #2d2d2d;
        cursor: pointer;
        transition: all 0.2s;
        color: white !important;
    }
    .quiz-option:hover {
        background-color: #3d3d3d;
    }
    .quiz-option.selected {
        background-color: #1a5276;
        border-color: #4a90e2;
    }
    .quiz-option.correct {
        background-color: #145a32;
        border-color: #4CAF50;
    }
    .quiz-option.incorrect {
        background-color: #7b241c;
        border-color: #F44336;
    }
    </style>
    """, unsafe_allow_html=True)

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "document_text" not in st.session_state:
        st.session_state.document_text = ""
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None
    if "processing" not in st.session_state:
        st.session_state.processing = False
    if "current_quiz" not in st.session_state:
        st.session_state.current_quiz = None
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False
    if "selected_option" not in st.session_state:
        st.session_state.selected_option = None
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

def display_chat_message(role: str, content: str):
    """Displays chat messages with rich formatting based on content type"""
    with st.chat_message(role):
        if role == "assistant" and isinstance(content, dict):
            if content.get("type") == "study_plan":
                st.markdown(f"**{content['data']['title']}**")
                st.markdown("---")
                st.markdown(content['data']['content'])
            elif content.get("type") == "quiz":
                st.session_state.show_quiz = True
                st.session_state.current_quiz = content["data"]
                st.write(content.get("text", ""))
            else:
                st.write(content.get("text", "No content available"))
        else:
            st.markdown(content)

    

def generate_response(prompt: str, document_text: str):
    """Generate appropriate response based on prompt type"""
    prompt_lower = prompt.lower()
    
    if any(keyword in prompt_lower for keyword in ["plan", "schedule", "learn"]) and "day" in prompt_lower:
        days = 7  # Default
        if "5 day" in prompt_lower: days = 5
        elif "3 day" in prompt_lower: days = 3
        elif "7 day" in prompt_lower: days = 7
        
        exam_coach = ExamCoachAgent()
        
        subject = " ".join([word for word in prompt.split()if word.lower() not in ["create", "make", "generate", "study", "plan", 
"for", "days", "day", "revise", "a"]])

        plan = exam_coach.create_study_plan(
            subject=subject if subject else "Machine Learning",
            days=days,
            current_level="intermediate"
        )

        return {
            "type": "study_plan",
            "data": {
                "title": f"{days}-Day Study Plan",
                "content": plan  
            }
        }
    
    elif "quiz" in prompt_lower or "test me" in prompt_lower:
        quiz_master = QuizMasterAgent()
        quiz = quiz_master.generate_quiz(prompt, document_text)
        st.session_state.current_quiz = quiz
        st.session_state.quiz_answers = {}
        st.session_state.quiz_submitted = False
        return "Here's your quiz! Select your answers below."
    
    else:
        explanation_agent = ExplanationAgent()
        return explanation_agent.explain_topic(prompt, document_text)

def format_study_plan(plan: list, days: int) -> str:
    """Format study plan with enhanced visual structure and organization"""
    plan_header = f"""
    <div style='
        border-bottom: 2px solid #4a90e2;
        padding-bottom: 10px;
        margin-bottom: 20px;
    '>
        <h2 style='
            color: #4a90e2;
            margin-bottom: 5px;
        '>📚 Personalized {days}-Day Organic Chemistry Study Plan</h2>
        <p style='
            font-style: italic;
            color: #aaaaaa;
            margin-top: 0;
        '>Structured to help you master organic chemistry concepts efficiently</p>
    </div>
    """
    
    day_sections = []
    for i, day in enumerate(plan[:days]):
        if not day.get('content', '').strip():
            continue
        sections = {
            'topics': {'icon': '📚', 'title': 'Topics to Cover'},
            'techniques': {'icon': '✍️', 'title': 'Study Techniques'},
            'practice': {'icon': '🔍', 'title': 'Practice Activities'},
            'time': {'icon': '⏱️', 'title': 'Time Allocation'},
            'concepts': {'icon': '🎯', 'title': 'Key Concepts'},
            'resources': {'icon': '📖', 'title': 'Recommended Resources'}
        }
        current_section = None
        for line in day['content'].split('\n'):
            line = line.strip()
            if not line:
                continue
            if line.startswith('1. Topics to cover:'):
                current_section = 'topics'
            elif line.startswith('2. Recommended study techniques:'):
                current_section = 'techniques'
            elif line.startswith('3. Practice activities:'):
                current_section = 'practice'
            elif line.startswith('4. Time allocation:'):
                current_section = 'time'
            elif line.startswith('5. Key concepts to focus on:'):
                current_section = 'concepts'
            elif line.startswith('6. Recommended resources:'):
                current_section = 'resources'
            elif current_section and line.startswith('- '):
                sections[current_section].setdefault('items', []).append(line[2:])
        day_title = day.get('title', f'Day {i+1}')
        day_section = f"""
        <div class='study-day' style='
            background-color: #2d2d2d;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 25px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        '>
            <div style='
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
                border-bottom: 1px solid #444;
                padding-bottom: 10px;
            '>
                <h3 style='
                    color: #4a90e2;
                    margin: 0;
                    font-size: 1.2em;
                '>{day_title}</h3>
                <span style='
                    background-color: #1a5276;
                    color: white;
                    padding: 5px 12px;
                    border-radius: 20px;
                    font-size: 0.85em;
                    font-weight: 500;
                '>
                    {day.get('duration', '1-2 hours')}
                </span>
            </div>
            
            <div style='margin-bottom: 20px;'>
        """
        for key, section in sections.items():
            if section.get('items'):
                day_section += build_section(
                    icon=section['icon'],
                    title=section['title'],
                    items=section['items'],
                    is_resources=(key == 'resources')
                )
        day_section += f"""
            </div>
            
            <div style='
                margin-top: 15px;
                padding: 12px;
                background-color: #252525;
                border-radius: 6px;
                border-left: 4px solid #4a90e2;
            '>
                <p style='
                    margin: 0;
                    font-size: 0.95em;
                    color: #d4d4d4;
                '>
                    <strong style='color: #58a6ff;'>Pro Tip:</strong> 
                    {day.get('tip', 'Review previous material before starting new concepts.')}
                </p>
            </div>
        </div>
        """
        day_sections.append(day_section)
    
    plan_footer = """
    <div style='
        margin-top: 30px;
        padding: 20px;
        background-color: #1a3a1a;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
    '>
        <h4 style='
            color: #4CAF50;
            margin-top: 0;
            margin-bottom: 15px;
            font-size: 1.1em;
        '>📝 Study Plan Success Tips</h4>
        <ul style='
            margin-bottom: 0;
            padding-left: 25px;
        '>
            <li style='margin-bottom: 8px;'>Take <strong>short breaks</strong> every 45-60 minutes to maintain focus</li>
            <li style='margin-bottom: 8px;'><strong>Active recall</strong> (self-testing) is more effective than passive reading</li>
            <li style='margin-bottom: 8px;'>Review difficult concepts at the <strong>beginning</strong> of each study session</li>
            <li style='margin-bottom: 0;'>Use <strong>spaced repetition</strong> for better long-term retention</li>
        </ul>
    </div>
    """
    
    return plan_header + "".join(day_sections) + plan_footer

def build_section(icon: str, title: str, items: list, is_resources: bool = False) -> str:
    """Build consistent content sections with icons and styling"""
    if not items:
        return ""
    
    items_html = "".join([
        f"<li style='margin-bottom: 8px;'>{'🔗 ' if is_resources else '• '}{item}</li>"
        for item in items
    ])
    
    return f"""
    <div style='
        margin-bottom: 18px;
    '>
        <div style='
            display: flex;
            align-items: center;
            margin-bottom: 8px;
            color: #58a6ff;
        '>
            <span style='
                font-size: 1.2em;
                margin-right: 8px;
            '>{icon}</span>
            <h4 style='
                margin: 0;
                font-size: 1.05em;
            '>{title}</h4>
        </div>
        <ul style='
            margin: 0;
            padding-left: 30px;
            {'list-style-type: none;' if not is_resources else ''}
        '>
            {items_html}
        </ul>
    </div>
    """
def handle_file_upload():
    """Processes uploaded file and extracts text"""
    st.sidebar.title("📄 Study Materials")
    uploaded_file = st.sidebar.file_uploader(
        "Upload PDF or image files",
        type=["pdf", "png", "jpg", "jpeg"],
        key=f"file_uploader_{st.session_state.session_id}",
        label_visibility="collapsed"
    )
    
    if uploaded_file and (st.session_state.uploaded_file != uploaded_file):
        st.session_state.uploaded_file = uploaded_file
        st.session_state.processing = True
        
        try:
            st.session_state.document_text = process_uploaded_file(uploaded_file)
            st.sidebar.success("Document processed successfully!")
            st.session_state.messages.append({
                "role": "assistant", 
                "content": f"I've processed your {uploaded_file.type} document. You can now ask questions about it."
            })
        except Exception as e:
            st.sidebar.error(f"Error processing file: {str(e)}")
        
        st.session_state.processing = False

def handle_quiz_selection(question_idx, option_idx):
    """Handles quiz answer selection"""
    st.session_state.quiz_answers[str(question_idx)] = option_idx
    st.session_state.selected_option = option_idx

def render_quiz(quiz):
    """Render interactive quiz with unique keys"""
    if not quiz or not isinstance(quiz, dict) or 'questions' not in quiz:
        return
    
    if not st.session_state.quiz_submitted:
        st.markdown(f"### {quiz.get('topic', 'Quiz')}")
        
        for i, question in enumerate(quiz['questions']):
            if not isinstance(question, dict) or 'options' not in question:
                continue
                
            st.markdown(f"**{i+1}. {question.get('question', '')}**")
            
            cols = st.columns(2)
            for j, option in enumerate(question['options']):
                with cols[j % 2]:
                    selected = st.session_state.quiz_answers.get(str(i)) == j
                    st.button(
                        option,
                        key=f"q{i}_o{j}_{uuid.uuid4()}",
                        on_click=handle_quiz_selection,
                        args=(i, j),
                        type="primary" if selected else "secondary"
                    )
            
        if st.button(
            "Submit Quiz",
            key=f"submit_{uuid.uuid4()}", 
            on_click=lambda: st.session_state.update({
                "quiz_submitted": True,
                "messages": st.session_state.messages + [{
                    "role": "assistant",
                    "content": "Quiz submitted! Check your results above."
                }]
            })
        ):
            st.rerun()
    else:
        correct = 0
        results = []
        
        for i, question in enumerate(quiz['questions']):
            if not isinstance(question, dict) or 'options' not in question:
                continue
                
            user_answer = st.session_state.quiz_answers.get(str(i))
            correct_answer = question.get('correct_answer', -1)
            
            if isinstance(correct_answer, str) and correct_answer.isdigit():
                correct_answer = int(correct_answer)
            elif not isinstance(correct_answer, int):
                correct_answer = -1
                
            is_correct = user_answer == correct_answer if user_answer is not None else False
            
            if is_correct:
                correct += 1
            
            user_answer_text = question['options'][user_answer] if user_answer is not None and 0 <= user_answer < len(question['options']) else "No answer"
            correct_answer_text = question['options'][correct_answer] if 0 <= correct_answer < len(question['options']) else "Invalid answer"
            
            results.append({
                "question": question.get('question', ''),
                "user_answer": user_answer_text,
                "correct_answer": correct_answer_text,
                "is_correct": is_correct,
                "explanation": question.get('explanation', '')
            })
        
        score_percentage = int(correct/len(quiz['questions'])*100)
        st.markdown(f"### Quiz Results: {correct}/{len(quiz['questions'])} ({score_percentage}%)")
        
        if score_percentage >= 80:
            st.markdown("🎉 Excellent work! 🎉")
        elif score_percentage >= 60:
            st.markdown("👍 Good job! 👍")
        else:
            st.markdown("💪 Keep practicing! 💪")
        
        for result in results:
            with st.expander(f"Question: {result['question']}"):
                st.markdown(f"**Your answer:** {'✅' if result['is_correct'] else '❌'} {result['user_answer']}")
                if not result['is_correct']:
                    st.markdown(f"**Correct answer:** {result['correct_answer']}")
                if result['explanation']:
                    st.markdown(f"**Explanation:** {result['explanation']}")
        
        if st.button(
            "Submitted Quiz" ,
            key=f"try_again_{uuid.uuid4()}", 
            on_click=lambda: st.session_state.update({
                "quiz_submitted": False,
                "quiz_answers": {},
                "current_quiz": None,
                "messages": st.session_state.messages
            })
        ):
            st.rerun()
def main():
    set_custom_style()
    initialize_session_state()
    with st.sidebar:
        handle_file_upload()
        if st.session_state.document_text:
            st.markdown("### Document Preview")
            st.text_area(
                "Extracted Text", 
                value=st.session_state.document_text[:500] + ("..." if len(st.session_state.document_text) > 500 else ""), 
                height=200,
                disabled=True,
                key=f"document_preview_{st.session_state.session_id}"
            )
    
    st.title("🧠 Study Mentor AI")

    for message in st.session_state.messages:
        display_chat_message(message["role"], message["content"])
        
        # Render quiz after assistant message
        if message["role"] == "assistant" and st.session_state.current_quiz and "quiz" in message["content"]:
            render_quiz(st.session_state.current_quiz)

    if prompt := st.chat_input("Type your question here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.spinner("Thinking..."):
            response = generate_response(prompt, st.session_state.document_text)
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response
            })
        
        st.rerun()

if __name__ == "__main__":
    main()