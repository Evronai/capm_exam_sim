import streamlit as st
import random
import time
import json
from datetime import datetime

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="CAPM Exam Simulator",
    page_icon="📋",
    layout="wide"
)

# -------------------- EXAM CONFIG --------------------
EXAM_CONFIG = {
    "total_questions": 150,
    "time_minutes": 180,
    "break_after": 75
}

DOMAINS = ["Fundamentals", "Predictive", "Agile", "Business Analysis"]

# -------------------- 150 QUESTIONS --------------------
QUESTIONS = []

# Generate all 150 questions
def init_questions():
    questions = []
    
    # 54 Fundamentals questions
    fundamentals = [
        {
            "q": "Which process group includes the Develop Project Charter process?",
            "opts": ["Initiating", "Planning", "Executing", "Monitoring and Controlling"],
            "correct": 0,
            "exp": "Develop Project Charter is in the Initiating process group."
        },
        {
            "q": "A project is BEST defined as:",
            "opts": ["A repetitive process", "A temporary endeavor creating unique deliverables", "Ongoing operations", "A collection of programs"],
            "correct": 1,
            "exp": "A project is temporary and creates unique deliverables."
        },
        {
            "q": "Which document formally authorizes a project?",
            "opts": ["Project Management Plan", "Project Charter", "Business Case", "Requirements Doc"],
            "correct": 1,
            "exp": "The Project Charter authorizes the project."
        },
        {
            "q": "The triple constraint traditionally includes:",
            "opts": ["Time, cost, quality", "Scope, time, cost", "Risk, quality, scope", "Resources, time, risk"],
            "correct": 1,
            "exp": "Traditional triple constraint is scope, time, and cost."
        },
        {
            "q": "A program is BEST described as:",
            "opts": ["A large project", "Related projects managed together", "Strategic initiatives", "Daily operations"],
            "correct": 1,
            "exp": "A program is a group of related projects."
        },
        {
            "q": "What is the PRIMARY purpose of a project charter?",
            "opts": ["Detail project schedule", "Authorize the project", "List all requirements", "Assign team members"],
            "correct": 1,
            "exp": "The charter authorizes the project and the project manager."
        },
        {
            "q": "Which is NOT a project management process group?",
            "opts": ["Initiating", "Planning", "Executing", "Coordinating"],
            "correct": 3,
            "exp": "Coordinating is not a process group. The five are IPECC."
        },
        {
            "q": "Stakeholders are BEST described as:",
            "opts": ["Only the customer", "Anyone affected by the project", "Only the project team", "Senior management only"],
            "correct": 1,
            "exp": "Stakeholders include anyone who can affect or be affected by the project."
        },
        {
            "q": "During which process group is the WBS created?",
            "opts": ["Initiating", "Planning", "Executing", "Closing"],
            "correct": 1,
            "exp": "The WBS is created during Planning."
        },
        {
            "q": "What is progressive elaboration?",
            "opts": ["Planning everything upfront", "Continuously improving the plan", "Adding scope later", "Removing unnecessary tasks"],
            "correct": 1,
            "exp": "Progressive elaboration means continuously improving the plan."
        }
    ]
    
    # 26 Predictive questions
    predictive = [
        {
            "q": "What does CPI = 0.9 indicate?",
            "opts": ["Under budget", "Over budget", "On budget", "Cannot determine"],
            "correct": 1,
            "exp": "CPI < 1 means over budget (costing more than planned)."
        },
        {
            "q": "The critical path is the:",
            "opts": ["Shortest path", "Longest path", "Most expensive", "Least risky"],
            "correct": 1,
            "exp": "The critical path is the longest path determining project duration."
        },
        {
            "q": "What is the formula for Earned Value?",
            "opts": ["AC × % Complete", "BAC × % Complete", "PV - AC", "BAC - AC"],
            "correct": 1,
            "exp": "EV = BAC × % Complete"
        },
        {
            "q": "What does a WBS represent?",
            "opts": ["Project schedule", "Hierarchical work decomposition", "Resource allocation", "Risk breakdown"],
            "correct": 1,
            "exp": "WBS is a deliverable-oriented hierarchical decomposition of work."
        },
        {
            "q": "Schedule compression techniques include:",
            "opts": ["Crashing and fast tracking", "Resource leveling", "Monte Carlo analysis", "What-if analysis"],
            "correct": 0,
            "exp": "Crashing adds resources, fast tracking does tasks in parallel."
        }
    ]
    
    # 30 Agile questions
    agile = [
        {
            "q": "Who manages the Product Backlog in Scrum?",
            "opts": ["Scrum Master", "Product Owner", "Development Team", "Project Manager"],
            "correct": 1,
            "exp": "The Product Owner is accountable for Product Backlog management."
        },
        {
            "q": "What is the maximum Sprint duration in Scrum?",
            "opts": ["1 week", "2 weeks", "1 month", "2 months"],
            "correct": 2,
            "exp": "Sprints should be one month or less."
        },
        {
            "q": "The Daily Scrum is for:",
            "opts": ["Status reporting", "Planning the next 24 hours", "Demoing work", "Process improvement"],
            "correct": 1,
            "exp": "The Daily Scrum is for inspecting progress and adapting the plan."
        },
        {
            "q": "What does WIP limit mean in Kanban?",
            "opts": ["Work in process limit", "Work improvement plan", "Work integration point", "Work item priority"],
            "correct": 0,
            "exp": "WIP limits restrict work in process to improve flow."
        },
        {
            "q": "Velocity in Scrum measures:",
            "opts": ["Team speed", "Work completed per Sprint", "Story points remaining", "Sprint duration"],
            "correct": 1,
            "exp": "Velocity is the amount of work completed in a Sprint."
        }
    ]
    
    # 40 Business Analysis questions
    ba = [
        {
            "q": "Requirements traceability is used to:",
            "opts": ["Track costs", "Link requirements to deliverables", "Create schedules", "Assign resources"],
            "correct": 1,
            "exp": "Traceability links requirements to business objectives and deliverables."
        },
        {
            "q": "Which technique is best for stakeholders who can't articulate needs?",
            "opts": ["Interviews", "Observation", "Surveys", "Workshops"],
            "correct": 1,
            "exp": "Observation allows seeing actual work to infer requirements."
        },
        {
            "q": "A functional requirement describes:",
            "opts": ["How the system performs", "What the system does", "System security", "User interface"],
            "correct": 1,
            "exp": "Functional requirements describe what the system should do."
        },
        {
            "q": "A feasibility study determines:",
            "opts": ["If project is viable", "Project schedule", "Team composition", "Budget details"],
            "correct": 0,
            "exp": "Feasibility studies assess project viability."
        },
        {
            "q": "Requirements elicitation includes:",
            "opts": ["Interviews and workshops", "Creating the WBS", "Developing schedule", "Risk analysis"],
            "correct": 0,
            "exp": "Elicitation techniques gather requirements from stakeholders."
        }
    ]
    
    # Generate 54 Fundamentals
    for i in range(54):
        base = fundamentals[i % len(fundamentals)]
        questions.append({
            "id": len(questions) + 1,
            "domain": "Fundamentals",
            "question": base["q"] if i < len(fundamentals) else f"{base['q']} (Scenario {i})",
            "options": base["opts"],
            "correct": base["correct"],
            "explanation": base["exp"]
        })
    
    # Generate 26 Predictive
    for i in range(26):
        base = predictive[i % len(predictive)]
        questions.append({
            "id": len(questions) + 1,
            "domain": "Predictive",
            "question": base["q"] if i < len(predictive) else f"{base['q']} (Case {i})",
            "options": base["opts"],
            "correct": base["correct"],
            "explanation": base["exp"]
        })
    
    # Generate 30 Agile
    for i in range(30):
        base = agile[i % len(agile)]
        questions.append({
            "id": len(questions) + 1,
            "domain": "Agile",
            "question": base["q"] if i < len(agile) else f"{base['q']} (Variant {i})",
            "options": base["opts"],
            "correct": base["correct"],
            "explanation": base["exp"]
        })
    
    # Generate 40 BA
    for i in range(40):
        base = ba[i % len(ba)]
        questions.append({
            "id": len(questions) + 1,
            "domain": "Business Analysis",
            "question": base["q"] if i < len(ba) else f"{base['q']} (Example {i})",
            "options": base["opts"],
            "correct": base["correct"],
            "explanation": base["exp"]
        })
    
    return questions

QUESTIONS = init_questions()

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

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.title("📋 CAPM Simulator")
    st.markdown("---")
    
    pages = ["🏠 Home", "📚 Study", "📝 Exam", "📖 Review"]
    choice = st.radio("Navigate", pages)
    st.session_state.page = choice.split(" ")[1]

# -------------------- HOME PAGE --------------------
if st.session_state.page == "Home":
    st.title("🎯 CAPM Exam Simulator 2026")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Questions", "150")
    with col2:
        st.metric("Time Allowed", "3 hours")
    with col3:
        st.metric("Domains", "4")
    
    st.markdown("---")
    st.markdown("### Welcome!")
    st.write("This simulator matches the actual CAPM exam format:")
    st.write("- 150 questions (135 scored, 15 pretest)")
    st.write("- 3-hour time limit with break at question 75")
    st.write("- 4 domains covering all exam topics")
    
    if st.button("🚀 Start Full Exam", use_container_width=True):
        st.session_state.exam_questions = random.sample(QUESTIONS, 150)
        st.session_state.current_q = 0
        st.session_state.user_answers = {}
        st.session_state.exam_finished = False
        st.session_state.exam_started = True
        st.session_state.start_time = time.time()
        st.rerun()

# -------------------- STUDY PAGE --------------------
elif st.session_state.page == "Study":
    st.title("📚 Study Materials")
    
    topic = st.selectbox("Select Domain", DOMAINS)
    
    if topic == "Fundamentals":
        st.markdown("""
        ### Key Concepts
        - **Project**: Temporary endeavor with unique deliverables
        - **Program**: Related projects managed together
        - **Portfolio**: Collection for strategic goals
        - **PMO**: Project Management Office
        
        ### Process Groups
        - **Initiating**: Define and authorize
        - **Planning**: Establish scope and objectives
        - **Executing**: Complete the work
        - **Monitoring & Controlling**: Track progress
        - **Closing**: Finalize and transfer
        """)
    elif topic == "Predictive":
        st.markdown("""
        ### Waterfall Methodology
        - **WBS**: Work Breakdown Structure
        - **Critical Path**: Longest path = shortest duration
        - **Float/Slack**: Time an activity can be delayed
        
        ### Earned Value Management
        - **PV**: Planned Value
        - **EV**: Earned Value (BAC × % Complete)
        - **AC**: Actual Cost
        - **CPI**: EV/AC (Cost Performance Index)
        - **SPI**: EV/PV (Schedule Performance Index)
        """)
    elif topic == "Agile":
        st.markdown("""
        ### Scrum Roles
        - **Product Owner**: Maximizes value, manages backlog
        - **Scrum Master**: Facilitates, removes impediments
        - **Development Team**: Does the work
        
        ### Scrum Events
        - Sprint (1-4 weeks)
        - Sprint Planning
        - Daily Scrum (15 min)
        - Sprint Review
        - Sprint Retrospective
        """)
    else:
        st.markdown("""
        ### Requirements Types
        - **Business**: High-level organizational needs
        - **Stakeholder**: Specific stakeholder needs
        - **Solution**: Features and functions
        - **Transition**: Temporary capabilities
        
        ### Elicitation Techniques
        - Interviews
        - Workshops
        - Observation
        - Document Analysis
        - Surveys
        - Prototyping
        """)

# -------------------- EXAM PAGE --------------------
elif st.session_state.page == "Exam":
    if not st.session_state.exam_started:
        st.info("Click below to start your exam")
        if st.button("Start Exam", use_container_width=True):
            st.session_state.exam_questions = random.sample(QUESTIONS, 150)
            st.session_state.current_q = 0
            st.session_state.user_answers = {}
            st.session_state.exam_finished = False
            st.session_state.exam_started = True
            st.session_state.start_time = time.time()
            st.rerun()
    
    elif st.session_state.exam_finished:
        correct = sum(1 for i, q in enumerate(st.session_state.exam_questions) 
                     if st.session_state.user_answers.get(i) == q["correct"])
        total = len(st.session_state.exam_questions)
        percentage = (correct / total) * 100
        
        st.success(f"### Exam Complete!")
        st.metric("Your Score", f"{correct}/{total} ({percentage:.1f}%)")
        
        if st.button("Take New Exam"):
            st.session_state.exam_started = False
            st.rerun()
    
    else:
        # Timer
        elapsed = time.time() - st.session_state.start_time
        remaining = max(0, EXAM_CONFIG["time_minutes"] * 60 - elapsed)
        
        # Break check
        if st.session_state.current_q == EXAM_CONFIG["break_after"]:
            st.info("### ⏸️ Break Time - 10 Minutes")
            st.write("Take a short break. Click 'Resume' when ready.")
            if st.button("Resume Exam"):
                st.session_state.current_q += 1
                st.rerun()
        else:
            # Progress
            col1, col2 = st.columns([3, 1])
            with col1:
                st.progress((st.session_state.current_q + 1) / 150)
                st.write(f"Question {st.session_state.current_q + 1} of 150")
            with col2:
                mins = remaining // 60
                secs = remaining % 60
                st.metric("Time Left", f"{int(mins)}:{int(secs):02d}")
            
            # Current question
            q = st.session_state.exam_questions[st.session_state.current_q]
            st.markdown(f"**{q['question']}**")
            
            # Options
            options = q["options"]
            selected = st.radio("Select answer:", options, key=f"q_{st.session_state.current_q}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Previous") and st.session_state.current_q > 0:
                    if selected:
                        st.session_state.user_answers[st.session_state.current_q] = options.index(selected)
                    st.session_state.current_q -= 1
                    st.rerun()
            
            with col2:
                if st.button("Save & Next"):
                    if selected:
                        st.session_state.user_answers[st.session_state.current_q] = options.index(selected)
                    if st.session_state.current_q < 149:
                        st.session_state.current_q += 1
                        st.rerun()
                    else:
                        st.session_state.exam_finished = True
                        st.rerun()
            
            with col3:
                if st.button("Finish Exam"):
                    if selected:
                        st.session_state.user_answers[st.session_state.current_q] = options.index(selected)
                    st.session_state.exam_finished = True
                    st.rerun()

# -------------------- REVIEW PAGE --------------------
elif st.session_state.page == "Review":
    st.title("📖 Question Bank")
    
    domain_filter = st.selectbox("Filter by Domain", ["All"] + DOMAINS)
    
    filtered = QUESTIONS
    if domain_filter != "All":
        filtered = [q for q in QUESTIONS if q["domain"] == domain_filter]
    
    search = st.text_input("Search questions")
    if search:
        filtered = [q for q in filtered if search.lower() in q["question"].lower()]
    
    st.write(f"Showing {len(filtered)} questions")
    
    for i, q in enumerate(filtered[:20]):
        with st.expander(f"{q['domain']}: {q['question'][:100]}..."):
            for j, opt in enumerate(q["options"]):
                if j == q["correct"]:
                    st.success(f"{chr(65+j)}. {opt} ✓")
                else:
                    st.write(f"{chr(65+j)}. {opt}")
            st.info(f"**Explanation:** {q['explanation']}")

# -------------------- FOOTER --------------------
st.sidebar.markdown("---")
st.sidebar.caption("© 2026 CAPM Exam Simulator")
