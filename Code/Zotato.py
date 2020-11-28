
import collections #For deque to implement Queue functionality

class Wallet:
	def __init__(self,balance):
		self._balance=float(balance)

	def add_money(self,amount):
		self._balance+=amount
	def withdraw_money(self,amount):
		self._balance-=amount
	def is_desired_balance_available(self,neededAmount):
		return self._balance>=neededAmount
	def get_balance(self):
		return self._balance

class Reward:
	def __init__(self,balance):
		self._balance=float(balance)

	def add_money(self,amount):
		self._balance+=amount
	def withdraw_money(self,amount):
		self._balance-=amount
	def is_desired_balance_available(self,neededAmount):
		return self._balance>=neededAmount
	def get_balance(self):
		return self._balance

class Food:
	def __init__(self,id,name,price,quantity,discount,category,restaurant):
		self._id=id
		self._name=name
		self._price=float(price)
		self._quantity=quantity
		self._discount=float(discount)
		self._category=category
		self._restaurant=restaurant

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
			self._name=name
		elif option==2:
			price=float(input())
			self._price=price
		elif option==3:
			quantity=int(input())
			self._quantity=quantity
		elif option==4:
			category=input()
			self._category=category
		elif option==5:
			discount=float(input())
			self._discount=discount
		else:
			print("Invalid Option, no attribute modified")

	def get_id(self):
		return self._id
	def get_name(self):
		return self._name
	def get_price(self):
		return self._price
	def get_discount_rate(self):
		return self._discount
	def get_discount(self,amount):
		return (amount*self._discount)/100

	def display_details(self):
		print(str(self._id)+" "+self._name+" "+str(self._price)+" "+str(self._quantity)+" "+str(self._discount)+"% off "+self._category)
	def display_extended_details(self):
		print(str(self._id)+" "+self._restaurant.get_name()+" - "+self._name+" "+str(self._price)+" "+str(self._quantity)+" "+str(self._discount)+"% off "+self._category)
	def add_quantity(self,quantity):
		self._quantity+=quantity
	def pick_quantity(self,quantitySold):
		self._quantity-=quantitySold
	def is_desired_quantity_available(self,quantityWanted):
		return self._quantity>=quantityWanted

class Item:
	def __init__(self,id,name,quantity,rate):
		self._id=id
		self._name=name
		self._quantity=quantity
		self._rate=float(rate)

	def get_id(self):
		return self._id
	def get_quantity(self):
		return self._quantity
	def get_rate(self):
		return self._rate

	def reduce_quantity(self,quantity):
		self._quantity-=quantity
	def increase_quantity(self,quantity):
		self._quantity+=quantity

	def display_details(self):
		print("Item: ID- "+str(self._id)+" Name- "+self._name+" Quantity- "+str(self._quantity)+" Rate- "+str(self._rate))
	def display_details_detailed(self,restaurant):
		print(str(self._id)+" "+restaurant.get_name()+" - "+self._name+" - "+str(self._rate)+" - "+str(self._quantity)+" - "+str(restaurant.get_food_items()[self._id].get_discount_rate())+"% off")

class Order:
	def __init__(self,restaurant,customer,deliveryCharge):
		self._restaurant=restaurant
		self._customer=customer
		self._items={}
		self._amount=0.0
		self._deliveryCharge=float(deliveryCharge)

	def get_amount(self):
		self._calculate_amount()
		return self._amount
	def get_delivery_charge(self):
		return self._deliveryCharge
	def get_items_count(self):
		return len(self._items)

	def add_to_cart(self,id,name,quantity,rate):
		if id in self._items:
			self.increase_item_quantity(id,quantity)
		else:
			self.add_item(id,name,quantity,rate)
	def return_order(self):
		for item in self._items.values():
			self._restaurant.get_food_items()[item.get_id()].add_quantity(item.get_quantity())

	def add_item(self,id,name,quantity,rate):
		self._items[id]=Item(id,name,quantity,rate)
	def remove_item(self,id):
		self._restaurant.get_food_items()[id].add_quantity(self._items[id].get_quantity())
		del self._items[id]
	def increase_item_quantity(self,id,quantity):
		self._items[id].increase_quantity(quantity)
	def reduce_item_quantity(self,id,quantity):
		self._restaurant.get_food_items()[id].add_quantity(quantity)
		self._items[id].reduce_quantity(quantity)
		if self._items[id].get_quantity()==0:
			del self._items[id]

	def display_items_detailed(self):
		for item in self._items.values():
			item.display_details_detailed(self._restaurant)
	def display_items(self):
		for item in self._items.values():
			item.display_details()

	def display_details(self):
		print("Restaurant- "+self._restaurant.get_name()+" | "+" Amount- "+str(self._amount)+" | "+" Delivery Charge- "+str(self._deliveryCharge))
		self.display_items()

	def _calculate_amount(self):
		self._amount=0
		for id in self._items.keys():
			itemAmount=self._items[id].get_quantity()*self._items[id].get_rate()
			itemAmount-=self._restaurant.get_food_items()[id].get_discount(itemAmount)
			self._amount+=itemAmount
		self._amount-=self._restaurant.get_overall_bill_discount(self._amount)
		self._amount-=self._restaurant.get_off(self._amount)
		self._amount-=self._customer.get_off(self._amount)


class Customer:
	_uniqueId=1
	def __init__(self,name,address,amount,category="NA",deliveryCharge=40):
		self._id=Customer._uniqueId
		Customer._uniqueId+=1
		self._name=name
		self._address=address
		self._deliveryCharge=float(deliveryCharge)
		self._category=category
		self._walletAccount=Wallet(amount)
		self._rewardAccount=Reward(0)
		self._currentRestaurant=None
		self._currentOrder=None
		self._recentOrders=collections.deque()

	def get_id(self):
		return self._id
	def get_name(self):
		return self._name
	def display_details(self):
		print(self._name+("" if self._category=="NA" else ("("+self._category+")"))+", "+self._address+", "+str(self._walletAccount.get_balance())+"/-")
	def display_brief(self):
		print(str(self._id)+") "+self._name+("" if self._category=="NA" else (" ("+self._category+")")))
	def gain_reward(self,reward):
		self._rewardAccount.add_money(reward)
	def display_reward(self):
		print("Reward Points: "+str(self._rewardAccount.get_balance()))
	def get_off(self,amount):
		return 0

	def modify_order(self):
		print("Choose item ID to modify-")
		self._currentOrder.display_items_detailed()
		option1=int(input())
		print("Choose action- ")
		print("1) Remove")
		print("2) Reduce")
		option2=int(input())
		if option2==1:
			self._currentOrder.remove_item(option1)
		elif option2==2:
			print("Enter quantity to remove- ",end="")
			option3=int(input())
			self._currentOrder.reduce_item_quantity(option1,option3)
	def add_items_to_cart(self):
		if len(self._currentRestaurant.get_food_items())==0:
			print("No item available")
			return
		print("Choose item by code")
		self._currentRestaurant.display_food_items()
		id=int(input())
		print("Enter item quantity-")
		quantity=int(input())
		if self._currentRestaurant.get_food_items()[id].is_desired_quantity_available(quantity):
			self._currentRestaurant.get_food_items()[id].pick_quantity(quantity)
			self._currentOrder.add_to_cart(id,self._currentRestaurant.get_food_items()[id].get_name(),quantity,self._currentRestaurant.get_food_items()[id].get_price())
			print("Items added to cart")
		else:
			print("Desired quantity not available, nothing got added to cart, returnig back to Customer window")
	def do_checkOut(self,zotatoTransactionAccount,zotatoDeliveryFeeAccount):
		if self._currentOrder is None:
			print("Nothing in cart")
			return
		exit=False
		while not exit:
			if self._currentOrder.get_items_count()==0:
				print("Nothing in cart")
				self._currentOrder=None
				return
			self._currentOrder.display_items_detailed()
			print("Delivery charge - "+str(self._currentOrder.get_delivery_charge()))
			print("Total order value - INR "+str(self._currentOrder.get_amount())+"/-")
			amountPayable=self._currentOrder.get_amount()+self._currentOrder.get_delivery_charge()
			availableBalance=self._walletAccount.get_balance()+self._rewardAccount.get_balance()
			if amountPayable<=availableBalance:
				if self._rewardAccount.is_desired_balance_available(amountPayable):
					self._rewardAccount.withdraw_money(availableBalance)
				else:
					rewardBalance=self._rewardAccount.get_balance()
					amountPayable-=rewardBalance
					self._rewardAccount.withdraw_money(rewardBalance)
					self._walletAccount.withdraw_money(amountPayable)
				reward=self._currentRestaurant.get_reward(self._currentOrder.get_amount())
				self.gain_reward(reward)
				self._currentRestaurant.gain_reward(reward)
				self._currentRestaurant.order_completed()
				zotatoTransactionAccount.add_money(self._currentOrder.get_amount()/100)
				zotatoDeliveryFeeAccount.add_money(self._currentOrder.get_delivery_charge())
				print("1) Proceed to checkout")
				input()
				print(str(self._currentOrder.get_items_count())+" items successfully bought for INR "+str(self._currentOrder.get_amount()+self._currentOrder.get_delivery_charge()))
				self._recentOrders.append(self._currentOrder)
				if len(self._recentOrders)>10:
					self._recentOrders.popleft()
				self._currentOrder=None
				self._currentRestaurant=None
				exit=True
			else:
				print("Insufficient Balance, remove/reduce some items...")
				print("Available balance- "+str(availableBalance)+", Amount needed- "+str(amountPayable))
				self.modify_order()
	def display_recent_orders(self):
		count=1
		for order in self._recentOrders:
			print(str(count)+") ",end="")
			count+=1
			order.display_details()
		if len(self._recentOrders)==0:
			print("No recent orders")

	def service_window(self,restaurants,zotatoTransactionAccount,zotatoDeliveryFeeAccount):
		exit=False
		while not exit:
			print("Welcome "+self._name)
			print("Customer Menu")
			print("1) "+("Select Restaurant" if self._currentRestaurant is None else "Select Item"))
			print("2) Checkout cart")
			print("3) Reward won")
			print("4) Print recent orders")
			print("5) Exit")
			option=int(input())
			if option==1:
				if self._currentRestaurant is None:
					print("Choose Restaurant")
					for restaurant in restaurants.values():
						restaurant.display_brief()
					id=int(input())
					self._currentRestaurant=restaurants[id]
					self._currentOrder=Order(self._currentRestaurant,self,self._deliveryCharge)
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
				if not(self._currentOrder is None):
					self._currentOrder.return_order()
				self._currentRestaurant=None
				self._currentOrder=None
				exit=True
			else:
				if not(self._currentOrder is None):
					self._currentOrder.return_order()
				self._currentRestaurant=None
				self._currentOrder=None
				print("Invalid option, returning to home window!!!")
				exit=True

class Restaurant:
	_uniqueId=1
	def __init__(self,name,address,category="NA",discount=0,rewardSchemeSupply=5,rewardSchemeDemand=100):
		self._id=Restaurant._uniqueId
		Restaurant._uniqueId+=1
		self._name=name
		self._address=address
		self._category=category
		self._numberOfOrdersTaken=0
		self._rewardAccount=Reward(0)
		self._discount=float(discount)
		self._rewardSchemeSupply=float(rewardSchemeSupply)
		self._rewardSchemeDemand=float(rewardSchemeDemand)
		self._foodItemsCount=0
		self._foodItems={}

	def get_id(self):
		return self._id
	def get_name(self):
		return self._name
	def display_details(self):
		print(self._name+" "+(""  if self._category=="NA" else ("("+self._category+")"))+", "+self._address+", "+str(self._numberOfOrdersTaken))
	def display_brief(self):
		print(str(self._id)+") "+self._name+("" if self._category=="NA" else (" ("+self._category+")")))
	def gain_reward(self,reward):
		self._rewardAccount.add_money(reward)
	def display_reward(self):
		print("Reward Points: "+str(self._rewardAccount.get_balance()))
	def get_off(self,amount):
		return 0

	def order_completed(self):
		self._numberOfOrdersTaken+=1
	def get_discount(self):
		return self._discount
	def get_food_items(self):
		return self._foodItems
	def get_reward(self,amount):
		return (amount//self._rewardSchemeDemand)*self._rewardSchemeSupply
	def display_food_items(self):
		for food in self._foodItems.values():
			food.display_extended_details()
	def get_overall_bill_discount(self,amount):
		return (self._discount*amount)/100

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
		self._foodItemsCount+=1
		food=Food(self._foodItemsCount,name,price,quantity,offer,category,self)
		self._foodItems[food.get_id()]=food
		self._foodItems[food.get_id()].display_details()
	def edit_item(self):
		print("Choose item by code")
		self.display_food_items()
		option=int(input())
		self._foodItems[option].edit_details()
		self._foodItems[option].display_extended_details()
	def modify_discount(self):
		if self._category=="NA":
			print("Option not avialable for restaurant")
			return
		print("Enter discount on bill value - ",end="")
		discount=int(input())
		self._discount=discount

	def service_window(self):
		exit=False
		while not exit:
			print("Welcome "+self._name)
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
		self._off=50.0
		self._billLimit=200.0

	def get_off(self,amount):
		if amount>=self._billLimit:
			return self._off
		else:
			return 0

class SpecialCustomer(Customer):
	def __init__(self,name,address,amount):
		Customer.__init__(self,name,address,amount,"Special",20)
		self._off=25.0
		self._billLimit=200.0

	def get_off(self,amount):
		if amount>=self._billLimit:
			return self._off
		else:
			return 0

class FastFoodRestaurant(Restaurant):
	def __init__(self,name,address,discount):
		Restaurant.__init__(self,name,address,"Fast Food",discount,10,150)

class AuthenticRestaurant(Restaurant):
	def __init__(self,name,address,discount):
		Restaurant.__init__(self,name,address,"Authentic",discount,25,200)
		self._off=50
		self._billLimit=200

	def get_off(self,amount):
		if amount>=self._billLimit:
			return self._off
		else:
			return 0


class Zotato:
	def __init__(self):
		self._customers={}
		self._restaurants={}
		self._transctionFees=Wallet(0)
		self._deliveryFees=Wallet(0)

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
		self._restaurants[option].service_window()
	def customer_window(self):
		self.display_customers()
		option=int(input())
		self._customers[option].service_window(self._restaurants,self._transctionFees,self._deliveryFees)
	def user_details_window(self):
		print("1) Customer List")
		print("2) Restaurant List")
		option=int(input())
		if option==1:
			self.display_customers()
			option=int(input())
			self._customers[option].display_details()
		elif option==2:
			self.display_restaurants()
			option=int(input())
			self._restaurants[option].display_details()
		else:
			print("Invalid Option!!!, Returing back to previous menu")
	def display_company_account(self):
		print("Total Company balance - INR "+str(self._transctionFees.get_balance())+"/-")
		print("Total Delivery Charges collected - INR "+str(self._deliveryFees.get_balance())+"/-")

	def add_customer(self,customer):
		self._customers[customer.get_id()]=customer
	def add_restaurant(self,restaurant):
		self._restaurants[restaurant.get_id()]=restaurant

	def display_restaurants(self):
		for restaurant in self._restaurants.values():
			restaurant.display_brief()
	def display_customers(self):
		for customer in self._customers.values():
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