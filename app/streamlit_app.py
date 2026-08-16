import streamlit as st
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.title("Job Recommendation Engine")
st.write("Enter your skills and get matching job postings.")

# --- Moved OUTSIDE load_data, so they're just normal top-level functions ---
def extract_words(title):
    title = str(title).lower()
    title = re.sub(r'[^a-z\s]', ' ', title)
    return title.split()

stopwords = {'for','in','a','the','and','to','of','on','with','is','an','at','by','&','you','your'}

def clean_words(words):
    return [w for w in words if w not in stopwords and len(w) > 2]

@st.cache_data
def load_data():
    df = pd.read_csv('../data/cleaned_jobs.csv')
    df['title_clean_text'] = df['title'].apply(lambda t: ' '.join(clean_words(extract_words(t))))
    vectorizer = TfidfVectorizer(max_features=5000)
    tfidf_matrix = vectorizer.fit_transform(df['title_clean_text'])
    return df, vectorizer, tfidf_matrix

df, vectorizer, tfidf_matrix = load_data()

def recommend_jobs(user_skills, top_n=10):
    cleaned = clean_words(extract_words(user_skills))
    user_text = ' '.join(cleaned)
    user_vector = vectorizer.transform([user_text])
    similarities = cosine_similarity(user_vector, tfidf_matrix).flatten()
    top_indices = similarities.argsort()[-top_n:][::-1]
    results = df.iloc[top_indices][['title', 'is_hourly', 'avg_hourly_rate', 'budget', 'country']].copy()
    results['match_score'] = similarities[top_indices]
    return results

skills_input = st.text_input("Your skills:", placeholder="e.g. python data analysis")

if st.button("Search") and skills_input:
    results = recommend_jobs(skills_input)
    st.write(f"Top {len(results)} matches:")
    for _, row in results.iterrows():
        rate_info = f"Hourly: ${row['avg_hourly_rate']}" if row['is_hourly'] else f"Budget: ${row['budget']}"
        st.markdown(f"**{row['title']}** — {rate_info} — {row['country']} (score: {row['match_score']:.3f})")