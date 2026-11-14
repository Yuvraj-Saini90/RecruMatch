"""Skill taxonomy and normalization dictionary for technical and professional skills."""

import re
from typing import Dict, List, Set, Optional

# Categorized Skill Taxonomy
SKILL_TAXONOMY: Dict[str, List[str]] = {
    "Programming Languages": [
        "Python", "Java", "C", "C++", "C#", "JavaScript", "TypeScript",
        "Go", "Rust", "Ruby", "PHP", "Swift", "Kotlin", "Dart",
        "R", "Scala", "MATLAB", "Perl", "Shell Scripting", "Bash", "SQL"
    ],
    "Frameworks & Libraries": [
        "React", "Node.js", "Express.js", "Django", "Flask", "FastAPI",
        "Spring", "Spring Boot", "Angular", "Vue.js", "Next.js", "NestJS",
        "ASP.NET", ".NET", "Ruby on Rails", "Laravel", "Flutter", "React Native",
        "Bootstrap", "Tailwind CSS", "jQuery", "Redux", "GraphQL"
    ],
    "Data Science & AI / ML": [
        "Machine Learning", "Deep Learning", "Natural Language Processing",
        "Computer Vision", "TensorFlow", "PyTorch", "Keras", "Scikit-learn",
        "Pandas", "NumPy", "SciPy", "OpenCV", "Hugging Face", "spaCy", "NLTK",
        "Matplotlib", "Seaborn", "XGBoost", "LightGBM", "Data Analysis",
        "Data Engineering", "Big Data", "Apache Spark", "Hadoop", "Generative AI",
        "Large Language Models", "Transformers", "Statistics"
    ],
    "Databases & Storage": [
        "MySQL", "PostgreSQL", "MongoDB", "Redis", "SQLite", "Oracle",
        "Microsoft SQL Server", "Cassandra", "DynamoDB", "Firebase",
        "Elasticsearch", "Neo4j", "MariaDB", "Snowflake", "BigQuery"
    ],
    "Cloud & DevOps": [
        "AWS", "Microsoft Azure", "Google Cloud Platform", "Docker", "Kubernetes",
        "CI/CD", "Jenkins", "GitHub Actions", "GitLab CI", "Terraform",
        "Ansible", "Linux", "Unix", "Nginx", "Apache", "Prometheus",
        "Grafana", "Serverless", "Microservices"
    ],
    "Web Technologies & Tools": [
        "HTML", "HTML5", "CSS", "CSS3", "REST API",
        "WebSockets", "JSON", "XML", "Git", "GitHub", "GitLab",
        "Bitbucket", "Postman", "Swagger", "JIRA", "Agile", "Scrum",
        "Unit Testing", "Jest", "PyTest", "System Design"
    ]
}

# Skill Normalization Map (lowercase alias/variation -> Canonical Name)
SKILL_NORMALIZATION: Dict[str, str] = {
    # ML & AI
    "ml": "Machine Learning",
    "machine learning": "Machine Learning",
    "machine-learning": "Machine Learning",
    "dl": "Deep Learning",
    "deep learning": "Deep Learning",
    "nlp": "Natural Language Processing",
    "natural language processing": "Natural Language Processing",
    "cv": "Computer Vision",
    "computer vision": "Computer Vision",
    "genai": "Generative AI",
    "generative ai": "Generative AI",
    "llm": "Large Language Models",
    "llms": "Large Language Models",
    "large language models": "Large Language Models",
    "tf": "TensorFlow",
    "tensorflow": "TensorFlow",
    "torch": "PyTorch",
    "pytorch": "PyTorch",
    "sklearn": "Scikit-learn",
    "scikit-learn": "Scikit-learn",
    "scikit learn": "Scikit-learn",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "scipy": "SciPy",
    "opencv": "OpenCV",
    "cv2": "OpenCV",
    "spacy": "spaCy",
    "nltk": "NLTK",
    "huggingface": "Hugging Face",
    "hugging face": "Hugging Face",
    "xgboost": "XGBoost",
    "lightgbm": "LightGBM",
    "spark": "Apache Spark",
    "apache spark": "Apache Spark",
    "pyspark": "Apache Spark",

    # Programming Languages
    "python": "Python",
    "py": "Python",
    "python3": "Python",
    "java": "Java",
    "core java": "Java",
    "c": "C",
    "c++": "C++",
    "cpp": "C++",
    "c#": "C#",
    "csharp": "C#",
    "c sharp": "C#",
    "javascript": "JavaScript",
    "js": "JavaScript",
    "typescript": "TypeScript",
    "ts": "TypeScript",
    "golang": "Go",
    "go": "Go",
    "rust": "Rust",
    "ruby": "Ruby",
    "php": "PHP",
    "swift": "Swift",
    "kotlin": "Kotlin",
    "dart": "Dart",
    "r": "R",
    "scala": "Scala",
    "matlab": "MATLAB",
    "bash": "Bash",
    "shell": "Shell Scripting",
    "shell scripting": "Shell Scripting",
    "sql": "SQL",

    # Web & Frameworks
    "react": "React",
    "react.js": "React",
    "reactjs": "React",
    "react native": "React Native",
    "node": "Node.js",
    "nodejs": "Node.js",
    "node.js": "Node.js",
    "express": "Express.js",
    "express.js": "Express.js",
    "expressjs": "Express.js",
    "django": "Django",
    "flask": "Flask",
    "fastapi": "FastAPI",
    "fast api": "FastAPI",
    "spring": "Spring",
    "springboot": "Spring Boot",
    "spring boot": "Spring Boot",
    "angular": "Angular",
    "angularjs": "Angular",
    "vue": "Vue.js",
    "vuejs": "Vue.js",
    "vue.js": "Vue.js",
    "next": "Next.js",
    "next.js": "Next.js",
    "nextjs": "Next.js",
    "nest": "NestJS",
    "nestjs": "NestJS",
    ".net": ".NET",
    "dotnet": ".NET",
    "asp.net": "ASP.NET",
    "rails": "Ruby on Rails",
    "ruby on rails": "Ruby on Rails",
    "laravel": "Laravel",
    "flutter": "Flutter",
    "bootstrap": "Bootstrap",
    "tailwind": "Tailwind CSS",
    "tailwindcss": "Tailwind CSS",
    "tailwind css": "Tailwind CSS",
    "jquery": "jQuery",
    "redux": "Redux",
    "graphql": "GraphQL",

    # Databases
    "mysql": "MySQL",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "psql": "PostgreSQL",
    "mongodb": "MongoDB",
    "mongo": "MongoDB",
    "redis": "Redis",
    "sqlite": "SQLite",
    "sqlite3": "SQLite",
    "oracle": "Oracle",
    "mssql": "Microsoft SQL Server",
    "sql server": "Microsoft SQL Server",
    "cassandra": "Cassandra",
    "dynamodb": "DynamoDB",
    "firebase": "Firebase",
    "firestore": "Firebase",
    "elasticsearch": "Elasticsearch",
    "elastic search": "Elasticsearch",
    "neo4j": "Neo4j",
    "snowflake": "Snowflake",
    "bigquery": "BigQuery",

    # Cloud & DevOps
    "aws": "AWS",
    "amazon web services": "AWS",
    "azure": "Microsoft Azure",
    "microsoft azure": "Microsoft Azure",
    "gcp": "Google Cloud Platform",
    "google cloud": "Google Cloud Platform",
    "google cloud platform": "Google Cloud Platform",
    "docker": "Docker",
    "k8s": "Kubernetes",
    "kubernetes": "Kubernetes",
    "ci/cd": "CI/CD",
    "cicd": "CI/CD",
    "jenkins": "Jenkins",
    "github actions": "GitHub Actions",
    "gitlab ci": "GitLab CI",
    "terraform": "Terraform",
    "ansible": "Ansible",
    "linux": "Linux",
    "unix": "Unix",
    "nginx": "Nginx",
    "apache": "Apache",
    "prometheus": "Prometheus",
    "grafana": "Grafana",
    "serverless": "Serverless",
    "microservices": "Microservices",

    # Tools & Practices
    "html": "HTML",
    "html5": "HTML",
    "css": "CSS",
    "css3": "CSS",
    "rest": "REST API",
    "rest api": "REST API",
    "rest apis": "REST API",
    "restful": "REST API",
    "restful api": "REST API",
    "restful apis": "REST API",
    "websocket": "WebSockets",
    "websockets": "WebSockets",
    "git": "Git",
    "github": "GitHub",
    "gitlab": "GitLab",
    "postman": "Postman",
    "swagger": "Swagger",
    "jira": "JIRA",
    "agile": "Agile",
    "scrum": "Scrum",
    "unit test": "Unit Testing",
    "unit testing": "Unit Testing",
    "pytest": "PyTest",
    "jest": "Jest",
    "system design": "System Design",
    "data structures": "Data Structures",
    "algorithms": "Algorithms",
    "dsa": "Data Structures & Algorithms"
}


def normalize_skill(skill_raw: str) -> Optional[str]:
    """Normalize a raw skill string to its canonical representation."""
    cleaned = skill_raw.strip().lower()
    return SKILL_NORMALIZATION.get(cleaned)


def get_all_canonical_skills() -> Set[str]:
    """Return the set of all canonical skill names across all categories."""
    canonical = set()
    for skills in SKILL_TAXONOMY.values():
        canonical.update(skills)
    canonical.update(SKILL_NORMALIZATION.values())
    return canonical


def get_skill_category(skill_name: str) -> str:
    """Find which category a canonical skill belongs to."""
    for category, skills in SKILL_TAXONOMY.items():
        if skill_name in skills:
            return category
    return "Other Technical Skills"
