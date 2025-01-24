-- create table Flights, database called "assesment" was created earlier w cli psql (task 1.)
-- these are not used in the actual code, but I made them here first
-- you can find these hardcoded in the main program queries.py

CREATE TABLE IF NOT EXISTS Flights ( -- using if not exists, so i can run these many times
    id SERIAL PRIMARY KEY, -- id should have automatically growing value in postgres
    flight_number varchar(255) NOT NULL, -- flight number w varchar
    departure_time timestamp NOT NULL, -- departure time w timestamp
    arrival_time timestamp NOT NULL, -- arrival time w timestamp
    departure_airport varchar(255) NOT NULL, -- departure airport w varvhar
    destination_airport varchar(255) NOT NULL -- dest airport w varchar
);