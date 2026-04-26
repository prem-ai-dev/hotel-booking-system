class Booking:
    def __init__(self,id,guest,hotel,room_type,check_in,check_out,night):
        self.id=id
        self.guest=guest
        self.hotel=hotel
        self.room_type=room_type
        self.check_in=check_in
        self.check_out=check_out
        self.night=night
        self.status="confirmed"
    
    def __str__(self):
        return (f"Booking Id : {self.id}\n"
                f"Customer Name : {self.guest.name}\n"
                f"Hotel Name : {self.hotel.name}\n"
                f"Room Type : {self.room_type}\n"
                f"Status : {self.status}")
    
    def get_total(self,hotel,room_type,nights):
        total_price= hotel.rooms[room_type]["price"]*nights
        return total_price