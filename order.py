#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 08:20:20 2021

@author: zhu
"""

class Order:
    def __init__(self, traderId, side, price, qty, orderId, timestamp):
        self.traderId = traderId
        self.side = side
        self.price = price
        self.qty = qty
        self.orderId = orderId
        self.timestamp = timestamp
    
    def tostr(self):
        return ("orderid:=" + str(self.orderId) + ",timestamp:=" + str(self.timestamp))


class orderAcknowledgement:
    def __init__(self, orderId, timestamp):
        self.orderId = orderId
        self.timestamp = timestamp
        
    def tostr(self):
        return ("orderid:=" + str(self.orderId) + ",timestamp:=" + str(self.timestamp))


class fillMessage:
     def __init__(self, orderId, fillId, timestamp, qty):
        self.orderId = orderId
        self.fillId = fillId
        self.timestamp = timestamp
        self.qty = qty
    
     def tostr(self):
        return ("orderid:=" + str(self.orderId) + ",fillId:=" + str(self.fillId) + 
                ",qty:=" + str(self.qty) + ",timestamp:=" + str(self.timestamp))


class cancelFeedback:
    def __init__(self, orderId, boolResp, timestamp):
        self.orderId = orderId
        self.boolResp = boolResp
        self.timestamp = timestamp
    
    def tostr(self):
        return ("orderid:=" + str(self.orderId) + ",timestamp:=" + str(self.timestamp))

        
        
        