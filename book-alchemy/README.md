# Book Alchemy

A simple library management web application with the following features:

- Searching for stored books by title
- Sorting displayed books by title or author in ascending or descending order
- Removing stored books

## Tech Stack:

- Flask
- Jinja2 templates
- SQLAlchemy
- SQLite

## Setup

1. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   
2. **Run the app**:
   ```bash
   python app.py
   
Navigate to the http://localhost:5002.

**Note**: Sometimes the ports may be occupied. In that case, change the port parameter value in the `app.run` method in the file: `app.py`.