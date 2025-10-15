# 🎬 Movie Recommendation System

A **content-based movie recommendation system** built using **Python** that recommends movies similar to a selected title based on **metadata** such as *genres, cast, crew, keywords,* and *overview*.  

This system uses **Natural Language Processing (NLP)** techniques along with **cosine similarity** to calculate relationships between movies and features an **interactive web interface built with Streamlit**.

---

## 📖 Overview

This project aims to enhance the movie discovery experience by analyzing metadata from thousands of movies and recommending similar ones based on textual and categorical features.  

It demonstrates concepts of:
- Data cleaning and preprocessing  
- Feature engineering  
- Text vectorization  
- Cosine similarity computation  
- Web app deployment with Streamlit  

---

## 📂 Dataset Details

The system uses publicly available datasets from [Kaggle TMDb 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata).

1. **tmdb_5000_movies.csv**  
   Contains details such as:
   - `id`
   - `title`
   - `overview`
   - `genres`
   - `keywords`
   - `runtime`, `budget`, `revenue`

2. **tmdb_5000_credits.csv**  
   Contains:
   - `movie_id`
   - `title`
   - `cast` (actors)
   - `crew` (directors, writers, etc.)

> Both datasets are merged using the `title` column to form a unified dataframe.

---

## ⚙️ Features

✅ **Content-Based Recommendation:**  
Finds and suggests movies with similar metadata.  

✅ **Metadata Used:**  
`overview`, `genres`, `keywords`, `cast`, `crew`.  

✅ **Text Preprocessing:**  
- Lowercasing and removing spaces  
- Tokenization  
- Stemming using `PorterStemmer` (from NLTK)  

✅ **Vectorization:**  
`CountVectorizer` from scikit-learn is used to convert text into numerical vectors.  

✅ **Similarity Computation:**  
Uses **cosine similarity** to measure movie closeness based on vectorized metadata.  

✅ **Frontend:**  
A **Streamlit-based** user interface that allows interactive selection and displays recommendations in a beautiful card layout.

---

## 🧩 Project Architecture

```
Data Collection → Data Cleaning → Feature Extraction → Text Vectorization → Similarity Calculation → Streamlit Frontend
```

**Backend (Python Scripts):**
- Data processing using Pandas and NLTK
- Model creation and pickle serialization

**Frontend (Streamlit):**
- Dropdown for movie selection
- Button to generate recommendations
- Dynamic result display using responsive columns

---

## 🛠️ Installation Guide

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/susmarika-01/Internship-Projects.git
cd Internship-Projects
git checkout movie-recommender

```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

**Dependencies include:**
```
pandas
numpy
nltk
scikit-learn
streamlit
pickle (built-in)
```

### 3️⃣ Download NLTK Data
```python
import nltk
nltk.download('punkt')
```

---

## 🏃‍♂️ How to Run

Make sure the CSV datasets and pickle files (`movies.pkl`, `movies.dict.pkl`, `similarity.pkl`) are in the same folder as your script.

### Run the Streamlit App
```bash
streamlit run app.py
```

Then open the local URL (usually http://localhost:8501) in your browser.

Use the dropdown to select your favorite movie and click **Get Recommendations**.

---

## 🔍 Example Output

The app displays **5 recommended movies** in a clean, card-style layout.

**Example:**
> Selected Movie: *Avatar*

**Output:**
- Guardians of the Galaxy  
- Aliens  
- Star Wars: Episode IV - A New Hope  
- Avatar: The Way of Water  
- Star Trek Into Darkness

---

## 💾 Model Saving with Pickle

During preprocessing, the system saves the processed dataframe and similarity matrix for faster loading:

```python
pickle.dump(new_df, open("movies.pkl", "wb"))
pickle.dump(new_df.to_dict(), open("movies.dict.pkl", "wb"))
pickle.dump(similarity, open("similarity.pkl", "wb"))
```

**Pickle Files:**
- `movies.pkl` – Processed dataframe  
- `movies.dict.pkl` – Dictionary format for easier loading  
- `similarity.pkl` – Precomputed cosine similarity matrix  

---

## 🧠 How It Works — Step-by-Step

1. **Merge Datasets** (`movies` + `credits`)  
2. **Select Features:** `overview`, `genres`, `keywords`, `cast`, `crew`  
3. **Preprocess Text:** clean, lowercase, tokenize, and stem words  
4. **Combine Features:** create a single `tags` column  
5. **Vectorize Text:** use `CountVectorizer` (Bag of Words model)  
6. **Compute Cosine Similarity:** find movie-to-movie distance  
7. **Recommend Top 5:** movies with highest similarity scores  

---

## 🧰 Tools and Libraries

- 🧮 **Data Handling:** Pandas, NumPy  
- 🗣️ **Natural Language Processing:** NLTK  
- 🤖 **Machine Learning:** Scikit-learn  
- 🌐 **Frontend Framework:** Streamlit  
- 💾 **Data Serialization:** Pickle  

---

## 📂 Project Structure

```
movie-recommendation-system/
├── tmdb_5000_movies.csv
├── tmdb_5000_credits.csv
├── movies.pkl
├── movies.dict.pkl
├── similarity.pkl
├── app.py
├── main.ipynb
├── requirements.txt
└── README.md
```

---

## 🖥️ Example UI

> 🎨 Built with Streamlit for simplicity and modern design.

The interface includes:
- Gradient header with title and subtitle  
- Dropdown list to select movie  
- Animated “Get Recommendations” button  
- Recommended movies shown in responsive cards  

  
---

## 📈 Performance Notes

- Efficient preprocessing and vectorization enable sub-second recommendations.  
- Uses pre-saved pickle files for faster load times.  
- Optimized sorting using Python’s built-in functions.

---

