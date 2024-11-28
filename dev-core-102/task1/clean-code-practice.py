import datetime

loyalty_program_members = ["Abdulla", "Ivan", "Jacob"]

products = [{"model": "BMW", "price": 10000}, {"model": "Mercedes", "price": 12000}, {"model": "Toyota", "price": 6000}, {"model": "Porsche", "price": 20000}, {"model": "Daewoo", "price": 1000}]

user_name_input = input('Write your name here! ')
print("Welcome,",user_name_input,",this is our current model range!")
for product in products:
    print("Model: ",product["model"]," Price: ", product["price"])
    print("---------------------------------")

user_product_input = input('Please choose your preferred model here! ')

def get_users_choice(model):
    for product in products: 
        if product["model"] == model: 
            return product["price"]
    
    print(f"Model '{model}' not found.")
    return None

def apply_basic_discount(price, discount_rate=0.05):
    return price * (1 - discount_rate)

def apply_loyalty_discount(price, loyalty_discount_rate=0.1): 
    return price * (1 - loyalty_discount_rate)

def apply_basic_tax(price, tax_rate=0.07):
    return price * (1 + tax_rate)

def apply_wildcard_tax(price, additional_tax_rate=0.03):
    current_minute = datetime.datetime.now().minute
    if current_minute % 2 == 0:
        return price
    return price * (1 + additional_tax_rate)

def calculate_final_price(client_name, initial_price):
    price_after_basic_discount = apply_basic_discount(initial_price)
    
    if client_name in loyalty_program_members:
        price_after_loyalty_discount = apply_loyalty_discount(price_after_basic_discount)
    else:
        price_after_loyalty_discount = price_after_basic_discount
    
    price_after_basic_tax = apply_basic_tax(price_after_loyalty_discount)
    
    final_price = apply_wildcard_tax(price_after_basic_tax)
    
    return round(final_price, 2)

def add_to_loyalty_program(client_name):
    if client_name not in loyalty_program_members:
        loyalty_program_members.append(client_name)
        print(f"Client {client_name} was added to loyalty program.")
    else:
        print(f"Client {client_name} is already in loyalty program.")

if __name__ == "__main__":
    client = user_name_input
    initial_price = get_users_choice(user_product_input)
    final_price = calculate_final_price(client, initial_price)
    print(f"Sum of product for client {client} is: {final_price} USD.")
    
    add_to_loyalty_program(client)