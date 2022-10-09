def raise_money(user, amount):
    user.money += amount
    user.save()

def reduce_money(user, amount):
    user.money -= amount
    user.save()