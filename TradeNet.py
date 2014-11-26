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

# ----- View -----
class GUI:

	def __init__(self):
		self.window = Tk()
		self.window.minsize(450, 250)
		self.window.title("TradeNet")
		self.build_widgets()
		self.api = API()
		self.window.mainloop()
		
	def submit(self):
		symbol = self.input_txt.get()
		if not symbol in _symbol_set:
			self.status.set("Invalid symbol")
		else:
			self.status.set("Valid symbol")
			self.api.fetch_quote(symbol)
			self.fill_display(self.api.quote)
			
	def fill_display(self, quote):
		for key in self.data_fields:
			self.data_fields[key].set(quote[key])
	
	def build_widgets(self):
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

		# display fields
		self.data_fields = {}

		symbol_txt = StringVar()
		symbol_l = Label(self.window, text = "Symbol: ")
		symbol_l.grid(row = 1, sticky = E)
		symbol_lbl = Label(self.window, textvariable = symbol_txt)
		symbol_lbl.grid(row = 1, column = 1, sticky = W, columnspan = 3)
		self.data_fields["symbol"] = symbol_txt

		description_txt = StringVar()
		description_l = Label(self.window, text = "Description: ")
		description_l.grid(row = 2, sticky = E)
		description_lbl = Label(self.window, textvariable = description_txt)
		description_lbl.grid(row = 2, column = 1, sticky = W, columnspan = 3)
		self.data_fields["description"] = description_txt

		exch_txt = StringVar()
		exch_l = Label(self.window, text = "Exchange: ")
		exch_l.grid(row = 3, sticky = E)
		exch_lbl = Label(self.window, textvariable = exch_txt)
		exch_lbl.grid(row = 3, column = 1, sticky = W, columnspan = 3)
		self.data_fields["exch"] = exch_txt

		close_txt = StringVar()
		close_l = Label(self.window, text = "Closing Price: ")
		close_l.grid(row = 4, sticky = E)
		close_lbl = Label(self.window, textvariable = close_txt)
		close_lbl.grid(row = 4, column = 1, sticky = W, columnspan = 3)
		self.data_fields["close"] = close_txt

		change_txt = StringVar()
		change_l = Label(self.window, text = "Daily Net Change: ")
		change_l.grid(row = 5, sticky = E)
		change_lbl = Label(self.window, textvariable = change_txt)
		change_lbl.grid(row = 5, column = 1, sticky = W, columnspan = 3)
		self.data_fields["change"] = change_txt

		change_percentage_txt = StringVar()
		change_percentage_l = Label(self.window, text = "Daily Net Change Percentage: ")
		change_percentage_l.grid(row = 6, sticky = E)
		change_percentage_lbl = Label(self.window, textvariable = change_percentage_txt)
		change_percentage_lbl.grid(row = 6, column = 1, sticky = W, columnspan = 3)
		self.data_fields["change_percentage"] = change_percentage_txt

		volume_txt = StringVar()
		volume_l = Label(self.window, text = "Volume: ")
		volume_l.grid(row = 7, sticky = E)
		volume_lbl = Label(self.window, textvariable = volume_txt)
		volume_lbl.grid(row = 7, column = 1, sticky = W, columnspan = 3)
		self.data_fields["volume"] = volume_txt

		average_volume_txt = StringVar()
		average_volume_l = Label(self.window, text = "Average Volume: ")
		average_volume_l.grid(row = 8, sticky = E)
		average_volume_lbl = Label(self.window, textvariable = average_volume_txt)
		average_volume_lbl.grid(row = 8, column = 1, sticky = W, columnspan = 3)
		self.data_fields["average_volume"] = average_volume_txt

		week_52_high_txt = StringVar()
		week_52_high_l = Label(self.window, text = "52 Week High: ")
		week_52_high_l.grid(row = 9, sticky = E)
		week_52_high_lbl = Label(self.window, textvariable = week_52_high_txt)
		week_52_high_lbl.grid(row = 9, column = 1, sticky = W, columnspan = 3)
		self.data_fields["week_52_high"] = week_52_high_txt

		week_52_low_txt = StringVar()
		week_52_low_l = Label(self.window, text = "52 Week Low: ")
		week_52_low_l.grid(row = 10, sticky = E)
		week_52_low_lbl = Label(self.window, textvariable = week_52_low_txt)
		week_52_low_lbl.grid(row = 10, column = 1, sticky = W, columnspan = 3)
		self.data_fields["week_52_low"] = week_52_low_txt

app = GUI()
