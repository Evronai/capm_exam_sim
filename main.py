import streamlit as st
import random
import time
import json
import sqlite3
from datetime import datetime
import uuid
import os

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="CAPM Exam Simulator 2026",
    page_icon="📋",
    layout="wide"
)

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
    :root {
        --primary: #1E3A8A;
        --secondary: #2563EB;
        --success: #059669;
        --warning: #D97706;
        --danger: #DC2626;
    }
    .stButton > button {
        background-color: var(--primary);
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        width: 100%;
    }
    .metric-card {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# -------------------- EXAM CONFIG --------------------
EXAM_CONFIG = {
    "total_questions": 150,
    "scored_questions": 135,
    "pretest_questions": 15,
    "time_minutes": 180,
    "break_after": 75
}

DOMAIN_WEIGHTS = {
    "Fundamentals": 36,
    "Predictive": 17,
    "Agile": 20,
    "Business Analysis": 27
}

# -------------------- SIMPLIFIED QUESTION BANK --------------------
QUESTIONS = [
    # Domain 1: Fundamentals
    {
        "id": 1,
        "domain": "Fundamentals",
        "question": "Which process group includes the Develop Project Charter process?",
        "options": ["Initiating", "Planning", "Executing", "Monitoring and Controlling"],
        "correct": 0,
        "explanation": "Develop Project Charter is in the Initiating process group."
    },
    {
        "id": 2,
        "domain": "Fundamentals",
        "question": "A project is BEST defined as:",
        "options": [
            "A repetitive process",
            "A temporary endeavor creating unique deliverables",
            "Ongoing operations",
            "A collection of programs"
        ],
        "correct": 1,
        "explanation": "A project is temporary and creates unique deliverables."
    },
    {
        "id": 3,
        "domain": "Fundamentals",
        "question": "Which document formally authorizes a project?",
        "options": ["Project Management Plan", "Project Charter", "Business Case", "Requirements Doc"],
        "correct": 1,
        "explanation": "The Project Charter authorizes the project and names the PM."
    },
    {
        "id": 4,
        "domain": "Fundamentals",
        "question": "The triple constraint traditionally includes:",
        "options": ["Time, cost, quality", "Scope, time, cost", "Risk, quality, scope", "Resources, time, risk"],
        "correct": 1,
        "explanation": "The traditional triple constraint is scope, time, and cost."
    },
    {
        "id": 5,
        "domain": "Fundamentals",
        "question": "A program is BEST described as:",
        "options": ["A large project", "Related projects managed together", "Strategic initiatives", "Daily operations"],
        "correct": 1,
        "explanation": "A program is a group of related projects managed coordinately."
    },
    
    # Domain 2: Predictive
    {
        "id": 6,
        "domain": "Predictive",
        "question": "What does SPI = 0.8 indicate?",
        "options": ["Ahead of schedule", "Behind schedule", "On schedule", "Over budget"],
        "correct": 1,
        "explanation": "SPI < 1 indicates behind schedule. Only 80% of planned work completed."
    },
    {
        "id": 7,
        "domain": "Predictive",
        "question": "The critical path is the:",
        "options": ["Shortest path", "Longest path", "Most expensive path", "Riskiest path"],
        "correct": 1,
        "explanation": "The critical path is the longest path and determines project duration."
    },
    {
        "id": 8,
        "domain": "Predictive",
        "question": "What is the formula for Earned Value (EV)?",
        "options": ["AC × % Complete", "BAC × % Complete", "PV - AC", "BAC - AC"],
        "correct": 1,
        "explanation": "EV = BAC × % Complete. It represents value of work completed."
    },
    
    # Domain 3: Agile
    {
        "id": 9,
        "domain": "Agile",
        "question": "Who manages the Product Backlog in Scrum?",
        "options": ["Scrum Master", "Product Owner", "Development Team", "Project Manager"],
        "correct": 1,
        "explanation": "The Product Owner is accountable for Product Backlog management."
    },
    {
        "id": 10,
        "domain": "Agile",
        "question": "What is the maximum Sprint duration in Scrum?",
        "options": ["1 week", "2 weeks", "1 month", "2 months"],
        "correct": 2,
        "explanation": "Sprints should be one month or less to maintain consistency."
    },
    
    # Domain 4: Business Analysis
    {
        "id": 11,
        "domain": "Business Analysis",
        "question": "Requirements traceability is used to:",
        "options": ["Track costs", "Link requirements to deliverables", "Create schedules", "Assign resources"],
        "correct": 1,
        "explanation": "Traceability links requirements to business objectives and deliverables."
    },
    {
        "id": 12,
        "domain": "Business Analysis",
        "question": "Which technique is best for stakeholders who can't articulate needs?",
        "options": ["Interviews", "Observation", "Surveys", "Workshops"],
        "correct": 1,
        "explanation": "Observation allows seeing actual work to infer requirements."
    }
]

# Generate remaining questions to reach 150
while len(QUESTIONS) < 150:
    for q in QUESTIONS[:10]:
        new_q = q.copy()
        new_q["id"] = len(QUESTIONS) + 1
        new_q["question"] = f"Sample: {q['question']}"
        QUESTIONS.append(new_q)

# -------------------- HELPER FUNCTIONS --------------------
def get_user_id():
    if 'user_id' not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())[:8]
    return st.session_state.user_id

def generate_full_exam():
    exam = []
    # Simple distribution - just take first 150 questions
    exam = QUESTIONS[:150].copy()
    random.shuffle(exam)
    return exam

def calculate_score(questions, answers):
    correct = sum(1 for i, q in enumerate(questions) 
                 if i in answers and answers[i] == q["correct"])
    return correct, len(questions), (correct/len(questions)*100)

def format_time(seconds):
    return f"{seconds//3600:02d}:{(seconds%3600)//60:02d}:{seconds%60:02d}"

# -------------------- SESSION STATE --------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "exam_questions" not in st.session_state:
    st.session_state.exam_questions = []
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}
if "exam_finished" not in st.session_state:
    st.session_state.exam_finished = False
if "exam_started" not in st.session_state:
    st.session_state.exam_started = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "time_remaining" not in st.session_state:
    st.session_state.time_remaining = EXAM_CONFIG["time_minutes"] * 60

user_id = get_user_id()

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.title("📋 CAPM Simulator")
    st.markdown(f"**User:** {user_id}")
    
    pages = ["🏠 Home", "📚 Study", "📝 Exam", "📖 Review"]
    choice = st.radio("Go to", pages)
    st.session_state.page = choice.split(" ")[1]

# -------------------- PAGES --------------------
if st.session_state.page == "Home":
    st.title("CAPM® Exam Simulator")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Questions", "150")
    col2.metric("Time", "3 hours")
    col3.metric("Domains", "4")
    
    if st.button("📝 Start Full Exam", use_container_width=True):
        st.session_state.exam_questions = generate_full_exam()
        st.session_state.current_q = 0
        st.session_state.user_answers = {}
        st.session_state.exam_finished = False
        st.session_state.exam_started = True
        st.session_state.start_time = time.time()
        st.rerun()

elif st.session_state.page == "Study":
    st.title("Study Materials")
    topic = st.selectbox("Topic", list(DOMAIN_WEIGHTS.keys()))
    
    if topic == "Fundamentals":
        st.info("""
        **Key Concepts:**
        - Project: Temporary with unique deliverables
        - Program: Related projects managed together
        - Portfolio: Collection for strategic goals
        - Process Groups: IPECC (Initiating, Planning, Executing, Monitoring & Controlling, Closing)
        """)
    elif topic == "Predictive":
        st.info("""
        **Waterfall Methodology:**
        - WBS: Work Breakdown Structure
        - Critical Path: Longest path = shortest duration
        - EVM: PV, EV, AC, CPI, SPI
        - Formulas: EV = BAC × % Complete
        """)
    elif topic == "Agile":
        st.info("""
        **Scrum Framework:**
        - Roles: Product Owner, Scrum Master, Developers
        - Events: Sprint, Daily Scrum, Review, Retrospective
        - Artifacts: Product Backlog, Sprint Backlog, Increment
        """)
    else:
        st.info("""
        **Business Analysis:**
        - Requirements: Functional vs Non-functional
        - Elicitation: Interviews, Workshops, Observation
        - Traceability: Link requirements to deliverables
        """)

elif st.session_state.page == "Exam":
    if not st.session_state.exam_started:
        st.info("Click Start Exam to begin")
        if st.button("Start Exam"):
            st.session_state.exam_questions = generate_full_exam()
            st.session_state.current_q = 0
            st.session_state.user_answers = {}
            st.session_state.exam_finished = False
            st.session_state.exam_started = True
            st.session_state.start_time = time.time()
            st.rerun()
    else:
        if st.session_state.exam_finished:
            correct, total, pct = calculate_score(
                st.session_state.exam_questions, 
                st.session_state.user_answers
            )
            st.success(f"Score: {correct}/{total} ({pct:.1f}%)")
            
            if st.button("New Exam"):
                st.session_state.exam_started = False
                st.rerun()
        else:
            # Update timer
            elapsed = time.time() - st.session_state.start_time
            remaining = max(0, EXAM_CONFIG["time_minutes"] * 60 - elapsed)
            
            q_idx = st.session_state.current_q
            q = st.session_state.exam_questions[q_idx]
            
            st.header(f"Question {q_idx + 1}/150")
            st.metric("Time Left", format_time(remaining))
            st.write(f"**{q['question']}**")
            
            answer = st.radio("Select answer:", q["options"], key=f"q_{q_idx}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Save & Next") and answer:
                    st.session_state.user_answers[q_idx] = q["options"].index(answer)
                    if q_idx < 149:
                        st.session_state.current_q += 1
                        st.rerun()
                    else:
                        st.session_state.exam_finished = True
                        st.rerun()

elif st.session_state.page == "Review":
    st.title("Question Review")
    for i, q in enumerate(QUESTIONS[:20]):  # Show first 20
        with st.expander(f"Q{i+1}: {q['question'][:50]}..."):
            st.write(f"**Domain:** {q['domain']}")
            for j, opt in enumerate(q["options"]):
                if j == q["correct"]:
                    st.success(f"{chr(65+j)}. {opt} ✓")
                else:
                    st.write(f"{chr(65+j)}. {opt}")
            st.info(f"**Explanation:** {q['explanation']}")

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 CAPM Exam Simulator")
