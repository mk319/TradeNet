Establish and create Account Management (AM) Server database to store at minimum:

• Customer information (ID, first name, address, account balance, current profit and loss)

• Transactions (ID, stock, #shares bought / sold [positive / negative], date and time)

• Portfolio (CustomerID, stocks, shares, purchase price)

Create separate Trade Execution server (standalone [e.g., sockets, Java RMI] or using technology of choice
[e.g., Tomcat, GlassFish, Django])

• Tradiers Market connection for current equity pricing (last price) for any listed equity

• AM Server connection to store buy/sell transactions and update customer account info as needed

• Logic to execute trades

Create Client Interface (can extend previously built interface from PP #3)

• List stock information

• Execute buy / sell transactions for a customer ID

• Fields: CustomerID, Stock ticker, Buy / Sell button, number of shares, account balance

• View Portfolio

• List stocks held, current price, # of shares, and value (price * shares)

• List Transaction history

Logic in either the client or server to reject trades

• Based on account balance - are funds available to complete the transaction

• For sell transactions, do they own the shares to sell
