# 🎬 Movie Recommendation System

A **content-based movie recommendation system** built in Python that recommends movies similar to a selected title using **movie metadata** such as genres, cast, crew, keywords, and overview. This project uses **Natural Language Processing (NLP)** techniques along with **cosine similarity** to calculate movie similarity, and it includes an **interactive Streamlit web interface**.

## 📂 Dataset

This project uses two datasets from [TMDb](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata):

1. **tmdb_5000_movies.csv** – contains information about movies like `title`, `overview`, `genres`, `keywords`, etc.  
2. **tmdb_5000_credits.csv** – contains information about movie `cast` and `crew`.  

> Both datasets are combined using the `title` column.

## ⚙️ Features

- **Content-based Recommendation:** Suggests movies similar to the selected movie  
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
````

2. Install dependencies:

```bash
pip install -r requirements.txt
```

Dependencies include: `pandas`, `numpy`, `nltk`, `scikit-learn`, `streamlit`, `pickle` (built-in)

3. Download NLTK data:

```python
import nltk
nltk.download('punkt')
```

## 🏃‍♂️ How to Run

1. Make sure the CSV datasets and pickle files are in the same folder as the script
2. Run the Streamlit app:

```bash
streamlit run app.py
```

3. Use the dropdown to select your favorite movie and click **Get Recommendations** to see similar movies

## 🔍 Example Output

The app displays **5 recommended movies** in a responsive card layout.

For example, selecting `"Avatar"` may return:

* Guardians of the Galaxy
* Aliens
* Star Wars: Episode IV - A New Hope
* Avatar: The Way of Water
* Star Trek Into Darkness

## 💾 Saving Models

Processed data and similarity matrix are saved using `pickle`:

```python
pickle.dump(new_df, open("movies.pkl", "wb"))
pickle.dump(new_df.to_dict(), open("movies.dict.pkl", "wb"))
pickle.dump(similarity, open("similarity.pkl", "wb"))
```

## 🧠 How It Works

1. Merge movies and credits datasets
2. Clean and preprocess metadata (`genres`, `keywords`, `cast`, `crew`, `overview`)
3. Combine features into a single `tags` column
4. Apply stemming and convert text to lowercase
5. Vectorize using `CountVectorizer`
6. Compute cosine similarity between movies
7. Recommend top 5 movies based on similarity

## 📂 Project Structure

```
├── tmdb_5000_movies.csv
├── tmdb_5000_credits.csv
├── movies.pkl
├── movies.dict.pkl
├── similarity.pkl
├── app.py
├── README.md
└── requirements.txt
```
