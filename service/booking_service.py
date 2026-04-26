from datetime import datetime
from service.guest_service import *
from models.booking import Booking
from models.guest import Guest
from models.hotel import Hotel
import json


class BookingService:
    def __init__(self):
        self.guests = []
        self.hotels = []
        self.bookings = []

    # ---------------- FIND METHODS ----------------
    def find_guest(self, guest_id):
        for g in self.guests:
            if g.id == guest_id:
                return g
        raise Exception("Guest not found")

    def find_hotel(self, hotel_id):
        for h in self.hotels:
            if h.id == hotel_id:
                return h
        raise Exception("Hotel not found")

    def find_booking(self, booking_id):
        for b in self.bookings:
            if b.id == booking_id:
                return b
        raise Exception("Booking not found")

    # ---------------- BOOK ROOM ----------------
    def book_room(self, guest_id, hotel_id, room_type, check_in, check_out):
        guest = self.find_guest(guest_id)
        hotel = self.find_hotel(hotel_id)

        check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d")

        if check_out_date <= check_in_date:
            raise Exception("Invalid dates")

        if room_type not in hotel.rooms:
            raise Exception("Room type not available")

        if hotel.rooms[room_type]["available"] == 0:
            raise Exception("No rooms available")

        nights = (check_out_date - check_in_date).days
        total_price = hotel.rooms[room_type]["price"] * nights

        deduct_wallet_balance(guest,total_price)
        hotel.rooms[room_type]["available"] -= 1

        booking_id = len(self.bookings) + 1
        booking = Booking(
            booking_id, guest, hotel, room_type,
            check_in, check_out, nights
        )

        self.bookings.append(booking)
        guest.booking_history.append(booking_id)

        return f"Booking successful! ID: {booking_id}"

    # ---------------- CANCEL BOOKING ----------------
    def cancel_booking(self, booking_id):
        booking = self.find_booking(booking_id)

        if booking.status != "confirmed":
            raise Exception("Cannot cancel this booking")

        refund = booking.get_total(booking.hotel,booking.room_type,booking.night)
        add_wallet_balance(booking.guest,refund)

        booking.hotel.rooms[booking.room_type]["available"] += 1
        booking.status = "cancelled"

        return f"Booking {booking_id} cancelled successfully"

    # ---------------- COMPLETE BOOKING ----------------
    def complete_booking(self, booking_id):
        booking = self.find_booking(booking_id)

        if booking.status != "confirmed":
            raise Exception("Cannot complete this booking")

        booking.status = "completed"

    # ---------------- GUEST HISTORY ----------------
    def guest_history(self, guest_id):
        return [str(b) for b in self.bookings if b.guest.id == guest_id]

    # ---------------- SEARCH HOTELS ----------------
    def search_hotels(self, location, room_type):
        return [
            h for h in self.hotels
            if h.location == location and room_type in h.rooms
        ]

    # ---------------- SAVE DATA ----------------
    def save_data(self):
        # Guests
        with open("data/guests.json", "w") as f:
            json.dump([
                {
                    "id": g.id,
                    "name": g.name,
                    "email": g.email,
                    "wallet_balance": g.wallet_balance,
                    "booking_history": g.booking_history
                } for g in self.guests
            ], f, indent=4)

        # Hotels
        with open("data/hotels.json", "w") as f:
            json.dump([
                {
                    "id": h.id,
                    "name": h.name,
                    "location": h.location,
                    "rooms": h.rooms,
                    "rating": h.rating
                } for h in self.hotels
            ], f, indent=4)

        # Bookings
        with open("data/bookings.json", "w") as f:
            json.dump([
                {
                    "id": b.id,
                    "guest_id": b.guest.id,
                    "hotel_id": b.hotel.id,
                    "room_type": b.room_type,
                    "check_in": b.check_in,
                    "check_out": b.check_out,
                    "nights": b.night,
                    "status": b.status
                } for b in self.bookings
            ], f, indent=4)

    # ---------------- LOAD DATA ----------------
    def load_data(self):
        self.guests = []
        self.hotels = []
        self.bookings = []

        # -------- LOAD GUESTS --------
        try:
            with open("data/guests.json", "r") as f:
                guests_data = json.load(f)
                for g in guests_data:
                    guest = Guest(
                        g["id"],
                        g["name"],
                        g["email"],
                        g["wallet_balance"]
                    )
                    guest.booking_history = g.get("booking_history", [])
                    self.guests.append(guest)
        except FileNotFoundError:
            print("guests.json not found")

        # -------- LOAD HOTELS --------
        try:
            with open("data/hotels.json", "r") as f:
                hotels_data = json.load(f)
                for h in hotels_data:
                    hotel = Hotel(
                        h["id"],
                        h["name"],
                        h["location"]
                    )
                    hotel.rooms = h.get("rooms", {})
                    hotel.rating = h.get("rating", 0)
                    self.hotels.append(hotel)
        except FileNotFoundError:
            print("hotels.json not found")

        # -------- LOAD BOOKINGS --------
        try:
            with open("data/bookings.json", "r") as f:
                bookings_data = json.load(f)
                for b in bookings_data:
                    guest = self.find_guest(b["guest_id"])
                    hotel = self.find_hotel(b["hotel_id"])

                    booking = Booking(
                        b["id"],
                        guest,
                        hotel,
                        b["room_type"],
                        b["check_in"],
                        b["check_out"],
                        b["nights"]
                    )

                    booking.status = b.get("status", "confirmed")
                    self.bookings.append(booking)

        except FileNotFoundError:
            print("bookings.json not found")