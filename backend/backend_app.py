from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


def _validate_post(post: dict) -> (bool, str):
    missing_keys = []
    if "title" not in post or post["title"] == "":
        missing_keys.append("title")
    if "content" not in post or post["content"] == "":
        missing_keys.append("content")

    return len(missing_keys) == 0, ", ".join(missing_keys)


@app.route('/api/posts', methods=['POST'])
def add_post():
    new_post = request.get_json()

    is_post_valid, missing_keys = _validate_post(new_post)
    if not is_post_valid:
        return jsonify({"error": f"Missing keys: {missing_keys}"}), 400

    POSTS.append(new_post)

    return jsonify(new_post), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
