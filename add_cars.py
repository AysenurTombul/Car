from app import app, db, Car  


cars = [
    Car(
        make="Toyota",
        model="Corolla",
        transmission="Automatic",
        deposit=100,
        mileage=200,
        age_limit=18,
        cost_per_day=50,
        image_url="https://i0.shbdn.com/photos/19/59/25/x5_1210195925mon.jpg",
        office_id=1
    ),
    Car(
        make="Honda",
        model="Civic",
        transmission="Manual",
        deposit=80,
        mileage=150,
        age_limit=21,
        cost_per_day=40,
        image_url="https://i0.shbdn.com/photos/19/59/25/x5_1210195925mon.jpg",
        office_id=1
    ),
    Car(
        make="Ford",
        model="Focus",
        transmission="Automatic",
        deposit=120,
        mileage=250,
        age_limit=20,
        cost_per_day=60,
        image_url="https://i0.shbdn.com/photos/19/59/25/x5_1210195925mon.jpg",
        office_id=1
    ),
    Car(
        make="BMW",
        model="3 Series",
        transmission="Automatic",
        deposit=200,
        mileage=300,
        age_limit=25,
        cost_per_day=100,
        image_url="https://i0.shbdn.com/photos/19/59/25/x5_1210195925mon.jpg",
        office_id=1
    ),
    Car(
        make="Mercedes",
        model="C Class",
        transmission="Automatic",
        deposit=250,
        mileage=350,
        age_limit=25,
        cost_per_day=120,
        image_url="https://i0.shbdn.com/photos/19/59/25/x5_1210195925mon.jpg",
        office_id=1
    )
]


with app.app_context():
    db.session.add_all(cars)
    db.session.commit()
    print("Arabalar başarıyla eklendi!")
