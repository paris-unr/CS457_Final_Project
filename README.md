# CS457 Final Project - Car Database Manager

A simple web app for managing a car database with full CRUD operations. Built with Flask and PostgreSQL.

## What It Does

This app lets you manage a car database through a web interface. You can add, view, edit, delete, and search records across 5 different tables. It also imports car data from a CSV file.

## Database Schema

The database has 5 tables in Third Normal Form:

- **companies** - Car manufacturers (Ferrari, Toyota, etc.)
- **fuel_types** - Types of fuel (Petrol, Diesel, Hybrid, etc.)
- **engines** - Engine specs (type, CC, horsepower, torque)
- **cars** - Main car info with foreign keys to company, engine, and fuel type
- **performance** - Performance metrics (top speed, 0-100 acceleration)

## Setup

1. **Install PostgreSQL** (if not already installed)
   ```bash
   # macOS
   brew install postgresql
   brew services start postgresql
   
   # Ubuntu
   sudo apt install postgresql
   sudo systemctl start postgresql
   ```

2. **Create database and user**
   ```bash
   sudo -u postgres psql
   CREATE DATABASE db;
   CREATE USER p4ris WITH PASSWORD 'p4ris';
   GRANT ALL PRIVILEGES ON DATABASE db TO p4ris;
   \q
   ```

3. **Install Python dependencies**
   ```bash
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file (already exists):
   ```
   DATABASE_URL="postgresql://p4ris:p4ris@localhost:5432/db"
   ```

5. **Run the app**
   ```bash
   flask run
   ```

6. **Open in browser**
   
   Go to `http://127.0.0.1:5000`

## Features

- **View** all records in any table
- **Add** new records with a form
- **Edit** existing records
- **Delete** records
- **Search** by name/type
- **Import CSV** data from `data/CarsDatasets2025.csv`

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL
- **Frontend**: HTML, TailwindCSS, Vanilla JavaScript
- **ORM**: SQLAlchemy

## Project Structure

```
.
├── app.py              # Flask app setup
├── models.py           # Database models (5 tables)
├── views.py            # API routes and frontend route
├── controller.py       # CSV import logic
├── templates/
│   └── index.html      # Frontend UI
├── data/
│   └── CarsDatasets2025.csv
└── requirements.txt
```

## API Endpoints

Each table has full CRUD endpoints:

- `GET /api/{table}` - Get all records
- `GET /api/{table}/<id>` - Get one record
- `POST /api/{table}` - Create record
- `PUT /api/{table}/<id>` - Update record
- `DELETE /api/{table}/<id>` - Delete record
- `GET /api/{table}/search?q=query` - Search records

Tables: `companies`, `fuel_types`, `engines`, `cars`, `performance`

## Notes

- The database is normalized to Third Normal Form (3NF)
- Foreign key relationships maintain data integrity
- CSV import parses messy data (e.g., "$1,100,000" → 1100000)
- All CRUD operations have error handling
