# Movie Theater

Simple terminal application in Python providing actions over movie data developed as an exercise in Python.

## Prerequisites:
Locally installed:
1. Python
2. pip

To run this program install required packages:

```commandline
pip install -r requirements.txt
```

## Usage

You can start the application by running the main.py file from a terminal.
The default example file `movies.json` prefilled with movies will be used 
for storage.

```commandline
python main.py
```

Optionally you can specify the file that would serve as a storage for the movies:
Two file formats are available: JSON and CSV.

Example:
```commandline
python main.py file_name.json
```
or
```commandline
python main.py file_name.csv
```

