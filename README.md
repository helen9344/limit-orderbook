# orderbook
## Summary
Implementation of a limit orderbook. The two main classes are Trader and Exchange.

A Trader has an id, a hashmap of standing orders (orderId as key), and a list of all messages received from Exchange. A Trader can:
1. add an order by specifying: side [buy or sell], price, qty
2. cancel an order by specifying: orderId, qty.
A timestamp is generated with each request. 

The Exchange has a hashmap of standing orders (orderId as key) and process orders when matches are found. The Exchange also has a double linked list storing buying  orderId and a list for their prices in ascending order. Another double linked list and ascending list are used for storing selling orderId and prices. The Exchange process orders when matches are found and send traders:
1. orderAcknowledgement when an order is received
2. fillMessage when an order is filled (fully or partially indicated by qty)
3. cancelFeedback regarding cancel request. 

A log is automatically generated for the Exchange for all messages it sent out. 


## File descriptions
- Trader.py - Trader class
- Exchange.py - Exchange class
- Order.py - Order class contain Order object and message objects
- config.py - configure log for exchange
- unitTest_ExchangeBook.py, unitTest_traderBook.py - unit tests for exchange's orderbook and trader's orderbook
- unitTest_ExchangeBook.ipynb - a duplicate of unitTest_ExchangeBook.py in jupyter notebook to show that the orderbook is working and passing tests. 

## Question 1. Asymptotic complexity of operations
- add order - O(log(n))
- cancel order - O(log(n))

To add an order,
* check whether a trade can be made - O(1) as it just compares the price of the order with the highest buy price or lower selll price on the orderbook. 
* process trade if exist - O(n) as the most costly operation of adding is O(n).
  * O(1) to edit quanity of an order only
  * O(1) to remove a existing sell order as the costly operation is to delete price which in this case it is at begining of a list, thus O(1), O(1) to delete from orderId hashmap and linkedlist for sell order
  * O(n) to remove existing buy order as O(n) to delete its price in the list, O(1) to delete from orderId hashmap and linkedlist for sell order
* add remaining or original order to the orderbook - O(n) due to the dominant operation of adding to a list
  * O(log(n)) to find where to add price and orderId, O(n) to add price to a list, O(1) to add orderId to double-linked list, O(1) to add order to hashmap or oderId.



To cancel an order, the exchange needs to 
* find the order by orderId - O(1) to find item by key in dict
* edit its quanity or remove it form orderbook - O(n) as the dominant case of deletion is O(n).
  * O(1) to edit quanity of an order only
  * O(log(n)) to use bisect find item by price, O(n) to delete the price in a list, O(1) to delete double-linked list of orderId, O(1) to delete orderId in hashmap in average case and O(n) in worst case. 

## Question 2. Effcient storage

Inspecting the exchanges transaction log are there any data properties which can be exploited to store the data more efficiently? There is no need for an implementation here, just describe an idea.
