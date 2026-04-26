class Guest:
    def __init__(self,id,name,email,balance):
        self.id=id
        self.name=name
        self.email=email
        self.wallet_balance=balance
        self.booking_history=[]
    
    def __str__(self):
        return (f"Customer Name : {self.name}\n"
                f"Customer Email : {self.email}\n"
                f"Customer Wallet Balance : {self.wallet_balance}")