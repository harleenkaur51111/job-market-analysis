from flask import Flask, request, jsonify
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# --- Load and prepare data once, when the server starts ---
df = pd.read_csv('../data/cleaned_jobs.csv')

def extract_words(title):
    title = str(title).lower()
    title = re.sub(r'[^a-z\s]', ' ', title)
    return title.split()

stopwords = {'for','in','a','the','and','to','of','on','with','is','an','at','by','&','you','your'}

def clean_words(words):
    return [w for w in words if w not in stopwords and len(w) > 2]

df['title_clean_text'] = df['title'].apply(lambda t: ' '.join(clean_words(extract_words(t))))

vectorizer = TfidfVectorizer(max_features=5000)
tfidf_matrix = vectorizer.fit_transform(df['title_clean_text'])

# --- The recommendation logic, same as in the notebook ---
def recommend_jobs(user_skills, top_n=10):
    cleaned = clean_words(extract_words(user_skills))
    user_text = ' '.join(cleaned)
    user_vector = vectorizer.transform([user_text])
    similarities = cosine_similarity(user_vector, tfidf_matrix).flatten()
    top_indices = similarities.argsort()[-top_n:][::-1]
    results = df.iloc[top_indices][['title', 'is_hourly', 'avg_hourly_rate', 'budget', 'country']].copy()
    results['match_score'] = similarities[top_indices]
    return results

# --- API endpoint ---
@app.route('/recommend', methods=['GET'])
def recommend():
    skills = request.args.get('skills', '')
    if not skills:
        return jsonify({'error': 'Please provide a skills parameter, e.g. /recommend?skills=python+developer'}), 400
    top_n = int(request.args.get('top_n', 10))
    results = recommend_jobs(skills, top_n)
    return jsonify(results.to_dict(orient='records'))

if __name__ == '__main__':
   app.run(host='0.0.0.0', debug=True, port=5000)