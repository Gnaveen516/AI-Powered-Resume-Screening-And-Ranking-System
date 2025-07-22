# AI Resume Screening & Ranking System

![Resume Screening Banner](https://media.istockphoto.com/id/157307281/photo/magnifying-glass-on-resume.jpg?s=612x612&w=0&k=20&c=4GOxsmLgRc-TkdGTp3sSUwo-JronCIXg0Doj5P8Jwxw=)

## 🚀 Overview
A powerful, AI-driven web application for automated resume screening and ranking. Upload multiple resumes and instantly see how well each matches a job description, with smart keyword extraction, technical/industry skill matching, and beautiful, color-coded scoring.

---

## ✨ Features
- **AI-Powered Keyword Extraction:** Extracts technical, industry, and soft skills from job descriptions using NLP and fuzzy matching.
- **Smart Resume Parsing:** Reads and analyzes PDF resumes, focusing on relevant sections.
- **Comprehensive Skill Matching:** Compares job description keywords with all words in each resume for maximum accuracy.
- **Color-Coded Ranking:** Visual progress bars and color indicators (red/orange/green) for instant match quality feedback.
- **Tailored Suggestions:** Shows missing keywords and suggests where to improve each resume.
- **Modern Streamlit UI:** Fast, interactive, and easy to use.

---

## 🛠️ Tech Stack
- **Python 3.11+**
- **Streamlit** (UI)
- **PyPDF2** (PDF parsing)
- **spaCy** (NLP)
- **NLTK** (WordNet for synonyms)
- **yake** (optional keyword extraction)

---

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/resume_screening_and_ranking_system.git
   cd resume_screening_and_ranking_system
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Download spaCy model:**
   ```bash
   python -m spacy download en_core_web_sm
   ```
4. **(Optional) Download NLTK data:**
   ```bash
   python -m nltk.downloader wordnet stopwords punkt
   ```

---

## 🚦 Usage

1. **Start the app:**
   ```bash
   streamlit run app.py
   ```
2. **Enter a job description** in the text area.
3. **Upload one or more PDF resumes.**
4. **View ranked results** with color-coded match percentages, matched/missing keywords, and improvement suggestions.

---

## 🎨 Screenshots

![screenshot](https://user-images.githubusercontent.com/674621/146651003-2e7b4e7e-8b7e-4e7e-8b7e-2e7b4e7e8b7e.png)

---

## 🤖 How It Works
- **Keyword Extraction:** Uses NLP and fuzzy matching to extract all relevant skills and industry terms from the job description.
- **Resume Parsing:** Extracts text from PDFs and compares every keyword with all words in the resume.
- **Scoring:** Calculates a match percentage and displays it with a color-coded progress bar.
- **Suggestions:** Lists missing keywords and where to add them for a better match.

---

## 📝 Customization
- Expand the `TECHNICAL_SKILLS`, `IT_INDUSTRY_KEYWORDS`, and `SOFT_SKILLS` lists in `app.py` for your domain.
- Adjust color thresholds or UI in the Streamlit code as desired.

---

## 📄 License
MIT License. See [LICENSE](LICENSE) for details.

---

## 🙌 Contributions
Pull requests and suggestions are welcome! Please open an issue or PR to discuss improvements.

---

## 💡 Credits
- [Streamlit](https://streamlit.io/)
- [spaCy](https://spacy.io/)
- [NLTK](https://www.nltk.org/)
- [PyPDF2](https://pypdf2.readthedocs.io/)
- [yake](https://github.com/LIAAD/yake)

---

