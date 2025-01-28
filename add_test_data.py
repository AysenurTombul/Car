from app import db, Office, Car

offices = [
    Office(name="İzmir Alsancak", city="İzmir"),
    Office(name="İstanbul Taksim", city="İstanbul")
]
db.session.add_all(offices)
db.session.commit()

cars = [
    Car(make="Renault", model="Clio", transmission="Manual", deposit=2500, mileage=1000, age_limit=21, cost_per_day=1914, image_url="https://i0.shbdn.com/photos/19/59/25/x5_1210195925mon.jpg", office_id=1),
    Car(make="Fiat", model="Egea", transmission="Manual", deposit=2500, mileage=1000, age_limit=21, cost_per_day=1963, image_url="https://i0.shbdn.com/photos/19/59/25/x5_1210195925mon.jpg", office_id=1),
    Car(make="Renault", model="Clio AT", transmission="Automatic", deposit=2500, mileage=1000, age_limit=21, cost_per_day=2179, image_url="https://i0.shbdn.com/photos/19/59/25/x5_1210195925mon.jpg", office_id=2)
]
db.session.add_all(cars)
db.session.commit()
