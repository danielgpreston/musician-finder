# 🎵 musician-finder 🎵
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   
App that helps you find other musicians

Looking to start a band or meet other musicians? Browse musicians in your area based on what instruments they play, what genres they are interested in, their commitment levels/experience, and more.

## 🎼 Getting Started 🎼

Follow these instructions to set up and run Musician Finder locally.

### Prerequisites

Make sure you have the following installed:

- **Node.js** (version 20 or later recommended)
- **npm** (included with Node.js)
- **Git**
- **python 3+**

You can verify your installations by running:

```bash
node -v
npm -v
git --version
python --version
```
## Frontend

### 1. Clone the Repository

Clone the project from GitHub:

```bash
git clone <repo-url>
```

Navigate into the frontend folder:

```bash
cd musician-finder
```

### 2. Navigate to the Frontend Directory

The React application is located inside `src/frontend`.

```bash
cd src
cd frontend
```

### 3. Install Packages

Install the required packages:

```bash
npm install
```

This installs the project's dependencies, including React, Vite, React Router, and any other packages listed in `package.json`.

You only need to repeat this step when dependencies change or when setting up the project for the first time.

### 4. Host the Application Locally

Run:

```bash
npm run dev
```

Vite will start a local development server.

### 5. Open the Application

Open your browser and navigate to:

http://localhost:5173/

The Musician Finder application should now be running locally.
To stop the application, return to the terminal and press Ctrl + C

- **Frontend:** React with Vite
- **Routing:** React Router
- **Icons:** Lucide React
- **Styling:** CSS


## Backend

### 1. Follow Previous Step 1 from Frontend setup.
```bash
git clone <repo-url>
``` 
etc.

### 2. Navigate to the Backend Directory

The Django application is located inside `src/backend`.

```bash
cd src
cd backend
```
### 3. Install Packages

**Installing using python (with `/venv/` and `requirments.txt`)**

*Install the required packages:*

```bash
# Create the virtual environment for packages
python -m venv venv
```
*Activate it*

```bash
# Windows
.\venv\Scripts\activate # usually a .ps1 file
# Linux
source venv/bin/activate
```
*Finally, install the packages with requirements.txt*
```bash
pip install -r requirements.txt
```

### 4. Host the Application Locally
```bash
python manage.py runserver
```

Should now be hosted/working in correspondence with the frontend. Let me know if I need to elaborate more or not.
 
Branching strategy: main (protected) → dev → feature/* branches, merged via reviewed pull request
Branch protection on main: pull request + approval required before merging, force pushes disabled
