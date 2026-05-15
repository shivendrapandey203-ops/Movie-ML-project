from flask import Flask, jsonify
from flask_cors import CORS
import pickle
import numpy as np
from model import MovieRecommender
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Load model
recommender = MovieRecommender()
recommender.load_data()

# Load saved models if they exist
try:
    with open('vectorizer.pkl', 'rb') as f:
        recommender.tfidf = pickle.load(f)
    with open('similarity.pkl', 'rb') as f:
        recommender.similarity = pickle.load(f)
    print("Loaded saved models")
except:
    recommender.build_model()
    print("Built new models")

@app.route('/similar/<movie_title>')
def similar_movies(movie_title):
    try:
        recommendations = recommender.recommend_similar_movies(movie_title)
        return jsonify({
            'success': True,
            'movies': recommendations,
            'query': movie_title
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/mood/<mood>')
def mood_movies(mood):
    try:
        recommendations = recommender.recommend_movies_by_mood(mood)
        return jsonify({
            'success': True,
            'movies': recommendations,
            'mood': mood
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/genre/<genre>')
def genre_movies(genre):
    try:
        recommendations = recommender.recommend_movies_by_genre(genre)
        return jsonify({
            'success': True,
            'movies': recommendations,
            'genre': genre
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/random')
def random_movies():
    try:
        recommendations = recommender.random_recommendation()
        return jsonify({
            'success': True,
            'movies': recommendations
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/search/<query>')
def search_movies(query):
    try:
        results = recommender.search_movies(query)
        return jsonify({
            'success': True,
            'movies': results,
            'query': query
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)