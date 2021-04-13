#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 08:35:55 2021

@author: zhu
"""


import time
import bisect
import uuid

from order import Order
from order import orderAcknowledgement
from order import fillMessage
from order import cancelFeedback
from trader import Trader

from llist import sllist

from config import getLogger

logger = getLogger(__name__)
 


class Exchange:

    def __init__(self, orderSell = None, orderBuy = None, sellPrices = None, buyPrices = None, 
                 orderMap = None, standingBuys = None, msgs = None):
        self.orderSell = sllist()
        self.orderBuy = sllist()
        self.sellPrices = [] # price of sell orders, nondescenidng
        self.buyPrices = [] # price of buy orders, nondescenidng
        
        self.orderMap = {} # Hashmap of all standing orders with orderId as key
        self.traderMap = {} # Hashmap of traders connected with trader id as key
        
    
    def connectToTrader(self, trader):
       self.traderMap[trader.id] = trader
       
    def __createOrderId(self):
        return (uuid.uuid1())
       
     
    def sendMsg(self, traderId, msg):
        trader = self.traderMap[traderId]
        trader.accept_msg(msg)
        logger.info("send:FillMsg~" + "traderId:=" + str(traderId) +"," + msg.tostr())
       
        
    def orderAdd(self, traderId, side, price, qty, ts):
        
        if traderId not in self.traderMap.keys():
            raise ValueError('trader not recognized')
        
        new_orderId = self.__createOrderId()
        
        order = Order(traderId, side, price, qty, new_orderId, ts)
        logger.info("receive:OrderAdd~" + "traderId:=" + str(traderId) +"," +  order.tostr())
        
        orderNotFilled = True
        if order.side == "buy":
            # check condition where trade can be made
            if len(self.sellPrices)>0 and self.sellPrices[0] <= order.price:
                trade_exist = True
                totalQty_filled = 0 
                
                while trade_exist:
                    cheapest_sell = self.orderMap[self.orderSell[0]]
                    fill_qty = min(order.qty, cheapest_sell.qty)
                    totalQty_filled += fill_qty
                    
                    # update buy order and sell order
                    order.qty -= fill_qty
                    cheapest_sell.qty -= fill_qty
                    
                    # send fill message to seller
                    fill_msg_seller = fillMessage(cheapest_sell.orderId, uuid.uuid1(), time.time(), fill_qty)
                    self.sendMsg(cheapest_sell.traderId, fill_msg_seller)

                    if cheapest_sell.qty == 0:
                        self.orderMap.pop(cheapest_sell.orderId)
                        self.sellPrices.pop(0)
                        self.orderSell.remove(self.orderSell.nodeat(0))
                        
                    trade_exist = order.qty>0 and len(self.sellPrices)>0 and self.sellPrices[0] <= order.price
                    # orderNotFilled = order.qty>0
                    
                # send fillMessage to buyer
                fill_msg_buyer = fillMessage(order.orderId, uuid.uuid1(), time.time(), totalQty_filled)
                self.sendMsg(order.traderId, fill_msg_buyer)

            #  add order when no trade, or remaing order after trade
            if order.qty > 0:
                self.orderMap[order.orderId] = order
                insert_ind = bisect.bisect_right(self.buyPrices, order.price)
                self.buyPrices.insert(insert_ind, order.price)
                
                if insert_ind == 0:
                    self.orderBuy.append(order.orderId)
                else:
                    prev_node = self.orderBuy.nodeat(insert_ind-1)
                    self.orderBuy.insertafter(order.orderId, prev_node)

        else: # order.side == "sell"
            # check condition where trade can be made
            if len(self.buyPrices)>0 and self.buyPrices[-1] >= order.price:
                trade_exist = True
                totalQty_filled = 0
                
                while trade_exist:
                    highest_price_early_ind = bisect.bisect_left(self.buyPrices, self.buyPrices[-1])
                    highest_early_buy = self.orderMap[self.orderBuy[highest_price_early_ind]]
                    fill_qty = min(highest_early_buy.qty, order.qty)
                    totalQty_filled += fill_qty
                    
                    # update buy order and send fillMessage to buyer
                    highest_early_buy.qty -= fill_qty
                    fill_msg_buyer = fillMessage(highest_early_buy.orderId, uuid.uuid1(), time.time(), fill_qty)
                    self.sendMsg(highest_early_buy.traderId, fill_msg_buyer)

                    if highest_early_buy.qty == 0:
                        self.orderMap.pop(highest_early_buy.orderId)
                        self.buyPrices.pop(highest_price_early_ind)
                        self.orderBuy.remove(self.orderBuy.nodeat(highest_price_early_ind))
                    
                    # update buy order 
                    order.qty -= fill_qty
                    trade_exist = order.qty>0 and len(self.buyPrices)>0 and self.buyPrices[-1] >= order.price
                    orderNotFilled = order.qty>0
    
                fill_msg_seller = fillMessage(order.orderId, uuid.uuid1(), time.time(), totalQty_filled)
                self.sendMsg(order.traderId, fill_msg_seller)

            #  add order when no trade, or remaing order after trade
            if order.qty > 0 and orderNotFilled:
                
                self.orderMap[order.orderId] = order
                insert_ind = bisect.bisect_right(self.sellPrices, order.price)
                self.sellPrices.insert(insert_ind, order.price)
                
                if insert_ind == 0:
                    self.orderSell.append(order.orderId)
                else:
                    prev_node = self.orderSell.nodeat(insert_ind-1)
                    self.orderSell.insertafter(order.orderId, prev_node)
                    
        orderAck = orderAcknowledgement(new_orderId, ts)
        logger.info("send:OrderAcknowledgementMsg~" + "," + orderAck.tostr())
        return (orderAck)
    
    
    
    def orderCancel(self, order_id, qty, ts):
        
        timestamp = time.time()
        
        if len(self.orderMap) > 0 and order_id in self.orderMap and self.orderMap[order_id].qty >= qty:
            order = self.orderMap[order_id]
            
            if qty < order.qty: # case of reduce order 
                order.qty -= qty
            else: 
                # case of delete an order
                self.orderMap.pop(order_id)
                
                if order.side == "buy":
                    stop_ind = bisect.bisect_right(self.buyPrices, order.price)
                    possible_orders = list(self.orderBuy)[:stop_ind][::-1]
                    delete_ind = possible_orders.index(order_id)
                    self.buyPrices.pop(delete_ind)
                    self.orderBuy.remove(self.orderBuy.nodeat(delete_ind))
                
                else: 
                    # order.side == "sell"
                    stop_ind = bisect.bisect_right(self.sellPrices, order.price)
                    possible_orders = list(self.orderSell)[:stop_ind][::-1]
                    delete_ind = possible_orders.index(order_id)
                    self.sellPrices.pop(delete_ind)
                    self.orderSell.remove(self.orderSell.nodeat(delete_ind))
                    
            cancelStatus = cancelFeedback(order_id, True, timestamp)
            logger.info("receive:OrderCancel~" + "," + cancelStatus.tostr())
        
        else:
            cancelStatus = cancelFeedback(order_id, False, timestamp)
        
        return(cancelStatus)
    
        
