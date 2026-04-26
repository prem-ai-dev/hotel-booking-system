def add_wallet_balance(guest,amount):
    if amount < 0:
         raise Exception("wallet amount cannot be negative")
    
    guest.wallet_balance += amount

def deduct_wallet_balance(guest,amount):
    if amount > guest.wallet_balance:
        raise Exception("Insufficent balance")
    
    guest.wallet_balance -= amount