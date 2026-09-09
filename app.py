"""
STUDY MATE
AI Study Assistant

Features:
1. Study Materials - PDF upload and FAISS indexing
2. Ask AI - RAG Q&A and AI Agent
3. Quiz - AI generated MCQ tests
4. My Progress - Learning analytics and memory
5. Study Plan - Personalized exam preparation
"""

from datetime import date, timedelta

import streamlit as st

import config
import rag
import quiz
import memory
import study_plan
import tools


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="STUDY MATE",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
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

    st.title("📘 STUDY MATE")
    st.caption("AI STUDY ASSISTANT")

    st.divider()

    st.subheader("Workspace")

    nav_choice = st.radio(
        "Choose a section",
        [
            "📚 Study Materials",
            "💬 Ask AI",
            "📝 Quiz",
            "📊 My Progress",
            "📅 Study Plan",
        ],
        index=0,
    )

    st.divider()

    st.subheader("Knowledge Base")

    sidebar_status = rag.get_vector_store_status()

    if sidebar_status["is_ready"]:

        st.success("Knowledge base active")

        st.metric(
            "Searchable Chunks",
            sidebar_status["total_chunks"],
        )

        st.caption(
            f"{len(sidebar_status['indexed_files'])} document(s) indexed"
        )

    else:

        st.info("No study materials indexed yet.")

    st.divider()

    st.caption("STUDY MATE")
    st.caption("Learn • Practice • Improve")


# ============================================================
# MAIN HEADER
# ============================================================

st.title("📘 STUDY MATE")

st.caption(
    "Your personal AI-powered learning workspace"
)

st.divider()


# ============================================================
# HOME / SECTION INTRO
# ============================================================

if nav_choice == "📚 Study Materials":

    st.header("📚 Study Materials")

    st.write(
        "Build your personal AI knowledge base by uploading "
        "lecture notes, textbooks, course slides and other PDF materials."
    )

elif nav_choice == "💬 Ask AI":

    st.header("💬 Ask AI")

    st.write(
        "Ask questions about your uploaded study materials "
        "and get answers using Retrieval-Augmented Generation."
    )

elif nav_choice == "📝 Quiz":

    st.header("📝 Quiz Center")

    st.write(
        "Generate interactive multiple-choice quizzes "
        "and test your understanding."
    )

elif nav_choice == "📊 My Progress":

    st.header("📊 My Progress")

    st.write(
        "Track your learning activity, quiz performance, "
        "weak areas and recent questions."
    )

elif nav_choice == "📅 Study Plan":

    st.header("📅 Study Plan")

    st.write(
        "Create a personalized study schedule based on "
        "your exam date, available time and weak topics."
    )


# ============================================================
# 1. STUDY MATERIALS
# ============================================================

if nav_choice == "📚 Study Materials":

    st.divider()

    left_col, right_col = st.columns(
        [1.6, 1],
        gap="large",
    )

    # --------------------------------------------------------
    # UPLOAD
    # --------------------------------------------------------

    with left_col:

        st.subheader("📄 Upload Materials")

        st.info(
            "Upload one or more PDF files. "
            "STUDY MATE will extract the text, create chunks "
            "and add them to the FAISS knowledge base."
        )

        uploaded_files = st.file_uploader(
            "Choose PDF files",
            type=["pdf"],
            accept_multiple_files=True,
            help="Upload lecture notes, textbooks or course slides.",
        )

        if uploaded_files:

            st.success(
                f"{len(uploaded_files)} file(s) selected."
            )

            for uploaded_file in uploaded_files:

                st.write(
                    f"📄 **{uploaded_file.name}**"
                )

            process_button = st.button(
                "🚀 Process & Index Materials",
                type="primary",
                use_container_width=True,
            )

            if process_button:

                for uploaded_file in uploaded_files:

                    file_path = (
                        config.UPLOADS_DIR
                        / uploaded_file.name
                    )

                    with open(file_path, "wb") as f:
                        f.write(
                            uploaded_file.getbuffer()
                        )

                    with st.spinner(
                        f"Processing {uploaded_file.name}..."
                    ):

                        try:

                            result = (
                                rag.process_and_index_pdf(
                                    file_path,
                                    uploaded_file.name,
                                )
                            )

                            st.success(
                                f"Successfully processed: "
                                f"{result['file_name']}"
                            )

                            r1, r2, r3 = st.columns(3)

                            with r1:
                                st.metric(
                                    "Pages",
                                    result["total_pages"],
                                )

                            with r2:
                                st.metric(
                                    "New Chunks",
                                    result["total_chunks"],
                                )

                            with r3:
                                st.metric(
                                    "Total Chunks",
                                    result["total_index_size"],
                                )

                        except ValueError as error:

                            st.error(
                                f"⚠️ {error}"
                            )

                        except Exception as error:

                            st.error(
                                f"❌ Error processing "
                                f"{uploaded_file.name}: {error}"
                            )

    # --------------------------------------------------------
    # KNOWLEDGE BASE
    # --------------------------------------------------------

    with right_col:

        st.subheader("🗂 Knowledge Base")

        status = rag.get_vector_store_status()

        if status["is_ready"]:

            st.success(
                f"Index active — "
                f"{status['total_chunks']} searchable chunks"
            )

            st.write("**Indexed documents:**")

            for file_name in status["indexed_files"]:

                st.write(
                    f"📄 {file_name}"
                )

            st.divider()

            if st.button(
                "🗑️ Clear Vector Index",
                use_container_width=True,
            ):

                rag.clear_vector_store()

                st.success(
                    "Vector index cleared."
                )

                st.rerun()

        else:

            st.info(
                "Your knowledge base is empty.\n\n"
                "Upload a PDF to enable RAG question answering."
            )


# ============================================================
# 2. ASK AI
# ============================================================

elif nav_choice == "💬 Ask AI":

    st.divider()

    mode_col, clear_col = st.columns(
        [3, 1],
        gap="large",
    )

    with mode_col:

        interaction_mode = st.radio(
            "Interaction Mode",
            [
                "Direct Study Q&A (RAG)",
                "AI Agent (Intent Router)",
            ],
            horizontal=True,
            help=(
                "Direct RAG answers from your materials. "
                "AI Agent mode can route requests to different tools."
            ),
        )

    with clear_col:

        st.write("")

        if st.button(
            "🧹 Clear Chat",
            use_container_width=True,
        ):

            st.session_state.chat_history = []

            st.rerun()

    st.divider()

    # --------------------------------------------------------
    # QUICK ACTIONS
    # --------------------------------------------------------

    st.subheader("⚡ Quick Actions")

    q1, q2, q3 = st.columns(3)

    quick_question = None

    with q1:

        if st.button(
            "📌 Summarize",
            use_container_width=True,
        ):

            quick_question = (
                "What is the main concept discussed "
                "in this material?"
            )

    with q2:

        if st.button(
            "📝 Create Quiz",
            use_container_width=True,
        ):

            quick_question = "Give me a quiz"

    with q3:

        if st.button(
            "📅 Create Study Plan",
            use_container_width=True,
        ):

            quick_question = "Create a study plan"

    # --------------------------------------------------------
    # CHAT HISTORY
    # --------------------------------------------------------

    for message in st.session_state.chat_history:

        with st.chat_message(
            message["role"]
        ):

            if message.get("tool"):

                st.caption(
                    f"⚙️ Tool used: "
                    f"{message['tool']}"
                )

            st.markdown(
                message["content"]
            )

            sources = message.get(
                "sources",
                [],
            )

            if sources:

                with st.expander(
                    "🔍 View Sources & Citations"
                ):

                    for source in sources:

                        st.write(
                            f"**File:** "
                            f"{source['file_name']}"
                        )

                        st.write(
                            f"**Page:** "
                            f"{source['page']}"
                        )

                        st.write(
                            f"**Score:** "
                            f"{source['score']}"
                        )

                        st.caption(
                            f"“{source['snippet']}”"
                        )

                        st.divider()

    # --------------------------------------------------------
    # USER INPUT
    # --------------------------------------------------------

    user_input = st.chat_input(
        "Ask something about your study materials..."
    )

    prompt_to_run = (
        quick_question
        if quick_question
        else user_input
    )

    if prompt_to_run:

        if not config.is_gemini_configured():

            st.error(
                "⚠️ Gemini AI is not configured. "
                "Please check your GEMINI_API_KEY."
            )

            st.stop()

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": prompt_to_run,
            }
        )

        with st.chat_message("user"):

            st.markdown(
                prompt_to_run
            )

        with st.chat_message("assistant"):

            with st.spinner(
                "STUDY MATE is thinking..."
            ):

                try:

                    # ------------------------------------------------
                    # AI AGENT
                    # ------------------------------------------------

                    if (
                        interaction_mode
                        == "AI Agent (Intent Router)"
                    ):

                        result = (
                            tools.route_and_execute(
                                prompt_to_run
                            )
                        )

                        st.caption(
                            f"⚙️ Tool used: "
                            f"{result['tool_selected']}"
                        )

                        st.markdown(
                            result["response"]
                        )

                        sources = result.get(
                            "sources",
                            [],
                        )

                        if sources:

                            with st.expander(
                                "🔍 View Sources & Citations"
                            ):

                                for source in sources:

                                    st.write(
                                        f"**File:** "
                                        f"{source['file_name']}"
                                    )

                                    st.write(
                                        f"**Page:** "
                                        f"{source['page']}"
                                    )

                                    st.write(
                                        f"**Score:** "
                                        f"{source['score']}"
                                    )

                                    st.caption(
                                        f"“{source['snippet']}”"
                                    )

                        st.session_state.chat_history.append(
                            {
                                "role": "assistant",
                                "content": result[
                                    "response"
                                ],
                                "tool": result[
                                    "tool_selected"
                                ],
                                "sources": sources,
                            }
                        )

                    # ------------------------------------------------
                    # DIRECT RAG
                    # ------------------------------------------------

                    else:

                        rag_result = (
                            rag.answer_question(
                                prompt_to_run
                            )
                        )

                        st.markdown(
                            rag_result["answer"]
                        )

                        sources = rag_result.get(
                            "sources",
                            [],
                        )

                        if sources:

                            with st.expander(
                                "🔍 View Sources & Citations",
                                expanded=True,
                            ):

                                for source in sources:

                                    st.write(
                                        f"**File:** "
                                        f"{source['file_name']}"
                                    )

                                    st.write(
                                        f"**Page:** "
                                        f"{source['page']}"
                                    )

                                    st.write(
                                        f"**Similarity:** "
                                        f"{source['score']}"
                                    )

                                    st.caption(
                                        f"“{source['snippet']}”"
                                    )

                                    st.divider()

                        st.session_state.chat_history.append(
                            {
                                "role": "assistant",
                                "content": rag_result[
                                    "answer"
                                ],
                                "sources": sources,
                            }
                        )

                except Exception as error:

                    st.error(
                        f"❌ Error: {error}"
                    )


# ============================================================
# 3. QUIZ
# ============================================================

elif nav_choice == "📝 Quiz":

    st.divider()

    memory_data = memory.load_memory()

    default_topic = (
        memory_data["topics_studied"][-1]
        if memory_data["topics_studied"]
        else "Cloud Computing"
    )

    st.subheader("⚙️ Quiz Setup")

    setup1, setup2, setup3 = st.columns(
        [2, 1, 1],
        gap="medium",
    )

    with setup1:

        quiz_topic = st.text_input(
            "Quiz Topic",
            value=default_topic,
            help="Enter the topic you want to practice.",
        )

    with setup2:

        number_of_questions = st.selectbox(
            "Questions",
            [5, 10],
            index=0,
        )

    with setup3:

        difficulty = st.selectbox(
            "Difficulty",
            [
                "Easy",
                "Medium",
                "Hard",
            ],
            index=1,
        )

    generate_quiz = st.button(
        "⚡ Generate Quiz",
        type="primary",
        use_container_width=True,
    )

    if generate_quiz:

        if not config.is_gemini_configured():

            st.error(
                "⚠️ Gemini AI is not configured."
            )

        else:

            with st.spinner(
                f"Generating "
                f"{number_of_questions} questions..."
            ):

                try:

                    context_chunks = (
                        rag.search_study_material(
                            quiz_topic,
                            top_k=3,
                        )
                    )

                    context_string = (
                        "\n\n".join(
                            [
                                chunk["text"]
                                for chunk in context_chunks
                            ]
                        )
                        if context_chunks
                        else ""
                    )

                    questions = (
                        quiz.generate_quiz_questions(
                            topic=quiz_topic,
                            num_questions=number_of_questions,
                            difficulty=difficulty,
                            context=context_string,
                        )
                    )

                    st.session_state.current_quiz = (
                        questions
                    )

                    st.session_state.quiz_answers = {}

                    st.session_state.quiz_results = None

                    st.session_state.quiz_topic = (
                        quiz_topic
                    )

                    st.success(
                        f"Generated {len(questions)} "
                        f"questions."
                    )

                    st.rerun()

                except Exception as error:

                    st.error(
                        f"❌ Failed to generate quiz: "
                        f"{error}"
                    )

    # --------------------------------------------------------
    # ACTIVE QUIZ
    # --------------------------------------------------------

    if st.session_state.current_quiz:

        st.divider()

        st.subheader(
            f"✍️ {st.session_state.quiz_topic}"
        )

        st.caption(
            f"{len(st.session_state.current_quiz)} "
            f"questions"
        )

        with st.form("quiz_form"):

            for question in (
                st.session_state.current_quiz
            ):

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

                previous_choice = (
                    st.session_state.quiz_answers.get(
                        question["id"]
                    )
                )

                selected = st.radio(
                    f"Answer for question "
                    f"{question['id']}",
                    options,
                    index=None,
                    key=(
                        f"question_"
                        f"{question['id']}"
                    ),
                )

                if selected:

                    st.session_state.quiz_answers[
                        question["id"]
                    ] = selected[0]

                st.divider()

            submit_quiz = st.form_submit_button(
                "📊 Submit Quiz",
                type="primary",
                use_container_width=True,
            )

        if submit_quiz:

            with st.spinner(
                "Grading your quiz..."
            ):

                results = (
                    quiz.calculate_quiz_score(
                        questions=(
                            st.session_state.current_quiz
                        ),
                        user_answers=(
                            st.session_state.quiz_answers
                        ),
                        topic=(
                            st.session_state.quiz_topic
                        ),
                    )
                )

                st.session_state.quiz_results = (
                    results
                )

                st.rerun()

    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------

    if st.session_state.quiz_results:

        results = (
            st.session_state.quiz_results
        )

        st.divider()

        st.subheader("🏆 Quiz Results")

        result1, result2, result3 = st.columns(3)

        with result1:

            st.metric(
                "Score",
                f"{results['score']} / "
                f"{results['total']}",
            )

        with result2:

            st.metric(
                "Percentage",
                f"{results['percentage']}%",
            )

        with result3:

            if results["percentage"] >= 80:

                performance = "🌟 Excellent"

            elif results["percentage"] >= 60:

                performance = "👍 Good Job"

            else:

                performance = "⚠️ Needs Review"

            st.metric(
                "Performance",
                performance,
            )

        st.progress(
            results["percentage"] / 100
        )

        st.subheader(
            "📋 Detailed Review"
        )

        for item in results["details"]:

            if item["is_correct"]:

                st.success(
                    f"""
                    **Q{item['id']} — Correct**

                    **Question:** {item['question']}

                    **Your Answer:** {item['selected_option']}. {item['selected_text']}

                    **Explanation:** {item['explanation']}
                    """
                )

            else:

                st.error(
                    f"""
                    **Q{item['id']} — Incorrect**

                    **Question:** {item['question']}

                    **Your Answer:** {item['selected_option']}. {item['selected_text']}

                    **Correct Answer:** {item['correct_option']}. {item['correct_text']}

                    **Explanation:** {item['explanation']}
                    """
                )

        if results["weak_areas"]:

            st.warning(
                "⚠️ **Focus Areas:** "
                + ", ".join(
                    results["weak_areas"]
                )
            )

        st.info(
            "✅ This result has been recorded "
            "in My Progress."
        )


# ============================================================
# 4. MY PROGRESS
# ============================================================

elif nav_choice == "📊 My Progress":

    st.divider()

    summary = (
        memory.get_progress_summary()
    )

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    m1, m2, m3, m4 = st.columns(4)

    with m1:

        st.metric(
            "📚 Topics Studied",
            summary[
                "total_topics_studied"
            ],
        )

    with m2:

        st.metric(
            "💬 Questions Asked",
            summary[
                "total_questions_asked"
            ],
        )

    with m3:

        st.metric(
            "📝 Quizzes Completed",
            summary[
                "total_quizzes_taken"
            ],
        )

    with m4:

        st.metric(
            "🎯 Average Score",
            f"{summary['average_quiz_score']}%",
        )

    st.divider()

    # --------------------------------------------------------
    # TOPICS + WEAK AREAS
    # --------------------------------------------------------

    left_progress, right_progress = (
        st.columns(2, gap="large")
    )

    with left_progress:

        st.subheader(
            "📚 Topics Studied"
        )

        if summary["topics_studied"]:

            for topic in summary[
                "topics_studied"
            ]:

                st.write(
                    f"📘 **{topic}**"
                )

        else:

            st.info(
                "No topics recorded yet."
            )

        st.subheader(
            "⚠️ Focus Topics"
        )

        if summary["weak_topics"]:

            for weak_topic in summary[
                "weak_topics"
            ]:

                st.warning(
                    f"🔴 {weak_topic}"
                )

        else:

            st.success(
                "🎉 No weak topics flagged."
            )

    with right_progress:

        st.subheader(
            "📝 Quiz History"
        )

        if summary["quiz_history"]:

            for history in summary[
                "quiz_history"
            ]:

                if history["percentage"] >= 70:

                    icon = "🟢"

                else:

                    icon = "🔴"

                with st.expander(
                    f"{icon} "
                    f"{history['topic']} — "
                    f"{history['score']}/"
                    f"{history['total']} "
                    f"({history['percentage']}%)"
                ):

                    st.write(
                        f"📅 **Date:** "
                        f"{history['timestamp']}"
                    )

                    st.write(
                        f"🎯 **Score:** "
                        f"{history['score']} "
                        f"of {history['total']}"
                    )

                    if history.get(
                        "weak_areas"
                    ):

                        st.write(
                            "⚠️ **Weak Areas:** "
                            + ", ".join(
                                history[
                                    "weak_areas"
                                ]
                            )
                        )

        else:

            st.info(
                "No quizzes taken yet."
            )

    # --------------------------------------------------------
    # RECENT QUESTIONS
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "🕒 Recent Questions"
    )

    if summary["recent_questions"]:

        for recent_question in (
            summary["recent_questions"][:7]
        ):

            st.write(
                f"💬 "
                f"*{recent_question['question']}*"
            )

            st.caption(
                "Topic: "
                + recent_question.get(
                    "topic",
                    "General",
                )
            )

    else:

        st.info(
            "No questions asked yet."
        )

    st.divider()

    if st.button(
        "🗑️ Reset All Student Memory"
    ):

        memory.clear_memory()

        st.success(
            "Student memory reset successfully."
        )

        st.rerun()


# ============================================================
# 5. STUDY PLAN
# ============================================================

elif nav_choice == "📅 Study Plan":

    st.divider()

    memory_data = memory.load_memory()

    default_subject = (
        memory_data["topics_studied"][-1]
        if memory_data["topics_studied"]
        else "Cloud Computing"
    )

    st.subheader(
        "🎯 Exam Preparation"
    )

    plan_left, plan_right = st.columns(
        2,
        gap="large",
    )

    with plan_left:

        subject = st.text_input(
            "Subject / Course Name",
            value=default_subject,
        )

        exam_date = st.date_input(
            "Target Exam Date",
            value=(
                date.today()
                + timedelta(days=7)
            ),
            min_value=date.today(),
        )

        daily_hours = st.slider(
            "Daily Study Hours",
            min_value=1.0,
            max_value=8.0,
            value=2.5,
            step=0.5,
        )

    with plan_right:

        knowledge_level = st.selectbox(
            "Current Knowledge Level",
            [
                "Beginner",
                "Intermediate",
                "Advanced",
            ],
            index=1,
        )

        weak_topics = memory_data.get(
            "weak_topics",
            [],
        )

        selected_weak_topics = st.multiselect(
            "Priority Weak Topics",
            options=(
                weak_topics
                + [
                    "Exam Review",
                    "Core Theory",
                ]
            ),
            default=(
                weak_topics
                if weak_topics
                else []
            ),
        )

        custom_focus = st.text_input(
            "Additional Focus Topics",
            placeholder=(
                "Example: Virtualization, "
                "Service Models"
            ),
        )

        if custom_focus.strip():

            selected_weak_topics.append(
                custom_focus.strip()
            )

    generate_plan = st.button(
        "📅 Generate My Study Plan",
        type="primary",
        use_container_width=True,
    )

    if generate_plan:

        if not config.is_gemini_configured():

            st.error(
                "⚠️ Gemini AI is not configured."
            )

        else:

            with st.spinner(
                "Creating your personalized study plan..."
            ):

                try:

                    plan = (
                        study_plan.generate_study_plan(
                            subject=subject,
                            exam_date=str(
                                exam_date
                            ),
                            daily_hours=daily_hours,
                            knowledge_level=(
                                knowledge_level
                            ),
                            weak_topics=(
                                selected_weak_topics
                            ),
                        )
                    )

                    st.session_state.generated_plan = (
                        plan
                    )

                    st.success(
                        "Study plan generated successfully!"
                    )

                except Exception as error:

                    st.error(
                        f"❌ Error generating study plan: "
                        f"{error}"
                    )

    # --------------------------------------------------------
    # GENERATED PLAN
    # --------------------------------------------------------

    if st.session_state.generated_plan:

        plan = (
            st.session_state.generated_plan
        )

        st.divider()

        st.subheader(
            f"📋 {plan['subject']}"
        )

        d1, d2, d3 = st.columns(3)

        with d1:

            st.metric(
                "Days Remaining",
                plan["days_remaining"],
            )

        with d2:

            st.metric(
                "Daily Commitment",
                f"{plan['daily_hours']} hours",
            )

        with d3:

            st.metric(
                "Knowledge Level",
                plan["knowledge_level"],
            )

        st.divider()

        st.markdown(
            plan["plan_markdown"]
        )

        st.download_button(
            "📥 Download Study Plan",
            data=plan["plan_markdown"],
            file_name=(
                "Study_Plan_"
                + plan["subject"].replace(
                    " ",
                    "_",
                )
                + ".md"
            ),
            mime="text/markdown",
            use_container_width=True,
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "📘 STUDY MATE • AI STUDY ASSISTANT"
)

st.caption(
    "Learn smarter • Practice better • Prepare with confidence"
)