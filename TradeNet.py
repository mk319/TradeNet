from Tkinter import *
import urllib2
import json

# valid symbols
_symbol_set = ["FB", "AAPL", "GOOG", "MSFT", "CRM", "TWTR", "BABA", "SPY", "QQQ", "DIA"]

# ----- Model -----
class Quote:

	def __init__(self, data):
		self.data = data["quotes"]["quote"]
		
	def __getitem__(self, key):
		return self.data[key]
			
# ----- Controller -----
class API:

	def __init__(self):
		self.url = "https://sandbox.tradier.com/v1/markets/quotes?symbols="
		self.auth = "Bearer TSCALKvrKOHFY1VH05ML7oMBbil4"
		self.type = "application/json"
		
	def fetch_quote(self, symbol):
		url = self.url + symbol
		request = urllib2.Request(url)
		request.add_header("Accept", self.type)
		request.add_header("Authorization", self.auth)
		connection = urllib2.urlopen(request)
		data = json.load(connection)
		self.quote = Quote(data)


# ----- Transaction Log Window -----
class Transaction:

	def __init__(self):
		self.window = Tk()
		self.window.title("Transaction Log")
		self.turl = ""
		self.ttype = "application/json"
		self.build()

	def build(self):
		input_lbl = Label(self.window, text = "User ID: ")
		input_lbl.grid(row = 0, column = 0, sticky = E)

		input_txt = Entry(self.window)
		input_txt.grid(row = 0, column = 1)
		self.input_txt = input_txt

		submit_btn = Button(self.window, text = "Submit", command = self.submit)
		submit_btn.grid(row = 0, column = 2, padx = 5)

		Log = Label(self.window, text = "Log: ").grid(row = 2, column = 0, sticky = E)
		logbox = Listbox(self.window, width = 50)
		logbox.grid(row=4,column = 0, columnspan = 3)
		logs = None
		for log in logs:
			logstring =  log["stock"]+ "\t" + log["shares"] + "\t" + log["datetime"]
			logbox.insert(END, logstring)
				
	def submit(self):
		lurl = self.turl + self.input_txt.get()
		lrequest = urllib2.Request(lurl)
		lrequest.add_header("Accept", self.ttype)
		lconnection = urllib2.urlopen(lrequest)
		self.data = json.load(lconnection)
		self.logs = self.data
		return


# ----- Portfolio Window -----
class Portfolio:

	def __init__(self):
		self.window = Tk()
		self.window.title("Portfolio")
		self.balanceurl = ""
		self.type = "application/json"
		self.stockurl = ""
		self.build()

	def build(self):
		input_lbl = Label(self.window, text = "User ID: ")
		input_lbl.grid(row = 0, column = 0, sticky = E)

		input_txt = Entry(self.window)
		input_txt.grid(row = 0, column = 1)
		self.input_txt = input_txt

		submit_btn = Button(self.window, text = "Submit", command = self.submit)
		submit_btn.grid(row = 0, column = 2, padx = 5)

		balancelabel = Label(self.window, text = "Balance: ").grid(row = 2, column = 0, sticky = E)

		balance_txt = StringVar()
		balance_lbl = Label(self.window, textvariable = balance_txt)
		balance_lbl.grid(row = 2, column = 1, sticky = W)

		stockslabel = Label(self.window, text = "Stocks: ").grid(row = 3, column = 0, sticky = E)

		stockbox = Listbox(self.window, width = 50)
		stockbox.grid(row=4,column = 0, columnspan = 3)
		
		self.listofstocks = None
		for stock in self.listofstocks:
			stockstring =  stock["stock"]+ "\t" + stock["shares"] + "\t" + stock["purchaseprice"]
			stockbox.insert(END, stockstring)
				
			
		
		

	def submit(self):
		burl = self.balanceurl + self.input_txt.get()
		brequest = urllib2.Request(burl)
		brequest.add_header("Accept", self.type)
		bconnection = urllib2.urlopen(brequest)
		self.data = json.load(bconnection)
		self.balance = self.data["accountbalance"]
		balance_txt = self.balance

		surl = self.stockurl + self.input_txt.get()
		srequest = urllib2.Request(surl)
		srequest.add_header("Accept", self.type)
		sconnection = urllib2.urlopen(srequest)
		self.data = json.load(sconnection)
		self.listofstocks = self.data
		            
    
# ----- View -----
class GUI:

	def __init__(self):
		self.window = Tk()
		self.window.minsize(460, 240)
		self.window.title("TradeNet")
		self.build_widgets(self.window)
		self.api = API()
		self.window.mainloop()
		
	def portfoliocmd(self):
		portfolio = Portfolio()

		
	def transactioncmd(self):
		trans = Transaction()
		
		return
		
	
	def submit(self):
		symbol = self.input_txt.get()
		if not symbol in _symbol_set:
			self.status.set("Invalid symbol")
		else:
			self.status.set("Valid symbol")
			self.api.fetch_quote(symbol)
			self.fill_display(self.api.quote)

	def buy(self):
		user = id_txt.get()
		quantity = quantity_txt.get()
		
		buyurl = "" + user + "?" + quantity
		request = urllib2.Request(buyurl)
		request.add_header("Accept", "application/json")
		connection = urllib2.urlopen(request)
		self.data = json.load(connection)
		reply = self.data
				
		return

	def sell(self):
		user = id_txt.get()
		quantity = quantity_txt.get()
		
		sellurl = "" + user + "?" + quantity
		request = urllib2.Request(sellurl)
		request.add_header("Accept", "application/json")
		connection = urllib2.urlopen(request)
		self.data = json.load(connection)
		reply = self.data
		
		return
			
	def trade(self):
		id = self.id_txt.get()
			
	def fill_display(self, quote):
		for key in self.data_fields:
			self.data_fields[key].set(quote[key])
	
	def build_widgets(self, window):
		menubar = Menu(self.window)
		menubar.add_command(label="Portfolio", command = self.portfoliocmd)
		self.window.config(menu=menubar)
		
		menubar.add_command(label="Transaction Log", command = self.transactioncmd)
		self.window.config(menu=menubar)
	
		# input fields
		input_lbl = Label(self.window, text = "Enter symbol: ")
		input_lbl.grid(row = 0, column = 0, sticky = E)

		input_txt = Entry(self.window)
		input_txt.grid(row = 0, column = 1)
		self.input_txt = input_txt

		submit_btn = Button(self.window, text = "Submit", command = self.submit)
		submit_btn.grid(row = 0, column = 2, padx = 5)

		self.status = StringVar()
		output_lbl = Label(self.window, textvariable = self.status, width = 15, anchor = W)
		output_lbl.grid(row = 0, column = 3)

		#buy and sell
		id_lbl = Label(self.window, text = "Enter ID: ")
		id_lbl.grid(row = 12, column = 0, sticky = E)

		id_txt = Entry(self.window)
		id_txt.grid(row = 12, column = 1)
		self.id_txt = id_txt

		quantity_lbl = Label(self.window, text = "Enter Quantity: ")
		quantity_lbl.grid(row = 12, column = 2, sticky = E)

		quantity_txt = Entry(self.window)
		quantity_txt.grid(row = 12, column = 3)
		self.quantity_txt = quantity_txt

		buy_btn = Button(self.window, text = "Buy", command = self.buy)
		buy_btn.grid(row = 12, column = 4, padx = 0)

		sell_btn = Button(self.window, text = "Sell", command = self.sell)
		sell_btn.grid(row = 12, column = 5, padx = 0)

		# quote display fields
		self.data_fields = {}

		symbol_txt = StringVar()
		symbol_l = Label(self.window, text = "Symbol: ")
		symbol_l.grid(row = 2, sticky = E)
		symbol_lbl = Label(self.window, textvariable = symbol_txt)
		symbol_lbl.grid(row = 2, column = 1, sticky = W, columnspan = 3)
		self.data_fields["symbol"] = symbol_txt

		description_txt = StringVar()
		description_l = Label(self.window, text = "Description: ")
		description_l.grid(row = 3, sticky = E)
		description_lbl = Label(self.window, textvariable = description_txt)
		description_lbl.grid(row = 3, column = 1, sticky = W, columnspan = 3)
		self.data_fields["description"] = description_txt

		exch_txt = StringVar()
		exch_l = Label(self.window, text = "Exchange: ")
		exch_l.grid(row = 4, sticky = E)
		exch_lbl = Label(self.window, textvariable = exch_txt)
		exch_lbl.grid(row = 4, column = 1, sticky = W, columnspan = 3)
		self.data_fields["exch"] = exch_txt

		close_txt = StringVar()
		close_l = Label(self.window, text = "Closing Price: ")
		close_l.grid(row = 5, sticky = E)
		close_lbl = Label(self.window, textvariable = close_txt)
		close_lbl.grid(row = 5, column = 1, sticky = W, columnspan = 3)
		self.data_fields["close"] = close_txt

		change_txt = StringVar()
		change_l = Label(self.window, text = "Daily Net Change: ")
		change_l.grid(row = 6, sticky = E)
		change_lbl = Label(self.window, textvariable = change_txt)
		change_lbl.grid(row = 6, column = 1, sticky = W, columnspan = 3)
		self.data_fields["change"] = change_txt

		change_percentage_txt = StringVar()
		change_percentage_l = Label(self.window, text = "Daily Net Change Percentage: ")
		change_percentage_l.grid(row = 7, sticky = E)
		change_percentage_lbl = Label(self.window, textvariable = change_percentage_txt)
		change_percentage_lbl.grid(row = 7, column = 1, sticky = W, columnspan = 3)
		self.data_fields["change_percentage"] = change_percentage_txt

		volume_txt = StringVar()
		volume_l = Label(self.window, text = "Volume: ")
		volume_l.grid(row = 8, sticky = E)
		volume_lbl = Label(self.window, textvariable = volume_txt)
		volume_lbl.grid(row = 8, column = 1, sticky = W, columnspan = 3)
		self.data_fields["volume"] = volume_txt

		average_volume_txt = StringVar()
		average_volume_l = Label(self.window, text = "Average Volume: ")
		average_volume_l.grid(row = 9, sticky = E)
		average_volume_lbl = Label(self.window, textvariable = average_volume_txt)
		average_volume_lbl.grid(row = 9, column = 1, sticky = W, columnspan = 3)
		self.data_fields["average_volume"] = average_volume_txt

		week_52_high_txt = StringVar()
		week_52_high_l = Label(self.window, text = "52 Week High: ")
		week_52_high_l.grid(row = 10, sticky = E)
		week_52_high_lbl = Label(self.window, textvariable = week_52_high_txt)
		week_52_high_lbl.grid(row = 10, column = 1, sticky = W, columnspan = 3)
		self.data_fields["week_52_high"] = week_52_high_txt

		week_52_low_txt = StringVar()
		week_52_low_l = Label(self.window, text = "52 Week Low: ")
		week_52_low_l.grid(row = 11, sticky = E)
		week_52_low_lbl = Label(self.window, textvariable = week_52_low_txt)
		week_52_low_lbl.grid(row = 11, column = 1, sticky = W, columnspan = 3)
		self.data_fields["week_52_low"] = week_52_low_txt

app = GUI()
