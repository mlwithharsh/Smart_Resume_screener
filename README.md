##  Smart Resume Screener

A **real-world NLP project** that uses **semantic similarity**, **keyword matching**, and **experience extraction** to evaluate resumes against job descriptions and generate a match score.

##  Features

* 📄 Upload a resume in **PDF format**
* 🧾 Paste a job description (JD)
* ⚙️ Automatic skill extraction and comparison
* 🔍 **Semantic similarity** analysis using **SBERT (all-MiniLM-L6-v2)**
* 🧠 Keyword matching from predefined skill set
* 📅 Extract **years of experience** from resume
* ✅ Final score based on weighted metrics:

  * Semantic Similarity (60%)
  * Keyword Match (30%)
  * Experience Score (10%)

##  Sample Output

```
📊 Semantic Similarity: 0.71
📄 Keyword Match: 1.0
📅 Experience: 4 years
🎯 Final Resume Match Score: 82.6 %
✅ Match Level: Strong
```

---

##  Tech Stack

* `Python`
* `Streamlit`
* `sentence-transformers`
* `scikit-learn`
* `PyMuPDF` (for PDF text extraction)

## 📁 Project Structure

```
├── app.py                  # Streamlit web app
├── Smart Resume Screener.py   # Main logic (modular functions)
├── Harsh Sharma-CV2.pdf   # Sample resume
├── requirements.txt       # Python dependencies
```

##  Installation & Usage

```bash
# Clone the repository
git clone https://github.com/mlwithharsh/smart-resume-screener.git
cd smart-resume-screener

# Create virtual env (optional but recommended)
python -m venv env
source env/bin/activate  # or env\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---

## 🌐 Deployment

You can deploy this project on:

* **Streamlit Cloud** (Free & easy)
* **Render / HuggingFace Spaces**
* **Heroku / Azure / GCP / AWS**

Need help deploying? Ask for a deployment guide 😄

---

## 📌 TODO / Enhancements

* 📤 Allow multiple resumes for batch scoring
* 📈 Generate visual analytics dashboard
* 📝 Add resume formatting suggestions based on score
* 🧠 Integrate GPT-based suggestions for resume improvement

---

##  Author

**Harsh Sharma**
GitHub: [mlwithharsh](https://github.com/mlwithharsh)

If you like this project, please ⭐ the repo!

---

##  License

This project is licensed under the [MIT License](LICENSE).
