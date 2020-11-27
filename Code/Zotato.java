
/*Zotato- Food Delivery Platform
Author: Abhimanyu Gupta (2019226) (abhimanyu19226@iiitd.ac.in)
Functionality: A program to connect Restaurants with Customers using the services provided by Zatotato(food delivery technology company).
For Purpose: Assignment 2, CSE201-Advanced Programming, Monsoon 2020 at IIIT-Delhi
Includes: Zoatato.java - run and maintains the flow of the program
	Zotato.class - contains records of Zotato along with providing menu to use the services
	User.class - an interface to store user details which establish basic features of Customer and Restaurant class
	Customer.class - stores information of customers and provides services related to customers
	Restaurant.class - stores information of Restaurant and provides services related to restaurants
	Food.class - stores properties of a particular food item
	Item.class - stores properties of food item, currently picked by Customer
	Order.class - acts as a cart to store the order of the Customer
	MoneyAccount.class - an interface to store money and contains contracts for Wallet and Reward class
	Wallet.class - a money account to store cash of User
	Reward.class - an account to store rewards earned by User
	EliteCustomer.class - type of Customer inherited from Customer class
	SpecialCustomer.class - type of Customer inherited from Customer class
	AuthenticRestaurant.class - type of Restaurant inherited from Restaurant class
	FastFood.class - type of Restaurant inherited from Restaurant class
*/

import java.util.Scanner;
import java.util.HashMap;
import java.util.Queue;
import java.util.LinkedList;

interface MoneyAccount
{
	public void add_money(double amount);
	public void withdraw_money(double amount);
	public boolean is_desired_balance_available(double neededAmount);
	public double get_balance();
}

class Wallet implements MoneyAccount
{
	private double balance;

	public Wallet()
	{
		this.balance=0;
	}
	public Wallet(double amount)
	{
		this.balance=amount;
	}

	@Override
	public void add_money(double amount)
	{
		this.balance+=amount;
	}
	@Override
	public void withdraw_money(double amount)
	{
		this.balance-=amount;
	}
	@Override
	public boolean is_desired_balance_available(double neededAmount)
	{
		return this.balance>=neededAmount;
	}
	@Override
	public double get_balance()
	{
		return this.balance;
	}
}

class Reward implements MoneyAccount
{
	private double balance;

	public Reward()
	{
		this.balance=0;
	}
	public Reward(double amount)
	{
		this.balance=amount;
	}
	
	@Override
	public void add_money(double amount)
	{
		this.balance+=amount;
	}
	@Override
	public void withdraw_money(double amount)
	{
		this.balance-=amount;
	}
	@Override
	public boolean is_desired_balance_available(double neededAmount)
	{
		return this.balance>=neededAmount;
	}
	@Override
	public double get_balance()
	{
		return this.balance;
	}
}

class Food
{
	final private int id;
	private String name;
	private double price;
	private int quantity;
	private double discount;
	private String category;

	final private Restaurant restaurant;

	public Food()
	{
		this.id=-1;
		this.name="Undefined";
		this.price=-1;
		this.quantity=-1;
		this.discount=-1;
		this.category="Undefined";
		this.restaurant=null;
	}
	public Food(int id,String name,double price,int quantity,double discount,String category,Restaurant restaurant)
	{
		this.id=id;
		this.name=name;
		this.price=price;
		this.quantity=quantity;
		this.discount=discount;
		this.category=category;
		this.restaurant=restaurant;
	}

	public void edit_details(Scanner sc)
	{
		System.out.println("Choose an attribute to edit:");
		System.out.println("1) Name");
		System.out.println("2) Price");
		System.out.println("3) Quantity");
		System.out.println("4) Category");
		System.out.println("5) Offer");
		int option=sc.nextInt();
		sc.nextLine();
		String[] words={"name","price","quantity","category","offer"};
		System.out.print("Enter the new "+words[option-1]+" - ");
		switch(option)
		{
			case 1:
			{
				String name=sc.nextLine();
				this.name=name;
				break;
			}
			case 2:
			{	
				double price=sc.nextDouble();
				sc.nextLine();
				this.price=price;
				break;
			}
			case 3:
			{
				int quantity=sc.nextInt();
				sc.nextLine();
				this.quantity=quantity;
				break;
			}
			case 4:
			{
				String category=sc.nextLine();
				this.category=category;
				break;
			}
			case 5:
			{
				double discount=sc.nextDouble();
				sc.nextLine();
				this.discount=discount;
				break;
			}
			default:
				System.out.println("Invalid Option, no attribute modified");
		}
	}

	public int get_id()
	{
		return this.id;
	}
	public String get_name()
	{
		return this.name;
	}
	public double get_price()
	{
		return this.price;
	}
	public double get_discount()
	{
		return this.discount;
	}
	public double get_discount(double amount)
	{
		return (amount*this.discount)/100;
	}

	public void display_details()
	{
		System.out.println(this.id+" "+this.name+" "+this.price+" "+this.quantity+" "+this.discount+"% off "+this.category);
	}
	public void display_extended_details()
	{
		System.out.println(this.id+" "+this.restaurant.get_name()+" - "+this.name+" "+this.price+" "+this.quantity+" "+this.discount+"% off "+this.category);	
	}
	public void add_quantity(int quantity)
	{
		this.quantity+=quantity;
	}
	public void pick_quantity(int quantitySold)
	{
		this.quantity-=quantitySold;
	}
	public boolean is_desired_quantity_available(int quantityWanted)
	{
		return this.quantity>=quantityWanted;
	}
}

class Item
{
	private int id;
	private String name;
	private int quantity;
	private double rate;

	public Item()
	{
		this.id=-1;
		this.name="Undefined";
		this.quantity=-1;
		this.rate=-1;
	}
	public Item(int id,String name,int quantity,double rate)
	{
		this.id=id;
		this.name=name;
		this.quantity=quantity;
		this.rate=rate;
	}

	public int get_id()
	{
		return this.id;
	}
	public int get_quantity()
	{
		return this.quantity;
	}
	public double get_rate()
	{
		return this.rate;
	}
	public void reduce_quantity(int quantity)
	{
		this.quantity-=quantity;
	}
	public void increase_quantity(int quantity)
	{
		this.quantity+=quantity;
	}
	public void display_details_detailed(Restaurant restaurant)
	{
		System.out.println(this.id+" "+restaurant.get_name()+" - "+this.name+" - "+this.rate+" - "+this.quantity+" - "+restaurant.get_food_items().get(this.id).get_discount()+"% off");
	}
	public void display_details()
	{
		System.out.println("Item: ID- "+this.id+" Name- "+this.name+" Quantity- "+this.quantity+" Rate- "+this.rate);
	}
}

class Order
{
	final private Restaurant restaurant;
	final private Customer customer;
	private HashMap<Integer,Item> items;
	private double amount;
	private double deliveryCharge;

	public Order()
	{
		this.restaurant=null;
		this.customer=null;
		this.items=null;
		this.amount=-1;
		this.deliveryCharge=-1;
	}
	public Order(Restaurant restaurant,Customer customer,double deliveryCharge)
	{
		this.restaurant=restaurant;
		this.customer=customer;
		this.items=new HashMap<Integer,Item>();
		this.amount=0;
		this.deliveryCharge=deliveryCharge;
	}

	public void add_to_cart(int id,String name,int quantity,double rate)
	{
		if(this.items.containsKey(id))
			this.increase_item_quantity(id,quantity);
		else
			this.add_item(id,name,quantity,rate);
	}
	public void return_order()
	{
		for(Item i: this.items.values())
			this.restaurant.get_food_items().get(i.get_id()).add_quantity(i.get_quantity());
	}
	public void add_item(int id,String name,int quantity,double rate)
	{
		this.items.put(id,new Item(id,name,quantity,rate));
	}
	public void remove_item(int id)
	{
		this.restaurant.get_food_items().get(id).add_quantity(this.items.get(id).get_quantity());
		this.items.remove(id);
	}
	public void increase_item_quantity(int id,int quantity)
	{
		this.items.get(id).increase_quantity(quantity);
	}
	public void reduce_item_quantity(int id,int quantity)
	{
		this.restaurant.get_food_items().get(id).add_quantity(quantity);
		this.items.get(id).reduce_quantity(quantity);
		if(this.items.get(id).get_quantity()==0)
			this.items.remove(id);
	}
	public int get_items_count()
	{
		return this.items.size();
	}
	public void display_items_detailed()
	{
		for(Item i: this.items.values())
			i.display_details_detailed(this.restaurant);
	}
	public void display_items()
	{
		for(Item i: this.items.values())
			i.display_details();
	}
	public void display_details()
	{
		System.out.println("Restaurant- "+this.restaurant.get_name()+" | "+" Amount- "+this.amount+" | "+" Delivery Charge- "+this.deliveryCharge);
		this.display_items();
	}
	public double get_amount()
	{
		this.calculate_amount();
		return this.amount;
	}
	public double get_delivery_charge()
	{
		return this.deliveryCharge;
	}
	private void calculate_amount()
	{
		this.amount=0;
		for(Integer id: items.keySet())
		{
			double itemAmount=this.items.get(id).get_quantity()*this.items.get(id).get_rate();
			itemAmount-=this.restaurant.get_food_items().get(id).get_discount(itemAmount);
			this.amount+=itemAmount;
		}
		this.amount-=this.restaurant.get_overall_bill_discount(amount);
		this.amount-=this.restaurant.get_off(this.amount);
		this.amount-=this.customer.get_off(this.amount);
	}
}

interface User
{
	public int get_id();
	public String get_name();
	public void display_details();
	public void display_brief();
	public void gain_reward(double reward);
	public void display_reward();
	public double get_off(double amount);
}

class Customer implements User
{
	private static int uniqueId;

	final private int id;
	final private String name;
	final private String address;
	final private String category;
	final private double deliveryCharge;
	final private Wallet walletAccount;
	final private Reward rewardAccount;

	private Restaurant currentRestaurant;
	private Order currentOrder;
	private Queue<Order> recentOrders;

	static
	{
		Customer.uniqueId=1;
	}

	public Customer()
	{
		this.id=Customer.uniqueId;
		++Customer.uniqueId;
		this.name="Undefined";
		this.address="Undefined";
		this.category="Undefined";
		this.deliveryCharge=-1;
		this.walletAccount=null;
		this.rewardAccount=null;
		this.currentRestaurant=null;
		this.currentOrder=null;
		this.recentOrders=null;
	}
	public Customer(String category)
	{
		this.id=Customer.uniqueId;
		++Customer.uniqueId;
		this.name="Undefined";
		this.address="Undefined";
		this.category=category;
		this.deliveryCharge=-1;
		this.walletAccount=null;
		this.rewardAccount=null;
		this.currentRestaurant=null;
		this.currentOrder=null;
		this.recentOrders=null;
	}
	public Customer(String name,String address,double amount)
	{
		this.id=Customer.uniqueId;
		++Customer.uniqueId;
		this.name=name;
		this.address=address;
		this.category="NA";
		this.deliveryCharge=40;
		this.walletAccount=new Wallet(amount);
		this.rewardAccount=new Reward(0);
		this.currentRestaurant=null;
		this.currentOrder=null;
		this.recentOrders=new LinkedList<Order>();
	}
	public Customer(String name,String address,double amount,String category,double deliveryCharge)
	{
		this.id=Customer.uniqueId;
		++Customer.uniqueId;
		this.name=name;
		this.address=address;
		this.deliveryCharge=deliveryCharge;
		this.category=category;
		this.walletAccount=new Wallet(amount);
		this.rewardAccount=new Reward(0);
		this.currentRestaurant=null;
		this.currentOrder=null;
		this.recentOrders=new LinkedList<Order>();
	}

	@Override
	public int get_id()
	{
		return this.id;
	}
	@Override
	public String get_name()
	{
		return this.name;
	}
	@Override
	public void display_details()
	{
		System.out.println(this.name+(this.category.equals("NA")?"":("("+this.category+")"))+", "+this.address+", "+this.walletAccount.get_balance()+"/-");
	}
	@Override
	public void display_brief()
	{
		System.out.println(this.id+") "+this.name+(this.category.equals("NA")?"":(" ("+this.category+")")));
	}
	@Override
	public void gain_reward(double reward)
	{
		this.rewardAccount.add_money(reward);
	}
	@Override
	public void display_reward()
	{
		System.out.println("Reward Points: "+this.rewardAccount.get_balance());
	}
	@Override
	public double get_off(double amount)
	{
		return 0;
	}

	public void modify_order(Scanner sc)
	{
		System.out.println("Choose item ID to modify-");
		this.currentOrder.display_items_detailed();
		int option1=sc.nextInt();
		sc.nextLine();
		System.out.println("Choose action- ");
		System.out.println("1) Remove");
		System.out.println("2) Reduce");
		int option2=sc.nextInt();
		sc.nextLine();
		if(option2==1)
			this.currentOrder.remove_item(option1);
		else if(option2==2)
		{
			System.out.print("Enter quantity to remove- ");
			int option3=sc.nextInt();
			sc.nextLine();
			this.currentOrder.reduce_item_quantity(option1,option3);
		}
	}

	public void add_items_to_cart(Scanner sc)
	{
		if(this.currentRestaurant.get_food_items().size()==0)
		{
			System.out.println("No item available");
			return;
		}
		System.out.println("Choose item by code");
		this.currentRestaurant.display_food_items();
		int id=sc.nextInt();
		sc.nextLine();
		System.out.println("Enter item quantity-");
		int quantity=sc.nextInt();
		sc.nextLine();
		if(this.currentRestaurant.get_food_items().get(id).is_desired_quantity_available(quantity))
		{
			this.currentRestaurant.get_food_items().get(id).pick_quantity(quantity);
			this.currentOrder.add_to_cart(id,this.currentRestaurant.get_food_items().get(id).get_name(),quantity,this.currentRestaurant.get_food_items().get(id).get_price());
			System.out.println("Items added to cart");
		}
		else
			System.out.println("Desired quantity not available, nothing got added to cart, returnig back to Customer window");
	}
	public void do_checkOut(Scanner sc,Wallet zotatoTransactionAccount,Wallet zotatoDeliveryFeeAccount)
	{
		if(this.currentOrder==null)
		{
			System.out.println("Nothing in cart");
			return;
		}
		boolean exit=false;
		while(!exit)
		{	
			if(this.currentOrder.get_items_count()==0)
			{
				System.out.println("Nothing in cart");
				this.currentOrder=null;
				return;
			}
			this.currentOrder.display_items_detailed();
			System.out.println("Delivery charge - "+this.currentOrder.get_delivery_charge());
			System.out.println("Total order value - INR "+this.currentOrder.get_amount()+"/-");
			double amountPayable=this.currentOrder.get_amount()+this.currentOrder.get_delivery_charge();
			double availableBalance=this.walletAccount.get_balance()+this.rewardAccount.get_balance();
			if(amountPayable<=availableBalance)
			{
				if(this.rewardAccount.is_desired_balance_available(amountPayable))
					this.rewardAccount.withdraw_money(availableBalance);
				else
				{
					double rewardBalance=this.rewardAccount.get_balance();
					amountPayable-=rewardBalance;
					this.rewardAccount.withdraw_money(rewardBalance);
					this.walletAccount.withdraw_money(amountPayable);
				}
				double reward=this.currentRestaurant.get_reward(this.currentOrder.get_amount());
				this.gain_reward(reward);
				this.currentRestaurant.gain_reward(reward);
				this.currentRestaurant.order_completed();
				zotatoTransactionAccount.add_money(this.currentOrder.get_amount()/100);
				zotatoDeliveryFeeAccount.add_money(this.currentOrder.get_delivery_charge());
				System.out.println("1) Proceed to checkout");
				sc.nextLine();
				System.out.println(this.currentOrder.get_items_count()+" items successfully bought for INR "+(this.currentOrder.get_amount()+this.currentOrder.get_delivery_charge()));
				this.recentOrders.add(this.currentOrder);
				if(this.recentOrders.size()>10)
					this.recentOrders.remove();
				this.currentOrder=null;
				this.currentRestaurant=null;
				exit=true;
			}
			else
			{
				System.out.println("Insufficient Balance, remove/reduce some items...");
				System.out.println("Available balance- "+availableBalance+", Amount needed- "+amountPayable);
				this.modify_order(sc);
			}
		}
	}
	public void display_recent_orders()
	{
		int count=1;
		for(Order o: this.recentOrders)
		{
			System.out.print(count+") ");
			++count;
			o.display_details();
		}
		if(this.recentOrders.size()==0)
			System.out.println("No recent orders");
	}

	public void service_window(Scanner sc,HashMap<Integer,Restaurant> restaurants,Wallet zotatoTransactionAccount,Wallet zotatoDeliveryFeeAccount)
	{	
		boolean exit=false;
		while(!exit)
		{
			System.out.println("Welcome "+this.name);
			System.out.println("Customer Menu");
			System.out.println("1) "+(this.currentRestaurant==null?"Select Restaurant":"Select Item"));
			System.out.println("2) Checkout cart");
			System.out.println("3) Reward won");
			System.out.println("4) Print recent orders");
			System.out.println("5) Exit");
		
			int option=sc.nextInt();
			sc.nextLine();
			switch(option)
			{
				case 1:
				{
					if(this.currentRestaurant==null)
					{
						System.out.println("Choose Restaurant");
						for(Restaurant r:restaurants.values())
							r.display_brief();
						int id=sc.nextInt();
						sc.nextLine();
						this.currentRestaurant=restaurants.get(id);
						this.currentOrder=new Order(this.currentRestaurant,this,this.deliveryCharge);
					}
					this.add_items_to_cart(sc);
					break;
				}
				case 2:
				{
					this.do_checkOut(sc,zotatoTransactionAccount,zotatoDeliveryFeeAccount);
					this.currentRestaurant=null;
					this.currentOrder=null;
					break;
				}
				case 3:
				{
					this.display_reward();
					break;
				}
				case 4:
				{
					this.display_recent_orders();
					break;
				}
				case 5:
				{
					if(this.currentOrder!=null)
						this.currentOrder.return_order();
					this.currentRestaurant=null;
					this.currentOrder=null;
					exit=true;
					break;
				}
				default:
				{
					if(this.currentOrder!=null)
						this.currentOrder.return_order();
					this.currentRestaurant=null;
					this.currentOrder=null;
					System.out.println("Invalid option, returning to home window!!!");
					exit=true;
				}
			}
		}
	}
}

class Restaurant implements User
{
	static private int uniqueId;

	final private int id;
	final private String name;
	final private String address;
	final private String category;
	private int numberOfOrdersTaken;
	final private Reward rewardAccount;
	private double discount;
	final private double rewardSchemeSupply;
	final private double rewardSchemeDemand;

	private int foodItemsCount;
	private HashMap<Integer,Food> foodItems;

	static
	{
		Restaurant.uniqueId=1;
	}

	public Restaurant()
	{
		this.id=Restaurant.uniqueId;
		++Restaurant.uniqueId;
		this.name="Undefined";
		this.address="Undefined";
		this.category="Undefined";
		this.numberOfOrdersTaken=-1;
		this.rewardAccount=null;
		this.discount=-1;
		this.rewardSchemeSupply=5;
		this.rewardSchemeDemand=100;

		this.foodItemsCount=0;
		this.foodItems=new HashMap<Integer,Food>();
	}
	public Restaurant(String category,double rewardSchemeSupply,double rewardSchemeDemand)
	{
		this.id=Restaurant.uniqueId;
		++Restaurant.uniqueId;
		this.name="Undefined";
		this.address="Undefined";
		this.category=category;
		this.numberOfOrdersTaken=-1;
		this.rewardAccount=null;
		this.discount=-1;
		this.rewardSchemeSupply=rewardSchemeSupply;
		this.rewardSchemeDemand=rewardSchemeDemand;

		this.foodItemsCount=0;
		this.foodItems=new HashMap<Integer,Food>();
	}
	public Restaurant(String name,String address)
	{
		this.id=Restaurant.uniqueId;
		++Restaurant.uniqueId;
		this.name=name;
		this.address=address;
		this.category="NA";
		this.numberOfOrdersTaken=0;
		this.rewardAccount=new Reward(0);
		this.discount=0;
		this.rewardSchemeSupply=5;
		this.rewardSchemeDemand=100;
	
		this.foodItemsCount=0;
		this.foodItems=new HashMap<Integer,Food>();
	}
	public Restaurant(String name,String address,String category,double discount,double rewardSchemeSupply,double rewardSchemeDemand)
	{
		this.id=Restaurant.uniqueId;
		++Restaurant.uniqueId;
		this.name=name;
		this.address=address;
		this.category=category;
		this.numberOfOrdersTaken=0;
		this.rewardAccount=new Reward(0);
		this.discount=discount;
		this.rewardSchemeSupply=rewardSchemeSupply;
		this.rewardSchemeDemand=rewardSchemeDemand;
	
		this.foodItemsCount=0;
		this.foodItems=new HashMap<Integer,Food>();
	}

	@Override
	public int get_id()
	{
		return this.id;
	}
	@Override
	public String get_name()
	{
		return this.name;
	}
	@Override
	public void display_details()
	{
		System.out.println(this.name+" "+(this.category.equals("NA")?"":("("+this.category+")"))+", "+this.address+", "+this.numberOfOrdersTaken);
	}
	@Override
	public void display_brief()
	{
		System.out.println(this.id+") "+this.name+(this.category.equals("NA")?"":(" ("+this.category+")")));
	}
	@Override
	public void gain_reward(double reward)
	{
		this.rewardAccount.add_money(reward);
	}
	@Override
	public void display_reward()
	{
		System.out.println("Reward Points: "+this.rewardAccount.get_balance());
	}
	@Override
	public double get_off(double amount)
	{
		return 0;
	}

	public void order_completed()
	{
		++this.numberOfOrdersTaken;	
	}
	public double get_discount()
	{
		return this.discount;
	}
	public HashMap<Integer,Food> get_food_items()
	{
		return this.foodItems;
	}
	public double get_reward(double amount)
	{
		return (int)(amount/this.rewardSchemeDemand)*this.rewardSchemeSupply;
	}
	public void display_food_items()
	{
		for(Food f:this.foodItems.values())
			f.display_extended_details();
	}
	public double get_overall_bill_discount(double amount)
	{
		return (this.discount*amount)/100;
	}
	
	public void add_item(Scanner sc)
	{
		System.out.println("Enter food items details");
		System.out.println("Food Name:");
		String name=sc.nextLine();
		System.out.println("Item Price:");
		double price=sc.nextDouble();
		sc.nextLine();
		System.out.println("Item Quantity:");
		int quantity=sc.nextInt();
		sc.nextLine();
		System.out.println("Item Category:");
		String category=sc.nextLine();
		System.out.println("Offer:");
		double offer=sc.nextDouble();
		sc.nextLine();

		++this.foodItemsCount;
		Food f=new Food(this.foodItemsCount,name,price,quantity,offer,category,this);
		this.foodItems.put(f.get_id(),f);

		this.foodItems.get(f.get_id()).display_details();
	}
	public void edit_item(Scanner sc)
	{
		System.out.println("Choose item by code");
		this.display_food_items();
		int option=sc.nextInt();
		sc.nextLine();
		this.foodItems.get(option).edit_details(sc);
		this.foodItems.get(option).display_extended_details();
	}
	public void modify_discount(Scanner sc)
	{
		if(this.category.equals("NA"))
		{
			System.out.println("Option not avialable for restaurant");
			return;
		}
		System.out.print("Enter discount on bill value - ");
		int discount=sc.nextInt();
		sc.nextLine();
		this.discount=discount;
	}

	public void service_window(Scanner sc)
	{
		boolean exit=false;
		while(!exit)
		{
			System.out.println("Welcome "+this.name);
			System.out.println("1) Add item");
			System.out.println("2) Edit item");
			System.out.println("3) Print rewards");
			System.out.println("4) Discount on bill value");
			System.out.println("5) Exit");
		
			int option=sc.nextInt();
			sc.nextLine();
			switch(option)
			{
				case 1:
				{
					this.add_item(sc);
					break;
				}
				case 2:
				{
					this.edit_item(sc);
					break;
				}
				case 3:
				{
					this.display_reward();
					break;
				}
				case 4:
				{
					this.modify_discount(sc);
					break;
				}
				case 5:
				{
					exit=true;
					break;
				}
				default:
				{
					System.out.println("Invalid option, returning to home window!!!");
					exit=true;
				}
			}
		}
	}
}

class EliteCustomer extends Customer
{
	final private double off;
	final private double billLimit;

	public EliteCustomer()
	{
		super("Elite");
		this.off=-1;
		this.billLimit=-1;
	}
	public EliteCustomer(String name,String address,double amount)
	{
		super(name,address,amount,"Elite",0);
		this.off=50;
		this.billLimit=200;
	}
	
	@Override
	public double get_off(double amount)
	{
		if(amount>=this.billLimit)
			return this.off;
		else
			return 0;
	}
}

class SpecialCustomer extends Customer
{
	final private double off;
	final private double billLimit;

	public SpecialCustomer()
	{
		super("Special");
		this.off=-1;
		this.billLimit=-1;
	}
	public SpecialCustomer(String name,String address,double amount)
	{
		super(name,address,amount,"Special",20);
		this.off=25;
		this.billLimit=200;
	}

	@Override
	public double get_off(double amount)
	{
		if(amount>=this.billLimit)
			return this.off;
		else
			return 0;
	}
}

class FastFoodRestaurant extends Restaurant
{
	public FastFoodRestaurant()
	{
		super("Fast Food",10,150);
	}
	public FastFoodRestaurant(String name,String address,double discount)
	{
		super(name,address,"Fast Food",discount,10,150);
	}
}

class AuthenticRestaurant extends Restaurant
{
	final private double off;
	final private double billLimit;

	public AuthenticRestaurant()
	{
		super("Authentic",25,200);
		this.off=-1;
		this.billLimit=-1;
	}
	public AuthenticRestaurant(String name,String address,double discount)
	{
		super(name,address,"Authentic",discount,25,200);
		this.off=50;
		this.billLimit=200;
	}

	@Override
	public double get_off(double amount)
	{
		if(amount>=this.billLimit)
			return this.off;
		else
			return 0;
	}
}

public class Zotato
{
	private HashMap<Integer,Customer> customers;
	private HashMap<Integer,Restaurant> restaurants;
	private Wallet transctionFees;
	private Wallet deliveryFees;

	public Zotato()
	{
		this.customers=new HashMap<Integer,Customer>();
		this.restaurants=new HashMap<Integer,Restaurant>();
		this.transctionFees=new Wallet(0);
		this.deliveryFees=new Wallet(0);
	}

	public void run_application(Scanner sc)
	{
		this.home_window(sc);
	}
	public void home_window(Scanner sc)
	{
		boolean exit=false;
		while(!exit)
		{
			System.out.println("Welcome to Zotato:");
			System.out.println("1) Enter as Restaurant Owner");
			System.out.println("2) Enter as Customer");
			System.out.println("3) Check User Details");
			System.out.println("4) Company Account details");
			System.out.println("5) Exit");

			int option=sc.nextInt();
			sc.nextLine();
			switch(option)
			{
				case 1:
				{
					this.restaurant_window(sc);
					break;
				}
				case 2:
				{
					this.customer_window(sc);
					break;
				}
				case 3:
				{
					this.user_details_window(sc);
					break;
				}
				case 4:
				{
					this.display_company_account();
					break;
				}
				case 5:
				{
					exit=true;
					break;
				}
				default:
				{
					System.out.println("Invalid option, terminating program!!!");
					exit=true;
				}
			}
		}
	}
	public void restaurant_window(Scanner sc)
	{
		System.out.println("Choose Restaurant");
		this.display_restaurants();
		int option=sc.nextInt();
		sc.nextLine();
		this.restaurants.get(option).service_window(sc);
	}
	public void customer_window(Scanner sc)
	{
		this.display_customers();
		int option=sc.nextInt();
		sc.nextLine();
		this.customers.get(option).service_window(sc,this.restaurants,this.transctionFees,this.deliveryFees);
	}
	public void user_details_window(Scanner sc)
	{
		System.out.println("1) Customer List");
		System.out.println("2) Restaurant List");
		int option=sc.nextInt();
		sc.nextLine();
		if(option==1)
		{
			this.display_customers();
			option=sc.nextInt();
			sc.nextLine();
			this.customers.get(option).display_details();
		}
		else if(option==2)
		{
			this.display_restaurants();
			option=sc.nextInt();
			sc.nextLine();
			this.restaurants.get(option).display_details();
		}
	}
	public void display_company_account()
	{
		System.out.println("Total Company balance - INR "+this.transctionFees.get_balance()+"/-");
		System.out.println("Total Delivery Charges collected - INR "+this.deliveryFees.get_balance()+"/-");
	}

	public void add_customer(Customer c)
	{
		this.customers.put(c.get_id(),c);
	}
	public void add_restaurant(Restaurant r)
	{
		this.restaurants.put(r.get_id(),r);
	}
	
	public void display_restaurants()
	{
		for(Restaurant r:this.restaurants.values())
			r.display_brief();
	}
	public void display_customers()
	{
		for(Customer c:this.customers.values())
			c.display_brief();
	}

	public void fill_defaults()
	{
		final int walletMoney=1000;
		Customer c=new EliteCustomer("Ram","Pune",walletMoney);
		this.customers.put(c.get_id(),c);
		c=new EliteCustomer("Sam","Delhi",walletMoney);
		this.customers.put(c.get_id(),c);
		c=new SpecialCustomer("Tim","Mumbai",walletMoney);
		this.customers.put(c.get_id(),c);
		c=new Customer("Kim","Bangalore",walletMoney);
		this.customers.put(c.get_id(),c);
		c=new Customer("Jim","Chennai",walletMoney);
		this.customers.put(c.get_id(),c);

		Restaurant r=new AuthenticRestaurant("Shah","Hyderbad",2);
		this.restaurants.put(r.get_id(),r);
		r=new Restaurant("Ravi's","Kolkata");
		this.restaurants.put(r.get_id(),r);
		r=new AuthenticRestaurant("The Chinese","Dispur",7);
		this.restaurants.put(r.get_id(),r);
		r=new FastFoodRestaurant("Wang's","Goa",15);
		this.restaurants.put(r.get_id(),r);
		r=new Restaurant("Paradise","Srinagar");
		this.restaurants.put(r.get_id(),r);
	}

	static public void main(String[] args)
	{
		Scanner sc=new Scanner(System.in);

		Zotato z=new Zotato();
		z.fill_defaults();

		z.run_application(sc);

		sc.close();
		return;
	}
}