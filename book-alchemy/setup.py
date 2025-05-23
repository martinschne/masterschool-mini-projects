from app import app, db

# Run this once to initiate the db scheme.
# NOTE: in this project it was already initiated.
with app.app_context():
    db.create_all()