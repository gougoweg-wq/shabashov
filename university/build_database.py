"""Builds the university database: university_database.xlsx + data.js (used by index.html).

Run:  python3 build_database.py
Edit the data in the Excel file afterwards and the web app will read it automatically
(when served over http) or via the "Import Excel" button.
"""
import json
import random
import string
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

OUT = Path(__file__).resolve().parent
UNIVERSITY = "University Academic Database"
EMAIL_DOMAIN = "university-edu.uz"

# ---------------------------------------------------------------- grade scale
GRADE_SCALE = [  # letter, points, min score, max score
    ("A+", 4.33, 97, 100), ("A", 4.00, 93, 96), ("A-", 3.67, 90, 92),
    ("B+", 3.33, 87, 89), ("B", 3.00, 83, 86), ("B-", 2.67, 80, 82),
    ("C+", 2.33, 77, 79), ("C", 2.00, 73, 76), ("C-", 1.67, 70, 72),
    ("D", 1.00, 60, 69), ("F", 0.00, 0, 59),
]


def letter_for(score):
    for letter, _, lo, hi in GRADE_SCALE:
        if lo <= score <= hi:
            return letter
    return "F"


TERMS = ["Spring 2025", "Fall 2025", "Spring 2026"]

# ---------------------------------------------------------------- programs & courses
# program -> (faculty, [semester1 courses, semester2 courses, semester3 courses]); each course = (code, title)
PROGRAMS = {
    "Master of Global Management": ("Faculty of Business", [
        [("TAM 530", "Data Analytics and Digital Transformation in a Global World"),
         ("TGM 586", "Global Entrepreneurship and Sustainable Business"),
         ("TAM 557", "Global Marketing in a Digital Age"),
         ("TAM 542", "Global Leadership and Personal Development"),
         ("TAM 511", "Global Accounting: Managing with Numbers")],
        [("IAL 503", "Applied International Leadership"),
         ("FIN 560", "International Finance"),
         ("TGM 551", "Global Marketing Strategy"),
         ("TAM 505", "Navigating Global and Regional Business Environments"),
         ("TGM 507", "Global Organizational Consulting")],
        [("TGM 610", "Cross-Cultural Negotiation"),
         ("TGM 622", "Global Supply Chain Management"),
         ("TAM 615", "Strategic Management in Emerging Markets"),
         ("TGM 630", "Corporate Governance and Ethics"),
         ("TGM 690", "Capstone: Global Management Project")],
    ]),
    "Bachelor of Software Engineering": ("Faculty of Computer Science", [
        [("CSE 101", "Introduction to Programming"), ("MTH 110", "Discrete Mathematics"),
         ("CSE 120", "Computer Systems Fundamentals"), ("ENG 101", "Academic English I"),
         ("MTH 120", "Calculus I")],
        [("CSE 150", "Object-Oriented Programming"), ("CSE 160", "Data Structures"),
         ("CSE 170", "Web Development Basics"), ("ENG 102", "Academic English II"),
         ("MTH 130", "Linear Algebra")],
        [("CSE 210", "Algorithms"), ("CSE 220", "Databases"),
         ("CSE 230", "Software Requirements Engineering"), ("CSE 240", "Operating Systems"),
         ("STA 201", "Probability and Statistics")],
    ]),
    "Master of Data Science": ("Faculty of Computer Science", [
        [("DSC 501", "Foundations of Data Science"), ("DSC 510", "Statistical Inference"),
         ("DSC 520", "Programming for Data Science (Python)"), ("DSC 530", "Data Management and SQL"),
         ("DSC 540", "Linear Algebra for Machine Learning")],
        [("DSC 550", "Machine Learning"), ("DSC 560", "Data Visualization"),
         ("DSC 570", "Big Data Platforms"), ("DSC 580", "Optimization Methods"),
         ("DSC 590", "Research Methods")],
        [("DSC 610", "Deep Learning"), ("DSC 620", "Natural Language Processing"),
         ("DSC 630", "Time Series Analysis"), ("DSC 640", "Data Ethics and Privacy"),
         ("DSC 690", "Capstone Project in Data Science")],
    ]),
    "Bachelor of Finance": ("Faculty of Economics & Finance", [
        [("ECO 101", "Principles of Microeconomics"), ("ACC 101", "Financial Accounting"),
         ("MTH 105", "Business Mathematics"), ("ENG 101", "Academic English I"),
         ("FIN 100", "Introduction to Finance")],
        [("ECO 102", "Principles of Macroeconomics"), ("ACC 102", "Managerial Accounting"),
         ("STA 110", "Business Statistics"), ("ENG 102", "Academic English II"),
         ("FIN 150", "Financial Markets and Institutions")],
        [("FIN 210", "Corporate Finance"), ("FIN 220", "Investments"),
         ("FIN 230", "Banking Operations"), ("ECO 210", "Econometrics I"),
         ("LAW 201", "Business Law")],
    ]),
    "Master of International Relations": ("Faculty of Social Sciences", [
        [("IRL 501", "Theories of International Relations"), ("IRL 510", "Global Political Economy"),
         ("IRL 520", "International Law"), ("IRL 530", "Research Design"),
         ("IRL 540", "Diplomacy and Statecraft")],
        [("IRL 550", "Security Studies"), ("IRL 560", "Central Asia in World Politics"),
         ("IRL 570", "International Organizations"), ("IRL 580", "Foreign Policy Analysis"),
         ("IRL 590", "Quantitative Methods")],
        [("IRL 610", "Conflict Resolution"), ("IRL 620", "Energy Geopolitics"),
         ("IRL 630", "Human Rights and Global Governance"), ("IRL 640", "Regional Integration"),
         ("IRL 690", "Master's Thesis Seminar")],
    ]),
    "Master of Business Administration": ("Faculty of Business", [
        [("MBA 501", "Managerial Economics"), ("MBA 510", "Financial Reporting and Analysis"),
         ("MBA 520", "Organizational Behavior"), ("MBA 530", "Marketing Management"),
         ("MBA 540", "Business Analytics")],
        [("MBA 550", "Corporate Finance"), ("MBA 560", "Operations Management"),
         ("MBA 570", "Strategic Human Resource Management"), ("MBA 580", "Business Ethics"),
         ("MBA 590", "Leadership and Change")],
        [("MBA 610", "Competitive Strategy"), ("MBA 620", "Entrepreneurship and Innovation"),
         ("MBA 630", "International Business"), ("MBA 640", "Negotiation"),
         ("MBA 690", "MBA Capstone Consulting Project")],
    ]),
    "Bachelor of Civil Engineering": ("Faculty of Engineering", [
        [("CIV 101", "Engineering Drawing"), ("MTH 120", "Calculus I"),
         ("PHY 101", "Physics I: Mechanics"), ("ENG 101", "Academic English I"),
         ("CHM 101", "General Chemistry")],
        [("CIV 150", "Statics"), ("MTH 140", "Calculus II"),
         ("PHY 102", "Physics II: Electricity and Magnetism"), ("ENG 102", "Academic English II"),
         ("CIV 160", "Surveying")],
        [("CIV 210", "Strength of Materials"), ("CIV 220", "Construction Materials"),
         ("CIV 230", "Fluid Mechanics"), ("MTH 210", "Differential Equations"),
         ("CIV 240", "Computer-Aided Design (CAD)")],
    ]),
    "Bachelor of Graphic Design": ("Faculty of Arts & Design", [
        [("ART 101", "Drawing Fundamentals"), ("DES 101", "Design Principles"),
         ("ART 110", "Color Theory"), ("ENG 101", "Academic English I"),
         ("HIS 101", "History of Art")],
        [("DES 150", "Typography I"), ("DES 160", "Digital Imaging"),
         ("DES 170", "Visual Communication"), ("ENG 102", "Academic English II"),
         ("ART 150", "Photography Basics")],
        [("DES 210", "Typography II"), ("DES 220", "Brand Identity Design"),
         ("DES 230", "UI/UX Design"), ("DES 240", "Motion Graphics"),
         ("DES 250", "Print Production")],
    ]),
}

ECTS_PER_COURSE = 6

# ---------------------------------------------------------------- students
# (id, name, program, gender, dob, ability)   ability = mean score for generated grades
STUDENTS = [
    ("m250251", "In'om Norqulov", "Master of Global Management", "M", "1998-03-14", None),
    ("m250268", "Alisher Juraev", "Bachelor of Software Engineering", "M", "2006-05-21", 89),
    ("m250269", "Fariza Yunusova", "Master of Business Administration", "F", "1999-11-02", 94),
    ("m250270", "Sardor Tursunov", "Master of Global Management", "M", "1997-07-09", 85),
    ("m250271", "Madina Rakhimova", "Bachelor of Finance", "F", "2006-01-30", 91),
    ("m250272", "Otabek Kalandarov", "Master of Data Science", "M", "1998-09-17", 84),
    ("m250273", "Zarina Ismoilova", "Master of International Relations", "F", "2000-04-25", 88),
    ("m250274", "Jamshidbek Mirzayev", "Bachelor of Civil Engineering", "M", "2005-12-12", 78),
    ("m250275", "Nigina Khasanova", "Bachelor of Graphic Design", "F", "2006-08-03", 95),
    ("m250276", "Bekzod Akhmedov", "Bachelor of Finance", "M", "2005-10-19", 82),
    ("m250277", "Dilshoda Matyakubova", "Master of International Relations", "F", "1999-02-08", 90),
    ("m250278", "Javohir Saidov", "Bachelor of Software Engineering", "M", "2006-06-27", 80),
]

# The record from the provided transcript, kept exactly as issued.
NORQULOV = {
    "passport": "AE5244941", "email": "inorkulov@aut-edu.uz", "issued": "2026-08-26",
    "terms": [
        ("Spring 2025", "Semester 1", [("TAM 530", "", None), ("TGM 586", "", None), ("TAM 557", "", None),
                                       ("TAM 542", "A+", 100), ("TAM 511", "", None)]),
        ("Fall 2025", "Semester 2", [("IAL 503", "B-", 82), ("FIN 560", "B", 53), ("TGM 551", "C", 74),
                                     ("TAM 505", "", None), ("TGM 507", "B+", 87)]),
    ],
}


def make_password(rng):
    alphabet = string.ascii_letters + string.digits
    return "".join(rng.choice(alphabet) for _ in range(8)) + rng.choice("!@#$%")


def build():
    rng = random.Random(2025)
    courses = {}
    for program, (_, sems) in PROGRAMS.items():
        for i, sem in enumerate(sems):
            for code, title in sem:
                courses.setdefault(code, {"code": code, "title": title, "ects": ECTS_PER_COURSE,
                                          "program": program, "semester": i + 1})

    students, grades = [], []
    for sid, name, program, gender, dob, ability in STUDENTS:
        faculty = PROGRAMS[program][0]
        level = "Master" if program.startswith("Master") else "Bachelor"
        first, last = name.replace("'", "").split(" ", 1)
        login = sid
        rec = {
            "student_id": sid, "full_name": name, "gender": gender, "date_of_birth": dob,
            "passport": "A" + rng.choice("CDE") + str(rng.randint(1000000, 9999999)),
            "phone": f"+998 9{rng.randint(0, 9)} {rng.randint(100, 999)} {rng.randint(10, 99)} {rng.randint(10, 99)}",
            "email": f"{first[0].lower()}{last.lower().replace(' ', '')}@{EMAIL_DOMAIN}",
            "login": login, "password": make_password(rng),
            "faculty": faculty, "program": program, "level": level,
            "enrollment_date": "Spring 2025", "status": "Active", "issued_date": "2026-09-15",
        }
        if sid == "m250251":
            rec.update(passport=NORQULOV["passport"], email=NORQULOV["email"], issued_date=NORQULOV["issued"])
            for term, sem, rows in NORQULOV["terms"]:
                for code, letter, score in rows:
                    grades.append({"student_id": sid, "term": term, "semester": sem, "course_code": code,
                                   "grade": letter, "score": score})
        else:
            for i, term in enumerate(TERMS):
                for code, _ in PROGRAMS[program][1][i]:
                    score = max(55, min(100, round(rng.gauss(ability, 5))))
                    grades.append({"student_id": sid, "term": term, "semester": f"Semester {i + 1}",
                                   "course_code": code, "grade": letter_for(score), "score": score})
        students.append(rec)
    return students, list(courses.values()), grades


# ---------------------------------------------------------------- Excel
HEAD_FILL = PatternFill("solid", fgColor="1F3A4D")
HEAD_FONT = Font(bold=True, color="FFFFFF")
THIN = Side(style="thin", color="D9D2C3")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def write_sheet(ws, headers, rows, widths):
    ws.append(headers)
    for row in rows:
        ws.append(row)
    for c in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=c)
        cell.fill, cell.font = HEAD_FILL, HEAD_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws.column_dimensions[get_column_letter(c)].width = widths[c - 1]
    for row in ws.iter_rows(min_row=1, max_row=ws.max_row, max_col=len(headers)):
        for cell in row:
            cell.border = BORDER
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    ws.row_dimensions[1].height = 30


def write_excel(students, courses, grades, path):
    wb = Workbook()

    ws = wb.active
    ws.title = "Students"
    s_headers = ["Student ID", "Full Name", "Gender", "Date of Birth", "Passport", "Phone", "Email",
                 "Login", "Password", "Faculty", "Program", "Level", "Enrollment Date", "Status",
                 "Transcript Issued Date"]
    s_keys = ["student_id", "full_name", "gender", "date_of_birth", "passport", "phone", "email", "login",
              "password", "faculty", "program", "level", "enrollment_date", "status", "issued_date"]
    write_sheet(ws, s_headers, [[s[k] for k in s_keys] for s in students],
                [12, 24, 8, 13, 13, 18, 28, 11, 14, 30, 36, 10, 15, 10, 15])
    dv = DataValidation(type="list", formula1='"Active,On leave,Graduated,Withdrawn"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"N2:N{max(200, len(students) + 1)}")

    wc = wb.create_sheet("Courses")
    write_sheet(wc, ["Course Code", "Course Title", "ECTS Credits", "Program", "Semester"],
                [[c["code"], c["title"], c["ects"], c["program"], c["semester"]] for c in courses],
                [13, 52, 12, 36, 10])

    wg = wb.create_sheet("Grades")
    g_headers = ["Student ID", "Student Name", "Term", "Semester", "Course Code", "Course Title", "ECTS",
                 "Grade", "Final Score", "Grade Points", "Quality Points"]
    rows = []
    for r, g in enumerate(grades, start=2):
        rows.append([
            g["student_id"], f'=IFERROR(VLOOKUP(A{r},Students!$A:$B,2,FALSE),"")', g["term"], g["semester"],
            g["course_code"], f'=IFERROR(VLOOKUP(E{r},Courses!$A:$C,2,FALSE),"")',
            f'=IFERROR(VLOOKUP(E{r},Courses!$A:$C,3,FALSE),0)', g["grade"] or None, g["score"],
            f'=IF(H{r}="","",VLOOKUP(H{r},\'Grade Scale\'!$A:$B,2,FALSE))',
            f'=IF(J{r}="",0,J{r}*G{r})',
        ])
    write_sheet(wg, g_headers, rows, [12, 24, 13, 12, 12, 50, 7, 8, 11, 12, 13])
    dvg = DataValidation(type="list", formula1="'Grade Scale'!$A$2:$A$12", allow_blank=True)
    wg.add_data_validation(dvg)
    dvg.add("H2:H2000")

    wsc = wb.create_sheet("Grade Scale")
    write_sheet(wsc, ["Letter", "Grade Points", "Min Score", "Max Score"],
                [list(x) for x in GRADE_SCALE], [10, 13, 11, 11])

    # GPA summary: semester GPA = quality points / all ECTS attempted in the term (ungraded count as 0,
    # same rule as the issued transcript); cumulative = all quality points / all ECTS attempted.
    wsum = wb.create_sheet("GPA Summary")
    headers = ["Student ID", "Student Name", "Program"]
    for t in TERMS:
        headers += [f"{t} GPA"]
    headers += ["Cumulative GPA", "ECTS Earned"]
    rows = []
    for r, s in enumerate(students, start=2):
        row = [s["student_id"], f"=VLOOKUP(A{r},Students!$A:$B,2,FALSE)", f"=VLOOKUP(A{r},Students!$A:$K,11,FALSE)"]
        for t in TERMS:
            row.append(f'=IFERROR(MIN(4,ROUND(SUMIFS(Grades!$K:$K,Grades!$A:$A,$A{r},Grades!$C:$C,"{t}")'
                       f'/SUMIFS(Grades!$G:$G,Grades!$A:$A,$A{r},Grades!$C:$C,"{t}"),2)),"")')
        row.append(f'=IFERROR(MIN(4,ROUND(SUMIFS(Grades!$K:$K,Grades!$A:$A,$A{r})'
                   f'/SUMIFS(Grades!$G:$G,Grades!$A:$A,$A{r}),2)),"")')
        row.append(f'=SUMIFS(Grades!$G:$G,Grades!$A:$A,$A{r},Grades!$H:$H,"<>",Grades!$H:$H,"<>F")')
        rows.append(row)
    write_sheet(wsum, headers, rows, [12, 24, 36, 16, 16, 16, 15, 12])

    wr = wb.create_sheet("README")
    for line in [
        UNIVERSITY,
        "",
        "Students    - one row per student (ID, passport, contacts, login/password, program, status).",
        "Courses     - course catalogue: code, title, ECTS credits.",
        "Grades      - one row per student per course. Fill in Student ID, Term, Semester, Course Code,",
        "              Grade and Final Score. Grey formula columns fill themselves.",
        "              Leave Grade empty for a course that is not graded yet (shows as '—').",
        "Grade Scale - letter -> grade points.",
        "GPA Summary - calculated automatically from the Grades sheet.",
        "",
        "GPA rule (same as the issued transcript): semester GPA = sum(grade points x ECTS) / ECTS of all",
        "courses in that term; ungraded courses count as 0; capped at 4.00. ECTS earned = credits of graded, non-F courses.",
        "",
        "Open index.html (in the same folder) to browse students and print transcripts.",
        "WARNING: this file contains passports and passwords - do not publish it on a public website.",
    ]:
        wr.append([line])
    wr.column_dimensions["A"].width = 110
    wr["A1"].font = Font(bold=True, size=14)
    wb.move_sheet("README", offset=-(len(wb.sheetnames) - 1))
    wb.active = 1
    wb.save(path)


def main():
    students, courses, grades = build()
    write_excel(students, courses, grades, OUT / "university_database.xlsx")
    data = {"university": UNIVERSITY, "terms": TERMS,
            "gradeScale": [{"letter": l, "points": p, "min": lo, "max": hi} for l, p, lo, hi in GRADE_SCALE],
            "students": students, "courses": courses, "grades": grades}
    (OUT / "data.js").write_text("window.UNIVERSITY_DATA = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n",
                                 encoding="utf-8")
    print(f"{len(students)} students, {len(courses)} courses, {len(grades)} grade records")


if __name__ == "__main__":
    main()
