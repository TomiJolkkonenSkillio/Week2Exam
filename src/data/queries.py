import psycopg2
from config import config
from database_population import randomize_data
from analytical_queries import print_flights_ordered_by_departure_time
from datetime import datetime

# @Tomi Jolkkonen Week 2 Exercise
# Task 1: Creating a new database was done with CLI and psql -U postgres, CREATE TABLE assesment
# Task 4. new database is added to database.ini and used through config.py

def database_design():
    con = None
    try:
        con = psycopg2.connect(**config())
        cursor = con.cursor()

        # Task 2 and 3: Database design and inserting 3 rows
        SQL_CREATE_TABLE = '''
        -- Create table Flights
        CREATE TABLE IF NOT EXISTS Flights (
            id SERIAL PRIMARY KEY,
            flight_number varchar(255) NOT NULL,
            departure_time timestamp NOT NULL,
            arrival_time timestamp NOT NULL,
            departure_airport varchar(255) NOT NULL,
            destination_airport varchar(255) NOT NULL
        );
        '''
        cursor.execute(SQL_CREATE_TABLE)

        # Check if the unique constraint already exists
        cursor.execute("""
        SELECT 1
        FROM information_schema.table_constraints
        WHERE table_name = 'flights'
          AND constraint_name = 'unique_flight';
        """)
        if not cursor.fetchone():
            # Add unique constraint
            cursor.execute("""
            ALTER TABLE Flights ADD CONSTRAINT unique_flight UNIQUE (flight_number, departure_time);
            """)

        # Insert 3 rows with ON CONFLICT handling
        SQL_INSERT_ROWS = '''
        INSERT INTO Flights (flight_number, departure_time, arrival_time, departure_airport, destination_airport)
        VALUES
            ('FL123', '2025-01-25 08:00:00', '2025-01-25 10:30:00', 'JFK', 'LAX'),
            ('FL456', '2025-01-26 14:15:00', '2025-01-26 16:45:00', 'ORD', 'ATL'),
            ('FL789', '2025-01-27 22:00:00', '2025-01-28 01:00:00', 'LHR', 'CDG')
        ON CONFLICT (flight_number, departure_time) DO NOTHING;
        '''
        cursor.execute(SQL_INSERT_ROWS)

        con.commit()
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if con is not None:
            con.close()

def main():
    # Uncomment the following line to create the table and insert 3 rows, randomize data, or print out values
    # database_design()
    # randomize_data(15)  # Task 5. Randomizing data 3 times to tables with faker, from file database_population.py 
    # randomize_data(7)
    # randomize_data(8)
    # print_flights_ordered_by_departure_time()  # Task 6. Printing out flights ordered by departure_time, from file analytical_queries.py

if __name__ == "__main__":
    main()
