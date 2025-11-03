# Intent Classification System

## Overview
This project is an **Intent Classification System** designed to predict the intent of user queries in real-time. It combines **Natural Language Processing (NLP)** techniques with machine learning to classify text input into predefined intents. The system uses **spaCy** for text embeddings, a **Support Vector Machine (SVM)** for classification, and **Streamlit** for a user-friendly front-end interface.

---

## Features
- Predicts user intent from natural language queries.
- Provides **confidence scores** for each prediction.
- Interactive frontend using **Streamlit** for real-time input.
- Full pipeline: data preprocessing, embedding, model training, evaluation, and deployment.
- Handles multiple intents and unknown queries using a confidence threshold.

---

## Technologies Used
- **Python** – Core programming language.
- **pandas** – Data manipulation and preprocessing.
- **spaCy** – NLP library for text embeddings.
- **Sentence-Transformers** – Optional for advanced contextual embeddings.
- **scikit-learn** – Machine learning library for SVM and evaluation.
- **Streamlit** – Frontend framework for interactive UI.
- **pickle** – Save and load trained models and label encoders.

