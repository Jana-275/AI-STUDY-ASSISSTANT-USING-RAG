# 🎓 StudyNova — AI Study Assistant

StudyNova is an AI-powered learning assistant that helps students study smarter using their own PDF study materials.

It combines **Retrieval-Augmented Generation (RAG)**, **Google Gemini AI**, semantic search, interactive quizzes, student progress tracking, and personalized study plans in a single Streamlit application.

---

## 🚀 Features

### 📚 1. Study Materials

- Upload PDF study materials.
- Extract text from PDFs using PyPDF.
- Split documents into searchable chunks.
- Generate semantic embeddings using Sentence Transformers.
- Store embeddings in a FAISS vector database.
- Display document processing statistics.
- Support multiple PDF study materials.

### 💬 2. Ask AI

- Ask questions about uploaded study materials.
- Uses RAG to retrieve relevant information from PDFs.
- Uses Google Gemini to generate answers.
- Answers are grounded in the uploaded materials.
- Displays source information and relevant document snippets.
- Helps reduce hallucination by restricting answers to retrieved study content.

### 📝 3. Interactive Quiz

- Generate multiple-choice questions from study materials.
- Choose the number of questions.
- Select difficulty level.
- Answer questions interactively.
- Submit the quiz and receive:
  - Score
  - Percentage
  - Correct/incorrect answers
  - Explanations
  - Weak topic identification

### 📊 4. My Progress

Tracks learning activity such as:

- Topics studied
- Questions asked
- Quiz history
- Average quiz score
- Weak topics
- Recent activity

Student progress is stored locally.

### 📅 5. Personalized Study Plan

Generate a study plan based on:

- Subject
- Exam date
- Daily study hours
- Current knowledge level
- Weak topics

The application generates a structured day-by-day study schedule.

### 🤖 6. AI Agent & Tools

StudyNova includes a lightweight intent-routing system that can identify requests such as:

- Study material questions
- Quiz requests
- Progress requests
- Study plan requests

Dedicated tools handle these operations without requiring a complex agent framework.

---

# 🏗️ System Architecture

```text
                    ┌─────────────────────────┐
                    │     Streamlit UI        │
                    │       StudyNova         │
                    └────────────┬────────────┘
                                 │
          ┌──────────────────────┼──────────────────────┐
          │                      │                      │
          ▼                      ▼                      ▼
   Study Materials            Ask AI                 Quiz / Plan
          │                      │                      │
          ▼                      ▼                      ▼
     PDF Extraction         Intent Router          AI Tools
          │                      │                      │
          ▼                      ▼                      │
      Text Chunking        Semantic Search             │
          │                      │                      │
          ▼                      ▼                      │
 Sentence Transformers      FAISS Vector Store         │
          │                      │                      │
          └──────────────┬───────┘                      │
                         ▼                              │
                  Retrieved Context                     │
                         │                              │
                         ▼                              │
                  Google Gemini                         │
                         │                              │
                         ▼                              │
                 AI Generated Answer                    │
                         │                              │
                         ▼                              │
                 Sources & Citations                    │
                                                        │
                         ┌──────────────────────────────┘
                         ▼
                 Student Memory
                 data/memory.json
```

---

# 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Streamlit | Web application UI |
| Google Gemini API | AI response generation |
| PyPDF | PDF text extraction |
| Sentence Transformers | Semantic embeddings |
| FAISS | Vector similarity search |
| python-dotenv | Environment variable management |
| JSON | Local student progress storage |

The RAG pipeline and tool routing are implemented directly in Python without requiring LangChain or LangGraph.

---

# 📁 Project Structure

```text
ai-study-assistant/
│
├── app.py
├── config.py
├── rag.py
├── quiz.py
├── memory.py
├── study_plan.py
├── tools.py
│
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── .streamlit/
│   └── config.toml
│
├── data/
│   ├── memory.json
│   └── vector_store/
│
└── uploads/
```

### File Description

| File | Purpose |
|---|---|
| `app.py` | Main Streamlit application |
| `config.py` | Configuration and environment variables |
| `rag.py` | PDF processing, embeddings, FAISS and RAG |
| `quiz.py` | Quiz generation and grading |
| `memory.py` | Student progress and memory |
| `study_plan.py` | Personalized study plan generation |
| `tools.py` | AI tools and intent routing |
| `requirements.txt` | Python dependencies |
| `.env.example` | Example environment configuration |
| `.gitignore` | Prevents secrets and generated files from being uploaded |

> **Note:** `data/`, `uploads/`, `.venv/`, `.env`, and generated cache files are intended to remain local and are excluded from GitHub through `.gitignore`.

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/Vicky15506/AI-STUDY-ASSISSTANT.git
```

Move into the project directory:

```bash
cd AI-STUDY-ASSISSTANT
```

---

## 2. Create a virtual environment

### Windows

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

You should see:

```text
(.venv)
```

or your existing environment indicator in the terminal.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

# 📦 3. Install Dependencies

With the virtual environment activated:

```powershell
python -m pip install -r requirements.txt
```

---

# 🔑 4. Configure Gemini API

Create a `.env` file in the project root.

You can copy the example file:

### Windows

```powershell
copy .env.example .env
```

Then open `.env` and configure your Gemini API key.

Example:

```env
GEMINI_API_KEY=your_actual_api_key_here
```

Do **not** upload `.env` to GitHub.

The `.gitignore` file prevents the API key from being committed.

---

# ▶️ 5. Run StudyNova

Make sure the virtual environment is active.

Run:

```powershell
python -m streamlit run app.py
```

Or:

```powershell
streamlit run app.py
```

The application will normally be available at:

```text
http://localhost:8501
```

---

# 🔍 How RAG Works

StudyNova uses Retrieval-Augmented Generation to answer questions based on uploaded study materials.

### Step 1 — PDF Extraction

PDF documents are processed using PyPDF.

### Step 2 — Text Chunking

Extracted text is divided into smaller chunks suitable for semantic search.

### Step 3 — Embedding Generation

Sentence Transformers converts text chunks into numerical vectors.

### Step 4 — FAISS Indexing

The vectors are stored in a FAISS index for fast similarity search.

### Step 5 — Question Retrieval

When a student asks a question:

```text
Question
   ↓
Embedding
   ↓
FAISS Similarity Search
   ↓
Relevant Document Chunks
```

### Step 6 — Gemini Generation

The retrieved information is provided to Google Gemini to generate a grounded response.

### Step 7 — Sources

Relevant source information can be displayed along with the answer.

---

# 🧠 Student Memory

StudyNova maintains local learning information such as:

```text
Topics Studied
Questions Asked
Quiz History
Weak Topics
Average Scores
Recent Activity
```

This information is stored locally in:

```text
data/memory.json
```

It is excluded from GitHub because it represents generated/local application data.

---

# 📝 Quiz Workflow

The quiz system follows this flow:

```text
Select Topic
     ↓
Select Difficulty
     ↓
Generate Questions
     ↓
Answer MCQs
     ↓
Submit Quiz
     ↓
Calculate Score
     ↓
Show Explanations
     ↓
Identify Weak Topics
     ↓
Update Student Memory
```

---

# 📅 Study Plan Workflow

Students provide:

- Subject
- Exam date
- Daily available study hours
- Knowledge level
- Weak topics

StudyNova then generates a structured study schedule.

Example:

```text
Day 1
├── Learn core concepts
├── Review notes
└── Practice questions

Day 2
├── Continue theory
├── Active recall
└── Practice MCQs

Day 3
├── Weak topic revision
├── Problem solving
└── Self-test
```

The generated study plan can also be downloaded as a Markdown file.

---

# 🎬 Demo Flow

A simple demonstration can follow these steps:

### 1. Launch StudyNova

```powershell
python -m streamlit run app.py
```

### 2. Upload Study Material

Open:

```text
📚 Study Materials
```

Upload a PDF and process it.

### 3. Ask a Question

Open:

```text
💬 Ask AI
```

Ask a question related to the uploaded material.

### 4. Check Sources

Open the sources section to inspect the retrieved document information.

### 5. Generate a Quiz

Open:

```text
📝 Quiz
```

Choose a topic and difficulty, then generate the quiz.

### 6. Submit the Quiz

Answer the questions and submit the quiz to see the score and explanations.

### 7. Check Progress

Open:

```text
📊 My Progress
```

Review quiz history, scores, topics and weak areas.

### 8. Generate Study Plan

Open:

```text
📅 Study Plan
```

Enter exam information and generate a personalized schedule.

---

# 🔐 Security

Never commit sensitive information such as:

```text
.env
API keys
Passwords
Access tokens
Personal credentials
```

The repository uses `.gitignore` to exclude sensitive and generated files.

For local development, keep your API key inside:

```text
.env
```

and use:

```text
.env.example
```

as the public configuration template.

---

# 🐛 Troubleshooting

## Streamlit is not recognized

Use:

```powershell
python -m streamlit run app.py
```

instead of:

```powershell
streamlit run app.py
```

---

## Missing Python package

Make sure the virtual environment is activated and run:

```powershell
python -m pip install -r requirements.txt
```

---

## Gemini API error

Check that your `.env` contains:

```env
GEMINI_API_KEY=your_actual_api_key_here
```

Also verify that the API key is valid and available to your configured Gemini model.

---

## PDF contains no text

Some PDFs are scanned images rather than text-based documents.

Try uploading a PDF containing selectable text.

---

## No study materials available

Upload and process at least one PDF before asking questions or generating material-based quizzes.

---

# 🌟 Future Improvements

Possible future enhancements include:

- User authentication
- Cloud database
- Online deployment
- Mobile application
- Voice-based questions
- OCR support for scanned PDFs
- Advanced analytics
- More quiz formats
- Multi-language support
- Cloud-based vector database
- Personalized AI tutoring

---

# 👩‍💻 Author

**Vicky15506**

GitHub:

https://github.com/Vicky15506

---

# 📄 License

This project is intended for educational and learning purposes.