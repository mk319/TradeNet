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
		self.window.resizable(0, 0)
		self.url = ""
		self.type = "application/json"
		self.build()

	def build(self):
		Label(self.window, text = "User ID: ").grid(row = 0, column = 0, sticky = E)

		input_txt = Entry(self.window)
		input_txt.grid(row = 0, column = 1)
		self.input_txt = input_txt

		Button(self.window, text = "Submit", command = self.submit).grid(row = 0, column = 2, padx = 5)

		Label(self.window, text = "Log: ").grid(row = 2, column = 0, sticky = E)
		
		logbox = Listbox(self.window, width = 50)
		logbox.grid(row=4,column = 0, columnspan = 3)
		logbox.insert(END, "Code    Shares    Purchase Price    Date")
		self.logbox = logbox

	def submit(self):
		url = self.url + self.input_txt.get()
		request = urllib2.Request(url)
		request.add_header("Accept", self.type)
		connection = urllib2.urlopen(request)
		logs = json.load(connection)
		
		self.logbox.delete(0, END)
		for log in logs:
			logstring =  log["stock"]+ "    " + log["shares"] + "    " + log["purchaseprice"] + "    " + log["datetime"]
			self.logbox.insert(END, logstring)

# ----- Portfolio Window -----
class Portfolio:

	def __init__(self):
		self.window = Tk()
		self.window.title("Portfolio")
		self.window.resizable(0, 0)
		self.balanceurl = ""
		self.stockurl = ""
		self.type = "application/json"
		self.api = API()
		self.build()

	def build(self):
		Label(self.window, text = "User ID: ").grid(row = 0, column = 0, sticky = E)

		input_txt = Entry(self.window)
		input_txt.grid(row = 0, column = 1)
		self.input_txt = input_txt

		Button(self.window, text = "Submit", command = self.submit).grid(row = 0, column = 2, padx = 5)

		Label(self.window, text = "Balance: ").grid(row = 2, column = 0, sticky = E)

		self.balance_txt = StringVar()
		Label(self.window, textvariable = self.balance_txt).grid(row = 2, column = 1, sticky = W)

		Label(self.window, text = "Stocks: ").grid(row = 3, column = 0, sticky = E)

		stockbox = Listbox(self.window, width = 50)
		stockbox.grid(row = 4, column = 0, columnspan = 3)
		stockbox.insert(END, "Code    Shares    Current Price    Current Value")
		self.stockbox = stockbox
		
	def submit(self):
		burl = self.balanceurl + self.input_txt.get()
		brequest = urllib2.Request(burl)
		brequest.add_header("Accept", self.type)
		bconnection = urllib2.urlopen(brequest)
		data = json.load(bconnection)
		self.balance_txt = data["accountbalance"]

		surl = self.stockurl + self.input_txt.get()
		srequest = urllib2.Request(surl)
		srequest.add_header("Accept", self.type)
		sconnection = urllib2.urlopen(srequest)
		listofstocks = json.load(sconnection)
		
		self.stockbox.delete(0, END)
		for stock in listofstocks:
			self.api.fetchquote(stock["stock"])
			stockstring =  stock["stock"]+ "    " + stock["shares"] + "    " + self.api.quote["close"] + "    " + self.api.quote["close"] * stock["shares"]
			stockbox.insert(END, stockstring)
		
# ----- View -----
class GUI:

	def __init__(self):
		self.window = Tk()
		self.window.resizable(0, 0)
		self.window.title("TradeNet")
		self.build_widgets(self.window)
		self.api = API()
		self.window.mainloop()
		
	def portfoliocmd(self):
		portfolio = Portfolio()
		
	def transactioncmd(self):
		trans = Transaction()
	
	def submit(self):
		symbol = self.input_txt.get()
		if not symbol in _symbol_set:
			self.status.set("Invalid symbol")
		else:
			self.status.set("Valid symbol")
			self.api.fetch_quote(symbol)
			self.fill_display(self.api.quote)

	def buy(self):
		user = self.id_txt.get()
		quantity = self.quantity_txt.get()
		symbol = self.input_txt.get()
		
		buyurl = "http://pluto.cse.msstate.edu:10045/TradeNet_war/BuyStock.html?stock=" + symbol + "&custId=" + user + "&shares=" + quantity
		request = urllib2.Request(buyurl)
		request.add_header("Accept", "application/json")
		connection = urllib2.urlopen(request)
		self.data = json.load(connection)
		reply = self.data
		success = Tk()
		if reply["success"]==1:
			sf = "Success"
		else:
			sf = "Failure"
		Label(success, text = reply["success"]).grid(row = 0, column = 0)

	def sell(self):
		user = self.id_txt.get()
		quantity = self.quantity_txt.get()
		symbol = self.input_txt.get()
		
		sellurl = "http://pluto.cse.msstate.edu:10045/TradeNet_war/SellStock.html?stock=" + symbol + "&custId=" + user + "&shares=" + quantity
		request = urllib2.Request(sellurl)
		request.add_header("Accept", "application/json")
		connection = urllib2.urlopen(request)
		self.data = json.load(connection)
		reply = self.data
			
	def trade(self):
		id = self.id_txt.get()
			
	def fill_display(self, quote):
		for key in self.data_fields:
			self.data_fields[key].set(quote[key])
	
	def build_widgets(self, window):
		menubar = Menu(self.window)
		menubar.add_command(label = "Portfolio", command = self.portfoliocmd)
		menubar.add_command(label = "Transaction Log", command = self.transactioncmd)
		self.window.config(menu = menubar)
	
		# input fields
		Label(self.window, text = "Enter symbol: ").grid(row = 0, column = 0, sticky = E)

		input_txt = Entry(self.window)
		input_txt.grid(row = 0, column = 1)
		self.input_txt = input_txt

		Button(self.window, text = "Submit", command = self.submit).grid(row = 0, column = 2, padx = 5, columnspan = 2)

		self.status = StringVar()
		Label(self.window, textvariable = self.status, width = 15, anchor = W).grid(row = 0, column = 4)

		# buy and sell
		Label(self.window, text = "Enter ID: ").grid(row = 12, column = 0, sticky = E)

		id_txt = Entry(self.window)
		id_txt.grid(row = 12, column = 1)
		self.id_txt = id_txt

		Label(self.window, text = "Enter Quantity: ").grid(row = 13, column = 0, sticky = E)

		quantity_txt = Entry(self.window)
		quantity_txt.grid(row = 13, column = 1)
		self.quantity_txt = quantity_txt

		Button(self.window, text = "Buy", command = self.buy).grid(row = 13, column = 2, padx = 5)
		Button(self.window, text = "Sell", command = self.sell).grid(row = 13, column = 3)

		# quote display fields
		self.data_fields = {}

		symbol_txt = StringVar()
		Label(self.window, text = "Symbol: ").grid(row = 2, sticky = E)
		Label(self.window, textvariable = symbol_txt).grid(row = 2, column = 1, sticky = W, columnspan = 4)
		self.data_fields["symbol"] = symbol_txt

		description_txt = StringVar()
		Label(self.window, text = "Description: ").grid(row = 3, sticky = E)
		Label(self.window, textvariable = description_txt).grid(row = 3, column = 1, sticky = W, columnspan = 4)
		self.data_fields["description"] = description_txt

		exch_txt = StringVar()
		Label(self.window, text = "Exchange: ").grid(row = 4, sticky = E)
		Label(self.window, textvariable = exch_txt).grid(row = 4, column = 1, sticky = W, columnspan = 4)
		self.data_fields["exch"] = exch_txt

		close_txt = StringVar()
		Label(self.window, text = "Closing Price: ").grid(row = 5, sticky = E)
		Label(self.window, textvariable = close_txt).grid(row = 5, column = 1, sticky = W, columnspan = 4)
		self.data_fields["close"] = close_txt

		change_txt = StringVar()
		Label(self.window, text = "Daily Net Change: ").grid(row = 6, sticky = E)
		Label(self.window, textvariable = change_txt).grid(row = 6, column = 1, sticky = W, columnspan = 4)
		self.data_fields["change"] = change_txt

		change_percentage_txt = StringVar()
		Label(self.window, text = "Daily Net Change Percentage: ").grid(row = 7, sticky = E)
		Label(self.window, textvariable = change_percentage_txt).grid(row = 7, column = 1, sticky = W, columnspan = 4)
		self.data_fields["change_percentage"] = change_percentage_txt

		volume_txt = StringVar()
		Label(self.window, text = "Volume: ").grid(row = 8, sticky = E)
		Label(self.window, textvariable = volume_txt).grid(row = 8, column = 1, sticky = W, columnspan = 4)
		self.data_fields["volume"] = volume_txt

		average_volume_txt = StringVar()
		Label(self.window, text = "Average Volume: ").grid(row = 9, sticky = E)
		Label(self.window, textvariable = average_volume_txt).grid(row = 9, column = 1, sticky = W, columnspan = 4)
		self.data_fields["average_volume"] = average_volume_txt

		week_52_high_txt = StringVar()
		Label(self.window, text = "52 Week High: ").grid(row = 10, sticky = E)
		Label(self.window, textvariable = week_52_high_txt).grid(row = 10, column = 1, sticky = W, columnspan = 4)
		self.data_fields["week_52_high"] = week_52_high_txt

		week_52_low_txt = StringVar()
		Label(self.window, text = "52 Week Low: ").grid(row = 11, sticky = E)
		Label(self.window, textvariable = week_52_low_txt).grid(row = 11, column = 1, sticky = W, columnspan = 4)
		self.data_fields["week_52_low"] = week_52_low_txt

GUI()
