"""Skill Knowledge Graph & Implicit Competency Reasoning Engine (Semantic DAG).

Represents technical domain hierarchies and prerequisite relationships.
Infers unmentioned but logically necessary competencies (e.g., PyTorch implies Python + Deep Learning)
so qualified candidates are not penalized for omitting obvious foundational keywords.
"""

from typing import Dict, List, Set, Any, Tuple


# Semantic Graph: Child Skill -> List of Implied Prerequisites / Parent Domains (with confidence 0.0 - 1.0)
SKILL_ONTOLOGY_GRAPH: Dict[str, List[Tuple[str, float, str]]] = {
    # AI / ML
    "PyTorch": [
        ("Python", 0.98, "Core Programming Language"),
        ("Deep Learning", 0.95, "Parent Domain"),
        ("Machine Learning", 0.90, "Foundational Discipline")
    ],
    "TensorFlow": [
        ("Python", 0.98, "Core Programming Language"),
        ("Deep Learning", 0.95, "Parent Domain"),
        ("Machine Learning", 0.90, "Foundational Discipline")
    ],
    "Scikit-learn": [
        ("Python", 0.98, "Core Programming Language"),
        ("Machine Learning", 0.95, "Core Framework Domain"),
        ("Statistics", 0.85, "Mathematical Foundation")
    ],
    "Hugging Face": [
        ("Python", 0.95, "Core Programming Language"),
        ("Natural Language Processing", 0.95, "Specialized Domain"),
        ("Transformers", 0.92, "Underlying Architecture")
    ],
    "Computer Vision": [
        ("Machine Learning", 0.90, "Parent Domain"),
        ("Python", 0.85, "Primary Language Ecosystem")
    ],
    "Natural Language Processing": [
        ("Machine Learning", 0.90, "Parent Domain"),
        ("Python", 0.85, "Primary Language Ecosystem")
    ],

    # Backend / Web
    "FastAPI": [
        ("Python", 0.98, "Core Programming Language"),
        ("REST API", 0.95, "Architectural Style"),
        ("Async Programming", 0.88, "Concurrency Model")
    ],
    "Django": [
        ("Python", 0.98, "Core Programming Language"),
        ("SQL", 0.88, "Database Query Language"),
        ("REST API", 0.85, "API Layer")
    ],
    "Flask": [
        ("Python", 0.98, "Core Programming Language"),
        ("REST API", 0.90, "Architectural Style")
    ],
    "React": [
        ("JavaScript", 0.98, "Core Programming Language"),
        ("HTML", 0.92, "Web Markup"),
        ("CSS", 0.90, "Web Styling")
    ],
    "Next.js": [
        ("React", 0.98, "Underlying UI Library"),
        ("JavaScript", 0.95, "Core Language"),
        ("TypeScript", 0.85, "Modern Typing System")
    ],
    "Node.js": [
        ("JavaScript", 0.98, "Runtime Language"),
        ("REST API", 0.88, "API Architecture")
    ],
    "Express.js": [
        ("Node.js", 0.98, "Runtime Platform"),
        ("JavaScript", 0.98, "Core Programming Language"),
        ("REST API", 0.90, "Architectural Style")
    ],
    "Spring Boot": [
        ("Java", 0.98, "Core Programming Language"),
        ("REST API", 0.90, "API Layer"),
        ("Microservices", 0.85, "Architecture")
    ],

    # Cloud & DevOps
    "Kubernetes": [
        ("Docker", 0.95, "Container Engine Prerequisite"),
        ("CI/CD", 0.85, "Deployment Automation"),
        ("Linux", 0.88, "Operating System Environment")
    ],
    "Docker": [
        ("Linux", 0.90, "Host Operating System Fundamentals"),
        ("CI/CD", 0.82, "DevOps Workflow")
    ],
    "Terraform": [
        ("Cloud Infrastructure", 0.92, "Target Domain"),
        ("DevOps", 0.90, "Operational Methodology")
    ],
    "PostgreSQL": [
        ("SQL", 0.98, "Relational Query Language"),
        ("Database Design", 0.85, "Structural Modeling")
    ],
    "MySQL": [
        ("SQL", 0.98, "Relational Query Language"),
        ("Database Design", 0.85, "Structural Modeling")
    ]
}


def infer_implicit_competencies(explicit_skills: List[str]) -> List[Dict[str, Any]]:
    """Traverse the skill ontology graph to deduce implicit competencies from claimed skills."""
    explicit_set = {s.strip().lower() for s in explicit_skills}
    inferred_map: Dict[str, Dict[str, Any]] = {}

    for skill in explicit_skills:
        for parent_skill, edges in SKILL_ONTOLOGY_GRAPH.items():
            if parent_skill.lower() == skill.lower():
                for implied_skill, confidence, relationship in edges:
                    # Only infer if candidate did NOT explicitly write it
                    if implied_skill.lower() not in explicit_set:
                        current = inferred_map.get(implied_skill)
                        if not current or confidence > current["confidence"]:
                            inferred_map[implied_skill] = {
                                "inferred_skill": implied_skill,
                                "source_skill": parent_skill,
                                "confidence": confidence,
                                "confidence_pct": f"{int(confidence * 100)}%",
                                "relationship": relationship
                            }

    # Sort descending by confidence
    return sorted(list(inferred_map.values()), key=lambda x: x["confidence"], reverse=True)
