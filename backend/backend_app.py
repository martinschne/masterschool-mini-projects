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

    # attach id to the new post
    new_post_id = max([post['id'] for post in POSTS], default=0) + 1
    new_post["id"] = new_post_id

    POSTS.append(new_post)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    global POSTS

    deleted_post = next((post for post in POSTS if post["id"] == id), None)

    if deleted_post is None:
        return jsonify({"error": "Post Not Found"}), 404

    POSTS = [post for post in POSTS if post["id"] != deleted_post["id"]]

    return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
