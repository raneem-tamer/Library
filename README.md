# Library Management API

## Overview
This is a RESTful API for managing a collection of books in a library.

## Features
- Add a new book
- List all books
- Search for books by author, published year, or genre
- Delete a book by ISBN
- Update book details by ISBN
- Documentation available via Swagger UI

## Setup Instructions

### Prerequisites
- Docker installed

### Running the Application

1. Build the Docker image:
   ```bash
   docker build -t library_management_api .