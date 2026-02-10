# Deployment Guide - OrbitThink Chatbot

Follow these steps to deploy your professional chatbot system. We will use a **Split Strategy** for maximum performance:
1. **Backend** (Logic & AI): Hugging Face Spaces (Docker).
2. **Frontend** (UI & Widget): Netlify (Static Hosting).

---

## 🏗️ Part 1: Backend Deployment (Hugging Face)
**Goal:** Run the Python API that connects to Groq.

1.  **Push Entire Project to GitHub**:
    - Push your root folder (containing `backend/`, `frontend/`, `Dockerfile`, etc.) to GitHub.
    - Hugging Face needs the **Dockerfile** in the root to build the backend.

2.  **Create a New Hugging Face Space**:
    - Go to [Hugging Face Spaces](https://huggingface.co/spaces).
    - **Name**: `orbitthink-chatbot`
    - **SDK**: Select **Docker** (Required).
    - **Public/Private**: Recommended Public (for ease of use).

3.  **Connect GitHub**:
    - In Space **Settings**, connect your repository.
    - Hugging Face will start building from your **Dockerfile**.

4.  **Add your Groq Key**:
    - In Space **Settings** -> **Variables and secrets**.
    - Add a **Secret** named `GROQ_API_KEY` with your actual key.

5.  **Get your Backend URL**:
    - Once the build is "Running", your URL looks like: 
      `https://<username>-orbitthink-chatbot.hf.space`
    - **Your API endpoint is**: `https://<username>-orbitthink-chatbot.hf.space/api/chat`

---

## 🎨 Part 2: Frontend Deployment (Netlify)
**Goal:** Host your landing page and the chat widget.

1.  **Login to Netlify**:
    - Go to [Netlify.com](https://www.netlify.com/) and click **Add new site** -> **Import from an existing project**.
    - Select your GitHub repo.

2.  **Configure Site Settings (CRITICAL)**:
    - **Base directory**: Leave empty (Root).
    - **Build command**: Leave empty.
    - **Publish directory**: Type **`frontend`** (This ensures your site opens at `yoursite.netlify.app` instead of `yoursite.netlify.app/frontend`).

3.  **Click Deploy**:
    - Netlify will host your `index.html` and `widget.js`.

---

## 🔗 Part 3: Connecting the Two (Final Step)

Before you are completely finished, you must point your Frontend to your new Backend.

1.  Open `frontend/widget.js`.
2.  Update the production URL at the top:
    ```javascript
    // Change this to your Hugging Face API URL
    const API_URL = "https://<username>-orbitthink-chatbot.hf.space/api/chat";
    ```
3.  **Push the change to GitHub**:
    - Netlify will automatically update your site in seconds!

---

## 📂 Summary: Which files go where?

| Platform | Folder Needed | Why? |
| :--- | :--- | :--- |
| **Hugging Face** | **Entire Project** | Needs `Dockerfile` (Root) and `backend/` logic. |
| **Netlify** | **`frontend/`** folder | Needs `index.html` and `widget.js` to show the site. |
| **GitHub** | **Entire Project** | This is your one-stop "Source of Truth". |
