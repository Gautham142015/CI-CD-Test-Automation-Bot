# Product Management Assistant

Welcome to the Product Management Assistant! This is a starter kit for a web application designed to be a "vibe coding for PMs" experience. It helps product managers turn unstructured text—like customer feedback, meeting notes, or feature ideas—into a prioritized backlog and a visual roadmap.

This project uses a React frontend and a Python (FastAPI) backend with OpenAI integration for natural language processing.

## Features

- **Natural Language Processing**: Paste unstructured text and have it automatically converted into structured tasks (features, pain points, enhancements).
- **AI-Powered Analysis**: Uses OpenAI's GPT-4o-mini to extract user stories, acceptance criteria, and priority levels.
- **Prioritized Backlog**: View all your processed tasks in a clean list.
- **Roadmap Visualization**: Get an instant overview of your product roadmap with a chart showing tasks grouped by priority. A future enhancement could be to add a timeline view for a more traditional roadmap.

## Tech Stack

- **Frontend**: React (with Vite), Tailwind CSS, shadcn/ui, Recharts
- **Backend**: Python (FastAPI)
- **AI**: OpenAI GPT-4o-mini
- **Database**: SQLite

## Getting Started

### Prerequisites

- Node.js and npm (for the frontend)
- Python 3.8+ and pip (for the backend)
- An OpenAI API key

### Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd product-management-app
    ```

2.  **Setup the Backend:**
    - Navigate to the backend directory:
      ```bash
      cd backend
      ```
    - Create a Python virtual environment (recommended):
      ```bash
      python -m venv venv
      source venv/bin/activate  # On Windows use `venv\Scripts\activate`
      ```
    - Install the required Python packages:
      ```bash
      pip install -r requirements.txt
      ```
    - Create a `.env` file in the `backend` directory and add your OpenAI API key:
      ```
      OPENAI_API_KEY="your-openai-api-key-here"
      ```

3.  **Setup the Frontend:**
    - In a new terminal, navigate to the frontend directory:
      ```bash
      cd frontend
      ```
    - Install the required npm packages:
      ```bash
      npm install
      ```

### Running the Application

1.  **Run the Backend Server:**
    - From the `backend` directory, run the following command to start the FastAPI server:
      ```bash
      make dev
      # Or run uvicorn directly:
      # uvicorn main:app --reload
      ```
    - The backend server will be running at `http://localhost:8000`.

2.  **Seed the Database (Optional):**
    - To populate the database with some example tasks, run the following command from the `backend` directory:
      ```bash
      make seed
      ```

3.  **Run the Frontend Application:**
    - From the `frontend` directory, run the following command to start the React development server:
      ```bash
      npm run dev
      ```
    - The frontend application will be available at `http://localhost:5173`.

## How to Use

1.  Open the web application in your browser (`http://localhost:5173`).
2.  In the input box, paste any unstructured text. For example:
    - "A customer complained that they can't reset their password on mobile."
    - "We should add AI-driven search to our grocery ordering app."
    - "Meeting notes: The team decided to prioritize the new onboarding flow for Q4."
3.  Click the "Process Text" button.
4.  The AI will analyze the text and add a new structured task to your backlog.
5.  The roadmap visualization will update to reflect the new task's priority.
