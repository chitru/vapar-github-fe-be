# Github Backend API

A simple frontend that allows users to search for repositories on GitHub and view details about a specific repository. It uses backend API built on top of FastAPI to fetch the data. Github free API is used to fetch the data and no authentication is required.

# Setup and installation

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

## Frontend

Frontend is build with:

- React
- Vite
- shadcn/ui (radix, tailwind)
- React Router
- Lucide Icons

Inside `frontend` folder, run the following commands:

```bash
npm install
npm run dev
```

## Backend

Backend is build with:

- FastAPI (Python)
- Github API (free)

Inside `backend` folder:

### 1. Create a virtual environment:

```bash
python -m venv github_backend_env
```

### 2. Activate the virtual environment:

**On macOS/Linux:**

```bash
source github_backend_env/bin/activate
```

**On Windows:**

```bash
github_backend_env\Scripts\activate
```

### 3. Verify activation:

```bash
which python  # Should show path to your venv
```

### 4. Install dependencies:

```bash
pip install -r requirements.txt
```

### 5. Run the server:

```bash
fastapi dev app/main.py
```

**Note:** Backend should be running on port 8000. If not, please update `frontend/src/lib/config.ts` with the correct port.

### Testing

Run the tests inside `backend` folder:

```bash
source github_backend_env/bin/activate && python -m pytest app/tests/test_functions.py
```

# Considerations

- search button placed to that api hits are limited
- making data persistent when user comes back from detail page
- pagination added
