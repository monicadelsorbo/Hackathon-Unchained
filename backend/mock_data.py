"""
UNCHAINED - Mock Data per demo hackathon.
3 dipendenti, 1 manager, 5 mentori, 30 corsi e-learning.
"""

# ── Profili Dipendenti ─────────────────────────────────────────────────────

EMPLOYEES = {
    "emp-001": {
        "id": "emp-001",
        "name": "Marco Bianchi",
        "current_role": "Junior Software Developer",
        "department": "Engineering",
        "cv_text": """
MARCO BIANCHI — Junior Software Developer

ESPERIENZA LAVORATIVA:
• Junior Developer presso TechFlow Srl (2023-presente)
  - Sviluppo feature in Python e JavaScript per piattaforma e-commerce
  - Manutenzione API REST con Flask
  - Bug fixing e code review con team di 4 sviluppatori
  - Utilizzo Git, Jira, CI/CD con GitHub Actions

• Stage sviluppatore presso DataLab (2022-2023, 6 mesi)
  - Supporto allo sviluppo backend in Python
  - Scrittura test unitari con pytest
  - Documentazione tecnica

FORMAZIONE:
• Laurea Triennale in Informatica, Università di Milano (2022)
  - Tesi: "Implementazione di un sistema di raccomandazione basato su collaborative filtering"

COMPETENZE TECNICHE:
• Linguaggi: Python (buono), JavaScript (base), SQL (base)
• Framework: Flask, React (base)
• Tools: Git, Docker (base), PostgreSQL
• Testing: pytest, unittest

COMPETENZE TRASVERSALI:
• Buona capacità di lavoro in team
• Problem solving analitico
• Comunicazione scritta efficace

LINGUE: Italiano (madrelingua), Inglese (B2)

INTERESSI: Machine Learning, Cloud Computing, Open Source
""",
        "hr_notes": "Marco è un developer promettente con ottime basi. Ha dimostrato iniziativa nei progetti di team ma necessita di approfondire architetture software, design patterns e competenze di leadership tecnica per passare a Senior. Puntuale, affidabile, buon team player.",
    },
    "emp-002": {
        "id": "emp-002",
        "name": "Giulia Rossi",
        "current_role": "Mid-Level UX Designer",
        "department": "Design",
        "cv_text": """
GIULIA ROSSI — Mid-Level UX Designer

ESPERIENZA LAVORATIVA:
• UX Designer presso CreativeHub (2021-presente)
  - Design di interfacce utente per app mobile e web (Figma, Sketch)
  - Conduzione user research: interviste, survey, usability testing
  - Creazione wireframe, prototipi interattivi e design system
  - Collaborazione con team di sviluppo (Agile/Scrum)
  - Redesign completo del flusso di onboarding (+35% completion rate)

• Junior UX Designer presso DigitalWave (2019-2021)
  - Wireframing e prototyping per 8 progetti client
  - Supporto alla ricerca utente e analisi competitor
  - Creazione di presentazioni e deliverable per stakeholder

FORMAZIONE:
• Master in Interaction Design, Politecnico di Milano (2019)
• Laurea in Design della Comunicazione, ISIA Firenze (2017)

COMPETENZE TECNICHE:
• Design: Figma (avanzato), Sketch, Adobe XD, Illustrator, Photoshop
• Prototyping: Figma Prototyping, InVision, Principle
• Research: UserTesting, Hotjar, Google Analytics, Maze
• Frontend awareness: HTML/CSS (base), comprensione React components

COMPETENZE TRASVERSALI:
• Empatia e ascolto attivo
• Presentazione e storytelling
• Collaborazione cross-funzionale
• Gestione stakeholder

LINGUE: Italiano (madrelingua), Inglese (C1), Spagnolo (A2)

INTERESSI: Design thinking, Accessibility, Service design, Mentoring junior
""",
        "hr_notes": "Giulia ha forti competenze di design e research. Per il ruolo di UX Lead deve sviluppare: leadership di team, strategic thinking, gestione budget/planning, competenze di facilitazione workshop. Ha già mostrato capacità di mentoring informale con i junior.",
    },
    "emp-003": {
        "id": "emp-003",
        "name": "Alessandro Ferretti",
        "current_role": "Senior Backend Developer",
        "department": "Engineering",
        "cv_text": """
ALESSANDRO FERRETTI — Senior Backend Developer

ESPERIENZA LAVORATIVA:
• Senior Backend Developer presso CloudScale (2020-presente)
  - Architettura e sviluppo microservizi in Python (FastAPI, Django)
  - Design e ottimizzazione database PostgreSQL, Redis, MongoDB
  - Implementazione event-driven architecture con Kafka
  - Gestione infrastruttura AWS (EC2, ECS, Lambda, S3, RDS)
  - Code review, mentoring di 3 junior developer
  - Riduzione latency API del 40% tramite caching e query optimization

• Backend Developer presso FinTech Solutions (2017-2020)
  - Sviluppo piattaforma di pagamenti in Python/Django
  - Integrazione con gateway di pagamento (Stripe, PayPal)
  - Implementazione sistema di autenticazione OAuth2/JWT
  - Gestione team di 2 developer per progetto di migrazione DB

• Junior Developer presso WebAgency (2015-2017)
  - Sviluppo backend PHP/Laravel e Python/Flask
  - API REST e integrazioni third-party

FORMAZIONE:
• Laurea Magistrale in Ingegneria Informatica, Politecnico di Torino (2015)
  - Tesi: "Scalabilità di sistemi distribuiti: analisi e pattern architetturali"
• AWS Solutions Architect Associate (2021)
• Kubernetes Administrator (CKA) (2022)

COMPETENZE TECNICHE:
• Linguaggi: Python (esperto), Go (intermedio), SQL (avanzato), TypeScript (base)
• Framework: FastAPI, Django, Flask, gRPC
• Cloud: AWS (avanzato), Docker, Kubernetes, Terraform
• Database: PostgreSQL, Redis, MongoDB, Elasticsearch
• Architettura: Microservizi, Event-driven, CQRS, Domain-Driven Design
• DevOps: CI/CD, GitHub Actions, ArgoCD, Prometheus, Grafana

COMPETENZE TRASVERSALI:
• Pensiero architetturale e visione di sistema
• Mentoring e knowledge sharing
• Comunicazione tecnica con stakeholder non-tecnici
• Decision making sotto pressione

LINGUE: Italiano (madrelingua), Inglese (C1)

INTERESSI: System design, Cloud-native, Tech leadership, Conference speaking
""",
        "hr_notes": "Alessandro è un ingegnere eccellente con profonda conoscenza tecnica. Per diventare Solutions Architect deve rafforzare: visione business, capacità di pre-sales, gestione relazione con C-level, governance IT, competenze di enterprise architecture. Ha il potenziale ma deve ampliare la prospettiva oltre il codice.",
    },
}


# ── Profilo Manager ────────────────────────────────────────────────────────

MANAGERS = {
    "mgr-001": {
        "id": "mgr-001",
        "name": "Laura Conti",
        "role": "Engineering Manager",
        "department": "Engineering",
        "email": "laura.conti@unchained.demo",
    }
}


# ── Profili Mentori ────────────────────────────────────────────────────────

MENTORS = [
    {
        "mentor_id": "mnt-001",
        "name": "Dr. Stefano Marini",
        "role": "Principal Engineer",
        "expertise": [
            "System Design",
            "Microservizi",
            "Cloud Architecture",
            "Python",
            "Leadership Tecnica",
        ],
        "completed_mentorships": 12,
        "availability": "3 ore/settimana",
        "bio": "15 anni di esperienza in architetture distribuite. Ex-Google, ha guidato la migrazione cloud di 3 aziende Fortune 500. Appassionato di mentoring e crescita dei talenti tecnici.",
    },
    {
        "mentor_id": "mnt-002",
        "name": "Chiara Fontana",
        "role": "Head of Design",
        "expertise": [
            "UX Strategy",
            "Design Leadership",
            "Service Design",
            "Design System",
            "Team Management",
        ],
        "completed_mentorships": 8,
        "availability": "2 ore/settimana",
        "bio": "12 anni nel design digitale. Ha costruito e guidato team di design fino a 15 persone. Specializzata in design strategy e trasformazione digitale. Speaker a conferenze internazionali.",
    },
    {
        "mentor_id": "mnt-003",
        "name": "Roberto Valli",
        "role": "Solutions Architect",
        "expertise": [
            "Enterprise Architecture",
            "Pre-Sales",
            "Cloud Strategy",
            "Governance IT",
            "Stakeholder Management",
        ],
        "completed_mentorships": 15,
        "availability": "2 ore/settimana",
        "bio": "18 anni nell'IT enterprise. Solutions Architect certificato AWS e Azure. Ha gestito progetti da 5M+ EUR. Esperto nel ponte tra business e tecnologia.",
    },
    {
        "mentor_id": "mnt-004",
        "name": "Valentina Greco",
        "role": "Staff Software Engineer",
        "expertise": [
            "Python",
            "Software Architecture",
            "Design Patterns",
            "Testing",
            "Code Quality",
            "Machine Learning",
        ],
        "completed_mentorships": 10,
        "availability": "4 ore/settimana",
        "bio": "10 anni di sviluppo software. Contributor open source attiva. Specializzata in clean code, architettura software e best practices. Tiene workshop interni su design patterns.",
    },
    {
        "mentor_id": "mnt-005",
        "name": "Andrea Colombo",
        "role": "VP of Engineering",
        "expertise": [
            "Engineering Management",
            "Strategic Planning",
            "Agile Transformation",
            "Comunicazione C-Level",
            "Budget Management",
        ],
        "completed_mentorships": 20,
        "availability": "1.5 ore/settimana",
        "bio": "20 anni nell'IT, di cui 8 in ruoli di leadership. Ha scalato team engineering da 10 a 80 persone. Esperto in organizational design e cultura ingegneristica.",
    },
]


# ── Catalogo Corsi E-Learning ──────────────────────────────────────────────

COURSE_CATALOG = [
    # --- Python & Backend ---
    {
        "course_id": "crs-001",
        "title": "Python for Advanced Developers",
        "platform": "Coursera",
        "url": "https://coursera.org/python-advanced",
        "duration_hours": 40,
        "cost_eur": 49.99,
        "rating": 4.7,
        "skill_tags": ["Python", "Design Patterns", "Advanced Programming"],
    },
    {
        "course_id": "crs-002",
        "title": "Software Architecture & Design Patterns in Python",
        "platform": "Udemy",
        "url": "https://udemy.com/software-arch-python",
        "duration_hours": 28,
        "cost_eur": 29.99,
        "rating": 4.5,
        "skill_tags": ["Software Architecture", "Design Patterns", "Python", "SOLID"],
    },
    {
        "course_id": "crs-003",
        "title": "Microservices with FastAPI",
        "platform": "Udemy",
        "url": "https://udemy.com/fastapi-microservices",
        "duration_hours": 22,
        "cost_eur": 24.99,
        "rating": 4.6,
        "skill_tags": ["Microservizi", "FastAPI", "Python", "API Design"],
    },
    {
        "course_id": "crs-004",
        "title": "Django REST Framework Masterclass",
        "platform": "Coursera",
        "url": "https://coursera.org/django-rest",
        "duration_hours": 35,
        "cost_eur": 49.99,
        "rating": 4.4,
        "skill_tags": ["Django", "REST API", "Python", "Backend"],
    },
    # --- Cloud & DevOps ---
    {
        "course_id": "crs-005",
        "title": "AWS Solutions Architect Professional",
        "platform": "Coursera",
        "url": "https://coursera.org/aws-sa-pro",
        "duration_hours": 60,
        "cost_eur": 79.99,
        "rating": 4.8,
        "skill_tags": ["AWS", "Cloud Architecture", "Enterprise Architecture"],
    },
    {
        "course_id": "crs-006",
        "title": "Kubernetes in Production",
        "platform": "LinkedIn Learning",
        "url": "https://linkedin.com/learning/k8s-production",
        "duration_hours": 18,
        "cost_eur": 34.99,
        "rating": 4.5,
        "skill_tags": ["Kubernetes", "DevOps", "Container Orchestration"],
    },
    {
        "course_id": "crs-007",
        "title": "Terraform & Infrastructure as Code",
        "platform": "Udemy",
        "url": "https://udemy.com/terraform-iac",
        "duration_hours": 25,
        "cost_eur": 27.99,
        "rating": 4.6,
        "skill_tags": ["Terraform", "IaC", "Cloud", "DevOps"],
    },
    {
        "course_id": "crs-008",
        "title": "Docker Deep Dive",
        "platform": "LinkedIn Learning",
        "url": "https://linkedin.com/learning/docker-deep-dive",
        "duration_hours": 15,
        "cost_eur": 29.99,
        "rating": 4.7,
        "skill_tags": ["Docker", "Containers", "DevOps"],
    },
    # --- System Design & Architecture ---
    {
        "course_id": "crs-009",
        "title": "System Design for Senior Engineers",
        "platform": "Coursera",
        "url": "https://coursera.org/system-design",
        "duration_hours": 45,
        "cost_eur": 59.99,
        "rating": 4.8,
        "skill_tags": ["System Design", "Scalability", "Software Architecture"],
    },
    {
        "course_id": "crs-010",
        "title": "Domain-Driven Design in Practice",
        "platform": "Udemy",
        "url": "https://udemy.com/ddd-practice",
        "duration_hours": 20,
        "cost_eur": 34.99,
        "rating": 4.4,
        "skill_tags": ["DDD", "Software Architecture", "Design Patterns"],
    },
    {
        "course_id": "crs-011",
        "title": "Enterprise Architecture Fundamentals",
        "platform": "Coursera",
        "url": "https://coursera.org/enterprise-arch",
        "duration_hours": 50,
        "cost_eur": 69.99,
        "rating": 4.3,
        "skill_tags": ["Enterprise Architecture", "Governance IT", "TOGAF"],
    },
    # --- Database ---
    {
        "course_id": "crs-012",
        "title": "Advanced PostgreSQL & Query Optimization",
        "platform": "Udemy",
        "url": "https://udemy.com/postgresql-advanced",
        "duration_hours": 22,
        "cost_eur": 24.99,
        "rating": 4.6,
        "skill_tags": ["PostgreSQL", "SQL", "Database", "Performance"],
    },
    {
        "course_id": "crs-013",
        "title": "MongoDB for Developers",
        "platform": "LinkedIn Learning",
        "url": "https://linkedin.com/learning/mongodb-dev",
        "duration_hours": 16,
        "cost_eur": 29.99,
        "rating": 4.3,
        "skill_tags": ["MongoDB", "NoSQL", "Database"],
    },
    # --- Frontend & JavaScript ---
    {
        "course_id": "crs-014",
        "title": "React & TypeScript Complete Guide",
        "platform": "Udemy",
        "url": "https://udemy.com/react-typescript",
        "duration_hours": 38,
        "cost_eur": 29.99,
        "rating": 4.7,
        "skill_tags": ["React", "TypeScript", "Frontend", "JavaScript"],
    },
    {
        "course_id": "crs-015",
        "title": "Advanced JavaScript Patterns",
        "platform": "Coursera",
        "url": "https://coursera.org/js-patterns",
        "duration_hours": 30,
        "cost_eur": 39.99,
        "rating": 4.5,
        "skill_tags": ["JavaScript", "Design Patterns", "Frontend"],
    },
    # --- Machine Learning & Data ---
    {
        "course_id": "crs-016",
        "title": "Machine Learning Specialization",
        "platform": "Coursera",
        "url": "https://coursera.org/ml-specialization",
        "duration_hours": 80,
        "cost_eur": 79.99,
        "rating": 4.9,
        "skill_tags": ["Machine Learning", "Python", "Data Science"],
    },
    {
        "course_id": "crs-017",
        "title": "Deep Learning with PyTorch",
        "platform": "Udemy",
        "url": "https://udemy.com/deep-learning-pytorch",
        "duration_hours": 35,
        "cost_eur": 34.99,
        "rating": 4.6,
        "skill_tags": ["Deep Learning", "PyTorch", "Machine Learning", "Python"],
    },
    {
        "course_id": "crs-018",
        "title": "Data Engineering with Python",
        "platform": "LinkedIn Learning",
        "url": "https://linkedin.com/learning/data-eng-python",
        "duration_hours": 25,
        "cost_eur": 34.99,
        "rating": 4.4,
        "skill_tags": ["Data Engineering", "Python", "ETL", "Data Pipeline"],
    },
    # --- UX Design ---
    {
        "course_id": "crs-019",
        "title": "UX Strategy & Design Leadership",
        "platform": "Coursera",
        "url": "https://coursera.org/ux-strategy",
        "duration_hours": 30,
        "cost_eur": 49.99,
        "rating": 4.5,
        "skill_tags": ["UX Strategy", "Design Leadership", "Product Strategy"],
    },
    {
        "course_id": "crs-020",
        "title": "Advanced User Research Methods",
        "platform": "LinkedIn Learning",
        "url": "https://linkedin.com/learning/user-research-advanced",
        "duration_hours": 18,
        "cost_eur": 29.99,
        "rating": 4.6,
        "skill_tags": ["User Research", "UX", "Usability Testing"],
    },
    {
        "course_id": "crs-021",
        "title": "Design Systems at Scale",
        "platform": "Udemy",
        "url": "https://udemy.com/design-systems",
        "duration_hours": 20,
        "cost_eur": 24.99,
        "rating": 4.4,
        "skill_tags": ["Design System", "UI Design", "Component Library"],
    },
    {
        "course_id": "crs-022",
        "title": "Service Design Thinking",
        "platform": "Coursera",
        "url": "https://coursera.org/service-design",
        "duration_hours": 25,
        "cost_eur": 39.99,
        "rating": 4.3,
        "skill_tags": ["Service Design", "Design Thinking", "Innovation"],
    },
    {
        "course_id": "crs-023",
        "title": "Accessibility & Inclusive Design",
        "platform": "LinkedIn Learning",
        "url": "https://linkedin.com/learning/accessibility",
        "duration_hours": 12,
        "cost_eur": 19.99,
        "rating": 4.7,
        "skill_tags": ["Accessibility", "Inclusive Design", "WCAG"],
    },
    # --- Leadership & Soft Skills ---
    {
        "course_id": "crs-024",
        "title": "Technical Leadership & Team Management",
        "platform": "Coursera",
        "url": "https://coursera.org/tech-leadership",
        "duration_hours": 25,
        "cost_eur": 49.99,
        "rating": 4.6,
        "skill_tags": ["Leadership Tecnica", "Team Management", "Mentoring"],
    },
    {
        "course_id": "crs-025",
        "title": "Comunicazione Efficace per Tech Leaders",
        "platform": "Udemy",
        "url": "https://udemy.com/comunicazione-tech-leaders",
        "duration_hours": 15,
        "cost_eur": 24.99,
        "rating": 4.4,
        "skill_tags": ["Comunicazione", "Presentazione", "Stakeholder Management"],
    },
    {
        "course_id": "crs-026",
        "title": "Agile Project Management",
        "platform": "LinkedIn Learning",
        "url": "https://linkedin.com/learning/agile-pm",
        "duration_hours": 20,
        "cost_eur": 29.99,
        "rating": 4.5,
        "skill_tags": ["Agile", "Scrum", "Project Management"],
    },
    {
        "course_id": "crs-027",
        "title": "Strategic Thinking for Managers",
        "platform": "Coursera",
        "url": "https://coursera.org/strategic-thinking",
        "duration_hours": 18,
        "cost_eur": 39.99,
        "rating": 4.3,
        "skill_tags": ["Strategic Thinking", "Decision Making", "Business Strategy"],
    },
    {
        "course_id": "crs-028",
        "title": "Conflict Resolution & Negotiation",
        "platform": "Udemy",
        "url": "https://udemy.com/conflict-negotiation",
        "duration_hours": 10,
        "cost_eur": 19.99,
        "rating": 4.2,
        "skill_tags": ["Conflict Resolution", "Negotiation", "Soft Skills"],
    },
    # --- Business & Pre-Sales ---
    {
        "course_id": "crs-029",
        "title": "IT Governance & Compliance",
        "platform": "Coursera",
        "url": "https://coursera.org/it-governance",
        "duration_hours": 30,
        "cost_eur": 49.99,
        "rating": 4.2,
        "skill_tags": ["Governance IT", "Compliance", "Risk Management"],
    },
    {
        "course_id": "crs-030",
        "title": "Pre-Sales Engineering & Solution Selling",
        "platform": "LinkedIn Learning",
        "url": "https://linkedin.com/learning/presales-engineering",
        "duration_hours": 15,
        "cost_eur": 34.99,
        "rating": 4.5,
        "skill_tags": ["Pre-Sales", "Solution Selling", "Client Management"],
    },
    # --- Testing & Quality ---
    {
        "course_id": "crs-031",
        "title": "Test-Driven Development in Python",
        "platform": "Udemy",
        "url": "https://udemy.com/tdd-python",
        "duration_hours": 20,
        "cost_eur": 24.99,
        "rating": 4.5,
        "skill_tags": ["Testing", "TDD", "Python", "Code Quality"],
    },
    {
        "course_id": "crs-032",
        "title": "Software Testing Masterclass",
        "platform": "Coursera",
        "url": "https://coursera.org/testing-masterclass",
        "duration_hours": 30,
        "cost_eur": 39.99,
        "rating": 4.4,
        "skill_tags": ["Testing", "QA", "Integration Testing", "E2E Testing"],
    },
    {
        "course_id": "crs-033",
        "title": "Code Review Best Practices",
        "platform": "LinkedIn Learning",
        "url": "https://linkedin.com/learning/code-review",
        "duration_hours": 8,
        "cost_eur": 19.99,
        "rating": 4.6,
        "skill_tags": ["Code Review", "Code Quality", "Best Practices"],
    },
    # --- Security ---
    {
        "course_id": "crs-034",
        "title": "Application Security Fundamentals",
        "platform": "Coursera",
        "url": "https://coursera.org/appsec-fundamentals",
        "duration_hours": 25,
        "cost_eur": 49.99,
        "rating": 4.5,
        "skill_tags": ["Security", "OWASP", "AppSec", "Backend"],
    },
    {
        "course_id": "crs-035",
        "title": "Cloud Security on AWS",
        "platform": "Udemy",
        "url": "https://udemy.com/cloud-security-aws",
        "duration_hours": 20,
        "cost_eur": 34.99,
        "rating": 4.3,
        "skill_tags": ["Security", "AWS", "Cloud", "IAM"],
    },
    # --- API Design ---
    {
        "course_id": "crs-036",
        "title": "RESTful API Design & Best Practices",
        "platform": "LinkedIn Learning",
        "url": "https://linkedin.com/learning/restful-api-design",
        "duration_hours": 14,
        "cost_eur": 29.99,
        "rating": 4.6,
        "skill_tags": ["API Design", "REST", "Backend", "Best Practices"],
    },
    {
        "course_id": "crs-037",
        "title": "GraphQL Complete Guide",
        "platform": "Udemy",
        "url": "https://udemy.com/graphql-complete",
        "duration_hours": 22,
        "cost_eur": 27.99,
        "rating": 4.5,
        "skill_tags": ["GraphQL", "API Design", "Backend", "Frontend"],
    },
    {
        "course_id": "crs-038",
        "title": "gRPC & Protocol Buffers",
        "platform": "Coursera",
        "url": "https://coursera.org/grpc-protobuf",
        "duration_hours": 16,
        "cost_eur": 34.99,
        "rating": 4.4,
        "skill_tags": ["gRPC", "Microservizi", "API Design", "Backend"],
    },
    # --- Go & Rust ---
    {
        "course_id": "crs-039",
        "title": "Go: The Complete Developer's Guide",
        "platform": "Udemy",
        "url": "https://udemy.com/go-complete",
        "duration_hours": 35,
        "cost_eur": 29.99,
        "rating": 4.7,
        "skill_tags": ["Go", "Backend", "Concurrency", "Microservizi"],
    },
    {
        "course_id": "crs-040",
        "title": "Rust Programming for Systems Developers",
        "platform": "Coursera",
        "url": "https://coursera.org/rust-systems",
        "duration_hours": 40,
        "cost_eur": 49.99,
        "rating": 4.6,
        "skill_tags": ["Rust", "Systems Programming", "Performance"],
    },
    # --- CI/CD & Observability ---
    {
        "course_id": "crs-041",
        "title": "CI/CD Pipelines with GitHub Actions",
        "platform": "LinkedIn Learning",
        "url": "https://linkedin.com/learning/cicd-github-actions",
        "duration_hours": 12,
        "cost_eur": 24.99,
        "rating": 4.5,
        "skill_tags": ["CI/CD", "GitHub Actions", "DevOps", "Automation"],
    },
    {
        "course_id": "crs-042",
        "title": "Observability: Prometheus, Grafana & OpenTelemetry",
        "platform": "Udemy",
        "url": "https://udemy.com/observability-stack",
        "duration_hours": 18,
        "cost_eur": 29.99,
        "rating": 4.4,
        "skill_tags": ["Observability", "Prometheus", "Grafana", "DevOps"],
    },
    # --- Event-Driven & Messaging ---
    {
        "course_id": "crs-043",
        "title": "Apache Kafka for Developers",
        "platform": "Coursera",
        "url": "https://coursera.org/kafka-developers",
        "duration_hours": 25,
        "cost_eur": 44.99,
        "rating": 4.6,
        "skill_tags": ["Kafka", "Event-Driven", "Microservizi", "Streaming"],
    },
    {
        "course_id": "crs-044",
        "title": "Event-Driven Architecture Patterns",
        "platform": "Udemy",
        "url": "https://udemy.com/event-driven-patterns",
        "duration_hours": 16,
        "cost_eur": 29.99,
        "rating": 4.3,
        "skill_tags": ["Event-Driven", "CQRS", "Software Architecture", "Microservizi"],
    },
    # --- Additional Cloud ---
    {
        "course_id": "crs-045",
        "title": "Azure Solutions Architect Expert",
        "platform": "Coursera",
        "url": "https://coursera.org/azure-sa-expert",
        "duration_hours": 55,
        "cost_eur": 74.99,
        "rating": 4.5,
        "skill_tags": ["Azure", "Cloud Architecture", "Enterprise Architecture"],
    },
    {
        "course_id": "crs-046",
        "title": "Google Cloud Professional Architect",
        "platform": "LinkedIn Learning",
        "url": "https://linkedin.com/learning/gcp-architect",
        "duration_hours": 50,
        "cost_eur": 69.99,
        "rating": 4.4,
        "skill_tags": ["GCP", "Cloud Architecture", "Enterprise Architecture"],
    },
    {
        "course_id": "crs-047",
        "title": "Serverless Architecture on AWS",
        "platform": "Udemy",
        "url": "https://udemy.com/serverless-aws",
        "duration_hours": 20,
        "cost_eur": 27.99,
        "rating": 4.5,
        "skill_tags": ["Serverless", "AWS Lambda", "Cloud", "API Gateway"],
    },
    # --- Additional UX & Design ---
    {
        "course_id": "crs-048",
        "title": "Facilitazione Workshop & Design Sprint",
        "platform": "Coursera",
        "url": "https://coursera.org/design-sprint",
        "duration_hours": 15,
        "cost_eur": 34.99,
        "rating": 4.5,
        "skill_tags": ["Facilitazione Workshop", "Design Sprint", "Design Thinking"],
    },
    {
        "course_id": "crs-049",
        "title": "Product Strategy for Designers",
        "platform": "Udemy",
        "url": "https://udemy.com/product-strategy-designers",
        "duration_hours": 18,
        "cost_eur": 29.99,
        "rating": 4.3,
        "skill_tags": ["Product Strategy", "UX Strategy", "Business Strategy"],
    },
    {
        "course_id": "crs-050",
        "title": "Design Metrics & KPIs",
        "platform": "LinkedIn Learning",
        "url": "https://linkedin.com/learning/design-metrics",
        "duration_hours": 10,
        "cost_eur": 19.99,
        "rating": 4.2,
        "skill_tags": ["Design Metrics", "UX", "Data-Driven Design", "Analytics"],
    },
    {
        "course_id": "crs-051",
        "title": "Interaction Design Fundamentals",
        "platform": "Coursera",
        "url": "https://coursera.org/interaction-design",
        "duration_hours": 22,
        "cost_eur": 39.99,
        "rating": 4.6,
        "skill_tags": ["Interaction Design", "UI Design", "UX", "Prototyping"],
    },
    # --- Additional Leadership ---
    {
        "course_id": "crs-052",
        "title": "Coaching & Mentoring Skills",
        "platform": "Coursera",
        "url": "https://coursera.org/coaching-mentoring",
        "duration_hours": 15,
        "cost_eur": 34.99,
        "rating": 4.5,
        "skill_tags": ["Mentoring", "Coaching", "Leadership Tecnica", "Soft Skills"],
    },
    {
        "course_id": "crs-053",
        "title": "Emotional Intelligence for Leaders",
        "platform": "Udemy",
        "url": "https://udemy.com/emotional-intelligence",
        "duration_hours": 12,
        "cost_eur": 24.99,
        "rating": 4.4,
        "skill_tags": ["Emotional Intelligence", "Leadership", "Soft Skills"],
    },
    {
        "course_id": "crs-054",
        "title": "Budget & Resource Planning for Tech Teams",
        "platform": "LinkedIn Learning",
        "url": "https://linkedin.com/learning/budget-planning-tech",
        "duration_hours": 10,
        "cost_eur": 24.99,
        "rating": 4.2,
        "skill_tags": ["Budget Management", "Resource Planning", "Team Management"],
    },
    {
        "course_id": "crs-055",
        "title": "Comunicazione C-Level per Tecnici",
        "platform": "Udemy",
        "url": "https://udemy.com/comunicazione-clevel",
        "duration_hours": 8,
        "cost_eur": 19.99,
        "rating": 4.3,
        "skill_tags": ["Comunicazione C-Level", "Presentazione", "Executive Communication"],
    },
    {
        "course_id": "crs-056",
        "title": "Building High-Performance Engineering Teams",
        "platform": "Coursera",
        "url": "https://coursera.org/high-perf-teams",
        "duration_hours": 20,
        "cost_eur": 44.99,
        "rating": 4.7,
        "skill_tags": ["Team Management", "Engineering Management", "Culture"],
    },
    # --- Data & Analytics ---
    {
        "course_id": "crs-057",
        "title": "SQL Avanzato per Data Analysis",
        "platform": "Udemy",
        "url": "https://udemy.com/sql-avanzato",
        "duration_hours": 18,
        "cost_eur": 24.99,
        "rating": 4.5,
        "skill_tags": ["SQL", "Data Analysis", "Database", "Analytics"],
    },
    {
        "course_id": "crs-058",
        "title": "Data Visualization con Python",
        "platform": "LinkedIn Learning",
        "url": "https://linkedin.com/learning/data-viz-python",
        "duration_hours": 15,
        "cost_eur": 29.99,
        "rating": 4.4,
        "skill_tags": ["Data Visualization", "Python", "Matplotlib", "Data Science"],
    },
    # --- Emerging Tech ---
    {
        "course_id": "crs-059",
        "title": "Generative AI & LLM Applications",
        "platform": "Coursera",
        "url": "https://coursera.org/gen-ai-llm",
        "duration_hours": 30,
        "cost_eur": 59.99,
        "rating": 4.8,
        "skill_tags": ["AI", "LLM", "Generative AI", "Python", "Machine Learning"],
    },
    {
        "course_id": "crs-060",
        "title": "MLOps: Machine Learning in Production",
        "platform": "Udemy",
        "url": "https://udemy.com/mlops-production",
        "duration_hours": 28,
        "cost_eur": 39.99,
        "rating": 4.5,
        "skill_tags": ["MLOps", "Machine Learning", "DevOps", "Docker", "CI/CD"],
    },
]


# ── Target Positions (competenze richieste) ────────────────────────────────

TARGET_POSITIONS = {
    "Senior Software Developer": {
        "required_hard_skills": [
            "Python",
            "Software Architecture",
            "Design Patterns",
            "System Design",
            "API Design",
            "Testing",
            "Cloud",
            "Database",
        ],
        "required_soft_skills": [
            "Leadership Tecnica",
            "Mentoring",
            "Code Review",
            "Comunicazione Tecnica",
            "Problem Solving Avanzato",
        ],
        "min_level": 4,
    },
    "UX Lead": {
        "required_hard_skills": [
            "UX Strategy",
            "Design System",
            "User Research",
            "Service Design",
            "Accessibility",
            "Design Thinking",
        ],
        "required_soft_skills": [
            "Design Leadership",
            "Team Management",
            "Stakeholder Management",
            "Strategic Thinking",
            "Facilitazione Workshop",
            "Budget Management",
        ],
        "min_level": 4,
    },
    "Solutions Architect": {
        "required_hard_skills": [
            "Enterprise Architecture",
            "Cloud Architecture",
            "System Design",
            "Governance IT",
            "Microservizi",
        ],
        "required_soft_skills": [
            "Pre-Sales",
            "Comunicazione C-Level",
            "Strategic Thinking",
            "Stakeholder Management",
            "Solution Selling",
            "Decision Making",
        ],
        "min_level": 4,
    },
}
