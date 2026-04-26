def add_room_type(hotel,room_type,price,total_room):
    if room_type in hotel.rooms:
        raise Exception("Already in room list")
    
    hotel.rooms[room_type]={
                            "price":price,
                            "total_rooms":total_room,
                            "available":total_room
                            }
    
def remove_room_type(hotel,room_type):
    if room_type not in hotel.rooms:
        raise Exception("room type is not available")
    
    del hotel.rooms[room_type]