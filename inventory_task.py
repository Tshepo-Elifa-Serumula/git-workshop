#========The beginning of the class==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        '''
        In this function, you must initialise the following attributes:
            ● country,
            ● code,
            ● product,
            ● cost, and
            ● quantity

        '''
        self.country = country
        self.code = code
        self.product = product
        self.cost = int(cost)
        self.quantity = int(quantity)
    '''
    I've found the get_quantity and get_cost functions in the class useless in this situation because
    the review told me to use them in a way that python did not allow as it would cause an error. I do understand
    the use of the functions in the template
    '''
    def __str__(self):
        '''
        Add a code to returns a string representation of a class.
        '''
        return f"Country: {self.country}\nCode: {self.code}\nProduct: {self.product}\nCost: {self.cost}\nQuantity: {self.quantity}\n"


#=============Shoe list===========
'''
The list will be used to store a list of objects of shoes.
'''

inventory = []

shoe_list = []

quantity = []

code_list = []

cost_list = []

def file_seperate(line):
    return line.strip().split(",")


#==========Functions outside the class==============
def read_shoes_data():
    '''
    This function will open the file inventory.txt
    and read the data from this file, then create a shoes object with this data
    and append this object into the shoes list. One line in this file represents
    data to create one object of shoes. You must use the try-except in this function
    for error handling. Remember to skip the first line using your code.
    '''
    inventory.clear()
    with open("inventory.txt", "r") as file:
        next(file)
        try:
            for line in file:
                temp = file_seperate(line)
                if len(temp) == 5:
                    inventory.append(Shoe(temp[0], temp[1], temp[2], temp[3], temp[4]))
        except UnicodeDecodeError:
            pass


def capture_shoes():
    '''
    This function will allow a user to capture data
    about a shoe and use this data to create a shoe object
    and append this object inside the shoe list.
    '''
    product = []
    order_country = input("Please enter the country: ")

    order_country_upper = order_country[0:1].upper()
    order_country = order_country_upper + order_country[1:len(order_country)]

    order_code = input("Please enter the code: ")
    order_product = input("Please enter the product: ")

    product_split = order_product.split()
    for split in range(len(product_split)):
        upper_product = product_split[split][0:1].upper()
        order_product = upper_product + product_split[split][1:len(product_split[split])]
        product.append(order_product)
    order_product = " ".join(product)

    read_shoes_data()
    for idx in range(len(inventory)):
        if order_product == inventory[idx].product:
            order_cost = inventory[idx].cost
            order_quantity = inventory[idx].quantity
            break
    if order_product != inventory[idx].product:
        order_cost = input("Please enter the cost of the product: $")
        order_quantity = input("Please enter how much inventory that product has: ")

    with open('inventory.txt', 'a') as file:
        file.write(f"\n{order_country},{order_code},{order_product},{order_cost},{order_quantity}")
    print("The order has successfully been added")


def view_all():
    '''
    This function will iterate over the shoes list and
    print the details of the shoes returned from the __str__
    function. Optional: you can organise your data in a table format
    by using Python’s tabulate module.
    '''
    read_shoes_data()
    for idx in range(len(inventory)):
        print(inventory[idx])


def re_stock(silent=True):
    '''
        This function will find the shoe object with the lowest quantity,
        which is the shoes that need to be re-stocked. Ask the user if they
        want to add this quantity of shoes and then update it.
        This quantity should be updated on the file for this shoe.
    '''
    read_shoes_data()
    quantity = min(inventory, key=lambda s: s.quantity)

    if not silent:
        print(f"Product: {quantity.product}\nQuantity: {quantity.quantity}")
        quantity_add = int(input("How much do you want to add?(Please enter a number): "))

        with open('inventory.txt', 'w') as file:
            for shoe in inventory:
                if shoe.product == quantity.product:
                    shoe.quantity = str(quantity_add + quantity.quantity)
            file.write("Country,Code,Product,Cost,Quantity\n")
            for line in inventory:
                file.write(f"{line.country},{line.code},{line.product},{line.cost},{line.quantity}\n")
    return


def search_shoe(silent=True):
    code_list.clear()
    shoe_list.clear()
    read_shoes_data()
    for idx in range(len(inventory)):
        code_list.append(inventory[idx].code)
        shoe_list.append(inventory[idx].product)
        shoe_codes = dict(zip(code_list, shoe_list))
    if not silent:
        code_input = input("Please enter the code: ")
        for key in shoe_codes:
            if code_input == key:
                print(f"Order: {shoe_codes[key]}")
                break
        else:
            print("That order does not exist")
    return


def value_per_item(silent=True):
    cost_list.clear()
    quantity.clear()
    read_shoes_data()
    for idx in range(len(inventory)):
        cost_list.append(inventory[idx].cost)
        quantity.append(inventory[idx].quantity)
        cost_qunty = [a * b for a, b in zip(quantity, cost_list)]
    if not silent:
        search_shoe(True)
        final_print = list(zip(shoe_list, cost_list, quantity, cost_qunty))
        for shoe in final_print:
            print(f"Product: {shoe[0]}/Price: {shoe[1]}/Quantity: {shoe[2]}\nTotal: {shoe[3]}")
    return


def highest_qty():
    value_per_item(True)
    read_shoes_data()
    max_qunty = max(quantity)

    for idx in range(len(inventory)):
        if inventory[idx].quantity == max_qunty:
            print(f"Product: {inventory[idx].product}/Quantity: {inventory[idx].quantity}/Price: {inventory[idx].cost}")

            discount_input = int(input("Please enter the dicount amount(Enter a number): "))

            discount = float(inventory[idx].cost) * (discount_input / 100)
            new_price = float(inventory[idx].cost) - discount
            inventory[idx].cost = "{:.2f}".format(new_price)

            with open("inventory.txt", "w") as file:
                for shoe in inventory:
                    if shoe.product == inventory[idx].product:
                        shoe.cost = inventory[idx].cost
                file.write("Country,Code,Product,Cost,Quantity\n")
                for line in inventory:
                    file.write(f"{line.country},{line.code},{line.product},{line.cost},{line.quantity}\n")
            print(f"New price:\nProduct: {inventory[idx].product}/Price: {inventory[idx].cost}")
            break




def menu_options():
    print("1: View all inventory\n"
            "2: Add a new order\n"
            "3: View the value per item\n"
            "4: Search an order by code\n"
            "5: Add inventory\n"
            "6: Post a discount on the highest inventory\n"
            "7: Exit")
    user_input = int(input("What would you like to do?(Please enter a number): "))
    return user_input


def Menu():
    answer = menu_options()

    while answer != int:
        if answer == 1:
            print("\n")
            view_all()
            answer = menu_options()
        elif answer == 2:
            print("\n")
            capture_shoes()
            answer = menu_options()
        elif answer == 3:
            print("\n")
            value_per_item(False)
            print("\n")
            answer = menu_options()
        elif answer == 4:
            print("\n")
            search_shoe(False)
            print("\n")
            answer = menu_options()
        elif answer == 5:
            print("\n")
            re_stock(False)
            answer = menu_options()
        elif answer == 6:
            print("\n")
            highest_qty()
            answer = menu_options()
        else:
            exit


Menu()
