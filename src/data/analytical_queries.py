import psycopg2
from config import config
from datetime import datetime

# Python function that prints out the flights table rows ordered by departure time
def print_flights_ordered_by_departure_time():
    try:
        con = psycopg2.connect(**config())
        cursor = con.cursor()

        # Fetch all rows from Flights table ordered by departure_time
        cursor.execute("SELECT * FROM Flights ORDER BY departure_time;")
        flights = cursor.fetchall()

        # Print out and clean the columns etc
        print("Flights ordered by departure_time:")
        print(f"{'ID':<5} {'Flight Number':<15} {'Departure Time':<25} {'Arrival Time':<25} {'Departure Airport':<20} {'Destination Airport':<20}")
        print("-" * 115)

        for flight in flights:
            # Format departure and arrival times from date and time objects to strings
            departure_time = flight[2].strftime("%Y-%m-%d %H:%M:%S")
            arrival_time = flight[3].strftime("%Y-%m-%d %H:%M:%S")
            print(f"{flight[0]:<5} {flight[1]:<15} {departure_time:<25} {arrival_time:<25} {flight[4]:<20} {flight[5]:<20}")

        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if con is not None:
            con.close()
