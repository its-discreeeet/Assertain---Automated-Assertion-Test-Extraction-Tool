**Assertain** is a Python-based tool to automate extraction assertions from Python test files from a github repository. This tool also contains a streamlit app for the GUI.

---

## Features

- Extracts `test assertions` from a github repository.
- Handles inheritance and tracks assertions within class hierarchies.
- Generates reports in csv format.
- Includes a **Streamlit-based GUI** for ease of use.
- Supports running locally or via Docker.

---

## Prerequisites

- Python 3.8 or higher
- Pip (Python package manager)
- Docker (optional, for containerized execution)

---

## Running Locally

### Clone the Repository
```
git clone https://github.com/its-discreeeet/exercise-uiuc--2025.git
cd <path-to-this-directory>
```

### Install Dependencies
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

Use repositories like these to see results
