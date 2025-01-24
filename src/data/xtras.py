import psycopg2
import random
from faker import Faker
from config import config
from datetime import timedelta

fake = Faker()

def randomize_data(num_flights, num_airlines):
    try:
        con = psycopg2.connect(**config())
        cursor = con.cursor()

        # creating Flights table, checking if it exists
        create_flights_table_sql = '''
        CREATE TABLE IF NOT EXISTS Flights (
            id SERIAL PRIMARY KEY,
            flight_number varchar(255) NOT NULL,
            departure_time TIMESTAMP NOT NULL,
            arrival_time TIMESTAMP NOT NULL,
            departure_airport varchar(255) NOT NULL,
            destination_airport varchar(255) NOT NULL
        );
        '''
        cursor.execute(create_flights_table_sql)

        # xtra Task 7: Create Airlines table with a foreign key reference to Flights
        create_airlines_table_sql = '''
        CREATE TABLE IF NOT EXISTS Airlines (
            id SERIAL PRIMARY KEY,  -- id will be automatically generated
            name varchar(255) NOT NULL,
            flights_id INT NOT NULL,
            FOREIGN KEY (flights_id) REFERENCES Flights(id)  -- Creating foreign key constraint
        );
        '''
        cursor.execute(create_airlines_table_sql)

        # xtra Task 8: Inserting Airlines data
        airline_ids = []
        for _ in range(num_airlines):
            airline_name = fake.company()
            insert_airline_sql = '''
            INSERT INTO Airlines (name, flights_id)
            VALUES (%s, %s)
            RETURNING id;
            '''
            cursor.execute(insert_airline_sql, (airline_name, 1)) 
            airline_id = cursor.fetchone()[0]
            airline_ids.append(airline_id) 

        # xtra Task 9: Inserting Flights data
        flight_ids = []
        for _ in range(num_flights):
            flight_number = fake.unique.bothify(text="FL###") 
            departure_time = fake.date_time_this_year() 
            arrival_time = departure_time + timedelta(hours=1, minutes=30) 
            departure_airport = fake.city() 
            destination_airport = fake.city()

            while destination_airport == departure_airport:
                destination_airport = fake.city()

            flights_sql = '''
                INSERT INTO Flights (flight_number, departure_time, arrival_time, departure_airport, destination_airport)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;
            '''
            cursor.execute(flights_sql, (flight_number, departure_time, arrival_time, departure_airport, destination_airport))
            flight_id = cursor.fetchone()[0] 
            flight_ids.append(flight_id) 

        # xtra Task 10: Link each flight to airline
        link_flights_to_airlines(flight_ids, airline_ids, cursor)

        con.commit()
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()


def link_flights_to_airlines(flight_ids, airline_ids, cursor):
    # xtra Task 10: Insert 6 rows matching flights with airlines
    for flight_id in flight_ids[:6]: 
        airline_id = random.choice(airline_ids)
        insert_link_sql = '''
        UPDATE Airlines
        SET flights_id = %s
        WHERE id = %s;
        '''
        cursor.execute(insert_link_sql, (flight_id, airline_id))

        print(f"Flight ID {flight_id} linked to Airline ID {airline_id}")


# print flights ordered by airline
def print_flights_ordered_by_airline():
    try:
        con = psycopg2.connect(**config())
        cursor = con.cursor()

        query = '''
        SELECT f.id, f.flight_number, f.departure_time, f.arrival_time, f.departure_airport, f.destination_airport, a.name AS airline_name
        FROM Flights f
        JOIN Airlines a ON f.id = a.flights_id
        ORDER BY a.name;
        '''
        cursor.execute(query)
        flights = cursor.fetchall()

        print(f"{'ID':<5} {'Flight Number':<15} {'Departure Time':<25} {'Arrival Time':<25} {'Departure Airport':<20} {'Destination Airport':<20} {'Airline Name':<30}")
        print("-" * 150)

        for flight in flights:
            # Formatting departure and arrival times as strings
            departure_time = flight[2].strftime("%Y-%m-%d %H:%M:%S")
            arrival_time = flight[3].strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"{flight[0]:<5} {flight[1]:<15} {departure_time:<25} {arrival_time:<25} {flight[4]:<20} {flight[5]:<20} {flight[6]:<30}")

        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if con is not None:
            con.close()


# remove flight and its airline from both tables
def remove_flight_and_airline(flight_id):
    try:
        con = psycopg2.connect(**config())
        cursor = con.cursor()

        delete_airline_sql = '''
        DELETE FROM Airlines
        WHERE flights_id = %s;
        '''
        cursor.execute(delete_airline_sql, (flight_id,))

        delete_flight_sql = '''
        DELETE FROM Flights
        WHERE id = %s;
        '''
        cursor.execute(delete_flight_sql, (flight_id,))

        con.commit()
        print(f"Flight ID {flight_id} and its associated airline have been removed.")

        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if con is not None:
            con.close()


def main():
    randomize_data(15, 6)  # Randomizing data for 15 flights and 6 airlines
    print_flights_ordered_by_airline()  # Print flights ordered by airline
    
    # Example of removing a flight and its airline by passing the flight ID
    flight_id_to_remove = 5  # This is an example; change it to an actual flight ID from your data
    remove_flight_and_airline(flight_id_to_remove)

if __name__ == "__main__":
    main()
