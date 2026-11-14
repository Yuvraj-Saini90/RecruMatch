"""Script to generate realistic demo resumes (PDF and DOCX) and sample Job Description."""

import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import docx
from docx.shared import Inches, Pt, RGBColor


def create_sample_job_description(dest_path: str):
    """Create a realistic Job Description file."""
    content = """Job Title: Senior Python & Machine Learning Engineer
Company: Apex Innovations
Location: Hybrid / Remote

About the Role:
We are seeking an experienced and passionate Senior Python & Machine Learning Engineer to design, build, and deploy production-grade machine learning pipelines and microservices. You will collaborate with cross-functional teams to integrate intelligent algorithms into our core SaaS platform.

Required Qualifications & Skills:
- Strong proficiency in Python with hands-on software development experience.
- Demonstrated experience in Machine Learning, Scikit-learn, and Pandas for model training and data preprocessing.
- Solid understanding of SQL and relational database systems.
- Practical experience with containerization using Docker.
- Experience building RESTful APIs using FastAPI or Django.
- Experience with Cloud deployments on AWS (Amazon Web Services).
- Proficient with version control systems including Git and GitHub.
- Minimum 3+ years of professional software development experience.
- Bachelor's degree (B.Tech / B.E. / B.S.) in Computer Science, Information Technology, or related discipline.

Preferred / Good-to-Have Skills:
- Hands-on experience with Kubernetes for container orchestration.
- Familiarity with PostgreSQL, Redis caching, and microservices architecture.
- Knowledge of Deep Learning frameworks such as TensorFlow or PyTorch.
- Familiarity with CI/CD automation pipelines.
- Master's degree in Computer Science, Data Science, or Artificial Intelligence.

Key Responsibilities:
- Architect and maintain scalable backend services and predictive analytics models.
- Build clean, documented, and testable code following engineering best practices.
- Monitor model performance, latency, and data drift in production environments.
"""
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(content)


def generate_pdf_resume(file_path: str, name: str, title: str, email: str, phone: str,
                        education: str, experience_text: str, skills_list: list,
                        projects: list, certifications: list):
    """Generate a clean, professional PDF resume using reportlab."""
    doc = SimpleDocTemplate(
        file_path,
        pagesize=letter,
        rightMargin=40, leftMargin=40,
        topMargin=40, bottomMargin=40
    )
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "ResumeTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#1e293b")
    )
    subtitle_style = ParagraphStyle(
        "ResumeSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#3b82f6")
    )
    contact_style = ParagraphStyle(
        "ResumeContact",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#64748b")
    )
    heading_style = ParagraphStyle(
        "ResumeHeading",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=10,
        spaceAfter=4
    )
    body_style = ParagraphStyle(
        "ResumeBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#334155")
    )

    story = []

    # Header
    story.append(Paragraph(name, title_style))
    story.append(Paragraph(title, subtitle_style))
    story.append(Paragraph(f"Email: {email} &nbsp;|&nbsp; Phone: {phone} &nbsp;|&nbsp; Location: Greater Noida, India", contact_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1"), spaceAfter=10))

    # Experience
    story.append(Paragraph("PROFESSIONAL EXPERIENCE", heading_style))
    story.append(Paragraph(experience_text, body_style))
    story.append(Spacer(1, 8))

    # Skills
    story.append(Paragraph("TECHNICAL SKILLS", heading_style))
    skills_formatted = ", ".join(skills_list)
    story.append(Paragraph(skills_formatted, body_style))
    story.append(Spacer(1, 8))

    # Education
    story.append(Paragraph("EDUCATION", heading_style))
    story.append(Paragraph(education, body_style))
    story.append(Spacer(1, 8))

    # Projects
    if projects:
        story.append(Paragraph("KEY PROJECTS", heading_style))
        for p in projects:
            story.append(Paragraph(f"• <b>{p['title']}:</b> {p['desc']}", body_style))
        story.append(Spacer(1, 8))

    # Certifications
    if certifications:
        story.append(Paragraph("CERTIFICATIONS", heading_style))
        for c in certifications:
            story.append(Paragraph(f"• {c}", body_style))

    doc.build(story)


def generate_docx_resume(file_path: str, name: str, title: str, email: str, phone: str,
                         education: str, experience_text: str, skills_list: list,
                         projects: list, certifications: list):
    """Generate a clean DOCX resume using python-docx."""
    doc = docx.Document()
    
    # Page Margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.6)
        section.bottom_margin = Inches(0.6)
        section.left_margin = Inches(0.6)
        section.right_margin = Inches(0.6)

    # Name
    p_name = doc.add_paragraph()
    run_name = p_name.add_run(name)
    run_name.font.size = Pt(20)
    run_name.font.bold = True
    run_name.font.color.rgb = RGBColor(30, 41, 59)

    # Subtitle
    p_sub = doc.add_paragraph()
    run_sub = p_sub.add_run(title)
    run_sub.font.size = Pt(12)
    run_sub.font.bold = True
    run_sub.font.color.rgb = RGBColor(59, 130, 246)

    # Contact
    p_contact = doc.add_paragraph()
    run_contact = p_contact.add_run(f"Email: {email} | Phone: {phone} | Location: Delhi NCR, India")
    run_contact.font.size = Pt(9.5)
    run_contact.font.color.rgb = RGBColor(100, 116, 139)

    # Experience
    h_exp = doc.add_heading(level=2)
    run_h_exp = h_exp.add_run("PROFESSIONAL EXPERIENCE")
    run_h_exp.font.size = Pt(12)
    run_h_exp.font.bold = True
    p_exp = doc.add_paragraph()
    p_exp.add_run(experience_text).font.size = Pt(10)

    # Skills in a Table (tests table extraction in python-docx!)
    h_sk = doc.add_heading(level=2)
    run_h_sk = h_sk.add_run("TECHNICAL SKILLS")
    run_h_sk.font.size = Pt(12)
    run_h_sk.font.bold = True

    table = doc.add_table(rows=1, cols=2)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = "Skill Domain"
    hdr_cells[1].text = "Technologies"
    
    row_1 = table.add_row().cells
    row_1[0].text = "Core Competencies"
    row_1[1].text = ", ".join(skills_list[:len(skills_list)//2])
    
    row_2 = table.add_row().cells
    row_2[0].text = "Secondary Tools"
    row_2[1].text = ", ".join(skills_list[len(skills_list)//2:])

    # Education
    h_edu = doc.add_heading(level=2)
    run_h_edu = h_edu.add_run("EDUCATION")
    run_h_edu.font.size = Pt(12)
    run_h_edu.font.bold = True
    p_edu = doc.add_paragraph()
    p_edu.add_run(education).font.size = Pt(10)

    # Projects
    if projects:
        h_proj = doc.add_heading(level=2)
        run_h_proj = h_proj.add_run("KEY PROJECTS")
        run_h_proj.font.size = Pt(12)
        run_h_proj.font.bold = True
        for p in projects:
            p_item = doc.add_paragraph(style='List Bullet')
            p_item.add_run(f"{p['title']}: ").bold = True
            p_item.add_run(p['desc'])

    # Certifications
    if certifications:
        h_cert = doc.add_heading(level=2)
        run_h_cert = h_cert.add_run("CERTIFICATIONS")
        run_h_cert.font.size = Pt(12)
        run_h_cert.font.bold = True
        for c in certifications:
            p_cert = doc.add_paragraph(style='List Bullet')
            p_cert.add_run(c)

    doc.save(file_path)


def main():
    base_dir = r"c:\Users\Yoru\OneDrive\Desktop\M_P"
    resumes_dir = os.path.join(base_dir, "data", "sample_resumes")
    os.makedirs(resumes_dir, exist_ok=True)

    # 1. Sample Job Description
    jd_path = os.path.join(base_dir, "data", "sample_job_description.txt")
    create_sample_job_description(jd_path)
    print("Created sample job description.")

    # 2. Candidate 1: Aman Verma (Strong Match - Senior Python/ML Dev) - PDF
    pdf_1 = os.path.join(resumes_dir, "Aman_Verma_Senior_Python_Dev.pdf")
    generate_pdf_resume(
        file_path=pdf_1,
        name="Aman Verma",
        title="Senior Python & Machine Learning Engineer",
        email="aman.verma.dev@example.com",
        phone="+91 98765 43210",
        education="B.Tech in Computer Science and Engineering, GNIOT Greater Noida (2021)",
        experience_text="Total Experience: 4 years of experience as Senior Software Engineer at InnovateTech Solutions (2022 - Present). Led design and development of scalable microservices, automated ML pipelines using Scikit-learn and Pandas, and containerized deployment with Docker and AWS.",
        skills_list=["Python", "FastAPI", "Django", "SQL", "PostgreSQL", "Machine Learning", "Scikit-learn", "Pandas", "NumPy", "Docker", "AWS", "Git", "Redis", "Linux", "REST API"],
        projects=[
            {"title": "Automated ML Inference Pipeline", "desc": "Built a scalable microservice serving scikit-learn models using FastAPI and Docker on AWS ECS."},
            {"title": "Financial Transaction Classifier", "desc": "Implemented high-throughput transaction categorizer using Python, PostgreSQL, and Pandas."}
        ],
        certifications=["AWS Certified Solutions Architect", "Docker Certified Associate"]
    )
    print("Created Aman_Verma_Senior_Python_Dev.pdf")

    # 3. Candidate 2: Priya Sharma (Strong/Good Match - Data Scientist) - PDF
    pdf_2 = os.path.join(resumes_dir, "Priya_Sharma_Data_Scientist.pdf")
    generate_pdf_resume(
        file_path=pdf_2,
        name="Priya Sharma",
        title="Data Scientist & AI Researcher",
        email="priya.sharma.ml@example.com",
        phone="+91 98123 45678",
        education="M.Tech in Artificial Intelligence & Data Science, Delhi University (2023)",
        experience_text="Total Experience: 2.5 years of experience as Data Scientist at QuantAnalytics Labs (2023 - Present). Specialized in statistical modeling, NLP pipelines with spaCy, and deep learning neural architectures using PyTorch and TensorFlow.",
        skills_list=["Python", "SQL", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Pandas", "NumPy", "Scikit-learn", "spaCy", "Git", "Data Analysis", "MySQL"],
        projects=[
            {"title": "NLP Sentiment Engine", "desc": "Developed multilingual sentiment analysis using spaCy and PyTorch."},
            {"title": "Customer Churn Prediction", "desc": "Trained predictive ensemble classifiers using Scikit-learn and Pandas."}
        ],
        certifications=["TensorFlow Developer Certificate"]
    )
    print("Created Priya_Sharma_Data_Scientist.pdf")

    # 4. Candidate 3: Rahul Kumar (Moderate Match - Junior Web Developer) - DOCX
    docx_1 = os.path.join(resumes_dir, "Rahul_Kumar_Junior_Web_Dev.docx")
    generate_docx_resume(
        file_path=docx_1,
        name="Rahul Kumar",
        title="Full Stack Web Developer",
        email="rahul.kumar.web@example.com",
        phone="+91 97234 56789",
        education="BCA in Computer Applications, AKTU University (2024)",
        experience_text="Total Experience: 1.2 years of experience as Junior Web Developer at WebCraft Studio (2024 - Present). Built responsive web user interfaces and RESTful APIs using React, Node.js, and MongoDB.",
        skills_list=["JavaScript", "React", "Node.js", "Express.js", "HTML", "CSS", "Python", "MongoDB", "Git", "REST API", "Tailwind CSS"],
        projects=[
            {"title": "E-Commerce Web Portal", "desc": "Created full-stack shopping application using React, Node.js, and MongoDB."},
            {"title": "Task Manager App", "desc": "Developed collaborative productivity tracker using JavaScript and Express."}
        ],
        certifications=["Meta Front-End Developer"]
    )
    print("Created Rahul_Kumar_Junior_Web_Dev.docx")

    # 5. Candidate 4: Sneha Gupta (Low/Specialized Match - DevOps Engineer) - DOCX
    docx_2 = os.path.join(resumes_dir, "Sneha_Gupta_Cloud_DevOps.docx")
    generate_docx_resume(
        file_path=docx_2,
        name="Sneha Gupta",
        title="Cloud Infrastructure & DevOps Engineer",
        email="sneha.gupta.ops@example.com",
        phone="+91 99345 67890",
        education="B.Tech in Information Technology, Engineering College (2022)",
        experience_text="Total Experience: 3.5 years of experience as Cloud & DevOps Engineer at CloudSphere Technologies (2022 - Present). Managed CI/CD automation pipelines, Kubernetes clusters, and infrastructure as code.",
        skills_list=["Docker", "Kubernetes", "AWS", "Terraform", "CI/CD", "Jenkins", "Linux", "Bash", "Ansible", "Nginx", "Git", "Prometheus", "Grafana"],
        projects=[
            {"title": "Multi-Region Kubernetes Cluster", "desc": "Automated deployment of resilient K8s clusters across AWS using Terraform."},
            {"title": "Zero-Downtime CI/CD Pipeline", "desc": "Designed enterprise deployment pipeline using Jenkins and Docker."}
        ],
        certifications=["Certified Kubernetes Administrator (CKA)", "AWS Certified Cloud Practitioner"]
    )
    print("Created Sneha_Gupta_Cloud_DevOps.docx")


if __name__ == "__main__":
    main()
