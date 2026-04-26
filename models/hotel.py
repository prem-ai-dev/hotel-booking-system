class Hotel:
    def __init__(self,id,name,city):
        self.id=id
        self.name=name
        self.location=city
        self.rooms={}
        self.rating=0
    
    def __str__(self):
        return (f"Hotel Name : {self.name}\nHotel Location : {self.location}\nHotel Rating : {self.rating}")