"""Resume content. Edit this file, then run `python3 build_resume.py` to rebuild resume.pdf."""

R = "Times-Roman"      # regular
B = "Times-Bold"       # bold
I = "Times-Italic"     # italic

NAME = "PRAHADHESVARYAA KS"
CONTACT = "prahadhesvarya.issm@gmail.com  |  9361152310  |  Chennai"

CONTENT = [
    # ------------------------------------------------------------ Summary
    {"type": "section", "title": "Summary"},
    {"type": "paragraph", "runs": [(
        "MBA student with a BCA background and a strong interest in business problem solving "
        "and process improvement. Experienced in working with teams, coordinating projects, and "
        "understanding business challenges to find practical solutions. Interested in applying AI "
        "and technology to improve business processes and support better decision making.", R)],
     "space_after": 3},

    # ----------------------------------------------------------- Education
    {"type": "section", "title": "Education"},
    {"type": "entry", "runs": [("MBA", B)]},
    {"type": "entry", "runs": [("ISSM Business School, Chennai", R)], "right": "2025 - present"},
    {"type": "entry", "runs": [("BCA", B)]},
    {"type": "entry", "runs": [("Bishop Heber College, Trichy", R)], "right": "2022 \u2013 2025"},
    {"type": "space", "amount": 2},

    # -------------------------------------------------------------- Skills
    {"type": "section", "title": "Skills"},
    {"type": "columns", "columns": [
        ["SQL", "MS Office", "Power BI"],
        ["Figma", "Presentation (PPT)", "Communication"],
        ["Proactive", "Team management", "AI Fundamentals"],
    ]},

    # ---------------------------------------------------------- Internship
    {"type": "section", "title": "Internship"},
    {"type": "entry", "runs": [("Audit Intern", B), ("  \u2013  Neuberg Diagnostics", R)]},
    {"type": "bullet", "runs": [(
        "Collaborated with Legal and IT teams to resolve documentation and process-related "
        "issues.", R)], "space_after": 3},

    # ------------------------------------------------------------- Projects
    {"type": "section", "title": "Projects"},
    {"type": "bullet", "runs": [
        ("BUSINESS EXPLORER", B),
        (" - Approached an ironing shop in Tambaram to understand real business challenges. "
         "Prepared a structured set of questions and interacted directly with the shop owner to "
         "understand daily operations and challenges. Suggested practical growth ideas like "
         "hostel tie ups, delivery options, and franchise models. Learned how small insights can "
         "create big impact.", R)]},
    {"type": "bullet", "runs": [
        ("HITTING THE FIELD", B),
        (" - Took up a live challenge to sell Polaroids at 5\u00d7 the price and ended up "
         "achieving 10\u00d7. Explored how customer preferences and pricing strategies work in "
         "real life. Visited multiple locations across Chennai including beaches and hostels to "
         "directly approach customers and pitch the product. Successfully sold 300 Polaroids. "
         "Gained hands on experience in communication, market analysis, and adaptability.", R)]},
    {"type": "bullet", "runs": [
        ("AIM", B),
        (" - Worked as part of a three member team to organize and deliver corporate readiness "
         "seminars across multiple colleges, reaching 1,500+ students. Conducted sessions on "
         "professional self introduction, Advanced Excel (VLOOKUP, HLOOKUP, IF, Conditional "
         "Formatting), and structured mock interviews.", R)]},
    {"type": "bullet", "runs": [
        ("Acquired skills", B),
        (" - Project Management, analytical problem solving, customer behaviour analysis.", R)],
     "space_after": 3},

    # -------------------------------------------------- Certificate courses
    {"type": "section", "title": "Certificate Courses"},
    {"type": "bullet", "runs": [("Fundamentals of Business Analyst", B), (" - Microsoft", R)],
     "justify": False, "space_after": 1},
    {"type": "bullet", "runs": [("Root Cause Analysis", B), (" - Udemy", R)],
     "justify": False, "space_after": 3},

    # -------------------------------------------------------- Achievements
    {"type": "section", "title": "Achievements"},
    {"type": "bullet", "runs": [
        ("Served as ", R), ("Vice President", B),
        (" of the BCA Department at Bishop Heber College, leading student initiatives and "
         "organizing key academic events.", R)]},
    {"type": "bullet", "runs": [
        ("Worked as ", R), ("Secretary", B),
        (" of the Communication Club, coordinating programs, preparing reports, and hosting "
         "sessions as emcee.", R)], "space_after": 3},

    # ----------------------------------------------------------- Languages
    {"type": "section", "title": "Languages"},
    {"type": "columns", "columns": [["Tamil"], ["English"], []]},

    # -------------------------------------------------------------- Footer
    {"type": "section", "title": "Additional Information"},
    {"type": "labeled", "label": "Hobbies", "value": "Book Reading, Painting"},
    {"type": "labeled", "label": "Web Link", "value": "linkedin.com/in/Prahadhesvaryaa K S"},
]
