
import collections #For deque to implement Queue functionality

class Wallet:
    def __init__(self,balance):
        self.balance=float(balance)

    def add_money(self,amount):
        self.balance+=amount
    def withdraw_money(self,amount):
        self.balance-=amount
    def is_desired_balance_available(self,neededAmount):
        return self.balance>=neededAmount
    def get_balance(self):
        return self.balance

class Reward:
    def __init__(self,balance):
        self.balance=float(balance)

    def add_money(self,amount):
        self.balance+=amount
    def withdraw_money(self,amount):
        self.balance-=amount
    def is_desired_balance_available(self,neededAmount):
        return self.balance>=neededAmount
    def get_balance(self):
        return self.balance

class Food:
    def __init__(self,id,name,price,quantity,discount,category,restaurant):
        self.id=id
        self.name=name
        self.price=float(price)
        self.quantity=quantity
        self.discount=float(discount)
        self.category=category
        self.restaurant=restaurant

    def edit_details(self):
        print("Choose an attribute to edit:")
        print("1) Name")
        print("2) Price")
        print("3) Quantity")
        print("4) Category")
        print("5) Offer")
        option=int(input())
        words=("name","price","quantity","category","offer")
        print("Enter the new "+words[option-1]+" - ",end="")
        if option==1:
            name=input()
            self.name=name
        elif option==2:
            price=float(input())
            self.price=price
        elif option==3:
            quantity=int(input())
            self.quantity=quantity
        elif option==4:
            category=input()
            self.category=category
        elif option==5:
            discount=float(input())
            self.discount=discount
        else:
            print("Invalid Option, no attribute modified")

    def get_id(self):
        return self.id
    def get_name(self):
        return self.name
    def get_price(self):
        return self.price
    def get_discount_rate(self):
        return self.discount
    def get_discount(self,amount):
        return (amount*self.discount)/100

    def display_details(self):
        print(str(self.id)+" "+self.name+" "+str(self.price)+" "+str(self.quantity)+" "+str(self.discount)+"% off "+self.category)
    def display_extended_details(self):
        print(str(self.id)+" "+self.restaurant.get_name()+" - "+self.name+" "+str(self.price)+" "+str(self.quantity)+" "+str(self.discount)+"% off "+self.category)
    def add_quantity(self,quantity):
        self.quantity+=quantity
    def pick_quantity(self,quantitySold):
        self.quantity-=quantitySold
    def is_desired_quantity_available(self,quantityWanted):
        return self.quantity>=quantityWanted

class Item:
    def __init__(self,id,name,quantity,rate):
        self.id=id
        self.name=name
        self.quantity=quantity
        self.rate=float(rate)

    def get_id(self):
        return self.id
    def get_quantity(self):
        return self.quantity
    def get_rate(self):
        return self.rate

    def reduce_quantity(self,quantity):
        self.quantity-=quantity
    def increase_quantity(self,quantity):
        self.quantity+=quantity

    def display_details(self):
        print("Item: ID- "+str(self.id)+" Name- "+self.name+" Quantity- "+str(self.quantity)+" Rate- "+str(self.rate))
    def display_details_detailed(self,restaurant):
        print(str(self.id)+" "+restaurant.get_name()+" - "+self.name+" - "+str(self.rate)+" - "+str(self.quantity)+" - "+str(restaurant.get_food_items()[self.id].get_discount_rate())+"% off")

class Order:
    def __init__(self,restaurant,customer,deliveryCharge):
        self.restaurant=restaurant
        self.customer=customer
        self.items={}
        self.amount=0.0
        self.deliveryCharge=float(deliveryCharge)

    def get_amount(self):
        self.calculate_amount()
        return self.amount
    def get_delivery_charge(self):
        return self.deliveryCharge
    def get_items_count(self):
        return len(self.items)

    def add_to_cart(self,id,name,quantity,rate):
        if id in self.items:
            self.increase_item_quantity(id,quantity)
        else:
            self.add_item(id,name,quantity,rate)
    def return_order(self):
        for item in self.items.values():
            self.restaurant.get_food_items()[item.get_id()].add_quantity(item.get_quantity())

    def add_item(self,id,name,quantity,rate):
        self.items[id]=Item(id,name,quantity,rate)
    def remove_item(self,id):
        self.restaurant.get_food_items()[id].add_quantity(self.items[id].get_quantity())
        del self.items[id]
    def increase_item_quantity(self,id,quantity):
        self.items[id].increase_quantity(quantity)
    def reduce_item_quantity(self,id,quantity):
        self.restaurant.get_food_items()[id].add_quantity(quantity)
        self.items[id].reduce_quantity(quantity)
        if self.items[id].get_quantity()==0:
            del self.items[id]

    def display_items_detailed(self):
        for item in self.items.values():
            item.display_details_detailed(self.restaurant)
    def display_items(self):
        for item in self.items.values():
            item.display_details()

    def display_details(self):
        print("Restaurant- "+self.restaurant.get_name()+" | "+" Amount- "+str(self.amount)+" | "+" Delivery Charge- "+str(self.deliveryCharge))
        self.display_items()

    def calculate_amount(self):
        self.amount=0
        for id in self.items.keys():
            itemAmount=self.items[id].get_quantity()*self.items[id].get_rate()
            itemAmount-=self.restaurant.get_food_items()[id].get_discount(itemAmount)
            self.amount+=itemAmount
        self.amount-=self.restaurant.get_overall_bill_discount(self.amount)
        self.amount-=self.restaurant.get_off(self.amount)
        self.amount-=self.customer.get_off(self.amount)


class Customer:
    uniqueId=1
    def __init__(self,name,address,amount,category="NA",deliveryCharge=40):
        self.id=Customer.uniqueId
        Customer.uniqueId+=1
        self.name=name
        self.address=address
        self.deliveryCharge=float(deliveryCharge)
        self.category=category
        self.walletAccount=Wallet(amount)
        self.rewardAccount=Reward(0)
        self.currentRestaurant=None
        self.currentOrder=None
        self.recentOrders=collections.deque()

    def get_id(self):
        return self.id
    def get_name(self):
        return self.name
    def display_details(self):
        print(self.name+("" if self.category=="NA" else ("("+self.category+")"))+", "+self.address+", "+str(self.walletAccount.get_balance())+"/-")
    def display_brief(self):
        print(str(self.id)+") "+self.name+("" if self.category=="NA" else (" ("+self.category+")")))
    def gain_reward(self,reward):
        self.rewardAccount.add_money(reward)
    def display_reward(self):
        print("Reward Points: "+str(self.rewardAccount.get_balance()))
    def get_off(self,amount):
        return 0

    def modify_order(self):
        print("Choose item ID to modify-")
        self.currentOrder.display_items_detailed()
        option1=int(input())
        print("Choose action- ")
        print("1) Remove")
        print("2) Reduce")
        option2=int(input())
        if option2==1:
            self.currentOrder.remove_item(option1)
        elif option2==2:
            print("Enter quantity to remove- ",end="")
            option3=int(input())
            self.currentOrder.reduce_item_quantity(option1,option3)
    def add_items_to_cart(self):
        if len(self.currentRestaurant.get_food_items())==0:
            print("No item available")
            return
        print("Choose item by code")
        self.currentRestaurant.display_food_items()
        id=int(input())
        print("Enter item quantity-")
        quantity=int(input())
        if self.currentRestaurant.get_food_items()[id].is_desired_quantity_available(quantity):
            self.currentRestaurant.get_food_items()[id].pick_quantity(quantity)
            self.currentOrder.add_to_cart(id,self.currentRestaurant.get_food_items()[id].get_name(),quantity,self.currentRestaurant.get_food_items()[id].get_price())
            print("Items added to cart")
        else:
            print("Desired quantity not available, nothing got added to cart, returnig back to Customer window")
    def do_checkOut(self,zotatoTransactionAccount,zotatoDeliveryFeeAccount):
        if self.currentOrder is None:
            print("Nothing in cart")
            return
        exit=False
        while not exit:
            if self.currentOrder.get_items_count()==0:
                print("Nothing in cart")
                self.currentOrder=None
                return
            self.currentOrder.display_items_detailed()
            print("Delivery charge - "+str(self.currentOrder.get_delivery_charge()))
            print("Total order value - INR "+str(self.currentOrder.get_amount())+"/-")
            amountPayable=self.currentOrder.get_amount()+self.currentOrder.get_delivery_charge()
            availableBalance=self.walletAccount.get_balance()+self.rewardAccount.get_balance()
            if amountPayable<=availableBalance:
                if self.rewardAccount.is_desired_balance_available(amountPayable):
                    self.rewardAccount.withdraw_money(availableBalance)
                else:
                    rewardBalance=self.rewardAccount.get_balance()
                    amountPayable-=rewardBalance
                    self.rewardAccount.withdraw_money(rewardBalance)
                    self.walletAccount.withdraw_money(amountPayable)
                reward=self.currentRestaurant.get_reward(self.currentOrder.get_amount())
                self.gain_reward(reward)
                self.currentRestaurant.gain_reward(reward)
                self.currentRestaurant.order_completed()
                zotatoTransactionAccount.add_money(self.currentOrder.get_amount()/100)
                zotatoDeliveryFeeAccount.add_money(self.currentOrder.get_delivery_charge())
                print("1) Proceed to checkout")
                input()
                print(str(self.currentOrder.get_items_count())+" items successfully bought for INR "+str(self.currentOrder.get_amount()+self.currentOrder.get_delivery_charge()))
                self.recentOrders.append(self.currentOrder)
                if len(self.recentOrders)>10:
                    self.recentOrders.popleft()
                self.currentOrder=None
                self.currentRestaurant=None
                exit=True
            else:
                print("Insufficient Balance, remove/reduce some items...")
                print("Available balance- "+str(availableBalance)+", Amount needed- "+str(amountPayable))
                self.modify_order()
    def display_recent_orders(self):
        count=1
        for order in self.recentOrders:
            print(str(count)+") ",end="")
            count+=1
            order.display_details()
        if len(self.recentOrders)==0:
            print("No recent orders")

    def service_window(self,restaurants,zotatoTransactionAccount,zotatoDeliveryFeeAccount):
        exit=False
        while not exit:
            print("Welcome "+self.name)
            print("Customer Menu")
            print("1) "+("Select Restaurant" if self.currentRestaurant is None else "Select Item"))
            print("2) Checkout cart")
            print("3) Reward won")
            print("4) Print recent orders")
            print("5) Exit")
            option=int(input())
            if option==1:
                if self.currentRestaurant is None:
                    print("Choose Restaurant")
                    for restaurant in restaurants.values():
                        restaurant.display_brief()
                    id=int(input())
                    self.currentRestaurant=restaurants[id]
                    self.currentOrder=Order(self.currentRestaurant,self,self.deliveryCharge)
                self.add_items_to_cart()
            elif option==2:
                self.do_checkOut(zotatoTransactionAccount,zotatoDeliveryFeeAccount)
                self.currentRestaurant=None
                self.currentOrder=None
            elif option==3:
                self.display_reward()
            elif option==4:
                self.display_recent_orders()
            elif option==5:
                if self.currentOrder is not None:
                    self.currentOrder.return_order()
                self.currentRestaurant=None
                self.currentOrder=None
                exit=True
            else:
                if self.currentOrder is not None:
                    self.currentOrder.return_order()
                self.currentRestaurant=None
                self.currentOrder=None
                print("Invalid option, returning to home window!!!")
                exit=True

class Restaurant:
    uniqueId=1
    def __init__(self,name,address,category="NA",discount=0,rewardSchemeSupply=5,rewardSchemeDemand=100):
        self.id=Restaurant.uniqueId
        Restaurant.uniqueId+=1
        self.name=name
        self.address=address
        self.category=category
        self.numberOfOrdersTaken=0
        self.rewardAccount=Reward(0)
        self.discount=float(discount)
        self.rewardSchemeSupply=float(rewardSchemeSupply)
        self.rewardSchemeDemand=float(rewardSchemeDemand)
        self.foodItemsCount=0
        self.foodItems={}

    def get_id(self):
        return self.id
    def get_name(self):
        return self.name
    def display_details(self):
        print(self.name+" "+(""  if self.category=="NA" else ("("+self.category+")"))+", "+self.address+", "+str(self.numberOfOrdersTaken))
    def display_brief(self):
        print(str(self.id)+") "+self.name+("" if self.category=="NA" else (" ("+self.category+")")))
    def gain_reward(self,reward):
        self.rewardAccount.add_money(reward)
    def display_reward(self):
        print("Reward Points: "+str(self.rewardAccount.get_balance()))
    def get_off(self,amount):
        return 0

    def order_completed(self):
        self.numberOfOrdersTaken+=1
    def get_discount(self):
        return self.discount
    def get_food_items(self):
        return self.foodItems
    def get_reward(self,amount):
        return (amount//self.rewardSchemeDemand)*self.rewardSchemeSupply
    def display_food_items(self):
        for food in self.foodItems.values():
            food.display_extended_details()
    def get_overall_bill_discount(self,amount):
        return (self.discount*amount)/100

    def add_item(self):
        print("Enter food items details")
        print("Food Name:")
        name=input()
        print("Item Price:")
        price=float(input())
        print("Item Quantity:")
        quantity=int(input())
        print("Item Category:")
        category=input()
        print("Offer:")
        offer=float(input())
        self.foodItemsCount+=1
        food=Food(self.foodItemsCount,name,price,quantity,offer,category,self)
        self.foodItems[food.get_id()]=food
        self.foodItems[food.get_id()].display_details()
    def edit_item(self):
        print("Choose item by code")
        self.display_food_items()
        option=int(input())
        self.foodItems[option].edit_details()
        self.foodItems[option].display_extended_details()
    def modify_discount(self):
        if self.category=="NA":
            print("Option not avialable for restaurant")
            return
        print("Enter discount on bill value - ",end="")
        discount=int(input())
        self.discount=discount

    def service_window(self):
        exit=False
        while not exit:
            print("Welcome "+self.name)
            print("1) Add item")
            print("2) Edit item")
            print("3) Print rewards")
            print("4) Discount on bill value")
            print("5) Exit")

            option=int(input())
            if option==1:
                self.add_item()
            elif option==2:
                self.edit_item()
            elif option==3:
                self.display_reward()
            elif option==4:
                self.modify_discount()
            elif option==5:
                exit=True
            else:
                print("Invalid option, returning to home window!!!")
                exit=True

class EliteCustomer(Customer):
    def __init__(self,name,address,amount):
        Customer.__init__(self,name,address,amount,"Elite",0)
        self.off=50.0
        self.billLimit=200.0

    def get_off(self,amount):
        if amount>=self.billLimit:
            return self.off
        else:
            return 0

class SpecialCustomer(Customer):
    def __init__(self,name,address,amount):
        Customer.__init__(self,name,address,amount,"Special",20)
        self.off=25.0
        self.billLimit=200.0

    def get_off(self,amount):
        if amount>=self.billLimit:
            return self.off
        else:
            return 0

class FastFoodRestaurant(Restaurant):
    def __init__(self,name,address,discount):
        Restaurant.__init__(self,name,address,"Fast Food",discount,10,150)

class AuthenticRestaurant(Restaurant):
    def __init__(self,name,address,discount):
        Restaurant.__init__(self,name,address,"Authentic",discount,25,200)
        self.off=50
        self.billLimit=200

    def get_off(self,amount):
        if amount>=self.billLimit:
            return self.off
        else:
            return 0


class Zotato:
    def __init__(self):
        self.customers={}
        self.restaurants={}
        self.transctionFees=Wallet(0)
        self.deliveryFees=Wallet(0)

    def run_application(self):
        self.home_window()
    def home_window(self):
        exit=False
        while not exit:
            print("Welcome to Zotato:")
            print("1) Enter as Restaurant Owner")
            print("2) Enter as Customer")
            print("3) Check User Details")
            print("4) Company Account details")
            print("5) Exit")

            option=int(input())
            if option==1:
                self.restaurant_window()
            elif option==2:
                self.customer_window()
            elif option==3:
                self.user_details_window()
            elif option==4:
                self.display_company_account()
            elif option==5:
                exit=True
            else:
                print("Invalid option, terminating program!!!")
                exit=True
    def restaurant_window(self):
        print("Choose Restaurant")
        self.display_restaurants()
        option=int(input())
        self.restaurants[option].service_window()
    def customer_window(self):
        self.display_customers()
        option=int(input())
        self.customers[option].service_window(self.restaurants,self.transctionFees,self.deliveryFees)
    def user_details_window(self):
        print("1) Customer List")
        print("2) Restaurant List")
        option=int(input())
        if option==1:
            self.display_customers()
            option=int(input())
            self.customers[option].display_details()
        elif option==2:
            self.display_restaurants()
            option=int(input())
            self.restaurants[option].display_details()
        else:
            print("Invalid Option!!!, Returing back to previous menu")
    def display_company_account(self):
        print("Total Company balance - INR "+str(self.transctionFees.get_balance())+"/-")
        print("Total Delivery Charges collected - INR "+str(self.deliveryFees.get_balance())+"/-")

    def add_customer(self,customer):
        self.customers[customer.get_id()]=customer
    def add_restaurant(self,restaurant):
        self.restaurants[restaurant.get_id()]=restaurant

    def display_restaurants(self):
        for restaurant in self.restaurants.values():
            restaurant.display_brief()
    def display_customers(self):
        for customer in self.customers.values():
            customer.display_brief()

def fill_defaults(zotato):
    walletMoney=1000
    customer=EliteCustomer("Ram","Pune",walletMoney)
    zotato.add_customer(customer)
    customer=EliteCustomer("Sam","Delhi",walletMoney)
    zotato.add_customer(customer)
    customer=SpecialCustomer("Tim","Mumbai",walletMoney)
    zotato.add_customer(customer)
    customer=Customer("Kim","Bangalore",walletMoney)
    zotato.add_customer(customer)
    customer=Customer("Jim","Chennai",walletMoney)
    zotato.add_customer(customer)

    restaurant=AuthenticRestaurant("Shah","Hyderbad",2)
    zotato.add_restaurant(restaurant)
    restaurant=Restaurant("Ravi's","Kolkata")
    zotato.add_restaurant(restaurant)
    restaurant=AuthenticRestaurant("The Chinese","Dispur",7)
    zotato.add_restaurant(restaurant)
    restaurant=FastFoodRestaurant("Wang's","Goa",15)
    zotato.add_restaurant(restaurant)
    restaurant=Restaurant("Paradise","Srinagar")
    zotato.add_restaurant(restaurant)

if __name__=="__main__":
    zotato=Zotato()
    fill_defaults(zotato)

    zotato.run_application()