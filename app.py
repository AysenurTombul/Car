from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from authlib.integrations.flask_client import OAuth
import os

# Ortam değişkenlerini yükle

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your_default_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///car_rental.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Ortam değişkenlerinden Google OAuth bilgilerini yükle
app.config['GOOGLE_CLIENT_ID'] = os.getenv('GOOGLE_CLIENT_ID')
app.config['GOOGLE_CLIENT_SECRET'] = os.getenv('GOOGLE_CLIENT_SECRET')

if not app.config['GOOGLE_CLIENT_ID'] or not app.config['GOOGLE_CLIENT_SECRET']:
    raise ValueError("Google OAuth Client ID ve Secret ortam değişkenlerinde tanımlanmalıdır.")

# Dosya yükleme için ayarlar
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
oauth = OAuth(app)

# OAuth Ayarları
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    client_kwargs={'scope': 'openid email profile'}
)

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(200), nullable=True)

class Office(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    city = db.Column(db.String(100), nullable=False)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    transmission = db.Column(db.String(20), nullable=False)
    deposit = db.Column(db.Float, nullable=False)
    mileage = db.Column(db.Integer, nullable=False)
    age_limit = db.Column(db.Integer, nullable=False)
    cost_per_day = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    office_id = db.Column(db.Integer, db.ForeignKey('office.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    user = current_user if current_user.is_authenticated else None
    offices = Office.query.all() if not user else Office.query.filter_by(city=user.city).all()
    return render_template('home.html', user=user, offices=offices)

@app.route('/_en')
def home_en():
    user = current_user if current_user.is_authenticated else None
    offices = Office.query.all() if not user else Office.query.filter_by(city=user.city).all()
    return render_template('home_en.html', user=user, offices=offices)

@app.route('/book_car', methods=['POST'])
def book_car():
    pickup_office = request.form.get('pickup_office')
    pickup_date = request.form.get('pickup_date')
    pickup_time = request.form.get('pickup_time')
    drop_office = request.form.get('drop_office')
    drop_date = request.form.get('drop_date')
    drop_time = request.form.get('drop_time')

    flash(f"Aracınız {pickup_date} tarihinde {pickup_time}'da {pickup_office} ofisinden alınacak.", "success")
    return redirect(url_for('search_cars', make='', transmission='', order_by=''))

@app.route('/book_car_en', methods=['POST'])
def book_car_en():
    pickup_office = request.form.get('pickup_office')
    pickup_date = request.form.get('pickup_date')
    pickup_time = request.form.get('pickup_time')
    drop_office = request.form.get('drop_office')
    drop_date = request.form.get('drop_date')
    drop_time = request.form.get('drop_time')

    flash(f"Your car will be ready on {pickup_date} at {pickup_time} from {pickup_office} office.", "success")
    return redirect(url_for('search_cars_en', make='', transmission='', order_by=''))

@app.route('/search_cars', methods=['GET'])
def search_cars():
    make = request.args.get('make', '').lower()
    transmission = request.args.get('transmission', '').lower()
    order_by = request.args.get('order_by', '')

    cars = Car.query

    if make:
        cars = cars.filter(Car.make.ilike(f'%{make}%'))

    if transmission:
        cars = cars.filter(Car.transmission.ilike(transmission))

    if order_by == 'low_price':
        cars = cars.order_by(Car.cost_per_day.asc())
    elif order_by == 'high_price':
        cars = cars.order_by(Car.cost_per_day.desc())

    cars = cars.all()
    return render_template('search_results.html', cars=cars)

@app.route('/search_cars_en', methods=['GET'])
def search_cars_en():
    make = request.args.get('make', '').lower()
    transmission = request.args.get('transmission', '').lower()
    order_by = request.args.get('order_by', '')

    cars = Car.query

    if make:
        cars = cars.filter(Car.make.ilike(f'%{make}%'))

    if transmission:
        cars = cars.filter(Car.transmission.ilike(transmission))

    if order_by == 'low_price':
        cars = cars.order_by(Car.cost_per_day.asc())
    elif order_by == 'high_price':
        cars = cars.order_by(Car.cost_per_day.desc())

    cars = cars.all()
    return render_template('search_results_en.html', cars=cars)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        country = request.form.get('country')
        city = request.form.get('city')
        profile_picture = request.files['profile_picture']

        if len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
            flash('Password must be at least 8 characters, include a number and a letter.', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='sha256')
        picture_path = None
        if profile_picture:
            picture_path = os.path.join(app.config['UPLOAD_FOLDER'], profile_picture.filename)
            profile_picture.save(picture_path)

        user = User(username=username, email=email, password=hashed_password, country=country, city=city,
                    profile_picture=picture_path)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/register_en', methods=['GET', 'POST'])
def register_en():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        country = request.form.get('country')
        city = request.form.get('city')
        profile_picture = request.files['profile_picture']

        if len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
            flash('Password must be at least 8 characters, include a number and a letter.', 'danger')
            return redirect(url_for('register_en'))

        hashed_password = generate_password_hash(password, method='sha256')
        picture_path = None
        if profile_picture:
            picture_path = os.path.join(app.config['UPLOAD_FOLDER'], profile_picture.filename)
            profile_picture.save(picture_path)

        user = User(username=username, email=email, password=hashed_password, country=country, city=city,
                    profile_picture=picture_path)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login_en'))

    return render_template('register_en.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash(f'Login successful! Welcome, {user.username}.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')

@app.route('/login_en', methods=['GET', 'POST'])
def login_en():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash(f'Login successful! Welcome, {user.username}.', 'success')
            return redirect(url_for('home_en'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login_en.html')

@app.route('/login/google')
def login_google():
    redirect_uri = url_for('authorize_google', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize/google')
def authorize_google():
    token = google.authorize_access_token()
    user_info = google.parse_id_token(token)
    email = user_info['email']
    username = user_info['name']

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(username=username, email=email, password='', country='', city='')
        db.session.add(user)
        db.session.commit()
    login_user(user)
    flash(f'Welcome, {user.username}!', 'success')
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/add_test_data')
def add_test_data():
    offices = [
        Office(name="İzmir Alsancak Şehir", latitude=38.422, longitude=27.131, city="İzmir"),
    ]
    cars = [
        Car(make="Renault", model="Clio", transmission="Manual", deposit=2500, mileage=1000, age_limit=21, cost_per_day=1914, image_url="https://via.placeholder.com/300x200?text=Renault+Clio", office_id=1),
    ]

    with app.app_context():
        db.session.add_all(offices)
        db.session.add_all(cars)
        db.session.commit()
    return "Test verileri başarıyla eklendi!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
