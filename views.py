from flask import Blueprint, jsonify, request, render_template
from models import db, User, Company, FuelType, Engine, Car, Performance
from controller import import_csv

main = Blueprint('main', __name__)

# Frontend route
@main.route('/')
def index():
    return render_template('index.html')

# Import CSV endpoint
@main.route('/api/import', methods=['POST'])
def api_import_csv():
    result = import_csv()
    if result:
        return jsonify({'message': 'CSV imported successfully'}), 200
    return jsonify({'error': 'Failed to import CSV'}), 500

# ==================== COMPANIES CRUD ====================
@main.route('/api/companies', methods=['GET'])
def get_companies():
    companies = Company.query.all()
    return jsonify([c.to_dict() for c in companies])

@main.route('/api/companies/<int:id>', methods=['GET'])
def get_company(id):
    company = Company.query.get_or_404(id)
    return jsonify(company.to_dict())

@main.route('/api/companies', methods=['POST'])
def create_company():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
    company = Company(name=data['name'])
    db.session.add(company)
    db.session.commit()
    return jsonify(company.to_dict()), 201

@main.route('/api/companies/<int:id>', methods=['PUT'])
def update_company(id):
    company = Company.query.get_or_404(id)
    data = request.get_json()
    if data.get('name'):
        company.name = data['name']
    db.session.commit()
    return jsonify(company.to_dict())

@main.route('/api/companies/<int:id>', methods=['DELETE'])
def delete_company(id):
    company = Company.query.get_or_404(id)
    db.session.delete(company)
    db.session.commit()
    return jsonify({'message': 'Deleted'}), 200

@main.route('/api/companies/search', methods=['GET'])
def search_companies():
    q = request.args.get('q', '')
    companies = Company.query.filter(Company.name.ilike(f'%{q}%')).all()
    return jsonify([c.to_dict() for c in companies])

# ==================== FUEL TYPES CRUD ====================
@main.route('/api/fuel_types', methods=['GET'])
def get_fuel_types():
    fuel_types = FuelType.query.all()
    return jsonify([f.to_dict() for f in fuel_types])

@main.route('/api/fuel_types/<int:id>', methods=['GET'])
def get_fuel_type(id):
    fuel_type = FuelType.query.get_or_404(id)
    return jsonify(fuel_type.to_dict())

@main.route('/api/fuel_types', methods=['POST'])
def create_fuel_type():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
    fuel_type = FuelType(name=data['name'])
    db.session.add(fuel_type)
    db.session.commit()
    return jsonify(fuel_type.to_dict()), 201

@main.route('/api/fuel_types/<int:id>', methods=['PUT'])
def update_fuel_type(id):
    fuel_type = FuelType.query.get_or_404(id)
    data = request.get_json()
    if data.get('name'):
        fuel_type.name = data['name']
    db.session.commit()
    return jsonify(fuel_type.to_dict())

@main.route('/api/fuel_types/<int:id>', methods=['DELETE'])
def delete_fuel_type(id):
    fuel_type = FuelType.query.get_or_404(id)
    db.session.delete(fuel_type)
    db.session.commit()
    return jsonify({'message': 'Deleted'}), 200

@main.route('/api/fuel_types/search', methods=['GET'])
def search_fuel_types():
    q = request.args.get('q', '')
    fuel_types = FuelType.query.filter(FuelType.name.ilike(f'%{q}%')).all()
    return jsonify([f.to_dict() for f in fuel_types])

# ==================== ENGINES CRUD ====================
@main.route('/api/engines', methods=['GET'])
def get_engines():
    engines = Engine.query.all()
    return jsonify([e.to_dict() for e in engines])

@main.route('/api/engines/<int:id>', methods=['GET'])
def get_engine(id):
    engine = Engine.query.get_or_404(id)
    return jsonify(engine.to_dict())

@main.route('/api/engines', methods=['POST'])
def create_engine():
    data = request.get_json()
    if not data or not data.get('type'):
        return jsonify({'error': 'Engine type is required'}), 400
    engine = Engine(
        type=data['type'],
        cc=data.get('cc'),
        horsepower=data.get('horsepower'),
        torque=data.get('torque')
    )
    db.session.add(engine)
    db.session.commit()
    return jsonify(engine.to_dict()), 201

@main.route('/api/engines/<int:id>', methods=['PUT'])
def update_engine(id):
    engine = Engine.query.get_or_404(id)
    data = request.get_json()
    if data.get('type'):
        engine.type = data['type']
    if 'cc' in data:
        engine.cc = data['cc']
    if 'horsepower' in data:
        engine.horsepower = data['horsepower']
    if 'torque' in data:
        engine.torque = data['torque']
    db.session.commit()
    return jsonify(engine.to_dict())

@main.route('/api/engines/<int:id>', methods=['DELETE'])
def delete_engine(id):
    engine = Engine.query.get_or_404(id)
    db.session.delete(engine)
    db.session.commit()
    return jsonify({'message': 'Deleted'}), 200

@main.route('/api/engines/search', methods=['GET'])
def search_engines():
    q = request.args.get('q', '')
    engines = Engine.query.filter(Engine.type.ilike(f'%{q}%')).all()
    return jsonify([e.to_dict() for e in engines])

# ==================== CARS CRUD ====================
@main.route('/api/cars', methods=['GET'])
def get_cars():
    cars = Car.query.all()
    return jsonify([c.to_dict() for c in cars])

@main.route('/api/cars/<int:id>', methods=['GET'])
def get_car(id):
    car = Car.query.get_or_404(id)
    return jsonify(car.to_dict())

@main.route('/api/cars', methods=['POST'])
def create_car():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('company_id'):
        return jsonify({'error': 'Name and company_id are required'}), 400
    car = Car(
        name=data['name'],
        company_id=data['company_id'],
        engine_id=data.get('engine_id'),
        fuel_type_id=data.get('fuel_type_id'),
        price=data.get('price'),
        seats=data.get('seats')
    )
    db.session.add(car)
    db.session.commit()
    return jsonify(car.to_dict()), 201

@main.route('/api/cars/<int:id>', methods=['PUT'])
def update_car(id):
    car = Car.query.get_or_404(id)
    data = request.get_json()
    if data.get('name'):
        car.name = data['name']
    if 'company_id' in data:
        car.company_id = data['company_id']
    if 'engine_id' in data:
        car.engine_id = data['engine_id']
    if 'fuel_type_id' in data:
        car.fuel_type_id = data['fuel_type_id']
    if 'price' in data:
        car.price = data['price']
    if 'seats' in data:
        car.seats = data['seats']
    db.session.commit()
    return jsonify(car.to_dict())

@main.route('/api/cars/<int:id>', methods=['DELETE'])
def delete_car(id):
    car = Car.query.get_or_404(id)
    db.session.delete(car)
    db.session.commit()
    return jsonify({'message': 'Deleted'}), 200

@main.route('/api/cars/search', methods=['GET'])
def search_cars():
    q = request.args.get('q', '')
    cars = Car.query.filter(Car.name.ilike(f'%{q}%')).all()
    return jsonify([c.to_dict() for c in cars])

# ==================== PERFORMANCE CRUD ====================
@main.route('/api/performance', methods=['GET'])
def get_performances():
    performances = Performance.query.all()
    return jsonify([p.to_dict() for p in performances])

@main.route('/api/performance/<int:id>', methods=['GET'])
def get_performance(id):
    performance = Performance.query.get_or_404(id)
    return jsonify(performance.to_dict())

@main.route('/api/performance', methods=['POST'])
def create_performance():
    data = request.get_json()
    if not data or not data.get('car_id'):
        return jsonify({'error': 'car_id is required'}), 400
    performance = Performance(
        car_id=data['car_id'],
        top_speed=data.get('top_speed'),
        acceleration_0_100=data.get('acceleration_0_100')
    )
    db.session.add(performance)
    db.session.commit()
    return jsonify(performance.to_dict()), 201

@main.route('/api/performance/<int:id>', methods=['PUT'])
def update_performance(id):
    performance = Performance.query.get_or_404(id)
    data = request.get_json()
    if 'car_id' in data:
        performance.car_id = data['car_id']
    if 'top_speed' in data:
        performance.top_speed = data['top_speed']
    if 'acceleration_0_100' in data:
        performance.acceleration_0_100 = data['acceleration_0_100']
    db.session.commit()
    return jsonify(performance.to_dict())

@main.route('/api/performance/<int:id>', methods=['DELETE'])
def delete_performance(id):
    performance = Performance.query.get_or_404(id)
    db.session.delete(performance)
    db.session.commit()
    return jsonify({'message': 'Deleted'}), 200

@main.route('/api/performance/search', methods=['GET'])
def search_performance():
    q = request.args.get('q', '')
    try:
        speed = int(q)
        performances = Performance.query.filter(Performance.top_speed >= speed).all()
    except ValueError:
        performances = Performance.query.all()
    return jsonify([p.to_dict() for p in performances])