# MasterBlog API

A simple blog web application with both frontend and backend components. The following features are included in this demo:

- Load all stored posts
- Perform create, read, update, and delete (CRUD) operations on posts
- Search for posts by title or content

## Setup

1. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```   

2. **Run the backend**:
   ```bash
   python frontend/frontend_app.py
   ```   

3. **Run the frontend**
   ```bash
   python backend/backend_app.py
   ```   

Navigate to the http://localhost:5001.

**Note**: Sometimes the ports may be occupied. In that case, change the port parameter value in the `app.run` method in the file that is causing the issue: `backend_app.py` or `frontend_app.py`.