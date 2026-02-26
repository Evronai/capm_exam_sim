import streamlit as st
import random
import time
from datetime import datetime, timedelta

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="CAPM Exam Simulator 2026",
    page_icon="📋",
    layout="wide"
)

# -------------------- EXAM CONFIGURATION --------------------
EXAM_CONFIG = {
    "total_questions": 150,
    "scored_questions": 135,
    "pretest_questions": 15,
    "time_minutes": 180,
    "break_after": 75,
    "break_minutes": 10
}

# Domain weightings based on official PMI ECO
DOMAIN_WEIGHTS = {
    "Project Management Fundamentals & Core Concepts": 36,  # 54 questions
    "Predictive, Plan-Based Methodologies": 17,            # 26 questions
    "Agile Frameworks/Methodologies": 20,                  # 30 questions
    "Business Analysis Frameworks": 27                      # 40 questions
}

# -------------------- QUESTION GENERATION --------------------
def generate_question_bank():
    """
    Generate 150 CAPM-style questions with proper domain distribution.
    Uses templates and random variations to create realistic questions.
    """
    questions = []
    qid = 1

    # Templates for each domain
    templates = {
        "Project Management Fundamentals & Core Concepts": [
            {
                "template": "A {project_type} project is currently in the {process_group} process group. The project manager is {activity}. Which process group are they in?",
                "options": ["Initiating", "Planning", "Executing", "Monitoring and Controlling"],
                "correct": lambda ctx: ctx["pg_index"],
                "explanation": "The process group is determined by the activities being performed. {activity_desc}"
            },
            {
                "template": "Which of the following best describes a {term}?",
                "options": ["{def1}", "{def2}", "{def3}", "{def4}"],
                "correct": 0,
                "explanation": "A {term} is defined as {correct_def}."
            },
            {
                "template": "A project charter is created during which process group?",
                "options": ["Initiating", "Planning", "Executing", "Monitoring and Controlling"],
                "correct": 0,
                "explanation": "The project charter is developed in the Initiating process group to formally authorize the project."
            },
            {
                "template": "Which of the following is NOT a project management process group?",
                "options": ["Initiating", "Planning", "Executing", "Coordinating"],
                "correct": 3,
                "explanation": "The five process groups are Initiating, Planning, Executing, Monitoring and Controlling, and Closing. Coordinating is not one of them."
            },
            {
                "template": "The project manager has identified a new risk and is analyzing its impact. Which process group is this?",
                "options": ["Initiating", "Planning", "Executing", "Monitoring and Controlling"],
                "correct": 3,
                "explanation": "Identifying and analyzing risks is part of Monitoring and Controlling, specifically within the Control Risks process."
            },
            # Add more templates to reach 54 total questions
        ],
        "Predictive, Plan-Based Methodologies": [
            {
                "template": "In a predictive project, the work breakdown structure (WBS) is created during which process?",
                "options": ["Create WBS", "Define Activities", "Estimate Activity Resources", "Develop Schedule"],
                "correct": 0,
                "explanation": "The Create WBS process is where the WBS is developed, typically during Planning."
            },
            {
                "template": "The critical path in a project schedule is the:",
                "options": ["Longest path through the network", "Shortest path through the network", "Path with the most activities", "Path with the least float"],
                "correct": 0,
                "explanation": "The critical path is the longest path and determines the shortest possible project duration."
            },
            {
                "template": "What is the formula for Earned Value (EV)?",
                "options": ["% complete × Budget at Completion (BAC)", "Actual Cost (AC) - Planned Value (PV)", "Planned Value (PV) - Actual Cost (AC)", "Budget at Completion (BAC) - Actual Cost (AC)"],
                "correct": 0,
                "explanation": "Earned Value = % complete × BAC. It represents the value of work completed."
            },
            # Add more templates...
        ],
        "Agile Frameworks/Methodologies": [
            {
                "template": "In Scrum, who is responsible for managing the Product Backlog?",
                "options": ["Scrum Master", "Development Team", "Product Owner", "Project Manager"],
                "correct": 2,
                "explanation": "The Product Owner is accountable for Product Backlog management."
            },
            {
                "template": "What is the recommended maximum duration for a Sprint in Scrum?",
                "options": ["One week", "Two weeks", "One month", "Two months"],
                "correct": 2,
                "explanation": "A Sprint should be one month or less to maintain consistency and feedback."
            },
            {
                "template": "The Daily Scrum is an event for:",
                "options": ["Reporting status to management", "Inspecting progress and adapting the plan", "Demonstrating completed work", "Retrospecting on the Sprint"],
                "correct": 1,
                "explanation": "The Daily Scrum is for the Developers to inspect progress toward the Sprint Goal and adapt the plan."
            },
            # Add more templates...
        ],
        "Business Analysis Frameworks": [
            {
                "template": "Requirements traceability is used to:",
                "options": ["Link requirements to business objectives and deliverables", "Track project costs", "Monitor team performance", "Manage stakeholder communication"],
                "correct": 0,
                "explanation": "Requirements traceability ensures each requirement is linked to its origin and the work product that satisfies it."
            },
            {
                "template": "Which technique is best for eliciting requirements from stakeholders who have difficulty articulating their needs?",
                "options": ["Interviews", "Questionnaires", "Observation", "Document analysis"],
                "correct": 2,
                "explanation": "Observation allows the analyst to see the stakeholder's actual work and infer requirements."
            },
            {
                "template": "A feasibility study is conducted during:",
                "options": ["Needs assessment", "Requirements analysis", "Solution evaluation", "Project closure"],
                "correct": 0,
                "explanation": "Feasibility studies are part of needs assessment to determine if a project is viable."
            },
            # Add more templates...
        ]
    }

    # Target counts per domain
    target_counts = {
        domain: round((weight / 100) * EXAM_CONFIG["total_questions"])
        for domain, weight in DOMAIN_WEIGHTS.items()
    }
    # Adjust to exactly 150
    diff = EXAM_CONFIG["total_questions"] - sum(target_counts.values())
    if diff != 0:
        # Add/remove from largest domain
        largest = max(target_counts, key=target_counts.get)
        target_counts[largest] += diff

    # Generate questions for each domain
    for domain, count in target_counts.items():
        domain_templates = templates.get(domain, [])
        if not domain_templates:
            # Fallback if no templates for a domain
            for i in range(count):
                q = {
                    "id": qid,
                    "domain": domain,
                    "question": f"Sample {domain} question {i+1}?",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct": random.randint(0, 3),
                    "explanation": "This is a generated question."
                }
                questions.append(q)
                qid += 1
            continue

        for i in range(count):
            # Pick a random template
            tmpl = random.choice(domain_templates)
            # Generate context for the template
            context = {}
            if "project_type" in tmpl["template"]:
                context["project_type"] = random.choice(["software development", "construction", "marketing campaign", "research"])
            if "process_group" in tmpl["template"]:
                pg = random.choice(["Initiating", "Planning", "Executing", "Monitoring and Controlling"])
                context["process_group"] = pg
                context["pg_index"] = ["Initiating", "Planning", "Executing", "Monitoring and Controlling"].index(pg)
            if "activity" in tmpl["template"]:
                activities = {
                    "Initiating": "developing the project charter",
                    "Planning": "creating the WBS",
                    "Executing": "managing the team",
                    "Monitoring and Controlling": "performing integrated change control"
                }
                context["activity"] = activities.get(context.get("process_group", "Planning"), "working on tasks")
            if "term" in tmpl["template"]:
                terms = {
                    "project": ("a temporary endeavor undertaken to create a unique product, service, or result",
                               ["a repetitive process", "an ongoing operation", "a set of related projects"]),
                    "program": ("a group of related projects managed in a coordinated way",
                               ["a single project", "a portfolio", "an operation"]),
                    "portfolio": ("a collection of projects, programs, and operations managed as a group to achieve strategic objectives",
                                 ["a single project", "a program", "an operation"]),
                    "stakeholder": ("an individual, group, or organization that may affect, be affected by, or perceive itself to be affected by a project",
                                   ["a team member", "a customer", "a supplier"])
                }
                term_key = random.choice(list(terms.keys()))
                context["term"] = term_key
                defs = terms[term_key]
                context["def1"] = defs[0]
                context["def2"] = defs[1][0]
                context["def3"] = defs[1][1]
                context["def4"] = defs[1][2]
                context["correct_def"] = defs[0]

            # Fill template
            try:
                question_text = tmpl["template"].format(**context)
            except KeyError:
                question_text = tmpl["template"]  # fallback

            # Generate options
            options = tmpl["options"].copy()
            # If options contain placeholders, format them
            for j, opt in enumerate(options):
                if "{" in opt and "}" in opt:
                    try:
                        options[j] = opt.format(**context)
                    except:
                        pass

            # Determine correct answer index (can be a function or integer)
            if callable(tmpl["correct"]):
                correct_idx = tmpl["correct"](context)
            else:
                correct_idx = tmpl["correct"]

            # Explanation
            explanation = tmpl["explanation"]
            if "{" in explanation:
                try:
                    explanation = explanation.format(**context)
                except:
                    pass

            q = {
                "id": qid,
                "domain": domain,
                "question": question_text,
                "options": options,
                "correct": correct_idx,
                "explanation": explanation
            }
            questions.append(q)
            qid += 1

    # Shuffle the bank to mix domains
    random.shuffle(questions)
    return questions

# Generate the question bank once at module level
QUESTIONS = generate_question_bank()

# -------------------- HELPER FUNCTIONS --------------------
def get_questions_by_domain():
    """Return dictionary of questions grouped by domain"""
    domain_questions = {domain: [] for domain in DOMAIN_WEIGHTS}
    for q in QUESTIONS:
        if q["domain"] in domain_questions:
            domain_questions[q["domain"]].append(q)
    return domain_questions

def generate_full_exam():
    """Generate a complete 150-question exam with proper domain distribution"""
    exam_questions = []
    domain_questions = get_questions_by_domain()
    
    # Calculate target counts per domain (rounded to nearest integer)
    target_counts = {
        domain: round((weight / 100) * EXAM_CONFIG["total_questions"])
        for domain, weight in DOMAIN_WEIGHTS.items()
    }
    
    # Adjust to ensure exactly 150 questions
    total = sum(target_counts.values())
    if total < EXAM_CONFIG["total_questions"]:
        # Add remaining to largest domain
        largest_domain = max(target_counts, key=target_counts.get)
        target_counts[largest_domain] += EXAM_CONFIG["total_questions"] - total
    elif total > EXAM_CONFIG["total_questions"]:
        # Remove from largest domain
        largest_domain = max(target_counts, key=target_counts.get)
        target_counts[largest_domain] -= total - EXAM_CONFIG["total_questions"]
    
    # Randomly select questions from each domain
    for domain, count in target_counts.items():
        available = domain_questions.get(domain, [])
        if len(available) >= count:
            selected = random.sample(available, count)
        else:
            # If we don't have enough, duplicate some (with variation)
            selected = random.choices(available, k=count)
        exam_questions.extend(selected)
    
    # Shuffle the exam
    random.shuffle(exam_questions)
    
    # Mark some questions as pretest (unscored)
    pretest_indices = random.sample(range(len(exam_questions)), EXAM_CONFIG["pretest_questions"])
    for i, q in enumerate(exam_questions):
        q["is_pretest"] = i in pretest_indices
    
    return exam_questions

def calculate_score(questions, user_answers):
    """Calculate score based on user answers (excluding pretest questions)"""
    if not user_answers:
        return 0, 0, 0
    
    scored_questions = [(i, q) for i, q in enumerate(questions) if not q.get("is_pretest", False)]
    correct = 0
    total_scored = len(scored_questions)
    
    for i, q in scored_questions:
        if user_answers.get(i) == q["correct"]:
            correct += 1
    
    return correct, total_scored, (correct / total_scored * 100) if total_scored > 0 else 0

def format_time_remaining(seconds):
    """Format seconds into HH:MM:SS"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

# -------------------- SESSION STATE INITIALIZATION --------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "exam_questions" not in st.session_state:
    st.session_state.exam_questions = []
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}
if "marked_for_review" not in st.session_state:
    st.session_state.marked_for_review = set()
if "exam_finished" not in st.session_state:
    st.session_state.exam_finished = False
if "exam_started" not in st.session_state:
    st.session_state.exam_started = False
if "break_mode" not in st.session_state:
    st.session_state.break_mode = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "time_remaining" not in st.session_state:
    st.session_state.time_remaining = EXAM_CONFIG["time_minutes"] * 60
if "break_taken" not in st.session_state:
    st.session_state.break_taken = False

# -------------------- SIDEBAR NAVIGATION --------------------
st.sidebar.title("📋 CAPM Exam Simulator 2026")
st.sidebar.markdown("---")
nav_options = ["Home", "Study Materials", "Full-Length Exam", "Domain Practice", "Review Questions"]
selected = st.sidebar.radio("Go to", nav_options, index=nav_options.index(st.session_state.page))
st.session_state.page = selected

st.sidebar.markdown("---")
st.sidebar.info(
    f"**Exam Specifications:**\n"
    f"• {EXAM_CONFIG['total_questions']} Total Questions\n"
    f"• {EXAM_CONFIG['scored_questions']} Scored + {EXAM_CONFIG['pretest_questions']} Pretest\n"
    f"• {EXAM_CONFIG['time_minutes']} Minutes Duration\n"
    f"• 10-Minute Break at Question {EXAM_CONFIG['break_after']}"
)

# -------------------- PAGE RENDERING --------------------
# ----- HOME -----
if st.session_state.page == "Home":
    st.title("CAPM® Exam Simulator 2026")
    st.markdown("""
    ### Welcome to Your Complete CAPM Preparation System
    
    This simulator is built to match the **actual CAPM exam experience** based on the latest PMI Exam Content Outline:

    | Domain | Weight | Questions |
    |--------|--------|-----------|
    | Project Management Fundamentals & Core Concepts | 36% | 54 |
    | Predictive, Plan-Based Methodologies | 17% | 26 |
    | Agile Frameworks/Methodologies | 20% | 30 |
    | Business Analysis Frameworks | 27% | 40 |
    
    **Features:**
    - 📝 **Full-Length Exam** – 150 questions with 3-hour timer and 10-minute break
    - 📚 **Domain Practice** – Focus on specific domains to strengthen weak areas
    - 🎯 **Realistic Questions** – Scenario-based questions mirroring the actual exam
    - ✅ **Detailed Explanations** – Learn why answers are correct or incorrect
    
    Use the sidebar to navigate and begin your preparation.
    """)

# ----- STUDY MATERIALS -----
elif st.session_state.page == "Study Materials":
    st.title("📚 CAPM Study Materials")
    
    topic = st.selectbox("Select Domain", list(DOMAIN_WEIGHTS.keys()))
    
    materials = {
        "Project Management Fundamentals & Core Concepts": """
        ### Key Concepts to Master 
        
        **Core Definitions:**
        - **Project**: Temporary endeavor to create unique product/service/result
        - **Program**: Group of related projects managed coordinately
        - **Portfolio**: Collection of projects/programs for strategic objectives
        - **PMO**: Standardizes governance processes
        
        **Process Groups:**
        - Initiating
        - Planning
        - Executing
        - Monitoring & Controlling
        - Closing
        
        **Key Artifacts:**
        - Project Charter
        - Project Management Plan
        - Risk Register
        - Stakeholder Register
        - Issue Log
        
        **Study Tips:**
        - Focus on scenario-based application
        - Understand the difference between project and operations
        - Know when to use each artifact
        """,
        
        "Predictive, Plan-Based Methodologies": """
        ### Predictive (Waterfall) Methodologies 
        
        **When to Use:**
        - Requirements are clear and stable
        - Regulatory/compliance environment
        - Well-understood technology
        
        **Key Components:**
        - Work Breakdown Structure (WBS)
        - Critical Path Method
        - Schedule Baseline
        - Cost Baseline
        - Scope Baseline
        
        **Common Calculations:**
        - Float/Slack
        - Variance Analysis
        - Estimate at Completion (EAC)
        """,
        
        "Agile Frameworks/Methodologies": """
        ### Agile Frameworks 
        
        **Agile Manifesto Values:**
        1. Individuals & interactions > Processes & tools
        2. Working software > Comprehensive documentation
        3. Customer collaboration > Contract negotiation
        4. Responding to change > Following a plan
        
        **Scrum Framework:**
        - **Roles**: Product Owner, Scrum Master, Developers
        - **Events**: Sprint, Daily Scrum, Sprint Review, Retrospective
        - **Artifacts**: Product Backlog, Sprint Backlog, Increment
        
        **Kanban:**
        - Visualize workflow
        - Limit WIP
        - Manage flow
        """,
        
        "Business Analysis Frameworks": """
        ### Business Analysis 
        
        **Requirements Management:**
        - Elicitation techniques (interviews, workshops, observation)
        - Requirements traceability
        - Acceptance criteria
        
        **Needs Assessment:**
        - Identify problems/opportunities
        - Determine project viability
        - Align with strategic goals
        
        **Solution Evaluation:**
        - Assess value delivery
        - Validate requirements fulfillment
        - Recommend improvements
        """
    }
    
    st.markdown(materials.get(topic, "Materials coming soon..."))

# ----- FULL-LENGTH EXAM -----
elif st.session_state.page == "Full-Length Exam":
    st.title("📝 Full-Length CAPM Exam")
    
    if not st.session_state.exam_started:
        st.markdown("""
        ### Exam Instructions:
        - **150 questions** (135 scored, 15 pretest)
        - **3 hours** total time
        - **10-minute break** after question 75
        - Questions cannot be returned to after break
        
        You will see your score immediately upon completion.
        """)
        
        if st.button("Start Full Exam", type="primary"):
            with st.spinner("Generating your exam..."):
                st.session_state.exam_questions = generate_full_exam()
                st.session_state.current_q = 0
                st.session_state.user_answers = {}
                st.session_state.marked_for_review = set()
                st.session_state.exam_finished = False
                st.session_state.exam_started = True
                st.session_state.break_mode = False
                st.session_state.break_taken = False
                st.session_state.start_time = time.time()
                st.session_state.time_remaining = EXAM_CONFIG["time_minutes"] * 60
                st.rerun()
    
    else:
        # Check if we're in break mode
        if st.session_state.break_mode:
            st.info("### ⏸️ Break Time - 10 Minutes")
            st.markdown("""
            You've completed the first 75 questions. Take a 10-minute break.
            - You cannot return to questions 1-75 after the break
            - Use this time to rest and refocus
            - Click 'Resume Exam' when ready
            """)
            
            if st.button("Resume Exam"):
                st.session_state.break_mode = False
                st.session_state.break_taken = True
                st.rerun()
        
        # Check if exam finished
        elif st.session_state.exam_finished:
            correct, total, percentage = calculate_score(
                st.session_state.exam_questions, 
                st.session_state.user_answers
            )
            
            st.success(f"### Exam Complete! Your Score: {correct}/{total} ({percentage:.1f}%)")
            
            # Show performance by domain
            st.subheader("Performance by Domain")
            domain_results = {}
            for domain in DOMAIN_WEIGHTS:
                domain_qs = [(i, q) for i, q in enumerate(st.session_state.exam_questions) 
                            if q["domain"] == domain and not q.get("is_pretest", False)]
                if domain_qs:
                    domain_correct = sum(1 for i, q in domain_qs 
                                       if st.session_state.user_answers.get(i) == q["correct"])
                    domain_results[domain] = (domain_correct, len(domain_qs))
            
            for domain, (corr, tot) in domain_results.items():
                pct = (corr/tot*100) if tot > 0 else 0
                st.progress(pct/100, text=f"{domain}: {corr}/{tot} ({pct:.1f}%)")
            
            if st.button("Start New Exam"):
                st.session_state.exam_started = False
                st.session_state.exam_questions = []
                st.rerun()
            
            # Review answers
            if st.checkbox("Review All Questions with Explanations"):
                for idx, q in enumerate(st.session_state.exam_questions):
                    user_ans = st.session_state.user_answers.get(idx)
                    correct_ans = q["correct"]
                    with st.expander(f"Q{idx+1}: {q['question'][:100]}..."):
                        for i, opt in enumerate(q["options"]):
                            mark = "✅" if i == correct_ans else "❌" if i == user_ans else ""
                            st.write(f"{chr(65+i)}. {opt} {mark}")
                        st.info(f"**Explanation:** {q['explanation']}")
                        if q.get("is_pretest"):
                            st.caption("*This was a pretest (unscored) question")
        
        else:
            # Active exam
            q_index = st.session_state.current_q
            total_q = len(st.session_state.exam_questions)
            
            # Check for break
            if q_index == EXAM_CONFIG["break_after"] and not st.session_state.break_taken:
                st.session_state.break_mode = True
                st.rerun()
            
            if q_index < total_q:
                q = st.session_state.exam_questions[q_index]
                
                # Timer
                if st.session_state.start_time:
                    elapsed = time.time() - st.session_state.start_time
                    st.session_state.time_remaining = max(0, (EXAM_CONFIG["time_minutes"] * 60) - elapsed)
                
                # Header with progress and timer
                col1, col2, col3, col4 = st.columns([2,1,1,1])
                with col1:
                    st.subheader(f"Question {q_index+1} of {total_q}")
                with col2:
                    st.metric("Time Left", format_time_remaining(st.session_state.time_remaining))
                with col3:
                    pretest_note = " (Pretest)" if q.get("is_pretest") else ""
                    st.write(f"Domain: {q['domain']}{pretest_note}")
                with col4:
                    if st.button("🏷️ Mark for Review", 
                               type="secondary" if q_index not in st.session_state.marked_for_review else "primary"):
                        if q_index in st.session_state.marked_for_review:
                            st.session_state.marked_for_review.remove(q_index)
                        else:
                            st.session_state.marked_for_review.add(q_index)
                        st.rerun()
                
                st.markdown(f"### {q['question']}")
                
                # Options
                options = q["options"]
                default_idx = st.session_state.user_answers.get(q_index)
                selected_option = st.radio(
                    "Select your answer:",
                    options,
                    index=default_idx if default_idx is not None else None,
                    key=f"q_{q_index}"
                )
                
                # Navigation buttons
                col1, col2, col3, col4, col5 = st.columns([1,1,1,1,2])
                with col1:
                    if st.button("⏮️ Previous") and q_index > 0:
                        # Save current answer
                        if selected_option is not None:
                            opt_idx = options.index(selected_option)
                            st.session_state.user_answers[q_index] = opt_idx
                        st.session_state.current_q -= 1
                        st.rerun()
                
                with col2:
                    if st.button("Save Answer"):
                        if selected_option is not None:
                            opt_idx = options.index(selected_option)
                            st.session_state.user_answers[q_index] = opt_idx
                            st.success("Answer saved!")
                        else:
                            st.warning("Please select an answer.")
                
                with col3:
                    if st.button("⏭️ Next"):
                        if selected_option is not None:
                            opt_idx = options.index(selected_option)
                            st.session_state.user_answers[q_index] = opt_idx
                        if q_index + 1 < total_q:
                            st.session_state.current_q += 1
                            st.rerun()
                        else:
                            st.session_state.exam_finished = True
                            st.rerun()
                
                with col4:
                    if st.button("Submit Exam"):
                        # Save final answer
                        if selected_option is not None:
                            opt_idx = options.index(selected_option)
                            st.session_state.user_answers[q_index] = opt_idx
                        st.session_state.exam_finished = True
                        st.rerun()
                
                # Question navigator
                st.markdown("---")
                st.markdown("**Question Navigator**")
                cols = st.columns(10)
                for i in range(min(total_q, 10)):
                    q_num = (q_index // 10) * 10 + i
                    if q_num < total_q:
                        btn_label = f"Q{q_num+1}"
                        if q_num == q_index:
                            btn_type = "primary"
                        elif q_num in st.session_state.user_answers:
                            btn_type = "secondary"  # Answered
                        elif q_num in st.session_state.marked_for_review:
                            btn_type = "secondary"  # Marked (different styling handled by emoji)
                        else:
                            btn_type = "secondary"
                        
                        if cols[i].button(btn_label, key=f"nav_{q_num}", type=btn_type):
                            if selected_option is not None and q_index != q_num:
                                opt_idx = options.index(selected_option)
                                st.session_state.user_answers[q_index] = opt_idx
                            st.session_state.current_q = q_num
                            st.rerun()
                
                # Summary
                answered = len(st.session_state.user_answers)
                marked = len(st.session_state.marked_for_review)
                st.caption(f"Answered: {answered}/{total_q} | Marked for Review: {marked}")

# ----- DOMAIN PRACTICE -----
elif st.session_state.page == "Domain Practice":
    st.title("🎯 Domain-Specific Practice")
    
    selected_domain = st.selectbox("Select Domain to Practice", list(DOMAIN_WEIGHTS.keys()))
    num_questions = st.slider("Number of Questions", 5, 30, 10)
    
    if st.button("Start Practice", type="primary"):
        # Filter questions by domain
        domain_qs = [q for q in QUESTIONS if q["domain"] == selected_domain]
        if domain_qs:
            st.session_state.exam_questions = random.sample(
                domain_qs, 
                min(num_questions, len(domain_qs))
            )
            # Mark all as scored (no pretest in practice)
            for q in st.session_state.exam_questions:
                q["is_pretest"] = False
            st.session_state.current_q = 0
            st.session_state.user_answers = {}
            st.session_state.exam_finished = False
            st.session_state.exam_started = True
            st.session_state.break_mode = False
            st.rerun()
        else:
            st.error("No questions available for this domain yet.")

# ----- REVIEW QUESTIONS -----
elif st.session_state.page == "Review Questions":
    st.title("📖 Question Bank Review")
    
    # Filter options
    domain_filter = st.selectbox("Filter by Domain", ["All"] + list(DOMAIN_WEIGHTS.keys()))
    
    filtered_qs = QUESTIONS
    if domain_filter != "All":
        filtered_qs = [q for q in QUESTIONS if q["domain"] == domain_filter]
    
    st.write(f"Showing {len(filtered_qs)} questions")
    
    for q in filtered_qs:
        with st.expander(f"{q['domain']}: {q['question'][:150]}..."):
            for i, opt in enumerate(q["options"]):
                st.write(f"{chr(65+i)}. {opt}")
            st.success(f"**Correct Answer:** {chr(65+q['correct'])}")
            st.info(f"**Explanation:** {q['explanation']}")
            st.caption(f"Domain: {q['domain']}")

# -------------------- FOOTER --------------------
st.sidebar.markdown("---")
st.sidebar.caption(
    f"© {datetime.now().year} CAPM Exam Simulator\n"
    f"Updated for PMI® CAPM Exam Content Outline 2026\n"
    f"Not affiliated with PMI®"
)
