import asyncio
from combo import Combo
class Customer:
    def __init__(self,inventory):
        
        self.inventory = inventory
        self.items_by_category = {"Burgers":[], "Sides":[], "Drinks": []}
        self.combos = []
        

    async def add_item(self,item_id):
    
        stock_number, item = await asyncio.gather(self.inventory.get_stock(item_id),self.inventory.get_item(item_id))
        
        if stock_number == 0:
            return False, item_id
        
        decrement_success = await self.inventory.decrement_stock(item_id)
        if not decrement_success:
            return False, item_id
        
        self.items_by_category[item["category"]].append(item)
        return True, item_id
    
    def arrange_order(self):
        self.get_combos()
        price = self.get_price()
        return price
        
        
    def get_price(self,):
        subtotal = 0
        if len(self.combos) != 0:
            for combo in self.combos:
                subtotal += combo.price
            
        for category in self.items_by_category.values():
            for item in category:
                subtotal += item["price"]
            
        return subtotal

    def get_combos(self):
        #sort by price
        
        self.items_by_category["Burgers"].sort(key = lambda x: x['price'])
        self.items_by_category["Sides"].sort(key = lambda x: x['price'])
        self.items_by_category["Drinks"].sort(key = lambda x: x['price'])
        while (self.items_by_category["Burgers"] and self.items_by_category["Sides"] and self.items_by_category["Drinks"]):
            burger = self.items_by_category["Burgers"].pop()
            side = self.items_by_category["Sides"].pop()
            drink = self.items_by_category["Drinks"].pop()
            combo = Combo(burger, side, drink)
            self.combos.append(combo)
            
        
    
    
    def __str__(self):
        string = ""

        for i, combo in enumerate(self.combos):
            string += str(combo)
            if i != len(self.combos) - 1:
                string += "\n"

        if len(self.combos) > 0:
            string += "\n"

        for category in self.items_by_category.values():
            for i, item in enumerate(category):
                name = item["name"] if "name" in item else item["size"]
                price = item["price"]
                subcategory = item["subcategory"]
                if subcategory == None:
                    subcategory = ""

                string += f"${price} {name} {subcategory}\n"

        return string[:-1]  # remove the last \n
    
    
    
            
        
        
        

        
        
    
    
    