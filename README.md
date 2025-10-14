# 🎬 Movie Recommendation System

A **content-based movie recommendation system** built in Python that recommends movies similar to a selected title using **movie metadata** such as genres, cast, crew, keywords, and overview.  

This project uses **Natural Language Processing (NLP)** techniques along with **cosine similarity** to calculate movie similarity, and it includes an **interactive Streamlit web interface**.

## 📂 Dataset

This project uses two datasets from [TMDb](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata):

1. **tmdb_5000_movies.csv** – contains information about movies like `title`, `overview`, `genres`, `keywords`, etc.  
2. **tmdb_5000_credits.csv** – contains information about movie `cast` and `crew`.  

> Both datasets are combined using the `title` column.

## ⚙️ Features

- **Content-based Recommendation:** Suggests movies similar to the selected movie.  
- **Metadata Used:** `overview`, `genres`, `keywords`, `cast`, `crew`  
- **Text Preprocessing:** Lowercasing, removing spaces, and stemming using NLTK  
- **Vectorization:** `CountVectorizer` from scikit-learn  
- **Similarity Calculation:** Cosine similarity between movies  
- **Interactive Frontend:** Streamlit interface for selecting movies and viewing recommendations

## 🛠️ Installation

1. Clone the repository:
```bash
git clone <your-repo-link>
cd movie-recommendation-system

2. Install dependencies:
pip install -r requirements.txt
Dependencies include: pandas, numpy, nltk, scikit-learn, streamlit, pickle (built-in)

3. Download NLTK data:
import nltk
nltk.download('punkt')

## How to Run
Make sure the CSV datasets and pickle files are in the same folder as the script.
Run the Streamlit app:
streamlit run app.py
Use the dropdown to select your favorite movie and click Get Recommendations to see similar movies.

🔍 Example Output
The app displays 5 recommended movies in a responsive card layout.
For example, selecting "Avatar" may return:
Guardians of the Galaxy
Aliens
Star Wars: Episode IV - A New Hope
Avatar: The Way of Water
Star Trek Into Darkness




