#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 09:41:46 2021

@author: zhu
"""


from order import Order
# from order import orderAcknowledgement
# from order import fillMessage
from trader import Trader
from exchange import Exchange

import unittest
import logging

class TestOrderBook(unittest.TestCase):
    
    def setUp(self):
        # SETUP the following default order book for testing:
        #------------------------------------------------
        # BUY                         SELL
        #-----------------            -------------------
        #Price      qty               Price        qty
        #------     ------            ------       ------
        #23.01      30                25.0         20
        #24.02      10                
        #        
        
        logging.disable(logging.INFO)                    
        
        self.e = Exchange()     
        
        # Set up trader and connect to exchange
        self.trader1 = Trader(1).connectToExchange(self.e)
        self.trader2 = Trader(2).connectToExchange(self.e)
            
        self.trader1.OrderAdd("buy", 23.01, 30, self.e)
        self.trader1.OrderAdd("sell", 25.0, 20, self.e)
        self.trader2.OrderAdd("buy", 24.02, 10, self.e)
    
    def tearDown(self):        
        logging.disable(logging.NOTSET)

    def test_sell_1(self):
        # Check adding 2 sell orders appear on exchange orderbook and trader's book
        self.trader2.OrderAdd("sell", 24.5, 15, self.e)
        self.assertTrue(list(self.trader1.standing_orders.keys())[1] in self.e.orderMap)
        self.assertTrue(list(self.trader2.standing_orders.keys())[1] in self.e.orderMap)
        self.assertTrue(len(self.trader1.standing_orders.keys()) == 2)
        self.assertTrue(len(self.trader2.standing_orders.keys()) == 2)
        
    
    def test_sell_2(self):
        # Test add an order can be filled partially
        self.trader2.OrderAdd("sell", 24, 5, self.e)
        self.assertTrue(list(self.trader1.standing_orders.keys())[0] in self.e.orderMap)
        self.assertTrue(list(self.trader2.standing_orders.keys())[0] in self.e.orderMap)
        self.assertTrue(len(self.trader1.standing_orders.keys()) == 2)
        self.assertTrue(len(self.trader2.standing_orders.keys()) == 1)
    
    def test_sell_3(self):
        # Test add an order can be filled completely
        self.trader2.OrderAdd("sell", 24, 10, self.e)
        self.assertTrue(list(self.trader1.standing_orders.keys())[0] in self.e.orderMap)
        self.assertTrue(list(self.trader1.standing_orders.keys())[1] in self.e.orderMap)
        self.assertTrue(len(self.trader1.standing_orders.keys()) == 2)
        self.assertTrue(len(self.trader2.standing_orders.keys()) == 0)
    
    def test_sell_4(self):
        # Test add an order can be filled completely with extra left
        self.trader2.OrderAdd("sell", 24, 17, self.e)
        self.assertTrue(list(self.trader1.standing_orders.keys())[0] in self.e.orderMap)
        self.assertTrue(list(self.trader1.standing_orders.keys())[1] in self.e.orderMap)
        self.assertTrue(list(self.trader2.standing_orders.keys())[0] in self.e.orderMap)
        self.assertTrue(len(self.trader1.standing_orders.keys()) == 2)
        self.assertTrue(len(self.trader2.standing_orders.keys()) == 1)

    def test_sell_5(self):
        # Test add an order can be filled completely by >1 orders
        self.trader2.OrderAdd("sell", 23, 55, self.e)
        self.assertTrue(list(self.trader1.standing_orders.keys())[0] in self.e.orderMap)
        self.assertTrue(list(self.trader2.standing_orders.keys())[0] in self.e.orderMap)
        self.assertTrue(len(self.trader1.standing_orders.keys()) == 1)
        self.assertTrue(len(self.trader2.standing_orders.keys()) == 1)
        
    def test_buy_1(self):
        # Check the added 2 buy orders appear on exchange orderbook and trader's book
        self.assertTrue(list(self.trader1.standing_orders.keys())[0] in self.e.orderMap)
        self.assertTrue(list(self.trader2.standing_orders.keys())[0] in self.e.orderMap)
        self.assertTrue(len(self.trader1.standing_orders.keys()) == 2)
        self.assertTrue(len(self.trader2.standing_orders.keys()) == 1)
        
    def test_buy_2(self):
        # Test add partially filled order
        self.trader2.OrderAdd("buy", 25.0, 10, self.e)
        self.assertTrue(list(self.trader1.standing_orders.keys())[0] in self.e.orderMap)
        self.assertTrue(list(self.trader1.standing_orders.keys())[1] in self.e.orderMap)
        self.assertTrue(list(self.trader2.standing_orders.keys())[0] in self.e.orderMap)
        self.assertTrue(len(self.trader1.standing_orders.keys()) == 2)
        self.assertTrue(len(self.trader2.standing_orders.keys()) == 1)
        
    def test_buy_3(self):
        # Test add an order can be filled completely
        self.trader2.OrderAdd("buy", 25.0, 20, self.e)
        self.assertTrue(list(self.trader1.standing_orders.keys())[0] in self.e.orderMap)
        self.assertTrue(list(self.trader2.standing_orders.keys())[0] in self.e.orderMap)
        self.assertTrue(len(self.trader1.standing_orders.keys()) == 1)
        self.assertTrue(len(self.trader2.standing_orders.keys()) == 1)
    
    def test_buy_4(self):
        # Test add an order can be filled with extra left
        self.trader2.OrderAdd("buy", 25.0, 30, self.e)
        self.assertTrue(list(self.trader1.standing_orders.keys())[0] in self.e.orderMap)
        self.assertTrue(list(self.trader2.standing_orders.keys())[0] in self.e.orderMap)
        self.assertTrue(list(self.trader2.standing_orders.keys())[1] in self.e.orderMap)
        self.assertTrue(len(self.trader1.standing_orders.keys()) == 1)
        self.assertTrue(len(self.trader2.standing_orders.keys()) == 2)
        
    def test_buy_5(self):
        # Test add an order can be filled completely by >1 orders
        self.trader2.OrderAdd("sell", 24.5, 10, self.e)
        self.trader2.OrderAdd("buy", 25, 55, self.e)
        self.assertTrue(list(self.trader1.standing_orders.keys())[0] in self.e.orderMap)
        self.assertTrue(list(self.trader2.standing_orders.keys())[0] in self.e.orderMap)
        self.assertTrue(list(self.trader2.standing_orders.keys())[1] in self.e.orderMap)
        self.assertTrue(len(self.trader1.standing_orders.keys()) == 1)
        self.assertTrue(len(self.trader2.standing_orders.keys()) == 2)
        
        
    def test_cancel_order1(self):
        # check unprocessed sell order can be cancelled
        trader1_order2 = list(self.trader1.standing_orders.keys())[1]
        self.trader1.OrderCancel(trader1_order2, 20, self.e)
        self.assertTrue(~(trader1_order2 in self.trader1.standing_orders)) # check order id delete
        
    def test_cancel_order2(self):
        # check unprocessed sell order can be cancelled
        trader1_order2 = list(self.trader1.standing_orders.keys())[1]
        self.trader1.OrderCancel(trader1_order2, 10, self.e)
        self.assertTrue(trader1_order2 in self.trader1.standing_orders) # check order id still there
    
    def test_cancel_order3(self):
        # check unprocessed buy order can be cancelled
        trader1_order1 = list(self.trader1.standing_orders.keys())[0]
        self.trader1.OrderCancel(trader1_order1, 30, self.e)
        self.assertTrue(~(trader1_order1 in self.trader1.standing_orders)) # check order id delete
    
    def test_cancel_order4(self):
        # check unprocessed buy order can be reduced
        trader1_order1 = list(self.trader1.standing_orders.keys())[0]
        self.trader1.OrderCancel(trader1_order1, 20, self.e)
        self.assertTrue(trader1_order1 in self.e.orderMap) # check order id still there

    def test_cancel_order5(self):
                # check nonexisting refused by trying double cancelation
        trader1_order1 = list(self.trader1.standing_orders.keys())[0]
        self.trader1.OrderCancel(trader1_order1, 30, self.e)
        self.trader1.OrderCancel(trader1_order1, 30, self.e)
        self.assertTrue(~(trader1_order1 in self.e.orderMap)) 



if __name__ == '__main__':
    unittest.main()
    
    
    