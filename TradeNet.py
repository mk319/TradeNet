from Tkinter import *
import urllib2
import json

# valid symbols
symbol_set = ["FB", "AAPL", "GOOG", "MSFT", "CRM", "TWTR", "BABA", "SPY", "QQQ", "DIA"]

# submit button command
def submit():
	symbol = input_txt.get()
	if not symbol in symbol_set:
		status.set("Invalid symbol")
	else:
		status.set("Valid symbol")
		url = "https://sandbox.tradier.com/v1/markets/quotes?symbols=" + symbol
		request = urllib2.Request(url)
		request.add_header("Accept", "application/json")
		request.add_header("Authorization", "Bearer TSCALKvrKOHFY1VH05ML7oMBbil4")
		connection = urllib2.urlopen(request)
		quote = json.load(connection)
		quote = quote["quotes"]["quote"]
		for key in data_fields:
			data_fields[key].set(quote[key])

# creates window
root = Tk()

# input fields
input_lbl = Label(root, text = "Enter symbol: ")
input_lbl.grid(row = 0, column = 0, sticky = E)

input_txt = Entry(root)
input_txt.grid(row = 0, column = 1)

submit_btn = Button(root, text = "Submit", command = submit)
submit_btn.grid(row = 0, column = 2, padx = 5)

status = StringVar()
output_lbl = Label(root, textvariable = status, width = 15, anchor = W)
output_lbl.grid(row = 0, column = 3)

# display fields
data_fields = {}

symbol_txt = StringVar()
symbol_l = Label(root, text = "Symbol: ")
symbol_l.grid(row = 1, sticky = E)
symbol_lbl = Label(root, textvariable = symbol_txt)
symbol_lbl.grid(row = 1, column = 1, sticky = W)
data_fields["symbol"] = symbol_txt

description_txt = StringVar()
description_l = Label(root, text = "Description: ")
description_l.grid(row = 2, sticky = E)
description_lbl = Label(root, textvariable = description_txt)
description_lbl.grid(row = 2, column = 1, sticky = W)
data_fields["description"] = description_txt

exch_txt = StringVar()
exch_l = Label(root, text = "Exchange: ")
exch_l.grid(row = 3, sticky = E)
exch_lbl = Label(root, textvariable = exch_txt)
exch_lbl.grid(row = 3, column = 1, sticky = W)
data_fields["exch"] = exch_txt

close_txt = StringVar()
close_l = Label(root, text = "Closing Price: ")
close_l.grid(row = 4, sticky = E)
close_lbl = Label(root, textvariable = close_txt)
close_lbl.grid(row = 4, column = 1, sticky = W)
data_fields["close"] = close_txt

change_txt = StringVar()
change_l = Label(root, text = "Daily Net Change: ")
change_l.grid(row = 5, sticky = E)
change_lbl = Label(root, textvariable = change_txt)
change_lbl.grid(row = 5, column = 1, sticky = W)
data_fields["change"] = change_txt

change_percentage_txt = StringVar()
change_percentage_l = Label(root, text = "Daily Net Change Percentage: ")
change_percentage_l.grid(row = 6, sticky = E)
change_percentage_lbl = Label(root, textvariable = change_percentage_txt)
change_percentage_lbl.grid(row = 6, column = 1, sticky = W)
data_fields["change_percentage"] = change_percentage_txt

volume_txt = StringVar()
volume_l = Label(root, text = "Volume: ")
volume_l.grid(row = 7, sticky = E)
volume_lbl = Label(root, textvariable = volume_txt)
volume_lbl.grid(row = 7, column = 1, sticky = W)
data_fields["volume"] = volume_txt

average_volume_txt = StringVar()
average_volume_l = Label(root, text = "Average Volume: ")
average_volume_l.grid(row = 8, sticky = E)
average_volume_lbl = Label(root, textvariable = average_volume_txt)
average_volume_lbl.grid(row = 8, column = 1, sticky = W)
data_fields["average_volume"] = average_volume_txt

week_52_high_txt = StringVar()
week_52_high_l = Label(root, text = "52 Week High: ")
week_52_high_l.grid(row = 9, sticky = E)
week_52_high_lbl = Label(root, textvariable = week_52_high_txt)
week_52_high_lbl.grid(row = 9, column = 1, sticky = W)
data_fields["week_52_high"] = week_52_high_txt

week_52_low_txt = StringVar()
week_52_low_l = Label(root, text = "52 Week Low: ")
week_52_low_l.grid(row = 10, sticky = E)
week_52_low_lbl = Label(root, textvariable = week_52_low_txt)
week_52_low_lbl.grid(row = 10, column = 1, sticky = W)
data_fields["week_52_low"] = week_52_low_txt

# shows window
root.mainloop()
