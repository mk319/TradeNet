from Tkinter import *
from urllib2 import *

# valid symbols
symbol_set = ["FB", "AAPL", "GOOG", "MSFT", "CRM", "TWTR", "BABA", "SPY", "QQQ", "DIA"]

# creates window
root = Tk()

input_label = Label(root, text = "Symbol: ")
input_label.pack(side = LEFT)

input = Entry(root, )
input.pack(side = RIGHT)

# shows window
root.mainloop()

# symbol = input.get()
# url = "https://api.tradier.com/v1/markets/quotes?symbols=" + symbol
# headers = {"Accept": "application/json", "Authorization": "Bearer YOUR_ACCESS_TOKEN"}
# request = urllib2.Request(url, headers)
# connection = urllib2.urlopen(request)
