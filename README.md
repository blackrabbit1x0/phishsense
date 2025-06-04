
# 🛡️ PhishSense: AI-Powered Phishing Email Detector

A sleek and smart desktop application to detect phishing emails using AI and deep learning, with an intuitive GUI and modern features.

---

## 🚀 Features

- 🧠 **AI-Based Analysis** using DistilBERT (via Hugging Face Transformers)
- 🖥️ **Modern GUI** built with `CustomTkinter`
- 📁 Support for both **.eml file uploads** and **direct text input**
- 🌗 **Light/Dark Mode** toggle
- 📊 **Confidence Scores** and **Risk Levels** displayed visually
- 💬 **Detailed Recommendations** per analysis
- 🕓 **History Tracking** of all analyses
- 📤 **Export Results** to text files
- 🧩 Clean and modular code structure for easy maintenance

---

## 🛠️ Tech Stack

| Component        | Tech / Library                      |
|------------------|--------------------------------------|
| Language         | Python 3.8+                          |
| GUI Framework    | CustomTkinter                        |
| AI Model         | DistilBERT via Hugging Face Transformers |
| File Parser      | email.parser, os, re, and pathlib    |
| Frontend Assets  | TailwindCSS, Vite, TypeScript (for extra UI work) |

---

## 📦 Installation

1. **Clone the repository:**

   ```bash
   git clone (https://github.com/blackrabbit1x0/phishsense.git)
   cd project
   ```

2. **Set up your Python environment:**

   Make sure you're using Python 3.8 or later.

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ How to Use

1. **Run the application:**

   ```bash
   python main.py
   ```

2. **Using the App:**
   - Choose between Light or Dark mode 🌗
   - Paste email content **or** upload an `.eml` file
   - Click **"Analyze"** to see phishing results
   - View **Confidence Score**, **Risk Level**, and detailed **AI-backed feedback**
   - Export results to `.txt` and view history

---

## 📂 Project Structure

```
project/
│
├── main.py               # App launcher and event controller
├── custom_gui.py         # GUI built with CustomTkinter
├── predict.py            # Model loading and prediction logic
├── parser_util.py        # Utilities for handling .eml and text parsing
├── requirements.txt      # Python dependencies
├── src/                  # Frontend assets (TypeScript + Tailwind)
│   └── App.tsx, etc.     
└── README.md             # You're reading it!
```

---

## 🤖 AI Model Details

- **Model**: `distilbert-base-uncased`
- **Task**: Text Classification
- **Platform**: Hugging Face Transformers

---

## 📝 License

This project is licensed under the MIT License.  
Feel free to use, improve, and share! 🌍

---

## 📧 Contact

For feedback, suggestions, or collaboration:  
**Suyash Shrestha**  
📧 `xuyash55@gmail.com`  

---

> “Stay safe. Stay smart. Detect phishing before it strikes.” 🧠⚠️
