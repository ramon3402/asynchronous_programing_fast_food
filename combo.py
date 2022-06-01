class Combo:
    discount = 0.15
    def __init__(self, burger, side , drink):
        self.burger = burger
        self.side = side
        self.drink = drink
        self.price = self.price_with_discount()
        
    def price_with_discount(self):
        subtotal = self.burger['price'] + self.side['price'] + self.drink['price']
        subtotal -=  round(subtotal * Combo.discount,2)
        return subtotal
    
    
    def __str__(self):
        string = f"${self.price} Burger combo\n"
        string += f"  {self.burger['name']}\n"
        string += f"  {self.side['size']} {self.side['subcategory']}\n"
        string += f"  {self.drink['size']} {self.drink['subcategory']}"
        return string