from flask import Flask, jsonify, request, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
import os
import json

app = Flask(__name__)

# Data file configuration
DATA_FILE = 'data.json'

# Function to load data from data.json
def load_books():
    if not os.path.exists(DATA_FILE):  # Ensure file exists
        with open(DATA_FILE, 'w') as file:
            json.dump([], file)
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

# Function to save data to data.json
def save_books(books):
    with open(DATA_FILE, 'w') as file:
        json.dump(books, file, indent=2)

# Swagger Configuration
SWAGGER_URL = '/api-docs'
API_URL = '/static/swagger.json'  
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Library Management API"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/')
def index():
    return "Hello, World!"

# API Endpoints
@app.route('/books', methods=['POST'])
def add_books():
    books_to_add = request.json  # Expecting a list of books
    books = load_books()
    if isinstance(books_to_add, list):
        books.extend(books_to_add)
        save_books(books)
        return jsonify(books_to_add), 201
    else:
        return jsonify({"error": "Invalid input, expected a list of books"}), 400

@app.route('/books', methods=['GET'])
def list_books():
    books = load_books()
    return jsonify(books)

@app.route('/books/search', methods=['GET'])
def search_books():
    author = request.args.get('author')
    year = request.args.get('year')
    genre = request.args.get('genre')
    books = load_books()
    results = [book for book in books if (
        (author is None or book.get('Author') == author) and
        (year is None or str(book.get('Published Year')) == year) and
        (genre is None or book.get('Genre') == genre)
    )]
    return jsonify(results)

@app.route('/books/<string:isbn>', methods=['DELETE'])
def delete_book(isbn):
    books = load_books()
    updated_books = [book for book in books if book.get('ISBN') != isbn]
    if len(updated_books) == len(books):
        return jsonify({"error": "Book not found"}), 404
    save_books(updated_books)
    return jsonify({"message": f"Book with ISBN {isbn} deleted successfully"}), 204

@app.route('/books/<string:isbn>', methods=['PUT'])
def update_book(isbn):
    book_data = request.json
    books = load_books()
    for book in books:
        if book.get('ISBN') == isbn:
            book.update(book_data)
            save_books(books)
            return jsonify(book), 200
    return jsonify({"error": "Book not found"}), 404  

@app.route('/static/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
