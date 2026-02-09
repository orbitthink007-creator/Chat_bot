# Deployment Guide - OrbitThink Chatbot

Follow these steps to deploy your chatbot to **Hugging Face Spaces** (Recommended) or Render.

## Prerequisites

- A GitHub account.
- A [Hugging Face](https://huggingface.co/) account (for Option 1).
- A [Render](https://render.com) account (for Option 2).
- Access to edit the code of `orbitthinkservices.com`.

## Step 1: Push Code to GitHub

1.  Initialize a git repository if you haven't already:
    ```bash
    git init
    git add .
    git commit -m "Initial commit"
    ```
2.  Create a new repository on GitHub.
3.  Push your code:
    ```bash
    git remote add origin <your-github-repo-url>
    git push -u origin main
    ```

---

## Option 1: Deploy to Hugging Face Spaces (Recommended)

Hugging Face Spaces offers a robust free tier for AI applications.

1.  **Create a New Space**:
    - Go to [Hugging Face Spaces](https://huggingface.co/spaces) and click **Create new Space**.
    - **Space Name**: e.g., `orbitthink-chatbot`
    - **License**: Apache 2.0 (or your choice)
    - **SDK**: Select **Docker**. (This is important!)
    - Click **Create Space**.

2.  **Connect Your GitHub Repo**:
    - In your new Space, go to **Settings**.
    - Scroll down to **Git** / **Connect a repository**.
    - Enter your GitHub repository URL (e.g., `https://github.com/orbitthink007-creator/Chat_bot`).
    - Authorize Hugging Face to access your repo.

3.  **Set Environment Variables**:
    - Still in **Settings**, scroll to **Variables and secrets**.
    - Click **New secret**.
    - **Name**: `GROQ_API_KEY`
    - **Value**: Paste your Groq API Key.
    - Click **Save**.

4.  **Build and Run**:
    - Hugging Face will automatically detect the `Dockerfile` in your repo and start building.
    - You can watch the build logs in the **App** tab.
    - Once built, your app will be live!

5.  **Get Your URL**:
    - Your URL will be `https://<your-username>-<space-name>.hf.space`.
    - Note: You might need to use `https://<your-username>-<space-name>.hf.space/api/chat` for the API endpoint.

---

## Option 2: Deploy to Render

1.  Log in to your Render dashboard.
2.  Click **New +** and select **Web Service**.
3.  Connect your GitHub repository.
4.  Render should automatically detect the configuration from `render.yaml`.
    - **Runtime**: Python 3
    - **Build Command**: `pip install -r backend/requirements.txt`
    - **Start Command**: `gunicorn -k uvicorn.workers.UvicornWorker backend.main:app --bind 0.0.0.0:10000`
5.  **Environment Variables**:
    - Scroll down to "Environment Variables" and add:
        - `GROQ_API_KEY`: Your Groq API Key.
6.  Click **Create Web Service**.
7.  Wait for the deployment to finish. Once live, copy your service URL (e.g., `https://orbitthink-chatbot.onrender.com`).

---

## Step 3: Update Frontend Widget

1.  Open `frontend/widget.js` in your local project.
2.  Find the line:
    ```javascript
    const API_URL = "http://localhost:8000/api/chat";
    ```
3.  Replace it with your new production URL.
    - **For Hugging Face**: `https://<your-username>-<space-name>.hf.space/api/chat`
    - **For Render**: `https://orbitthink-chatbot.onrender.com/api/chat`
4.  Commit and push this change to GitHub to keep your code updated.

## Step 4: Embed in Your Website

1.  Upload the `frontend/widget.js` file to your website's hosting (e.g., where `orbitthinkservices.com` is hosted) or serve it from a CDN.
    - If you can't host the JS file separately, you can copy the entire content of `widget.js` and wrap it in `<script>` tags.
2.  Add the following code to the `<body>` of your website's HTML pages where you want the bot to appear:

    ```html
    <!-- OrbitThink Chatot Widget -->
    <script src="path/to/your/uploaded/widget.js"></script>
    ```

    *If you paste the code directly:*
    ```html
    <script>
      // Paste the full content of widget.js here
    </script>
    ```

3.  Publish your website changes. The chatbot should now appear in the bottom right corner!
