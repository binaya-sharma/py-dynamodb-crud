import boto3 as b3
dynamodb = b3.resource('dynamodb', region_name='ap-south-1')

# Tables
flights_table = dynamodb.Table('py_dynamodb_crud_flights')
bookings_table = dynamodb.Table('py_dynamodb_crud_bookings')

# FLIGHT TABLE

# Create a Flight (PutItem)
def create_flight(flight_id, origin, arrival_time, departure_time, destination, price, seats_available):
    return flights_table.put_item(
        Item={
            'flight_id': flight_id,
            'origin': origin,
            'arrival_time': arrival_time,
            'departure_time': departure_time,
            'destination': destination,
            'price': price,
            'seats_available': seats_available
        }
    )

# Read a Flight (GetItem)
def get_flight(flight_id):
    response = flights_table.get_item(Key={'flight_id': flight_id})
    return response.get('Item', None)

# Update a Flight's Times (UpdateItem)
def update_flight_times(flight_id, new_departure_time, new_arrival_time):
    return flights_table.update_item(
        Key={'flight_id': flight_id},
        UpdateExpression='SET departure_time = :dt, arrival_time = :at',
        ExpressionAttributeValues={
            ':dt': new_departure_time,
            ':at': new_arrival_time
        },
        ReturnValues='UPDATED_NEW'
    )

# Delete a Flight (DeleteItem)
def delete_flight(flight_id):
    return flights_table.delete_item(Key={'flight_id': flight_id})

#BOOKINGS TABLE

# Create a Booking (PutItem)
def create_booking(booking_id, passenger_name, flight_id, seat_number, status='confirmed'):
    return bookings_table.put_item(
        Item={
            'booking_id': booking_id,
            'passenger_name': passenger_name,
            'flight_id': flight_id,
            'seat_number': seat_number,
            'status': status
        }
    )

# Read a Booking (GetItem)
def get_booking(booking_id):
    response = bookings_table.get_item(Key={'booking_id': booking_id})
    return response.get('Item', None)

# Update Booking Status (UpdateItem)
def update_booking_status(booking_id, new_status):
    return bookings_table.update_item(
        Key={'booking_id': booking_id},
        UpdateExpression='SET #st = :s',
        ExpressionAttributeNames={'#st': 'status'},
        ExpressionAttributeValues={':s': new_status},
        ReturnValues='UPDATED_NEW'
    )

# Delete a Booking (DeleteItem)
def delete_booking(booking_id):
    return bookings_table.delete_item(Key={'booking_id': booking_id})

# DEMO TEST RUN
if __name__ == '__main__':
    # Flights CRUD Demo
    create_flight(
        'FL100', 'KTM', '2025-06-10T09:00:00',
        '2025-06-10T12:00:00', 'PKR', 4500, 120
    )
    print("Created Flight:", get_flight('FL100'))

    update_flight_times('FL100', '2025-06-10T10:00:00', '2025-06-10T13:00:00')
    print("Updated Flight Times:", get_flight('FL100'))

    # delete_flight('FL100')  

    # Bookings CRUD Demo
    create_booking('BKG200', 'Binaya Sharma', 'FL100', '2A')
    print("Created Booking:", get_booking('BKG200'))

    update_booking_status('BKG200', 'canceled')
    print("Updated Booking Status:", get_booking('BKG200'))

    # delete_booking('BKG200')  