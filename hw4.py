
import unittest

# The Customer class
# The Customer class represents a customer who will order from the stalls.
class Customer: 
    # Constructor
    def __init__(self, name, wallet = 100):
        self.name = name
        self.wallet = wallet

    # Reload some deposit into the customer's wallet.
    def reload_money(self,deposit):
        self.wallet += deposit

    # The customer orders the food and there could be different cases   
    def validate_order(self, cashier, stall, item_name, quantity):
        if not(cashier.has_stall(stall)):
            print("Sorry, we don't have that vendor stall. Please try a different one.")
        elif not(stall.has_item(item_name, quantity)):  
            print("Our stall has run out of " + item_name + " :( Please try a different stall!")
        elif self.wallet < stall.compute_cost(quantity): 
            print("Don't have enough money for that :( Please reload more money!")
        else:
            bill = cashier.place_order(stall, item_name, quantity) 
            self.submit_order(cashier, stall, bill) 
    
    # Submit_order takes a cashier, a stall and an amount as parameters, 
    # it deducts the amount from the customer’s wallet and calls the receive_payment method on the cashier object
    def submit_order(self, cashier, stall, amount): 
        self.wallet -= amount
        cashier.receive_payment(stall,amount)


    # The __str__ method prints the customer's information.    
    def __str__(self):
        return "Hello! My name is " + self.name + ". I have $" + str(self.wallet) + " in my payment card."


# The Cashier class
# The Cashier class represents a cashier at the market. 
class Cashier:

    # Constructor
    def __init__(self, name, directory =[]):
        self.name = name
        self.directory = directory[:] # make a copy of the directory

    # Whether the stall is in the cashier's directory
    def has_stall(self, stall):
        return stall in self.directory

    # Adds a stall to the directory of the cashier.
    def add_stall(self, new_stall):
        self.directory.append(new_stall)

    # Receives payment from customer, and adds the money to the stall's earnings.
    def receive_payment(self, stall, money):
        stall.earnings += money

    # Places an order at the stall.
	# The cashier pays the stall the cost.
	# The stall processes the order
	# Function returns cost of the order, using compute_cost method
    def place_order(self, stall, item, quantity):
        stall.process_order(item, quantity)
        return stall.compute_cost(quantity) 
    
    # string function.
    def __str__(self):

        return "Hello, this is the " + self.name + " cashier. We take preloaded market payment cards only. We have " + str(sum([len(category) for category in self.directory.values()])) + " vendors in the farmers' market."

## Complete the Stall class here following the instructions in HW_4_instructions_rubric
class Stall:
    def __init__(self,name,inventory,cost=7,earnings=0):
        self.name = name
        self.inventory = inventory
        self.cost = cost
        self.earnings = earnings

    def process_order(self,name,quantity):
        for key in self.inventory:
            if name == key:
                if quantity < self.inventory[key]:
                    self.inventory[key] -= quantity
        self.earnings += self.compute_cost(quantity)

    def has_item(self,name,quantity):
        for k,v in self.inventory.items():
            if k == name and v >= quantity:
                return True
        return False


    def stock_up(self,name,quantity):
        if name in self.inventory.keys():
            self.inventory[name] += quantity
        else:
            self.inventory[name] = quantity


    def compute_cost(self,quantity):
        return self.cost * quantity

    def __str__(self):
        return "Hello, we are " + self.name + ". This is the current menu " + inventory.keys() + ". We charge $" + self.cost + " per item. We have $" + self.earnings + " in total."



class TestAllMethods(unittest.TestCase):
    
    def setUp(self):
        inventory = {"Burger":40, "Taco":50}
        self.f1 = Customer("Ted")
        self.f2 = Customer("Morgan", 150)
        self.s1 = Stall("The Grill Queen", inventory, cost = 10)
        self.s2 = Stall("Tamale Train", inventory, cost = 9)
        self.s3 = Stall("The Streatery", inventory)
        self.c1 = Cashier("West")
        self.c2 = Cashier("East")
        #the following codes show that the two cashiers have the same directory
        for c in [self.c1, self.c2]:
            for s in [self.s1,self.s2,self.s3]:
                c.add_stall(s)

	## Check to see whether constructors work
    def test_customer_constructor(self):
        self.assertEqual(self.f1.name, "Ted")
        self.assertEqual(self.f2.name, "Morgan")
        self.assertEqual(self.f1.wallet, 100)
        self.assertEqual(self.f2.wallet, 150)

	## Check to see whether constructors work
    def test_cashier_constructor(self):
        self.assertEqual(self.c1.name, "West")
        #cashier holds the directory - within the directory there are three stalls
        self.assertEqual(len(self.c1.directory), 3) 

	## Check to see whether constructors work
    def test_truck_constructor(self):
        self.assertEqual(self.s1.name, "The Grill Queen")
        self.assertEqual(self.s1.inventory, {"Burger":40, "Taco":50})
        self.assertEqual(self.s3.earnings, 0)
        self.assertEqual(self.s2.cost, 9)

	# Check that the stall can stock up properly.
    def test_stocking(self):
        inventory = {"Burger": 10}
        s4 = Stall("Misc Stall", inventory)

		# Testing whether stall can stock up on items
        self.assertEqual(s4.inventory, {"Burger": 10})
        s4.stock_up("Burger", 30)
        self.assertEqual(s4.inventory, {"Burger": 40})
        
    def test_make_payment(self):
		# Check to see how much money there is prior to a payment
        previous_custormer_wallet = self.f2.wallet
        previous_earnings_stall = self.s2.earnings
        
        self.f2.submit_order(self.c1, self.s2, 30)

		# See if money has changed hands
        self.assertEqual(self.f2.wallet, previous_custormer_wallet - 30)
        self.assertEqual(self.s2.earnings, previous_earnings_stall + 30)


	# Check to see that the server can serve from the different stalls
    def test_adding_and_serving_stall(self):
        c3 = Cashier("North", directory = [self.s1, self.s2])
        self.assertTrue(c3.has_stall(self.s1))
        self.assertFalse(c3.has_stall(self.s3)) 
        c3.add_stall(self.s3)
        self.assertTrue(c3.has_stall(self.s3))
        self.assertEqual(len(c3.directory), 3)


	# Test that computed cost works properly.
    def test_compute_cost(self):
        #what's wrong with the following statements?
        #can you correct them?
        self.assertEqual(self.s1.compute_cost(5), 50)
        self.assertEqual(self.s3.compute_cost(6), 42)

	# Check that the stall can properly see when it is empty
    def test_has_item(self):
        # Set up to run test cases

        # Test to see if has_item returns True when a stall has enough items left
        # Please follow the instructions below to create three different kinds of test cases 
        # Test case 1: the stall does not have this food item:
        self.assertFalse(self.s1.has_item("Salsa",2))
        
        # Test case 2: the stall does not have enough food item:
        self.assertFalse(self.s1.has_item("Burger",41))

        
        # Test case 3: the stall has the food item of the certain quantity: 
        self.assertTrue(self.s3.has_item("Taco",1))

	# Test validate order
    def test_validate_order(self):
		# case 1: test if a customer doesn't have enough money in their wallet to order
        self.f1.validate_order(self.c1,self.s1,"Taco",11)

		# case 2: test if the stall doesn't have enough food left in stock
        self.f2.validate_order(self.c2,self.s1,"Taco",52)

		# case 3: check if the cashier can order item from that stall
        self.f1.validate_order(self.c1,self.s2,"Burger",4)

    # Test if a customer can add money to their wallet
    def test_reload_money(self):
        self.f1.reload_money(100)
        self.assertEqual(self.f1.wallet,200)
    
### Write main function
def main():
    #Create different objects 
    inv1 = {'Bagels':12, 'Eggs':6,'Sausage':2}
    inv2 = {'Pasta':8,'Pizza':14, 'Bread':4}

    customer1 = Customer('Sonali',200)
    customer2 = Customer('Sarah',250)
    customer3 = Customer('Aoife',4)
    customer4 = Customer('Abby',9)

    stall1 = Stall("Breakfast Food",inv1,5)
    stall2 = Stall("Italian",inv2,11)

    cashier1 = Cashier('Mia',[stall1,stall2])
    cashier2 = Cashier('Kenzie',[stall1])


    #Try all cases in the validate_order function
    #Below you need to have *each customer instance* try the four cases
    #case 1: the cashier does not have the stall
    customer1.validate_order(cashier2,stall2,'Pizza',1)
    customer2.validate_order(cashier2,stall2,'Pizza',1) 
    
    #case 2: the casher has the stall, but not enough ordered food or the ordered food item
    customer1.validate_order(cashier1,stall1,'Bagels',100)
    customer2.validate_order(cashier2,stall1,'Bagels',100) 
    
    #case 3: the customer does not have enough money to pay for the order: 
    customer4.validate_order(cashier1,stall2,'Pizza',3)
    customer3.validate_order(cashier1,stall2,'Pizza',2) 
    
    #case 4: the customer successfully places an order
    customer1.validate_order(cashier1,stall1,'Sausage',1)
    customer2.validate_order(cashier1,stall2,'Bread',3)


if __name__ == "__main__":
	main()
	print("\n")
	unittest.main(verbosity = 2)
