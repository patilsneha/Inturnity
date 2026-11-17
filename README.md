# INTURNITY 🚀
### AI-Powered Semantic Internship Recommendation System

**INTURNITY** is an internship recommendation platform that helps students discover relevant internship opportunities based on the skills and information extracted from their resumes.

The application uses Natural Language Processing (NLP) and semantic similarity to match student profiles with available internships.

## ✨ Features

- **User Authentication:** Student registration and login functionality.
- **Resume Parsing:** Extracts text from uploaded PDF resumes.
- **Personal Information Extraction:** Identifies candidate names and email addresses.
- **Skill Detection:** Detects technical and professional skills using a predefined skill library and regular expressions.
- **Semantic Matching:** Uses Sentence Transformers to generate text embeddings.
- **Hybrid Recommendation System:** Combines cosine similarity with keyword matching to calculate internship match scores.
- **Top Recommendations:** Displays the five highest-ranked internship matches.
- **Wishlist Support:** Allows users to save internship preferences.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application interface |
| Sentence Transformers | Text embeddings and semantic matching |
| all-MiniLM-L6-v2 | Pre-trained language model |
| Pandas | Internship dataset processing |
| PDFPlumber | PDF resume text extraction |
| Regular Expressions | Name, email and skill extraction |
| Pickle | Saving generated embeddings |
| Git & GitHub | Version control |

## ⚙️ How It Works

1. **User Registration:** Students create an account and log in.
2. **Resume Upload:** The student uploads a PDF resume.
3. **Information Extraction:** The application extracts resume text, identifies the candidate's email and name, and detects skills.
4. **Embedding Generation:** Sentence Transformers converts resume content into numerical embeddings.
5. **Internship Processing:** Internship descriptions, company names and required skills are converted into embeddings.
6. **Similarity Calculation:** Cosine similarity measures how closely the resume matches each internship.
7. **Hybrid Scoring:** Direct keyword matches are used to adjust semantic similarity scores.
8. **Recommendations:** The application displays the top five matching internship opportunities.

## 📂 Project Structure

```text
Inturnity/
│
├── app.py
├── auth.py
├── auth_view.py
├── auth_run.py
├── constants.py
├── processor.py
├── engine.py
├── student_controller.py
├── student_view.py
│
├── portal_docs/
│   └── internship_postings.csv
│
├── grid.png
├── typewriter.png
├── test_processor.py
├── test_system.py
└── .gitignore
```

## 💻 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/patilsneha/Inturnity.git
```

### 2. Navigate to the project directory

```bash
cd Inturnity
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install streamlit pandas pdfplumber sentence-transformers
```

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 📊 Recommendation Methodology

Inturnity uses a hybrid recommendation approach:

- **Semantic Similarity:** Cosine similarity compares resume and internship embeddings.
- **Keyword Matching:** Identifies skills appearing in both the resume and internship requirements.
- **Score Adjustment:** Direct keyword matches boost the similarity score, while certain high semantic scores without keyword overlap are penalized.

This approach combines contextual text similarity with direct skill matching.

## 🔮 Future Scope

- Improve resume parsing and skill extraction.
- Introduce a more secure database for user management.
- Expand internship data sources.
- Explore scalable vector databases for larger datasets.
- Improve recommendation accuracy through additional evaluation.

## 👩‍💻 Acknowledgement

This repository is being used for learning, testing and further exploration of the Inturnity project. The original project author is credited in the source code.

---

**INTURNITY – Where Intern meets Opportunity.**
