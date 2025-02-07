The sql_generator.py has the entire code as of now.

## Features:
  1. Advanced SQL query generation from natural language inputs.
  2. Establishing connection to PostgresSQL server (locally) and executing generated queries.
  3. Results fetched from the PostgreSQL server can be utilised in two ways:
          a. Generating insights based on the user questions and the fetched results.
          b. Generating business reports (functional yet some changes to be made in pdf rendering)

## Requirements Installation:
  1. `pip install -r requirements.txt`

## Running the code locally:
  1. `conda create -n venv python=3.11`
  2. `conda activate venv`
  3. `pip install -r requirements.txt`
  4. `python sql_generator.py`