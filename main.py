import asyncio
from concurrent.futures import process
from customer import Customer
from inventory import Inventory


def display_catalogue(catalogue):
    burgers = catalogue["Burgers"]
    sides = catalogue["Sides"]
    drinks = catalogue["Drinks"]

    print("--------- Burgers -----------\n")
    for burger in burgers:
        item_id = burger["id"]
        name = burger["name"]
        price = burger["price"]
        print(f"{item_id}. {name} ${price}")

    print("\n---------- Sides ------------")
    for side in sides:
        sizes = sides[side]

        print(f"\n{side}")
        for size in sizes:
            item_id = size["id"]
            size_name = size["size"]
            price = size["price"]
            print(f"{item_id}. {size_name} ${price}")

    print("\n---------- Drinks ------------")
    for beverage in drinks:
        sizes = drinks[beverage]

        print(f"\n{beverage}")
        for size in sizes:
            item_id = size["id"]
            size_name = size["size"]
            price = size["price"]
            print(f"{item_id}. {size_name} ${price}")

    print("\n------------------------------\n")

async def take_order(num_of_items, inventory):
    customer = Customer(inventory)
    
    print("Please enter the number of items that you would like to add to your order. Enter q to complete your order")
    tasks = []
    while True:
        item_number = input("Enter an item number from the Menu: ")
        if item_number == 'q':
            break
        if not item_number.isdigit():
            print("Please enter a valid number.")
            continue
        item_number = int(item_number)
        if item_number < 1:
            print("Please enter a valid number.")
            continue
        
        if item_number > num_of_items:
            print(f"Please enter a number below {num_of_items + 1}")
            continue
        #passed invalid input checks
        '''create_task = asyncio.create_task(customer.add_item(item_number))
        tasks.append(create_task)'''
        add_to_order_task = asyncio.create_task(customer.add_item(item_number))
        tasks.append(add_to_order_task)
        
    print("Placing Order")
    for task in tasks:
        item_is_in_stock, item_id = await task
        if not item_is_in_stock:
            print(f"Unfortunately item number {item_id} is out of stock, and will be removed.")
                
    return customer
        
        
def display_order(subtotal, tax_total, total, customer_order):
    print("Here is a summary of your order:")
    print(customer_order)
    print(f"\nSubtotal:{subtotal}")
    print(f"\nTax: {tax_total}")
    print(f"\nTotal: {total}")
            


async def main():
    print("Welcome to Save More Fast Food")
    inventory = Inventory()
    catalogue = asyncio.create_task(inventory.get_catalogue())
    num_of_items = await inventory.get_number_of_items()  #will load in time before catalogue
    print("Loading the Menu....")
    #*****Does not work*****
    #await catalogue
    #display catalogue
    #***********************
    menu_loaded = await catalogue
    display_catalogue(menu_loaded)
    while True:
        customer_order = await take_order(num_of_items, inventory)
        process_order = customer_order.arrange_order()
        tax_rate = round(0.05 * process_order,2)
        
        total = round(process_order + tax_rate,2)
        print("total", total)
        display_order(process_order, tax_rate, total, customer_order)
        answer = input(f"Would you like to purchase this order for {total}. (yes/no)?")
        if answer not in ['yes','y']:
            break
        
    print("Thanks, Bye!")
        
        
    
if __name__ == "__main__":
    asyncio.run(main())
