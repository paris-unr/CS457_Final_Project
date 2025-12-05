import os
import pandas as pd
import re
from models import db, Company, FuelType, Engine, Car, Performance

INPUT_PATH = "data/CarsDatasets2025.csv"

def parse_numeric(value):
    """Extract numeric value from string (e.g., '1,200 cc' -> 1200)"""
    if pd.isna(value):
        return None
    match = re.search(r'[\d,]+', str(value))
    if match:
        return int(match.group().replace(',', ''))
    return None

def parse_price(value):
    """Extract price from string (e.g., '$1,100,000 ' -> 1100000)"""
    if pd.isna(value):
        return None
    match = re.search(r'[\d,]+', str(value))
    if match:
        return int(match.group().replace(',', ''))
    return None

def parse_float(value):
    """Extract float from string (e.g., '2.5 sec' -> 2.5)"""
    if pd.isna(value):
        return None
    match = re.search(r'[\d.]+', str(value))
    if match:
        return float(match.group())
    return None

def get_or_create_company(session, name):
    """Get existing company or create new one"""
    name = name.strip()
    company = session.query(Company).filter_by(name=name).first()
    if not company:
        company = Company(name=name)
        session.add(company)
        session.flush()
    return company

def get_or_create_fuel_type(session, name):
    """Get existing fuel type or create new one"""
    if pd.isna(name):
        return None
    name = name.strip()
    fuel_type = session.query(FuelType).filter_by(name=name).first()
    if not fuel_type:
        fuel_type = FuelType(name=name)
        session.add(fuel_type)
        session.flush()
    return fuel_type

def import_csv():
    """Import car data from CSV into 5 normalized database tables"""
    try:
        print(f"Loading CSV from {INPUT_PATH}")
        df = pd.read_csv(INPUT_PATH, encoding='latin-1')
        
        print(f"Found {len(df)} rows in CSV")
        
        # Track statistics
        companies_created = 0
        fuel_types_created = 0
        engines_created = 0
        cars_created = 0
        performances_created = 0
        
        for idx, row in df.iterrows():
            try:
                # Get or create company
                company = get_or_create_company(db.session, row['Company Names'])
                if company.id is None:
                    companies_created += 1
                
                # Get or create fuel type
                fuel_type = get_or_create_fuel_type(db.session, row['Fuel Types'])
                if fuel_type and fuel_type.id is None:
                    fuel_types_created += 1
                
                # Create engine
                engine = Engine(
                    type=row['Engines'] if not pd.isna(row['Engines']) else None,
                    cc=parse_numeric(row['CC/Battery Capacity']),
                    horsepower=parse_numeric(row['HorsePower']),
                    torque=parse_numeric(row['Torque'])
                )
                db.session.add(engine)
                db.session.flush()
                engines_created += 1
                
                # Create car
                car = Car(
                    name=row['Cars Names'],
                    company_id=company.id,
                    engine_id=engine.id,
                    fuel_type_id=fuel_type.id if fuel_type else None,
                    price=parse_price(row['Cars Prices']),
                    seats=parse_numeric(row['Seats'])
                )
                db.session.add(car)
                db.session.flush()
                cars_created += 1
                
                # Create performance
                performance = Performance(
                    car_id=car.id,
                    top_speed=parse_numeric(row['Total Speed']),
                    acceleration_0_100=parse_float(row['Performance(0 - 100 )KM/H'])
                )
                db.session.add(performance)
                performances_created += 1
                
            except Exception as e:
                print(f"Error processing row {idx}: {e}")
                db.session.rollback()
                continue
        
        # Commit all changes
        db.session.commit()
        
        print(f"Import complete!")
        print(f"  Companies: {companies_created} created")
        print(f"  Fuel Types: {fuel_types_created} created")
        print(f"  Engines: {engines_created} created")
        print(f"  Cars: {cars_created} created")
        print(f"  Performance records: {performances_created} created")
        
        return True
        
    except Exception as e:
        print(f"Failed to import CSV: {e}")
        db.session.rollback()
        return False
