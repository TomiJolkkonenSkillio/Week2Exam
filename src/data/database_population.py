import psycopg2
from faker import Faker
from config import config
from datetime import timedelta

fake = Faker()

def randomize_data(num_flights):
    try:
        con = psycopg2.connect(**config())
        cursor = con.cursor()

        for _ in range(num_flights):
            flight_number = fake.unique.bothify(text="FL###")  # Generate unique flight numbers
            departure_time = fake.date_time_this_year()  # Random departure time
            arrival_time = departure_time + timedelta(hours=1, minutes=30)  # Faking that arrival is 1.5 hours after departure
            departure_airport = fake.city()  # Random departure airport (fake.airport_name was not available by default in Faker library)
            destination_airport = fake.city()  # Random destination airport (same thing here, so adding cities)

            # Departure and destination airports cannot be the same
            while destination_airport == departure_airport:
                destination_airport = fake.city()

            # same code here that is hardcoded in queries.py for task 3, but now randomizing w faker
            flights_sql = '''
                INSERT INTO Flights (flight_number, departure_time, arrival_time, departure_airport, destination_airport)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (flight_number, departure_time) DO NOTHING;
            '''
            cursor.execute(flights_sql, (flight_number, departure_time, arrival_time, departure_airport, destination_airport))
        
        con.commit()
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()
