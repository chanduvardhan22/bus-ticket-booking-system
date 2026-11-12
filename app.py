import json
import os


# =========================
# BUS CLASS
# =========================
class Bus:
    def __init__(self, bus_id, name, source, destination, fare, total_seats=20):
        self.bus_id = bus_id
        self.name = name
        self.source = source
        self.destination = destination
        self.fare = fare
        self.total_seats = total_seats
        self.booked_seats = set()

    def available_seats(self):
        return self.total_seats - len(self.booked_seats)

    def display(self):
        print(
            f"{self.bus_id} | {self.name} | "
            f"{self.source} -> {self.destination} | "
            f"₹{self.fare} | Available: {self.available_seats()}"
        )


# =========================
# PASSENGER CLASS
# =========================
class Passenger:
    def __init__(self, name, age, phone):
        self.name = name
        self.age = age
        self.phone = phone


# =========================
# BOOKING CLASS
# =========================
class Booking:
    def __init__(self, booking_id, passenger, bus_id, seat_number):
        self.booking_id = booking_id
        self.passenger = passenger
        self.bus_id = bus_id
        self.seat_number = seat_number

    def display_ticket(self, bus):
        print("\n" + "=" * 40)
        print("              BUS TICKET")
        print("=" * 40)
        print(f"Booking ID  : {self.booking_id}")
        print(f"Passenger   : {self.passenger.name}")
        print(f"Age         : {self.passenger.age}")
        print(f"Phone       : {self.passenger.phone}")
        print(f"Bus ID      : {bus.bus_id}")
        print(f"Bus Name    : {bus.name}")
        print(f"From        : {bus.source}")
        print(f"To          : {bus.destination}")
        print(f"Seat Number : {self.seat_number}")
        print(f"Fare        : ₹{bus.fare}")
        print("=" * 40)


# =========================
# RESERVATION SYSTEM CLASS
# =========================
class BusReservationSystem:
    def __init__(self):
        self.buses = {}
        self.bookings = {}

        self.load_buses()
        self.load_bookings()

    # -------------------------
    # CREATE BUSES
    # -------------------------
    def load_buses(self):
        self.buses = {
            "B101": Bus(
                "B101",
                "Bangalore Express",
                "Bangalore",
                "Kadiri",
                450
            ),
            "B102": Bus(
                "B102",
                "Rayalaseema Travels",
                "Bangalore",
                "Kadiri",
                500
            ),
            "B103": Bus(
                "B103",
                "Andhra Super Fast",
                "Bangalore",
                "Hyderabad",
                700
            )
        }

    # -------------------------
    # LOAD BOOKINGS FROM FILE
    # -------------------------
    def load_bookings(self):
        if not os.path.exists("bookings.json"):
            return

        try:
            with open("bookings.json", "r") as file:
                data = json.load(file)

            for booking_data in data:
                passenger = Passenger(
                    booking_data["name"],
                    booking_data["age"],
                    booking_data["phone"]
                )

                booking = Booking(
                    booking_data["booking_id"],
                    passenger,
                    booking_data["bus_id"],
                    booking_data["seat_number"]
                )

                self.bookings[booking.booking_id] = booking

                # Mark seat as booked
                bus = self.buses.get(booking.bus_id)

                if bus:
                    bus.booked_seats.add(booking.seat_number)

        except (json.JSONDecodeError, KeyError, TypeError):
            print("Error reading bookings.json")

    # -------------------------
    # SAVE BOOKINGS
    # -------------------------
    def save_bookings(self):
        data = []

        for booking in self.bookings.values():
            data.append({
                "booking_id": booking.booking_id,
                "name": booking.passenger.name,
                "age": booking.passenger.age,
                "phone": booking.passenger.phone,
                "bus_id": booking.bus_id,
                "seat_number": booking.seat_number
            })

        with open("bookings.json", "w") as file:
            json.dump(data, file, indent=4)

    # -------------------------
    # VIEW BUSES
    # -------------------------
    def view_buses(self):
        print("\n" + "=" * 75)
        print("                           AVAILABLE BUSES")
        print("=" * 75)

        for bus in self.buses.values():
            bus.display()

    # -------------------------
    # SEARCH BUS
    # -------------------------
    def search_bus(self):
        source = input("Enter source: ").strip().lower()
        destination = input("Enter destination: ").strip().lower()

        found = False

        print("\nSearch Results")
        print("-" * 75)

        for bus in self.buses.values():
            if (
                bus.source.lower() == source
                and bus.destination.lower() == destination
            ):
                bus.display()
                found = True

        if not found:
            print("No buses found.")

    # -------------------------
    # VIEW SEATS
    # -------------------------
    def view_seats(self):
        bus_id = input("Enter Bus ID: ").strip().upper()

        if bus_id not in self.buses:
            print("Invalid Bus ID.")
            return

        bus = self.buses[bus_id]

        print(f"\nSeats for {bus.name}")
        print("-" * 50)

        for seat in range(1, bus.total_seats + 1):
            if seat in bus.booked_seats:
                print(f"Seat {seat}: BOOKED")
            else:
                print(f"Seat {seat}: AVAILABLE")

    # -------------------------
    # GENERATE BOOKING ID
    # -------------------------
    def generate_booking_id(self):
        number = 1001

        while f"T{number}" in self.bookings:
            number += 1

        return f"T{number}"

    # -------------------------
    # BOOK TICKET
    # -------------------------
    def book_ticket(self):
        bus_id = input("Enter Bus ID: ").strip().upper()

        if bus_id not in self.buses:
            print("Invalid Bus ID.")
            return

        bus = self.buses[bus_id]

        print(f"\nBus: {bus.name}")
        print(f"Route: {bus.source} -> {bus.destination}")
        print(f"Fare: ₹{bus.fare}")

        # Passenger details
        name = input("Enter passenger name: ").strip()

        if not name:
            print("Name cannot be empty.")
            return

        try:
            age = int(input("Enter passenger age: "))

            if age <= 0:
                print("Age must be greater than 0.")
                return

        except ValueError:
            print("Age must be a number.")
            return

        phone = input("Enter phone number: ").strip()

        if not phone.isdigit() or len(phone) != 10:
            print("Enter a valid 10-digit phone number.")
            return

        # Seat selection
        try:
            seat = int(input(f"Enter seat number (1-{bus.total_seats}): "))

            if seat < 1 or seat > bus.total_seats:
                print("Invalid seat number.")
                return

        except ValueError:
            print("Seat number must be a number.")
            return

        # Check whether seat is already booked
        if seat in bus.booked_seats:
            print("Sorry, this seat is already booked.")
            return

        # Create passenger
        passenger = Passenger(name, age, phone)

        # Generate booking ID
        booking_id = self.generate_booking_id()

        # Create booking
        booking = Booking(
            booking_id,
            passenger,
            bus_id,
            seat
        )

        # Save in dictionary
        self.bookings[booking_id] = booking

        # Mark seat as booked
        bus.booked_seats.add(seat)

        # Save to file
        self.save_bookings()

        print("\nBooking successful!")

        booking.display_ticket(bus)

    # -------------------------
    # CANCEL TICKET
    # -------------------------
    def cancel_ticket(self):
        booking_id = input("Enter Booking ID: ").strip().upper()

        if booking_id not in self.bookings:
            print("Booking not found.")
            return

        booking = self.bookings[booking_id]

        bus = self.buses.get(booking.bus_id)

        if bus:
            bus.booked_seats.discard(booking.seat_number)

        del self.bookings[booking_id]

        self.save_bookings()

        print("Ticket cancelled successfully.")

    # -------------------------
    # VIEW BOOKING
    # -------------------------
    def view_booking(self):
        booking_id = input("Enter Booking ID: ").strip().upper()

        if booking_id not in self.bookings:
            print("Booking not found.")
            return

        booking = self.bookings[booking_id]

        bus = self.buses.get(booking.bus_id)

        if bus:
            booking.display_ticket(bus)

    # -------------------------
    # VIEW ALL BOOKINGS
    # -------------------------
    def view_all_bookings(self):
        if not self.bookings:
            print("\nNo bookings available.")
            return

        print("\n" + "=" * 60)
        print("                    ALL BOOKINGS")
        print("=" * 60)

        for booking in self.bookings.values():
            print(
                f"Booking ID: {booking.booking_id} | "
                f"Passenger: {booking.passenger.name} | "
                f"Bus: {booking.bus_id} | "
                f"Seat: {booking.seat_number}"
            )

    # -------------------------
    # MAIN MENU
    # -------------------------
    def run(self):
        while True:
            print("\n")
            print("=" * 45)
            print("        BUS RESERVATION SYSTEM")
            print("=" * 45)

            print("1. View Buses")
            print("2. Search Bus")
            print("3. View Seats")
            print("4. Book Ticket")
            print("5. Cancel Ticket")
            print("6. View Booking")
            print("7. View All Bookings")
            print("8. Exit")

            try:
                choice = int(input("\nEnter your choice: "))

            except ValueError:
                print("Please enter a number.")
                continue

            if choice == 1:
                self.view_buses()

            elif choice == 2:
                self.search_bus()

            elif choice == 3:
                self.view_seats()

            elif choice == 4:
                self.book_ticket()

            elif choice == 5:
                self.cancel_ticket()

            elif choice == 6:
                self.view_booking()

            elif choice == 7:
                self.view_all_bookings()

            elif choice == 8:
                print("Thank you for using the Bus Reservation System!")
                break

            else:
                print("Invalid choice.")


# =========================
# PROGRAM START
# =========================

system = BusReservationSystem()
system.run()