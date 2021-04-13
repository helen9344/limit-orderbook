# orderbook
## Summary
Implementation of a limit orderbook. The two main classes are Trader and Exchange.

A Trader has an id, a hashmap of standing orders (orderId as key), and a list of all messages received from Exchange. A Trader can:
1. add an order by specifying: side [buy or sell], price, qty
2. cancel an order by specifying: orderId, qty.
A timestamp is generated with each request. 

The Exchange has a hashmap of standing orders (orderId as key) and process orders when matches are found. The Exchange also has a double linked list storing buying  orderId and their prices in ascending order. Another double linked list and ascending list is also used for storing selling orderId and prices. The Exchange process orders when matches are found and send traders:
1. orderAcknowledgement when an order is received
2. fillMessage when an order is filled (fully or partially)
3. cancelFeedback regarding cancel request. 

A log is automatically generated for all messages sent out from the Exchange. 


## File descriptions
- Trader.py - Trader class
- Exchange.py - Exchange class
- Order.py - Order class contain Order object and feedback message objects
- config.py - configure log for exchange
- unitTest_ExchangeBook.py, unitTest_traderBook.py - unit tests for exchange's orderbook and trader's orderbook

## Question 1. Asymptotic complexity of operations
- add order - O(log(n))
- cancel order - O(log(n))

To add an order,
* check whether a trade can be made - O(1) as it just compares the price of the order with the highest buy price or lower selll price on the orderbook. 
* process trade if exist - O(n) as the dominant case of deletion is O(n).
  * O(1) to edit quanity of an order only
  * dfd
* add remaining or original order to the orderbook - O(n) as.... 
  * O(n) to add price to a list, O(1) to add order to hashmap or oderId, O(1) to add orderId to double-linked list.



To cancel an order, the exchange needs to 
* find the order by orderId - O(1) to find item by key in dict
* edit its quanity or remove it form orderbook - O(n) as the dominant case of deletion is O(n).
  * O(1) to edit quanity of an order only
  * O(log(n)) to use bisect find item by price, O(n) to delete the price in a list, O(1) to delete double-linked list of orderId, O(1) to delete orderId in hashmap average case and O(n) in worst case. 

## Question 2. Effcient storage

Inspecting the exchanges transaction log are there any data properties which can be exploited to store the data more efficiently? There is no need for an implementation here, just describe an idea.
