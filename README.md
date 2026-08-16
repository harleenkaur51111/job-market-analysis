# Job Market Analysis and Recommendation System

A data analysis and recommendation system built on ~245K Upwork job postings (Feb 7 - Mar 24, 2024), covering keyword-salary correlation, emerging job categories, demand forecasting, country rate comparison, a content-based recommendation engine, and market trend tracking.

## Project Structure
job_market_project/
├── app/
│ ├── app.py # Flask REST API (recommendation engine)
│ ├── streamlit_app.py # Interactive UI for job recommendations
│ ├── dashboard.py # Market dynamics dashboard
│ └── requirements.txt
├── data/
│ └── cleaned_jobs.csv
├── reports/ # Saved charts/visualizations
├── 01_data_cleaning.ipynb # Full analysis notebook (Tasks 1-8)
├── Dockerfile
└── docker-compose.yml

## Running with Docker (recommended)

Build and start the API:
docker-compose up
The API will be available at `http://localhost:5000/recommend?skills=your+skills+here`

To stop:
Ctrl+C, then: docker-compose down

## Running Locally (without Docker)

Install dependencies:
cd app
pip install -r requirements.txt


Run the API:

python app.py


Run the interactive recommendation UI:

streamlit run streamlit_app.py


Run the market dashboard:

streamlit run dashboard.py


## API Documentation

### `GET /recommend`
Returns job postings matching the given skills, ranked by relevance.

**Query Parameters:**
- `skills` (required) — space-separated skills/keywords, e.g. `python data analysis`
- `top_n` (optional, default 10) — number of results to return

**Example:**

GET /recommend?skills=python+developer&top_n=5


**Example Response:**
```json
[
  {
    "title": "Python Developer",
    "is_hourly": true,
    "avg_hourly_rate": 25.0,
    "budget": null,
    "country": "Germany",
    "match_score": 0.94
  }
]
```

## Notes on Data Limitations
- Dataset covers ~6 weeks, not multiple months — trend analyses (Tasks 6, 8) are labeled accordingly.
- Hourly rate values show clustering around preset $2.50 bands, suggesting many postings use platform-suggested rate ranges rather than custom values (see Task 4 notebook section).
- Remote-work analysis (Task 7) is based on explicit title keyword matching only, not comprehensive remote-work classification.

