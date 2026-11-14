"""Dynamic Tailored Technical Interview Question & Competency Rubric Generator.

Generates targeted interview kits based on the mathematical delta between candidate
skills and JD requirements. Helps hiring managers verify claimed skills and test learning agility on gaps.
"""

from typing import Dict, Any, List

# Curated Technical Knowledge Rubric for key technology domains
SKILL_QUESTION_BANK: Dict[str, Dict[str, str]] = {
    "Python": {
        "question": "How do Python's GIL (Global Interpreter Lock) and asyncio differ when handling CPU-bound vs I/O-bound tasks?",
        "expected_signal": "Should mention threading vs multiprocessing, event loops, non-blocking I/O, and CPU-intensive offloading."
    },
    "FastAPI": {
        "question": "How do you structure dependency injection and async database sessions (e.g., with SQLAlchemy/encode/databases) to prevent connection leaks?",
        "expected_signal": "Understands `Depends()`, context managers, async session lifecycle, and middleware error handling."
    },
    "Django": {
        "question": "Explain how you optimize N+1 query problems in Django ORM and when you use `select_related` vs `prefetch_related`.",
        "expected_signal": "Differentiates single SQL joins (ForeignKey/OneToOne) vs separate batched lookups (ManyToMany)."
    },
    "React": {
        "question": "What causes unnecessary re-renders in React and how do you leverage `useMemo`, `useCallback`, and component composition to optimize rendering?",
        "expected_signal": "Understands reference equality, dependency arrays, reconciliation diffing, and memoization overhead."
    },
    "Node.js": {
        "question": "Explain how the Node.js event loop handles Microtasks (Promises, process.nextTick) vs Macrotasks (timers, I/O callbacks).",
        "expected_signal": "Clarifies execution priority, libuv thread pool, and non-blocking asynchronous patterns."
    },
    "SQL": {
        "question": "How do B-Tree and Hash indexes work in relational databases, and what are the trade-offs of indexing frequently updated tables?",
        "expected_signal": "Understands read speed improvements vs write/insert performance penalties and storage overhead."
    },
    "PostgreSQL": {
        "question": "How does PostgreSQL manage MVCC (Multi-Version Concurrency Control) and why is autovacuum critical for database health?",
        "expected_signal": "Mentions dead tuples, transaction visibility, table bloat, and vacuuming mechanisms."
    },
    "Docker": {
        "question": "How do multi-stage Docker builds reduce image size and enhance container security in production pipelines?",
        "expected_signal": "Explains stripping build dependencies/compilers from final slim runtime images and non-root execution."
    },
    "Kubernetes": {
        "question": "Explain the difference between Readiness and Liveness probes in Kubernetes, and what happens when each probe fails.",
        "expected_signal": "Liveness restarts container; Readiness removes Pod from Service endpoint routing to prevent 502/503 errors."
    },
    "AWS": {
        "question": "How do you design a high-availability, fault-tolerant architecture across multiple Availability Zones using load balancers and auto-scaling?",
        "expected_signal": "Covers stateless services, ALB/NLB health checks, multi-AZ RDS failover, and zero single-points-of-failure."
    },
    "Machine Learning": {
        "question": "How do you detect and mitigate data leakage between training and validation splits in tabular or time-series datasets?",
        "expected_signal": "Mentions fitting transformers/scalers only on train fold, temporal windowing, and target leakage detection."
    },
    "Deep Learning": {
        "question": "What is the vanishing/exploding gradient problem in deep networks, and how do residual connections (ResNet) or Layer Normalization resolve it?",
        "expected_signal": "Explains identity shortcut pathways, gradient propagation, and activation stabilization."
    },
    "Git": {
        "question": "When would you use `git rebase` instead of `git merge`, and what are the risks of rebasing shared public branches?",
        "expected_signal": "Understands linear commit history vs true historical topology, and dangers of rewriting pushed history."
    }
}


def generate_interview_kit(
    matched_skills: Any = None,
    missing_skills: Any = None,
    experience_years: float = 0.0,
    candidate_name: str = "Candidate"
) -> Dict[str, Any]:
    """Generate a structured, personalized technical interview kit for a candidate.
    
    Supports two calling conventions:
    1. generate_interview_kit(matched_skills, missing_skills, experience_years, candidate_name)
    2. generate_interview_kit(candidate_dict, jd_analysis_dict)
    """
    matched_list: List[str] = []
    missing_list: List[str] = []

    # Handle polymorphic call signature (candidate dict passed as first arg)
    if isinstance(matched_skills, dict):
        cand = matched_skills
        jd = missing_skills if isinstance(missing_skills, dict) else {}
        candidate_name = cand.get("candidate_name") or cand.get("name") or "Candidate"
        
        # Extract experience
        exp_prof = cand.get("candidate_profile", {}).get("experience", {})
        if isinstance(exp_prof, dict):
            experience_years = float(exp_prof.get("total_years", 0.0) or 0.0)
        else:
            experience_years = float(cand.get("experience_years", 0.0) or 0.0)

        # Extract matched skills
        bd = cand.get("breakdown", {})
        req_matched = bd.get("required_skills", {}).get("matched", [])
        pref_matched = bd.get("preferred_skills", {}).get("matched", [])
        matched_list = list(dict.fromkeys(req_matched + pref_matched))
        if not matched_list:
            matched_list = cand.get("candidate_profile", {}).get("skills", [])

        # Extract missing skills
        missing_list = bd.get("required_skills", {}).get("missing", [])
        if not missing_list and jd:
            jd_req = jd.get("required_skills", [])
            cand_skills_lower = {s.lower() for s in matched_list}
            missing_list = [s for s in jd_req if s.lower() not in cand_skills_lower]
    else:
        matched_list = list(matched_skills or [])
        missing_list = list(missing_skills or [])

    verification_questions = []
    gap_questions = []
    
    # 1. Verification Questions for Matched Skills (test authenticity)
    for skill in matched_list:
        for bank_skill, details in SKILL_QUESTION_BANK.items():
            if bank_skill.lower() == str(skill).lower():
                verification_questions.append({
                    "skill": bank_skill,
                    "type": "Skill Verification (Claimed on Resume)",
                    "question": details["question"],
                    "evaluation_guideline": details["expected_signal"],
                    "look_for": details["expected_signal"]
                })
                break
                
    # If no bank match found, add dynamic template
    if not verification_questions and matched_list:
        primary_skill = matched_list[0]
        verification_questions.append({
            "skill": primary_skill,
            "type": "Skill Verification (Claimed on Resume)",
            "question": f"Walk me through a production project where you utilized {primary_skill}. What was the most challenging technical roadblock and how did you resolve it?",
            "evaluation_guideline": "Look for depth of implementation details, debugging methodology, and trade-off awareness.",
            "look_for": "Look for depth of implementation details, debugging methodology, and trade-off awareness."
        })
        
    # 2. Probe Questions for Missing / Gap Skills (test learning agility)
    for missing in missing_list[:3]:  # Top 3 gaps
        guide = "Assesses conceptual adaptability, parallel framework knowledge, and proactive upskilling approach."
        gap_questions.append({
            "skill": missing,
            "missing_skill": missing,
            "type": "Skill Gap Probe (Required by Job Description)",
            "question": f"Our role relies heavily on {missing}, which wasn't highlighted on your resume. How do your existing technical skills translate to this area, and how would you ramp up quickly?",
            "evaluation_guideline": guide,
            "look_for": guide
        })
        
    # 3. Seniority / Behavioral Scenario Question based on years of experience
    if experience_years >= 5.0:
        seniority_level = "Senior / Lead"
        scenario_question = {
            "type": "Senior Architecture & Leadership",
            "context": "Senior Engineering Leadership & Architectural Trade-offs",
            "question": "How do you balance technical debt against urgent product feature deliveries, and how do you mentor junior developers during code reviews?",
            "evaluation_guideline": "Evaluates strategic engineering maturity, architectural foresight, and team empowerment.",
            "evaluation_criteria": "Evaluates strategic engineering maturity, architectural foresight, and team empowerment."
        }
    elif experience_years >= 2.0:
        seniority_level = "Mid-Level Professional"
        scenario_question = {
            "type": "System Reliability & Collaboration",
            "context": "Production Incident Management & Systems Debugging",
            "question": "Describe a scenario where a critical bug slipped into production. How did you diagnose the root cause, mitigate immediate impact, and prevent recurrence?",
            "evaluation_guideline": "Evaluates systematic debugging, post-mortem analysis, and automated testing rigor.",
            "evaluation_criteria": "Evaluates systematic debugging, post-mortem analysis, and automated testing rigor."
        }
    else:
        seniority_level = "Entry Level / Associate"
        scenario_question = {
            "type": "Foundational Problem Solving & Learning",
            "context": "Engineering Ramp-up & Self-Directed Problem Solving",
            "question": "When assigned a task involving an unfamiliar codebase or technology stack, what structured steps do you take to understand the architecture and contribute safely?",
            "evaluation_guideline": "Evaluates self-sufficiency, documentation reading habits, and effective question-asking.",
            "evaluation_criteria": "Evaluates self-sufficiency, documentation reading habits, and effective question-asking."
        }
        
    return {
        "candidate": candidate_name,
        "experience_level": seniority_level,
        "detected_experience_years": experience_years,
        "verification_questions": verification_questions[:4],
        "gap_questions": gap_questions,
        "gap_probe_questions": gap_questions,
        "scenario_question": scenario_question,
        "seniority_scenario": scenario_question,
        "total_questions": len(verification_questions[:4]) + len(gap_questions) + 1
    }

