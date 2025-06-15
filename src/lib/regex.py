import fitz
import re
from models.search import WorkExperienceEntry, EducationEntry

keywordsRandomSection = [
    "Accomplishment",
    "Accomplishments",
    "Activities and Honors",
    "Personal Information",
    "Languages",
    "Credentials",
    "Certifications",
    "Professional Affiliations",
    "Presentation"
]

keywordsSumSection = [
    "Summary",
    "Overview",
    "Executive Profile",
    "Professional Summary",
    "Career Focus",
    "Career Overview",
    "Objective",
    "Profile",
    "Executive Summary",
    "ABOUT",
    "Professional Profile",
    "Professional Overview",
    "Career Objective",
    "Interest"
]

keywordsJobSection = [
    "Experience",
    "Professional Experience",
    "Work Experience",
    "Work History",
    "Corporate Experience"
]

keywordsSkillSection = [
    "Skills",
    "Skills:",
    "Software Skills",
    "Highlights",
    "Skill Areas",
    "Skill Highlights",
    "Core Competencies",
    "Technical Skills",
    "Key Skills",
    "Expertise",
    "Summary of Skills",
    "Core Qualifications"
]

keywordsEduSection = [
    "Education",
    "Educations",
    "Education and Training",
    "Educational Background",
    "Specialized Training",
    "Professional Courses and Certifications"
]

keywordsSection = keywordsRandomSection + keywordsSumSection + keywordsJobSection + keywordsSkillSection + keywordsEduSection

# Ekstraksi seluruh teks pada file .pdf, mengembalikan dalam bentuk string
def pdfToString(filepath):
    pdf = fitz.open(filepath)
    text = ""
    for page in pdf:
        text += page.get_text()

    return text

# Membuat regex dari list of keywords
def createRegex(keywords):
    escapeKeywords = "|".join([re.escape(keyword) for keyword in keywords])
    result = f"^(?:{escapeKeywords})$"
    return result

# Mengembalikan string panjang, "" jika tidak memiliki summary (ada sekitar 70/600 cv yang gapunya summary)
def extractSummary(pathfile, keywordsSummary=keywordsSumSection, keywordsSection=keywordsSection):
    text = pdfToString(pathfile)
    patternSummary = re.compile(createRegex(keywordsSummary))
    patternSection = re.compile(createRegex(keywordsSection))

    startIdx = -1
    endIdx = -1
    inSection = False

    lines = text.split('\n')
    for i, line in enumerate(lines):
        if patternSummary.match(line) and not inSection:
            startIdx = i + 1
            inSection = True
        elif patternSection.match(line) and inSection:
            endIdx = i - 1
            break
    
    result = " ".join(lines[startIdx:endIdx + 1])
    return result

# Mengembalikan list[WorkExperienceEntry], harusnya tinggal di print setiap element dari listnya
def extractJob(pathfile, keywordsJob=keywordsJobSection, keywordsSection=keywordsSection):
    text = pdfToString(pathfile)
    patternJob = re.compile(createRegex(keywordsJob))
    patternSection = re.compile(createRegex(keywordsSection))
    patternTitle = r'^(?:(?:\b[A-Z][a-zA-Z]*\b|\b(?:at|to|in|of|for)\b)|[\/,&â€“ï¼\-]|\s+)+$'
    patterYear = r'\b(19\d{2}|20\d{2})\b'

    jobs = []
    jobsAsEntry = []
    inSection = False

    lines = text.split('\n')
    for line in lines:
        cleanedLine = line.strip().replace('\u200b', '')
        if not cleanedLine:
            continue

        if inSection:
            if patternSection.match(cleanedLine):
                break

            isTitle = re.fullmatch(patternTitle, cleanedLine)
            containYear = re.search(patterYear, cleanedLine)

            if isTitle or containYear:
                jobs.append(cleanedLine)
                entry = WorkExperienceEntry(
                    position=cleanedLine,
                    company="",
                    start_date="",
                    end_date="",
                    description=""
                )
                jobsAsEntry.append(entry)
        
        elif patternJob.match(cleanedLine):
            inSection = True
            
    return jobsAsEntry

# Mengembalikan list[EducationEntry], harusnya tinggal di print setiap element dari listnya
def extractEdu(pathfile, keywordsEdu=keywordsEduSection, keywordsSection=keywordsSection):
    text = pdfToString(pathfile)
    patternEdu = re.compile(createRegex(keywordsEdu))
    patternSection = re.compile(createRegex(keywordsSection))

    edus = []
    edusAsEntry = []
    inSection = False

    lines = text.split('\n')
    for line in lines:
        cleanedLine = line.strip().replace('\u200b', '')
        if not cleanedLine:
            continue

        if inSection:
            if patternSection.match(cleanedLine):
                break
            edus.append(cleanedLine)
            entry = EducationEntry(
                institution=cleanedLine,
                program="",
                start_date="",
                end_date=""
            )
            edusAsEntry.append(entry)
        
        elif patternEdu.match(cleanedLine):
            inSection = True
            
    return edusAsEntry

# Mengembalikan list[str], harusnya tinggal di print setiap element dari listnya
def extractSkill(pathfile, keywordsSkill=keywordsSkillSection, keywordsSection=keywordsSection):
    text = pdfToString(pathfile)
    patternSkill = re.compile(createRegex(keywordsSkill))
    patternSection = re.compile(createRegex(keywordsSection))

    skills = []
    inSection = False

    lines = text.split('\n')
    for line in lines:
        cleanedLine = line.strip().replace('\u200b', '')
        if not cleanedLine:
            continue

        if inSection:
            if patternSection.match(cleanedLine):
                break
            skills.append(cleanedLine)
        
        elif patternSkill.match(cleanedLine):
            inSection = True

    return skills


# for i in range(1, 11):
#     pathf = "../../dataset/" + seed.fileTerpilih[i]
#     res = extractSummary(pdfToString(pathf))
#     if len(res) < 1:
#         print(f"{pathf} : {len(res)}")

#     print("file:", pathf)
#     print(res)
#     # for item in res:
#     #     print("*", item)
#     print("=============================================")