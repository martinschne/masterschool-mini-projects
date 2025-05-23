import logging

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

ALLOWED_SORTING_KEYS = ["title", "content"]
ALLOWED_SORTING_DIRECTIONS = ["asc", "desc"]

@app.route('/api/posts', methods=['GET'])
def get_posts():
    sort_key = request.args.get("sort")
    direction = request.args.get("direction")

    # if the query parameters were not provided return all post unsorted
    if sort_key is None or direction is None:
        app.logger.info("Sorting parameters are incomplete or missing, returning unsorted posts.")
        return jsonify(POSTS)

    # validate sort param
    if sort_key not in ALLOWED_SORTING_KEYS:
        error_msg = f"Wrong sorting value, only these are allowed: {", ".join(ALLOWED_SORTING_KEYS)}"
        app.logger.error(error_msg)
        return jsonify({
            "error": error_msg
        }), 400

    # validate direction param
    if direction not in ALLOWED_SORTING_DIRECTIONS:
        error_msg = f"Wrong direction value, only these are allowed: {", ".join(ALLOWED_SORTING_DIRECTIONS)}"
        app.logger.error(error_msg)
        return jsonify({
            "error": error_msg
        }), 400

    app.logger.info(f"Returning posts sorted by {sort_key} in {direction}ending order.")

    # sort the posts according to sort and direction query parameters
    return sorted(POSTS, key=lambda post: post[sort_key], reverse=direction == "desc")


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
        error_msg = f"Missing keys: {missing_keys}"
        app.logger.error(error_msg)
        return jsonify({"error": error_msg}), 400

    # attach id to the new post
    new_post_id = max([post['id'] for post in POSTS], default=0) + 1
    new_post["id"] = new_post_id

    POSTS.append(new_post)
    app.logger.info(f"New post with id: {new_post_id} was added.")

    return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    global POSTS

    deleted_post = next((post for post in POSTS if post["id"] == id), None)

    if deleted_post is None:
        app.logger.error(f"Post with id {id} was not found. Deleting is not possible.")
        return jsonify({"error": "Post Not Found"}), 404

    POSTS = [post for post in POSTS if post["id"] != deleted_post["id"]]

    delete_success_msg = f"Post with id {id} has been deleted successfully."
    app.logger.info(delete_success_msg)

    return jsonify({"message": delete_success_msg}), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    global POSTS

    updated_post = next((post for post in POSTS if post["id"] == id), None)

    if updated_post is None:
        app.logger.error(f"Post with id {id} was not found. Updating is not possible.")
        return jsonify({"error": "Post Not Found"}), 404

    updates_sent = request.get_json()
    updated_post.update(updates_sent)

    updated_success_msg = f"Post with id {id} has been updated successfully."
    app.logger.info(updated_success_msg)

    return jsonify(updated_post), 200


@app.route('/api/posts/search', methods=['GET'])
def search():
    search_title = request.args.get("title", None)
    search_content = request.args.get("content", None)

    matching_posts = []

    for post in POSTS:
        matching_post_found = False

        if search_title is not None and search_title.lower() in post["title"].lower():
            matching_post_found = True
        if search_content is not None and search_content.lower() in post["content"].lower():
            matching_post_found = True

        if matching_post_found:
            matching_posts.append(post)

    app.logger.info(f"Search results: {len(matching_posts)} matching posts were found.")

    return jsonify(matching_posts), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
