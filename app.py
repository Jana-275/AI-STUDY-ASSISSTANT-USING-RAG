"""
StudyNova - AI Study Assistant
Main Streamlit Application

Features:
1. Study Materials
2. Ask AI
3. Quiz
4. My Progress
5. Study Plan
"""

import time
from datetime import date, timedelta

import streamlit as st

import config
import rag
import quiz
import memory
import study_plan
import tools


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="StudyNova | AI Study Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM DESIGN
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    .stApp {
        background: #f5f7fb;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid #1f2937;
    }

    section[data-testid="stSidebar"] * {
        color: #f9fafb;
    }

    section[data-testid="stSidebar"] .stRadio label {
        background: transparent;
        border-radius: 10px;
        padding: 10px 12px;
        margin-bottom: 4px;
        transition: 0.2s;
    }

    section[data-testid="stSidebar"] .stRadio label:hover {
        background: #1f2937;
    }

    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
        gap: 4px;
    }


    /* ---------- BUTTONS ---------- */

    .stButton > button {
        border-radius: 9px;
        border: 1px solid #dbe2ea;
        font-weight: 600;
        min-height: 42px;
        transition: 0.2s;
    }

    .stButton > button:hover {
        border-color: #6366f1;
        color: #4f46e5;
    }

    .stDownloadButton > button {
        border-radius: 9px;
        font-weight: 600;
    }


    /* ---------- INPUTS ---------- */

    .stTextInput input,
    .stTextArea textarea,
    .stSelectbox div[data-baseweb="select"],
    .stNumberInput input {
        border-radius: 9px;
    }


    /* ---------- CARDS ---------- */

    .card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 18px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    }

    .small-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 18px;
        height: 100%;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03);
    }


    /* ---------- BRAND ---------- */

    .brand {
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 2px;
    }

    .brand-sub {
        color: #9ca3af;
        font-size: 12px;
        letter-spacing: 2px;
        font-weight: 600;
    }


    /* ---------- PAGE HEADER ---------- */

    .page-title {
        font-size: 34px;
        font-weight: 800;
        color: #111827;
        letter-spacing: -1px;
        margin-bottom: 4px;
    }

    .page-description {
        color: #6b7280;
        font-size: 15px;
        margin-bottom: 25px;
    }


    /* ---------- HERO ---------- */

    .hero {
        background: linear-gradient(
            135deg,
            #111827 0%,
            #312e81 55%,
            #4f46e5 100%
        );
        color: white;
        border-radius: 20px;
        padding: 32px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px rgba(79, 70, 229, 0.18);
    }

    .hero-title {
        font-size: 27px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .hero-text {
        color: #e5e7eb;
        font-size: 15px;
        line-height: 1.6;
    }


    /* ---------- SECTION TITLE ---------- */

    .section-title {
        font-size: 20px;
        font-weight: 750;
        color: #111827;
        margin-top: 10px;
        margin-bottom: 12px;
    }


    /* ---------- METRICS ---------- */

    div[data-testid="metric-container"] {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 15px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03);
    }


    /* ---------- CHAT ---------- */

    div[data-testid="stChatMessage"] {
        border-radius: 14px;
        margin-bottom: 10px;
    }


    /* ---------- EXPANDERS ---------- */

    div[data-testid="stExpander"] {
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        background: white;
    }


    /* ---------- STATUS ---------- */

    .status-good {
        color: #047857;
        font-weight: 700;
    }

    .status-empty {
        color: #6b7280;
        font-weight: 600;
    }


    /* ---------- QUIZ ---------- */

    .quiz-header {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 20px;
    }

    .quiz-name {
        font-size: 23px;
        font-weight: 800;
        color: #111827;
    }

    .quiz-info {
        color: #6b7280;
        margin-top: 5px;
    }


    /* ---------- FOOTER ---------- */

    .app-footer {
        text-align: center;
        color: #9ca3af;
        font-size: 13px;
        padding-top: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "current_quiz" not in st.session_state:
    st.session_state.current_quiz = None

if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}

if "quiz_results" not in st.session_state:
    st.session_state.quiz_results = None

if "quiz_topic" not in st.session_state:
    st.session_state.quiz_topic = ""

if "generated_plan" not in st.session_state:
    st.session_state.generated_plan = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">StudyNova</div>
        <div class="brand-sub">AI STUDY ASSISTANT</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.caption("YOUR WORKSPACE")

    nav_choice = st.radio(
        "Navigation",
        [
            "📚 Study Materials",
            "💬 Ask AI",
            "📝 Quiz",
            "📊 My Progress",
            "📅 Study Plan",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")

    try:
        sidebar_status = rag.get_vector_store_status()

        if sidebar_status["is_ready"]:
            st.success(
                f"Knowledge base ready\n\n"
                f"{sidebar_status['total_chunks']} chunks"
            )
        else:
            st.info("Knowledge base is empty")

    except Exception:
        st.warning("Knowledge base unavailable")

    st.markdown("---")

    st.caption("StudyNova")
    st.caption("Learn smarter. Study better.")


# ============================================================
# MAIN APPLICATION HEADER
# ============================================================

st.markdown(
    """
    <div class="page-title">StudyNova</div>
    <div class="page-description">
        Your personal AI-powered workspace for learning, practice and exam preparation.
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 1. STUDY MATERIALS
# ============================================================

if nav_choice == "📚 Study Materials":

    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">Build your learning library</div>
            <div class="hero-text">
                Upload your lecture notes, textbooks and course materials.
                StudyNova processes your PDFs and creates a searchable knowledge base
                for AI-powered question answering.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.6, 1])

    with left:

        st.markdown(
            '<div class="section-title">Add study materials</div>',
            unsafe_allow_html=True,
        )

        uploaded_files = st.file_uploader(
            "Upload PDF files",
            type=["pdf"],
            accept_multiple_files=True,
            help="You can upload lecture notes, textbooks, question banks and study materials.",
        )

        if uploaded_files:

            st.info(
                f"{len(uploaded_files)} PDF file(s) selected."
            )

            process_btn = st.button(
                "Process & Add to Library",
                type="primary",
                use_container_width=True,
            )

            if process_btn:

                for uploaded_file in uploaded_files:

                    file_path = (
                        config.UPLOADS_DIR / uploaded_file.name
                    )

                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    with st.spinner(
                        f"Processing {uploaded_file.name}..."
                    ):

                        try:

                            result = rag.process_and_index_pdf(
                                file_path,
                                uploaded_file.name,
                            )

                            st.success(
                                f"Added {result['file_name']} to your library."
                            )

                            a, b, c = st.columns(3)

                            with a:
                                st.metric(
                                    "Pages",
                                    result["total_pages"],
                                )

                            with b:
                                st.metric(
                                    "Chunks",
                                    result["total_chunks"],
                                )

                            with c:
                                st.metric(
                                    "Total chunks",
                                    result["total_index_size"],
                                )

                        except ValueError as ex:
                            st.error(str(ex))

                        except Exception as ex:
                            st.error(
                                f"Could not process {uploaded_file.name}: {ex}"
                            )

    with right:

        st.markdown(
            '<div class="section-title">Library status</div>',
            unsafe_allow_html=True,
        )

        status = rag.get_vector_store_status()

        if status["is_ready"]:

            st.markdown(
                f"""
                <div class="small-card">
                    <strong>Knowledge base active</strong><br><br>
                    {status["total_chunks"]} searchable content chunks
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("")

            st.markdown("**Indexed files**")

            for filename in status["indexed_files"]:
                st.write(f"📄 {filename}")

            if st.button(
                "Clear Knowledge Base",
                use_container_width=True,
            ):
                rag.clear_vector_store()
                st.success("Knowledge base cleared.")
                time.sleep(0.5)
                st.rerun()

        else:

            st.markdown(
                """
                <div class="small-card">
                    <strong>No materials yet</strong><br><br>
                    Upload at least one PDF to activate StudyNova's
                    AI question answering.
                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# 2. ASK AI
# ============================================================

elif nav_choice == "💬 Ask AI":

    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">Ask StudyNova</div>
            <div class="hero-text">
                Ask questions about your uploaded materials and get answers
                grounded in your study content.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    top_left, top_right = st.columns([2, 1])

    with top_left:

        interaction_mode = st.radio(
            "Answering mode",
            [
                "Direct Study Q&A (RAG)",
                "AI Agent (Intent Router)",
            ],
            horizontal=True,
            help=(
                "Direct mode answers from your study materials. "
                "Agent mode can route requests to quizzes, study plans and progress."
            ),
        )

    with top_right:

        if st.button(
            "Clear conversation",
            use_container_width=True,
        ):
            st.session_state.chat_history = []
            st.rerun()

    st.markdown(
        '<div class="section-title">Quick actions</div>',
        unsafe_allow_html=True,
    )

    q1, q2, q3 = st.columns(3)

    quick_question = None

    with q1:
        if st.button(
            "Summarize my material",
            use_container_width=True,
        ):
            quick_question = (
                "What are the main concepts discussed in my study material?"
            )

    with q2:
        if st.button(
            "Explain important concepts",
            use_container_width=True,
        ):
            quick_question = (
                "Explain the most important concepts from my study material."
            )

    with q3:
        if st.button(
            "Create a quiz",
            use_container_width=True,
        ):
            quick_question = "Give me a quiz"

    st.markdown("---")

    for msg in st.session_state.chat_history:

        with st.chat_message(msg["role"]):

            if msg.get("tool"):
                st.caption(
                    f"Agent action: {msg['tool']}"
                )

            st.markdown(msg["content"])

            if msg.get("sources"):

                with st.expander(
                    "View sources",
                    expanded=False,
                ):

                    for src in msg["sources"]:

                        st.markdown(
                            f"**{src['file_name']}**  \n"
                            f"Page: {src['page']}  \n"
                            f"Relevance: {src['score']}"
                        )

                        st.caption(
                            src["snippet"]
                        )

                        st.divider()

    user_input = st.chat_input(
        "Ask anything about your study materials..."
    )

    prompt_to_run = (
        quick_question
        if quick_question
        else user_input
    )

    if prompt_to_run:

        if not config.is_gemini_configured():

            st.error(
                "Gemini AI is not configured. "
                "Please check your GEMINI_API_KEY in the .env file."
            )

            st.stop()

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": prompt_to_run,
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt_to_run)

        with st.chat_message("assistant"):

            with st.spinner("StudyNova is thinking..."):

                try:

                    if interaction_mode == "AI Agent (Intent Router)":

                        response = tools.route_and_execute(
                            prompt_to_run
                        )

                        st.caption(
                            f"Agent action: {response['tool_selected']}"
                        )

                        st.markdown(
                            response["response"]
                        )

                        sources = response.get(
                            "sources",
                            [],
                        )

                        if sources:

                            with st.expander(
                                "View sources",
                                expanded=False,
                            ):

                                for src in sources:

                                    st.markdown(
                                        f"**{src['file_name']}** — "
                                        f"Page {src['page']}"
                                    )

                                    st.caption(
                                        src["snippet"]
                                    )

                        st.session_state.chat_history.append(
                            {
                                "role": "assistant",
                                "content": response["response"],
                                "tool": response["tool_selected"],
                                "sources": sources,
                            }
                        )

                    else:

                        result = rag.answer_question(
                            prompt_to_run
                        )

                        st.markdown(
                            result["answer"]
                        )

                        sources = result.get(
                            "sources",
                            [],
                        )

                        if sources:

                            with st.expander(
                                "View sources",
                                expanded=False,
                            ):

                                for src in sources:

                                    st.markdown(
                                        f"**{src['file_name']}** — "
                                        f"Page {src['page']}"
                                    )

                                    st.caption(
                                        src["snippet"]
                                    )

                        st.session_state.chat_history.append(
                            {
                                "role": "assistant",
                                "content": result["answer"],
                                "sources": sources,
                            }
                        )

                except Exception as ex:

                    st.error(
                        f"Something went wrong: {ex}"
                    )


# ============================================================
# 3. QUIZ
# ============================================================

elif nav_choice == "📝 Quiz":

    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">Practice with AI-generated quizzes</div>
            <div class="hero-text">
                Test your understanding with questions generated from
                your selected topic and uploaded study material.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    mem_data = memory.load_memory()

    default_topic = (
        mem_data["topics_studied"][-1]
        if mem_data["topics_studied"]
        else "Cloud Computing"
    )

    st.markdown(
        '<div class="section-title">Quiz configuration</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns([2, 1, 1])

    with c1:

        quiz_topic = st.text_input(
            "Topic",
            value=default_topic,
            placeholder="Example: Cloud Computing",
        )

    with c2:

        num_q = st.selectbox(
            "Questions",
            [5, 10],
        )

    with c3:

        difficulty = st.selectbox(
            "Difficulty",
            ["Easy", "Medium", "Hard"],
            index=1,
        )

    if st.button(
        "Generate Quiz",
        type="primary",
        use_container_width=True,
    ):

        if not config.is_gemini_configured():

            st.error(
                "Gemini AI is not configured."
            )

        else:

            with st.spinner(
                f"Creating your {difficulty.lower()} quiz..."
            ):

                try:

                    context_chunks = (
                        rag.search_study_material(
                            quiz_topic,
                            top_k=3,
                        )
                    )

                    context = "\n\n".join(
                        [
                            chunk["text"]
                            for chunk in context_chunks
                        ]
                    )

                    questions = quiz.generate_quiz_questions(
                        topic=quiz_topic,
                        num_questions=num_q,
                        difficulty=difficulty,
                        context=context,
                    )

                    st.session_state.current_quiz = questions
                    st.session_state.quiz_answers = {}
                    st.session_state.quiz_results = None
                    st.session_state.quiz_topic = quiz_topic

                    st.success(
                        f"{len(questions)} questions generated."
                    )

                    time.sleep(0.5)
                    st.rerun()

                except Exception as ex:

                    st.error(
                        f"Quiz generation failed: {ex}"
                    )

    # --------------------------------------------------------
    # ACTIVE QUIZ
    # --------------------------------------------------------

    if st.session_state.current_quiz:

        st.markdown(
            f"""
            <div class="quiz-header">
                <div class="quiz-name">
                    {st.session_state.quiz_topic}
                </div>
                <div class="quiz-info">
                    {len(st.session_state.current_quiz)}
                    questions · Choose the best answer
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("study_nova_quiz"):

            for question in st.session_state.current_quiz:

                st.markdown(
                    f"### Question {question['id']}"
                )

                st.write(
                    question["question"]
                )

                options = [
                    f"{key}. {value}"
                    for key, value
                    in question["options"].items()
                ]

                previous = (
                    st.session_state.quiz_answers.get(
                        question["id"]
                    )
                )

                selected = st.radio(
                    "Choose your answer",
                    options,
                    key=f"question_{question['id']}",
                    index=(
                        [
                            item[0]
                            for item in options
                        ].index(previous)
                        if previous
                        and previous in [
                            item[0]
                            for item in options
                        ]
                        else None
                    ),
                    label_visibility="collapsed",
                )

                if selected:
                    st.session_state.quiz_answers[
                        question["id"]
                    ] = selected[0]

                st.divider()

            submit = st.form_submit_button(
                "Submit Quiz",
                type="primary",
                use_container_width=True,
            )

        if submit:

            with st.spinner(
                "Checking your answers..."
            ):

                result = quiz.calculate_quiz_score(
                    questions=st.session_state.current_quiz,
                    user_answers=st.session_state.quiz_answers,
                    topic=st.session_state.quiz_topic,
                )

                st.session_state.quiz_results = result

            st.rerun()

    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------

    if st.session_state.quiz_results:

        result = st.session_state.quiz_results

        st.markdown("---")

        st.markdown(
            '<div class="section-title">Your result</div>',
            unsafe_allow_html=True,
        )

        r1, r2, r3 = st.columns(3)

        with r1:
            st.metric(
                "Score",
                f"{result['score']} / {result['total']}",
            )

        with r2:
            st.metric(
                "Percentage",
                f"{result['percentage']}%",
            )

        with r3:

            if result["percentage"] >= 80:
                performance = "Excellent"
            elif result["percentage"] >= 60:
                performance = "Good"
            else:
                performance = "Needs Practice"

            st.metric(
                "Performance",
                performance,
            )

        st.progress(
            result["percentage"] / 100
        )

        if result["percentage"] >= 80:
            st.success(
                "Excellent work! You have a strong understanding of this topic."
            )
        elif result["percentage"] >= 60:
            st.info(
                "Good job! Review the incorrect answers once more."
            )
        else:
            st.warning(
                "Keep practicing. Focus especially on the weak areas below."
            )

        st.markdown(
            '<div class="section-title">Question review</div>',
            unsafe_allow_html=True,
        )

        for item in result["details"]:

            if item["is_correct"]:

                with st.expander(
                    f"Correct — Question {item['id']}"
                ):

                    st.write(
                        item["question"]
                    )

                    st.success(
                        f"Your answer: "
                        f"{item['selected_option']}. "
                        f"{item['selected_text']}"
                    )

                    st.info(
                        item["explanation"]
                    )

            else:

                with st.expander(
                    f"Review — Question {item['id']}"
                ):

                    st.write(
                        item["question"]
                    )

                    st.error(
                        f"Your answer: "
                        f"{item['selected_option']}. "
                        f"{item['selected_text']}"
                    )

                    st.success(
                        f"Correct answer: "
                        f"{item['correct_option']}. "
                        f"{item['correct_text']}"
                    )

                    st.info(
                        item["explanation"]
                    )

        if result["weak_areas"]:

            st.warning(
                "Focus areas: "
                + ", ".join(
                    result["weak_areas"]
                )
            )


# ============================================================
# 4. MY PROGRESS
# ============================================================

elif nav_choice == "📊 My Progress":

    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">Track your learning journey</div>
            <div class="hero-text">
                StudyNova remembers your topics, questions, quiz results
                and weak areas so you know what to study next.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    summary = memory.get_progress_summary()

    p1, p2, p3, p4 = st.columns(4)

    with p1:
        st.metric(
            "Topics Studied",
            summary["total_topics_studied"],
        )

    with p2:
        st.metric(
            "Questions Asked",
            summary["total_questions_asked"],
        )

    with p3:
        st.metric(
            "Quizzes Completed",
            summary["total_quizzes_taken"],
        )

    with p4:
        st.metric(
            "Average Score",
            f"{summary['average_quiz_score']}%",
        )

    st.markdown("---")

    left, right = st.columns(2)

    # --------------------------------------------------------
    # TOPICS
    # --------------------------------------------------------

    with left:

        st.markdown(
            '<div class="section-title">Topics studied</div>',
            unsafe_allow_html=True,
        )

        if summary["topics_studied"]:

            for topic in summary["topics_studied"]:

                st.markdown(
                    f"📘 **{topic}**"
                )

        else:

            st.info(
                "No topics recorded yet. "
                "Upload study materials to get started."
            )

        st.markdown(
            '<div class="section-title">Areas to improve</div>',
            unsafe_allow_html=True,
        )

        if summary["weak_topics"]:

            for topic in summary["weak_topics"]:

                st.warning(
                    f"Practice: {topic}"
                )

        else:

            st.success(
                "No weak topics identified yet."
            )

    # --------------------------------------------------------
    # HISTORY
    # --------------------------------------------------------

    with right:

        st.markdown(
            '<div class="section-title">Quiz history</div>',
            unsafe_allow_html=True,
        )

        if summary["quiz_history"]:

            for quiz_history in reversed(
                summary["quiz_history"]
            ):

                percentage = quiz_history[
                    "percentage"
                ]

                if percentage >= 70:
                    icon = "🟢"
                else:
                    icon = "🔴"

                with st.expander(
                    f"{icon} "
                    f"{quiz_history['topic']} — "
                    f"{quiz_history['score']}/"
                    f"{quiz_history['total']} "
                    f"({percentage}%)"
                ):

                    st.write(
                        f"Date: {quiz_history['timestamp']}"
                    )

                    if quiz_history.get(
                        "weak_areas"
                    ):

                        st.write(
                            "Weak areas: "
                            + ", ".join(
                                quiz_history[
                                    "weak_areas"
                                ]
                            )
                        )

        else:

            st.info(
                "No quizzes completed yet."
            )

    st.markdown("---")

    st.markdown(
        '<div class="section-title">Recent questions</div>',
        unsafe_allow_html=True,
    )

    if summary["recent_questions"]:

        for question in summary[
            "recent_questions"
        ][:7]:

            st.markdown(
                f"💬 {question['question']}"
            )

    else:

        st.info(
            "No questions asked yet."
        )

    st.markdown("---")

    if st.button(
        "Reset learning memory",
        use_container_width=True,
    ):

        memory.clear_memory()

        st.success(
            "Your learning memory has been reset."
        )

        time.sleep(0.5)
        st.rerun()


# ============================================================
# 5. STUDY PLAN
# ============================================================

elif nav_choice == "📅 Study Plan":

    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">Create your study roadmap</div>
            <div class="hero-text">
                Build a personalized day-by-day plan based on your exam date,
                available study time, knowledge level and weak topics.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    mem_data = memory.load_memory()

    default_subject = (
        mem_data["topics_studied"][-1]
        if mem_data["topics_studied"]
        else "Cloud Computing"
    )

    st.markdown(
        '<div class="section-title">Study details</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)

    with c1:

        subject = st.text_input(
            "Subject / Course",
            value=default_subject,
        )

        exam_date = st.date_input(
            "Exam date",
            value=date.today() + timedelta(days=7),
            min_value=date.today(),
        )

        daily_hours = st.slider(
            "Daily study time",
            min_value=1.0,
            max_value=8.0,
            value=2.5,
            step=0.5,
        )

    with c2:

        knowledge_level = st.selectbox(
            "Current knowledge level",
            [
                "Beginner",
                "Intermediate",
                "Advanced",
            ],
            index=1,
        )

        weak_topics = mem_data.get(
            "weak_topics",
            [],
        )

        options = list(
            dict.fromkeys(
                weak_topics
                + [
                    "Exam Review",
                    "Core Theory",
                ]
            )
        )

        selected_weak = st.multiselect(
            "Priority topics",
            options=options,
            default=weak_topics,
        )

        custom_topic = st.text_input(
            "Additional focus topic",
            placeholder="Example: Virtualization",
        )

        if custom_topic.strip():

            if custom_topic.strip() not in selected_weak:
                selected_weak.append(
                    custom_topic.strip()
                )

    st.markdown("")

    if st.button(
        "Generate My Study Plan",
        type="primary",
        use_container_width=True,
    ):

        if not config.is_gemini_configured():

            st.error(
                "Gemini AI is not configured."
            )

        else:

            with st.spinner(
                "Building your personalized plan..."
            ):

                try:

                    plan = (
                        study_plan.generate_study_plan(
                            subject=subject,
                            exam_date=str(exam_date),
                            daily_hours=daily_hours,
                            knowledge_level=knowledge_level,
                            weak_topics=selected_weak,
                        )
                    )

                    st.session_state.generated_plan = plan

                    st.success(
                        "Your study plan is ready."
                    )

                except Exception as ex:

                    st.error(
                        f"Could not generate study plan: {ex}"
                    )

    if st.session_state.generated_plan:

        plan = st.session_state.generated_plan

        st.markdown("---")

        st.markdown(
            f"## {plan['subject']}"
        )

        d1, d2, d3 = st.columns(3)

        with d1:
            st.metric(
                "Days remaining",
                plan["days_remaining"],
            )

        with d2:
            st.metric(
                "Daily commitment",
                f"{plan['daily_hours']} hrs",
            )

        with d3:
            st.metric(
                "Level",
                plan["knowledge_level"],
            )

        st.markdown("---")

        st.markdown(
            plan["plan_markdown"]
        )

        st.markdown("")

        st.download_button(
            "Download Study Plan",
            data=plan["plan_markdown"],
            file_name=(
                f"Study_Plan_"
                f"{plan['subject'].replace(' ', '_')}.md"
            ),
            mime="text/markdown",
            use_container_width=True,
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="app-footer">
        StudyNova · AI Study Assistant
    </div>
    """,
    unsafe_allow_html=True,
)