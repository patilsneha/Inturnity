import os

# --- BRANDING ---
APP_NAME = "INTURNITY"
TAGLINE = "Where Intern meets opportunity"
AUTHOR = "Souparnika Sunil"
TOPIC_NAME = "AI- Semantic Internship Allocation System"

# --- FILE PATHS ---
DATA_FOLDER = "portal_docs"
# Path to your main internship CSV
DATA_PATH = os.path.join(DATA_FOLDER, "internship_postings.csv")
# Path to the user database
USER_DB = os.path.join(DATA_FOLDER, "users.csv")
# Path to the pre-calculated AI vectors (Pickle file)
EMBEDDINGS_PATH = os.path.join(DATA_FOLDER, "internship_embeddings.pkl")

# --- AI SETTINGS ---
SLM_MODEL = "all-MiniLM-L6-v2"
TOP_K_RESULTS = 5
MATCH_THRESHOLD = 0.40

# --- CSV COLUMN MAPPING (Matching your internship_data.csv) ---
COL_ID = "Internship Id"
COL_ROLE = "Role"
COL_COMPANY = "Company Name"
COL_LOCATION = "Location"
COL_DURATION = "Duration"
COL_STIPEND = "Stipend"
COL_SKILLS = "Skills"
COL_PERKS = "Perks"
COL_LINK = "Website Link"

# --- USER DB COLUMNS ---
USER_COLS = ["full_name", "email", "password", "wishlist", "role"]

# --- MASTER SKILL LIBRARY ---
SKILL_LIBRARY = [
    # --- 1. CORE PROGRAMMING & LANGUAGES ---
    "python", "java", "sql", "c++", "c#", "javascript", "typescript", "php",
    "ruby", "swift", "kotlin", "go", "rust", "c", "dart", "r", "scala",

    # --- 2. WEB & MOBILE DEVELOPMENT ---
    "react", "node.js", "angular", "vue.js", "html5", "css3", "django", "flask",
    "next.js", "bootstrap", "tailwind css", "fastapi", "laravel", "flutter",
    "react native", "spring boot", "rest api", "graphql", "postman",

    # --- 3. DATA SCIENCE, AI & MACHINE LEARNING ---
    "machine learning", "data science", "deep learning", "nlp", "tensorflow",
    "pytorch", "pandas", "numpy", "scikit-learn", "opencv", "computer vision",
    "generative ai", "prompt engineering", "large language models", "llm",
    "bert", "nltk", "data mining", "predictive modeling",

    # --- 4. CLOUD, DEVOPS & INFRASTRUCTURE ---
    "aws", "docker", "kubernetes", "azure", "gcp", "git", "github", "jenkins",
    "ci/cd", "terraform", "ansible", "linux", "cloud computing", "serverless",
    "microservices", "model context protocol", "mcp",

    # --- 5. DATABASES & BIG DATA ---
    "mongodb", "postgresql", "mysql", "redis", "firebase", "cassandra",
    "apache spark", "hadoop", "databricks", "snowflake", "data warehousing",

    # --- 6. BUSINESS ANALYTICS & VISUALIZATION ---
    "tableau", "power bi", "excel", "vba", "google analytics", "looker",
    "sas", "spss", "statistics", "mathematics", "business analysis",
    "kpi mapping", "market research", "financial modeling",

    # --- 7. DIGITAL MARKETING & CONTENT ---
    "seo", "sem", "content writing", "social media marketing", "email marketing",
    "google ads", "meta ads", "copywriting", "growth hacking", "crm", "salesforce",
    "hubspot", "video editing", "canva", "figma", "ui/ux", "adobe xd",

    # --- 8. MANAGEMENT & SOFT SKILLS (CSBS Essentials) ---
    "project management", "agile", "scrum", "sdlc", "system design",
    "communication", "team collaboration", "critical thinking",
    "problem solving", "stakeholder management", "documentation"
]

ADMIN_PASSCODE = "admin1"