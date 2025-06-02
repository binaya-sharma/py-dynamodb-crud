01-py-dynamodb-crud

DynamoDB CRUD with Python - Flight & Booking System

Overview

This project demonstrates basic CRUD (Create, Read, Update, Delete) operations on DynamoDB tables using Python and Boto3. It manages flights and bookings data for a simple airline ticketing system.

--------------------------------------------------------------------------------

Key DynamoDB Concepts

- Partition Key: The unique primary key attribute that DynamoDB uses to distribute and access data. Every item must have a Partition Key.

- Sort Key (Optional): Used together with the Partition Key to enable multiple items with the same Partition Key but different Sort Keys. This allows sorting and more complex queries.

- Dynamic Attributes: DynamoDB requires only Partition (and optionally Sort) Keys defined upfront. Other attributes can be added dynamically for each item, providing schema flexibility.

- Querying Limitations: Efficient queries require the Partition Key (and Sort Key if defined). Non-key attributes cannot be queried directly unless secondary indexes exist. This is why CLI queries or SDK calls require the Partition Key.

- Secondary Indexes: Global Secondary Index (GSI) and Local Secondary Index (LSI) allow querying by non-key attributes. These are not used in this project but are important for advanced use cases.

--------------------------------------------------------------------------------

DynamoDB Table Setup

Flights Table (py_dynamodb_crud_flights)

--> Partition Key: flight_id (String)

--> Other Attributes: origin, arrival_time, departure_time, destination, price, seats_available

Bookings Table (py_dynamodb_crud_bookings)

--> Partition Key: booking_id (String)

--> Other Attributes: passenger_name, flight_id, seat_number, status

--------------------------------------------------------------------------------

Create Tables Using AWS CLI

Run these commands to create your tables:

<pre>
```bash
aws dynamodb create-table \
  --table-name py_dynamodb_crud_flights \
  --attribute-definitions AttributeName=flight_id,AttributeType=S \
  --key-schema AttributeName=flight_id,KeyType=HASH \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
  --region ap-south-1

aws dynamodb create-table \
  --table-name py_dynamodb_crud_bookings \
  --attribute-definitions AttributeName=booking_id,AttributeType=S \
  --key-schema AttributeName=booking_id,KeyType=HASH \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
  --region ap-south-1
  ```
</pre>


--------------------------------------------------------------------------------

Python API Functionality Explained

Flights Table APIs:

--> create_flight(flight_id, origin, arrival_time, departure_time, destination, price, seats_available)
  Inserts a new flight record. Fails if flight_id already exists (due to condition expression).

--> get_flight(flight_id)
  Retrieves flight details by flight_id. Returns None if not found.

--> update_flight_times(flight_id, new_departure_time, new_arrival_time)
  Updates departure and arrival times for a flight.

--> delete_flight(flight_id)
  Deletes a flight record by flight_id.

--------------------------------------------------------------------------------

Bookings Table APIs:

--> create_booking(booking_id, passenger_name, flight_id, seat_number, status='confirmed')
  Inserts a new booking. Prevents overwriting if booking_id exists.

--> get_booking(booking_id)
  Retrieves booking details by booking_id.

--> update_booking_status(booking_id, new_status)
  Updates the booking status (e.g., confirmed, canceled).

--> delete_booking(booking_id)
  Deletes a booking record.

--------------------------------------------------------------------------------

Why Only Partition and Sort Keys Are Required

DynamoDB tables must have Partition Keys to uniquely identify and distribute data internally. Sort Keys enable ordering within partitions. Other attributes do not require a predefined schema, allowing flexible and evolving data structures.

AWS CLI and API queries rely on keys because DynamoDB’s internal storage and indexing are optimized for key-based access. Querying non-key attributes requires secondary indexes.

--------------------------------------------------------------------------------

How to Run

1. Configure AWS CLI with credentials having DynamoDB permissions.
2. Create DynamoDB tables using the CLI commands above.
3. Run your Python script:

python dynamodb_crud.py

This will perform CRUD operations and print output.

--------------------------------------------------------------------------------

Additional Notes

--> Use conditional expressions (like attribute_not_exists) to avoid unintentionally overwriting items.

--> Queries require Partition Key and optionally Sort Key for efficient access. Scans should be avoided on large tables.

--> You can extend this project with error handling, pagination, secondary indexes, and integration with REST APIs or frameworks like Flask or FastAPI.

--------------------------------------------------------------------------------

### About DynamoDB API (Boto3) Used

```text
API Method     Purpose                   Description
--------------------------------------------------------------
put_item()     Create or replace item    Inserts a new item; with ConditionExpression prevents overwrite
get_item()     Retrieve an item by key   Returns the item if it exists
update_item()  Modify attributes         Updates attributes atomically
delete_item()  Remove an item by key     Deletes the item if it exists
