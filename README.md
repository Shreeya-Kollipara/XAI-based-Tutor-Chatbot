# 🎓 XAI Tutor Chatbot

<p align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?logo=streamlit)
![Llama](https://img.shields.io/badge/Llama-3.1--8B--Instant-orange)
![XAI](https://img.shields.io/badge/Explainable-AI-success)
![TF-IDF](https://img.shields.io/badge/Retrieval-TF--IDF-purple)
![License](https://img.shields.io/badge/License-MIT-green)

</p>

---

# 📖 Overview

**XAI Tutor Chatbot** is a hybrid **Explainable AI (XAI)** educational assistant designed to provide transparent, trustworthy, and interpretable responses to student queries.

Unlike conventional AI chatbots that return answers without justification, this system explains **why** an answer was generated, **which documents** influenced it, **which words contributed the most**, and **how confident** the model is in its prediction.

The project combines an **LLM-powered reasoning engine**, **interpretable TF-IDF retrieval**, and multiple **Explainable AI techniques** including **LIME**, **SHAP**, **Counterfactual Analysis**, and **Confidence Scoring** within a modular FastAPI and Streamlit architecture. :contentReference[oaicite:0]{index=0}

---

# ✨ Features

- 🤖 LLM-powered educational chatbot
- 📚 Hybrid Retrieval-Augmented Generation (RAG)
- 🔍 Interpretable TF-IDF document retrieval
- 💡 Explainable AI (XAI) pipeline
- 🧠 LIME word importance visualization
- 📊 SHAP feature contribution analysis
- 🔄 Counterfactual explanations
- 📈 Confidence scoring with reasoning breakdown
- 📜 Pipeline trace logging
- 🎯 Rule-based intent classification
- 📝 Socratic hints and quiz generation
- 🖼️ OCR support for image-based questions
- 🌐 FastAPI REST backend
- 🎨 Interactive Streamlit interface

---

# 🚀 Why XAI Tutor?

Traditional chatbots answer questions.

**XAI Tutor explains every answer.**

For every response, the chatbot shows:

✅ Why the answer was generated

✅ Which documents were retrieved

✅ Important words influencing the prediction

✅ Model confidence

✅ Alternative reasoning

✅ Learning hints

This makes the system particularly suitable for educational environments where transparency and trust are essential. :contentReference[oaicite:1]{index=1}

---

# 🏗️ High-Level Architecture

```text
                   User Query
                        │
                        ▼
              Input Processing Layer
                        │
                        ▼
              Intent Detection Layer
                        │
                        ▼
          TF-IDF Document Retrieval
                        │
                        ▼
               Decision Engine
        (Retrieve or General Answer)
                        │
                        ▼
              LLM Reasoning Engine
                        │
                        ▼
             Explainability Layer
      (LIME • SHAP • Counterfactuals)
                        │
                        ▼
          Confidence & Trace Logger
                        │
                        ▼
                Tutor Assistance
      (Hints • Simplification • Quiz)
                        │
                        ▼
              FastAPI REST Response
                        │
                        ▼
               Streamlit Frontend
```

---

# 🤖 Agentic Workflow

The chatbot follows a modular agent-based workflow where every stage is responsible for a single reasoning task.

```text
User Input
     │
     ▼
Input Processing
(Text Cleaning + OCR)
     │
     ▼
Intent Detection
     │
     ▼
Retriever Agent
(TF-IDF Search)
     │
     ▼
Decision Agent
     │
     ▼
LLM Reasoning Agent
     │
     ▼
XAI Agent
├── LIME
├── SHAP
├── Counterfactual
└── Confidence
     │
     ▼
Tutor Agent
(Hints + Quiz + Simplifier)
     │
     ▼
Frontend Response
```

---

# ⚙️ End-to-End Pipeline

```
1. User submits a question

↓

2. Input is cleaned and tokenized

↓

3. Intent Detection identifies query type

↓

4. TF-IDF retrieves the most relevant documents

↓

5. Decision engine selects retrieved context

↓

6. LLM generates a structured response

↓

7. XAI methods explain the prediction

↓

8. Tutor layer creates hints and quizzes

↓

9. FastAPI sends JSON response

↓

10. Streamlit displays explanations
```
---

# 🧠 Explainable AI (XAI) Pipeline

Unlike conventional AI systems, XAI Tutor provides transparent explanations for every prediction.

## 🔹 LIME (Local Interpretable Model-Agnostic Explanations)

LIME highlights the most influential words contributing to the generated answer.

**Provides**

- Word importance scores
- Local explanation
- Color-coded token visualization

---

## 🔹 SHAP (SHapley Additive exPlanations)

SHAP assigns contribution values to each feature based on game theory.

**Provides**

- Feature contribution scores
- Positive & negative influence
- Global interpretability

---

## 🔹 Counterfactual Analysis

Shows how the prediction changes when important words are modified or removed.

**Benefits**

- Explains decision boundaries
- Demonstrates model robustness
- Highlights influential query terms

---

## 🔹 Confidence Scoring

Confidence is computed using multiple factors including:

- Retrieval quality
- Answer completeness
- Model uncertainty

The final confidence score is categorized as:

🟢 High

🟡 Moderate

🔴 Low

---

# 🔄 Explainability Flow

```text
Generated Answer
        │
        ▼
  LIME Explanation
        │
        ▼
 SHAP Contributions
        │
        ▼
Counterfactual Analysis
        │
        ▼
Confidence Estimation
        │
        ▼
Final Explainable Response
```

---

# 💻 Technology Stack

| Category | Technology |
|-----------|------------|
| Language | Python |
| Backend | FastAPI |
| Frontend | Streamlit |
| LLM | Llama 3.1-8B-Instant |
| Retrieval | TF-IDF (scikit-learn) |
| Explainability | LIME, SHAP, Counterfactual Analysis |
| OCR | Tesseract OCR |
| Validation | Pydantic |
| HTTP Client | Requests |

---

# 📂 Project Structure

```text
xai_tutor_chatbot/

├── backend/
│   ├── app.py
│   ├── config.py
│   └── routes.py
│
├── models/
│   ├── llm.py
│   ├── retriever.py
│   └── classifier.py
│
├── xai/
│   ├── lime_explainer.py
│   ├── shap_explainer.py
│   ├── counterfactual.py
│   └── confidence.py
│
├── interpretability/
│   ├── trace_logger.py
│   └── decision_rules.py
│
├── tutor/
│   ├── hints.py
│   ├── quiz_generator.py
│   └── simplifier.py
│
├── utils/
│   ├── preprocessing.py
│   └── ocr.py
│
├── data/
│   └── documents.json
│
├── frontend/
│   └── app.py
│
├── requirements.txt
└── README.md
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/XAI-Tutor-Chatbot.git
```

Move into project

```bash
cd XAI-Tutor-Chatbot
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
API_KEY=your_api_key
MODEL_NAME=llama-3.1-8b-instant
API_URL=https://api.groq.com/openai/v1/chat/completions
```

Run the backend

```bash
uvicorn backend.app:app --reload --port 8000
```

Run the frontend

```bash
streamlit run frontend/app.py
```

Open:

```
Backend:
http://localhost:8000

API Docs:
http://localhost:8000/docs

Frontend:
http://localhost:8501
```

---

# 📡 API Endpoints

| Method | Endpoint | Description |
|----------|----------|-------------|
| POST | `/query` | Process user query |
| POST | `/upload-image` | OCR-based question answering |
| GET | `/health` | Backend health check |

---

# 📊 Output

Each response includes:

- ✅ AI-generated Answer
- ✅ Simplified Explanation
- ✅ Retrieved Evidence
- ✅ Similarity Score
- ✅ Confidence Score
- ✅ LIME Explanation
- ✅ SHAP Contributions
- ✅ Counterfactual Analysis
- ✅ Pipeline Trace
- ✅ Tutor Hints
- ✅ Quiz Questions

---
---

# 🎯 Example Workflow

### Example Query

> Explain the process of photosynthesis.

### Processing Pipeline

```text
User Query
      │
      ▼
Input Processing
      │
      ▼
Intent Detection
      │
      ▼
TF-IDF Retrieval
      │
      ▼
Relevant Documents
      │
      ▼
LLM Reasoning
      │
      ▼
LIME Explanation
      │
      ▼
SHAP Analysis
      │
      ▼
Counterfactual Generation
      │
      ▼
Confidence Calculation
      │
      ▼
Tutor Layer
      │
      ▼
Final Response
```

The final response includes:

- 📚 Answer
- 🔍 Retrieved Evidence
- 📊 Similarity Score
- 💡 LIME Explanation
- 📈 SHAP Contributions
- 🔄 Counterfactual Analysis
- 🎯 Confidence Score
- 📝 Learning Hints
- ❓ Quiz Questions

---

# 🌟 Key Highlights

- Hybrid Retrieval-Augmented Generation (RAG)
- Fully interpretable TF-IDF document retrieval
- Explainable AI-powered reasoning
- Interactive educational chatbot
- OCR support for image-based questions
- Multi-factor confidence estimation
- Modular and extensible architecture
- Transparent decision-making pipeline
- RESTful FastAPI backend
- Modern Streamlit frontend

---

# 📚 Explainability Techniques

| Technique | Purpose |
|-----------|---------|
| LIME | Identifies locally important words influencing predictions |
| SHAP | Quantifies feature contributions using Shapley values |
| Counterfactual Analysis | Explains how small input changes affect predictions |
| Confidence Scoring | Estimates reliability of generated responses |
| Pipeline Trace | Displays every stage involved in generating the answer |

---

# 🔬 Future Enhancements

- 🤖 Multi-Agent AI architecture
- 📄 PDF and document summarization
- 🎤 Voice-based question answering
- 🌍 Multilingual support
- 📹 Video lecture understanding
- 🧩 Personalized learning recommendations
- 📈 Learning analytics dashboard
- 📚 Vector database integration (FAISS/ChromaDB)
- ☁️ Cloud deployment with Docker and Kubernetes
- 📱 Mobile application support

---

# 📖 Research Motivation

Educational AI systems often function as black boxes, making it difficult for learners to understand the reasoning behind generated answers.

**XAI Tutor Chatbot** addresses this challenge by integrating interpretable retrieval techniques with Explainable AI methods, enabling students to explore not only *what* the answer is, but also *why* it was generated. The system enhances trust, transparency, and learning through visual explanations, confidence estimation, and evidence-backed reasoning.

---

# 🛠️ Built With

- Python
- FastAPI
- Streamlit
- scikit-learn
- Llama 3.1-8B-Instant
- TF-IDF Retrieval
- LIME
- SHAP
- Counterfactual Analysis
- Tesseract OCR
- Requests
- Pydantic

---


# 👩‍💻 Author

**Kollipara Naga Shreeya**

B.Tech Computer Science and Engineering (Artificial Intelligence & Machine Learning)

VIT Chennai

---

## ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.

Your support helps improve the project and encourages future development.

---

<p align="center">

### 🌟 "Making AI Transparent, Explainable, and Trustworthy for Education."

Made with ❤️ using Explainable AI

</p>
