# orderbook
## Summary
Implementation of a limit orderbook. The two main objects are Trader and Exchange.

Trader store his live (standing) order and can:
1. add an order by specifying: side [buy or sell], price, qty
2. cancel an order by specifying: orderId, qty.

Exchange keeps an orderbook and process orders when matches are found. Exchange also keeps a log of activities and send traders:
1. orderAcknowledgement when an order is received
2. fillMessage when an order is filled (fully or partially)
3. cancelFeedback regarding cancel request. 


## File descriptions
- Trader.py - Trader class
- Exchange.py - Exchange class
- Order.py - Order class contain Order object and feedback message objects
- config.py - configure log for exchange
- unitTest_ExchangeBook.py, unitTest_traderBook.py - unit tests for exchange's orderbook and trader's orderbook

## Question 1. Asymptotic complexity of operations
- add order - O(log(n))
- cancel order - 

## Question 2. Effcient storage

