PROFILE = {
    "name": "Benjamin Garcia",
    "title": "Benjamin Garcia",
    "tagline": "I turn code into meaningful creations.",
    "role": "Full-Stack Engineer",
    "location": "Los Angeles, CA",
    "email": "bentgarcia05@gmail.com",
    "photo": "img/portfolio/profile/me.jpg",
    "resume": "resume.pdf",
    "map_url": "https://www.google.com/maps/place/Westwood,+Los+Angeles,+CA/@34.0652211,-118.4610312,14z",
}

NAV_ITEMS = [
    {"label": "Home", "endpoint": "index"},
    {"label": "Timeline", "endpoint": "timeline"},
    {"label": "Hobbies", "endpoint": "hobbies"},
    {"label": "Projects", "endpoint": "projects"},
]

SOCIAL_LINKS = [
    {"label": "Email", "href": "mailto:bentgarcia05@gmail.com"},
    {"label": "LinkedIn", "href": "https://www.linkedin.com/in/btgarcia05/"},
    {"label": "GitHub", "href": "https://github.com/bgar324"},
    {"label": "logit", "href": "https://trylogit.me/u/ben"},
]

ABOUT_PARAGRAPHS = [
    "I'm a junior studying Computer Science at UCLA. I build production interfaces, full-stack systems, and AI tools.",
    "Currently, I work at Lindy as a Software Engineer Intern building core infrastructure and services for email and meeting agents. I also conduct research in UCLA's HCI Research Lab on multi-agent systems for scientific hypothesis generation.",
    "I care deeply about responsive, accessible interfaces that make complex systems feel clear, useful, and intuitive.",
]

EXPERIENCES = [
    {
        "role": "Software Engineer Intern",
        "company": "Lindy",
        "dates": "Jun 2026 - Present",
        "url": "https://www.lindy.ai",
        "image": "img/portfolio/companies/lindy.jpg",
        "description": "Building core infrastructure and services for Lindy's email and meeting agents, supporting the AI work assistant and no-code agent platform across inbox, scheduling, CRM, and other cross-app workflows.",
    },
    {
        "role": "Undergraduate Researcher",
        "company": "UCLA HCI Research Lab",
        "dates": "Dec 2025 - Present",
        "url": "https://www.hci.ucla.edu",
        "image": "img/portfolio/companies/ucla-hci.png",
        "description": "Collaborated on HI-COS, a multi-agent scientific hypothesis generation platform built with FastAPI, Pydantic AI, Supabase, Gemini, Next.js, React Flow, Zustand, and Tailwind.",
    },
    {
        "role": "Software Engineer Intern",
        "company": "Todd Agriscience",
        "dates": "Mar 2025 - Oct 2025",
        "url": "https://www.toddagriscience.com/",
        "image": "img/portfolio/companies/todd.png",
        "description": "Built and deployed Todd's first client-facing dashboard using Next.js, enabling 5-10 early customers to visualize AI-powered crop insights.",
    },
    {
        "role": "R&D Engineer Intern",
        "company": "Bonterra",
        "dates": "Jul 2025 - Aug 2025",
        "url": "https://www.bonterratech.com/",
        "image": "img/portfolio/companies/bonterra.jpg",
        "description": "Researched and prototyped agentic AI pipelines for nonprofit event analysis and presented findings to 40+ cross-functional stakeholders.",
    },
    {
        "role": "Software Engineer Intern",
        "company": "TensorStax",
        "dates": "May 2025 - Jun 2025",
        "url": "https://www.tensorstax.com",
        "image": "img/portfolio/companies/tensorstax.png",
        "description": "Designed secure credential-submission UI integrated with HashiCorp Vault and built low-latency frontend flows for enterprise data-source auth.",
    },
]

EDUCATION = [
    {
        "school": "University of California, Los Angeles",
        "degree": "BS, Computer Science",
        "dates": "2025 - Present",
        "url": "https://www.ucla.edu",
        "image": "img/portfolio/schools/ucla.webp",
        "description": "Software Engineer Lead at ACM Hack and exploretech.la.",
    },
    {
        "school": "Mt. San Antonio College",
        "degree": "Honors Transfer",
        "dates": "2023 - 2025",
        "url": "https://www.mtsac.edu",
        "image": "img/portfolio/schools/mtsac.webp",
        "description": "Outreach Officer and Frontend Developer for the Computer Science Club.",
    },
]

PROJECTS = [
    {
        "title": "GitProof",
        "summary": "Recruiter-facing GitHub reports that make public contribution history legible and credible.",
        "image": "img/portfolio/projects/gitproof.png",
        "url": "https://gitproof.dev",
        "github": "https://github.com/bgar324/gitproof-2",
        "tags": ["Astro", "TypeScript", "Tailwind", "Postgres", "GitHub API"],
    },
    {
        "title": "Logit",
        "summary": "A lightweight workout tracker built for fast logging and clear progress review.",
        "image": "img/portfolio/projects/logit.png",
        "url": "https://trylogit.me",
        "github": "https://github.com/bgar324/log-it",
        "tags": ["Next.js", "TypeScript", "Tailwind", "Postgres", "Recharts"],
    },
]

HOBBIES = [
    {
        "name": "Weightlifting",
        "image": "img/portfolio/projects/logit.png",
        "description": "Training consistently and building tools like Logit to make fast workout logging and progress review easier.",
    },
    {
        "name": "Time with my dog",
        "image": "img/portfolio/profile/me.jpg",
        "description": "Spending time away from the keyboard with my dog and family.",
    },
    {
        "name": "Elden Ring",
        "image": "img/portfolio/hobbies/hom.webp",
        "description": "Exploring the Lands Between and taking on late-game fights like Malenia and Promised Consort Radahn.",
    },
]

LOCATIONS = [
    {
        "name": "Los Angeles / Westwood",
        "description": "Home base while studying computer science at UCLA.",
        "url": PROFILE["map_url"],
    },
    {
        "name": "UCLA",
        "description": "Current school and research community.",
        "url": "https://www.google.com/maps/place/University+of+California,+Los+Angeles",
    },
    {
        "name": "Mt. San Antonio College",
        "description": "Honors transfer background and early CS club work.",
        "url": "https://www.google.com/maps/place/Mt.+San+Antonio+College",
    },
]
