# Opportuno - Backend

## Installation

### Requirements:
- Python at least 3.10
- Python virtual environment creation tool (e.g. `venv`)
- zip and unzip tools

### Steps:
1. Clone the repository
2. Create a virtual environment
```
python3 -m venv .venv
```
3. Activate the virtual environment
```
source .venv/bin/activate
```
4. Install the requirements
```
pip install -r requirements.txt
```
5. Change the `config.py` file and `firebase-credential.json` in `config/` folder to your own configuration
6. Extract the `data.zip` file

## Running the server
```
python manage.py runserver
```