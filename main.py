from service.booking_service import BookingService
from service.hotel_service import add_room_type
from models.guest import Guest
from models.hotel import Hotel

service = BookingService()

# ---------------- 1. CREATE HOTELS ----------------
h1 = Hotel(1, "Taj", "Chennai")
h2 = Hotel(2, "Oberoi", "Delhi")

service.hotels.extend([h1, h2])

# ---------------- 2. ADD ROOM TYPES ----------------
add_room_type(h1, "Deluxe", 1000, 2)
add_room_type(h1, "Suite", 2000, 1)

add_room_type(h2, "Deluxe", 1500, 1)
add_room_type(h2, "Suite", 2500, 0)  

# ---------------- 3. CREATE GUESTS ----------------
g1 = Guest(1, "John", "john@mail.com", 5000)
g2 = Guest(2, "Alice", "alice@mail.com", 500)

service.guests.extend([g1, g2])

# ---------------- 4. VALID BOOKING ----------------
print("\n--- VALID BOOKING ---")
print(service.book_room(1, 1, "Deluxe", "2026-04-20", "2026-04-22"))

# ---------------- 5. 0 AVAILABILITY ----------------
print("\n--- ZERO AVAILABILITY TEST ---")
try:
    print(service.book_room(1, 2, "Suite", "2026-04-20", "2026-04-22"))
except Exception as e:
    print("Error:", e)

# ---------------- 6. INVALID DATE ----------------
print("\n--- INVALID DATE TEST ---")
try:
    print(service.book_room(1, 1, "Deluxe", "2026-04-25", "2026-04-20"))
except Exception as e:
    print("Error:", e)

# ---------------- 7. INSUFFICIENT BALANCE ----------------
print("\n--- INSUFFICIENT BALANCE TEST ---")
try:
    print(service.book_room(2, 1, "Suite", "2026-04-20", "2026-04-25"))
except Exception as e:
    print("Error:", e)

# ---------------- 8. CANCEL BOOKING ----------------
print("\n--- CANCEL BOOKING ---")
print("Balance before:", g1.wallet_balance)
print(service.cancel_booking(1))
print("Balance after:", g1.wallet_balance)

# ---------------- 9. CANCEL COMPLETED BOOKING ----------------
print("\n--- CANCEL COMPLETED BOOKING TEST ---")
# First create another booking
print(service.book_room(1, 1, "Deluxe", "2026-04-22", "2026-04-24"))

# Complete it
service.complete_booking(2)

try:
    print(service.cancel_booking(2))
except Exception as e:
    print("Error:", e)

# ---------------- 10. COMPLETE BOOKING ----------------
print("\n--- COMPLETE BOOKING ---")
# Booking already completed above
print("Booking 2 completed")

# ---------------- 11. GUEST HISTORY ----------------
print("\n--- GUEST HISTORY ---")
for b in service.guest_history(1):
    print(b)

# ---------------- 13. SEARCH HOTELS ----------------
print("\n--- SEARCH HOTELS ---")
results = service.search_hotels("Chennai", "Deluxe")
for h in results:
    print(h)

# ---------------- 14. SAVE DATA ----------------
print("\n--- SAVING DATA ---")
service.save_data()
print("Data saved")

# ---------------- 15. LOAD DATA ----------------
print("\n--- LOADING DATA ---")
new_service = BookingService()
new_service.load_data()

print("\nLoaded Guest:")
print(new_service.guests[0])

print("\nLoaded Hotel:")
print(new_service.hotels[0])