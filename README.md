# Limit Orderbook
## Summary
Implementation of a limit orderbook. The two main classes are Trader and Exchange.

A instance of the **Trader** class contain _id_, _standing_order_: a hashmap of standing orders (orderId as key), and _log_: a list of all messages received from Exchange. A Trader instance can acess method
1. OrderAdd: place an order by specify side [buy or sell], price, qty
2. OrderCancel: an order by specifying: orderId, qty.
A timestamp is generated with each request. 

A instance of the **Exchange** class has _orderMap_: a hashmap of standing orders (orderId as key) and has main method _orderAdd_ and _orderCancel_ to add (which also match and cancel) and cancel orders. To facilitate order processing, the Exchange also contain _orderSell (orderBuy)_: a double linked list storing sell (buy) orderId and _sellPrices (buyPrices)_: a list for their prices in ascending order. The Exchange process orders when matches are found and send traders:
1. orderAcknowledgement when an order is received
2. fillMessage when an order is filled (fully or partially indicated by qty)
3. cancelFeedback regarding cancel request. 

A log is automatically generated for the Exchange for all messages it sent out. 


## File descriptions
- main files
 - Trader.py - Trader class
 - Exchange.py - Exchange class
 - Order.py - Order class contain Order object and message objects
- test files
 - config.py - configure log for exchange
 - unitTest_ExchangeBook.py, unitTest_traderBook.py - unit tests for exchange's orderbook and trader's orderbook
 - unitTest_ExchangeBook.ipynb - a duplicate of unitTest_ExchangeBook.py in jupyter notebook to show that the orderbook is working and passing tests. 

## Question 1. Asymptotic complexity of operations
- add order - O(n)
- cancel order - O(n)

To add an order,
* check whether a trade can be made - O(1) as it just compares the price of the order with the highest buy price or lower sell price on the orderbook. 
* process trade if exist - O(n) 
  * O(1) to remove a existing sell order as the costly operation is to delete price which in this case it is at begining of a list, thus O(1), O(1) to delete from orderId hashmap and linkedlist for sell order
  * O(n) to remove existing buy order as O(n) to delete its price in the list, O(1) to delete from orderId hashmap and linkedlist for sell order
* add remaining or original order to the orderbook - O(n) 
  * O(log(n)) to find where to add price and orderId, O(n) to add price to a list, O(1) to add orderId to double-linked list, O(1) to add order to hashmap or oderId.



To cancel an order, the exchange needs to 
* find the order by orderId - O(1) to find item by key in dict
* edit its quanity or remove it form orderbook - O(n) as the dominant case of deletion is O(n).
  * O(1) to edit quanity of an order only
  * O(log(n)) to use bisect find item by price, O(n) to delete the price in a list, O(1) to delete double-linked list of orderId, O(1) to delete orderId in hashmap in average case and O(n) in worst case. 

## Question 2. Effcient storage

Inspecting the exchanges transaction log are there any data properties which can be exploited to store the data more efficiently? There is no need for an implementation here, just describe an idea.
