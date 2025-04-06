# exercise-uiuc--2025

## Assertion Extractor Tool

**Assertion Extractor** is a Python-based tool to extract assertions from Python test files from a github repository. This tool also contains a streamlit app for the GUI.

---

## Features

- Extracts `assert` statements from a github repository.
- Handles inheritance and tracks assertions within class hierarchies.
- Generates reports in csv formats.
- Includes a **Streamlit-based GUI** for ease of use.
- Supports running locally or via Docker.

---

## Prerequisites

- Python 3.8 or higher
- Pip (Python package manager)
- Docker (optional, for containerized execution)

---

## Running Locally

### Step 1: Clone the Repository
```
git clone https://github.com/its-discreeeet/exercise-uiuc--2025.git
cd <path-to-this-directory>
```

### Step 2: Install Dependencies
```
pip install -r requirements.txt
```

### If you wish to use docker (ensure docker is installed and running)
```
./run.sh
```
Note: If you are on windows like me, use git bash to run this cmd

### Run core script directly without docker
```
cd code
python assertion_extractor.py <github repo url>
```

### Use streamlit GUI
```
cd code
streamlit run app.py
```

**A few of the repositories for which this tool is useful for** :-
- PyTest : https://github.com/pytest-dev/pytest
- Flask : https://github.com/pallets/flask
- Requests : https://github.com/psf/requests

Paste them directly to see the results
