#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 08:20:20 2021

@author: zhu
"""

import time
import warnings

from order import Order
from order import orderAcknowledgement
from order import fillMessage

class Trader:
     
    def show_orderId(self):
        return(list(self.orders.keys()))

    def __init__(self, traderId, limit_per_sec = 100):
        self.id = traderId
        self.standing_orders = {} # hashmap of orderId and Order for standing order
        self.fill_waiting = {}
        
        self.log = []
        self.last_time = 0    
        self.limit_per_sec = limit_per_sec
        self.count = 0
        
        
    def OrderAdd(self, side, price, qty, exchange):
        
        ts = time.time()
        
        if not self._is_below_limit(ts):
            warnings.warn('number of trades exceeded ' + str(self.limit_per_sec))
            return 
        
        orderAck = exchange.orderAdd(self.id, side, price, qty, ts)
        orderId = orderAck.orderId
        self.standing_orders[orderId] = Order(self.id, side, price, qty, orderId, ts)
        self.log.append(orderAck)
        
        if orderId in self.fill_waiting.keys():
            pending = self.fill_waiting[orderId]
            self.accept_msg(pending)
            self.fill_waiting.pop(orderId)
                                        

    def OrderCancel(self, orderId, qty, exchange):
        
        ts = time.time()
        
        if not self._is_below_limit(ts):
            warnings.warn('number of trades exceeded ' + str(self.limit_per_sec))
            return 
        
        cancel_feedback = exchange.orderCancel(orderId, qty, ts)
        self.log.append(cancel_feedback)
        if cancel_feedback.boolResp:
            self.standing_orders[orderId].qty -= qty
            if self.standing_orders[orderId].qty == 0:
                self.standing_orders.pop(orderId)
                
                
    def _is_below_limit(self, timestamp):
        if timestamp - self.last_time > 1 :
            self.count = 1
            self.last_time = timestamp
            return True
        else :
            if self.count + 1 > self.limit_per_sec :
                return False
        self.count +=1
        return True
        
        
    def connectToExchange(self, exchange):
        exchange.connectToTrader(self)
        return self
    
    def accept_msg(self, msg):
        
        orderId = msg.orderId
        if orderId not in self.standing_orders.keys():
            self.fill_waiting[orderId] = msg
            return
        
        self.log.append(msg)
        order = self.standing_orders[msg.orderId]
        order.qty -= msg.qty
        if order.qty == 0:
            self.standing_orders.pop(orderId)

    

