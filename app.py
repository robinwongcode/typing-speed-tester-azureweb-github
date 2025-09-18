from flask import Flask, render_template, request, jsonify
import requests
import time
import re

app = Flask(__name__)


def get_random_quote():
    """Fetch a random quote from the Quotable API"""
    try:
        response = requests.get("https://api.quotable.io/random")
        response.raise_for_status()
        data = response.json()
        return data["content"], data["author"]
    except requests.RequestException:
        # Fallback quotes if API is unavailable
        fallback_quotes = [
            ("The quick brown fox jumps over the lazy dog.", "Anonymous"),
            ("Programming isn't about what you know; it's about what you can figure out.", "Chris Pine"),
            ("The best way to predict the future is to invent it.", "Alan Kay")
        ]
        import random
        return random.choice(fallback_quotes)


def calculate_typing_stats(original_text, typed_text, time_taken):
    """Calculate WPM, accuracy, and other statistics"""
    # Calculate words per minute (WPM)
    word_count = len(original_text.split())
    wpm = (word_count / time_taken) * 60 if time_taken > 0 else 0

    # Calculate accuracy
    original_words = original_text.split()
    typed_words = typed_text.split()

    correct_chars = 0
    total_chars = len(original_text)

    for i in range(min(len(original_text), len(typed_text))):
        if original_text[i] == typed_text[i]:
            correct_chars += 1

    accuracy = (correct_chars / total_chars) * 100 if total_chars > 0 else 0

    return {
        "wpm": round(wpm, 2),
        "accuracy": round(accuracy, 2),
        "time_taken": round(time_taken, 2)
    }


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_quote')
def get_quote():
    quote, author = get_random_quote()
    return jsonify({"quote": quote, "author": author})


@app.route('/check_results', methods=['POST'])
def check_results():
    data = request.json
    original_text = data.get('original_text', '')
    typed_text = data.get('typed_text', '')
    time_taken = data.get('time_taken', 0)

    stats = calculate_typing_stats(original_text, typed_text, time_taken)
    return jsonify(stats)


if __name__ == '__main__':
    app.run(debug=True)