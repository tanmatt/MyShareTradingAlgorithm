# -*- coding: utf-8 -*-
"""
Created on Sat Jan 31 21:26:36 2015

@author: tthakur
"""

#call Yahoo API to convert names to symbols
#create list of symbols
#download csv for all symbols from quandl API

import json
import urllib2
import wget

NAME_LIST_FILE = 'Loyal3StockList31Jan.txt'
YAHOO_STOCK_API_PREFIX = 'http://d.yimg.com/autoc.finance.yahoo.com/autoc?query='
YAHOO_STOCK_API_SUFFIX = '&callback=YAHOO.Finance.SymbolSuggest.ssCallback'
QUANDL_API = 'https://www.quandl.com/api/v1/datasets/WIKI/'
QUANDL_FORMAT = '.csv'

DEBUG = True

class Stocks:
    
    def create_name_list(self):
        #read from file and create a list
        names = open(NAME_LIST_FILE, 'r')
        name_list = names.read()
        name_list = name_list.split('\n')
        names.close()
        
        if DEBUG:
            print '\n%d names added to list' %len(name_list)
            print name_list
        
        return name_list

    def nameToSymbol(self, name_list):
        name_list_encoded = []
        for i in range(0, len(name_list)):
            name_list_encoded.append(name_list[i].replace(' ','%20'))
        encoded = len(name_list_encoded)
        if DEBUG:
            print '\n%d name encoded created from %d names' % (encoded, len(name_list))
         

        symbol_list = []
        for i in range(0, encoded):
            resp = urllib2.urlopen(YAHOO_STOCK_API_PREFIX + name_list_encoded[i] + YAHOO_STOCK_API_SUFFIX)
            resp = resp.read()
            json_resp = json.loads(resp[39: -1])
            try:
                symbol_list.append(json_resp['ResultSet']['Result'][1]['symbol'])
            except Exception, ex:
                print 'Symbol: NA'
                if DEBUG:
                    print str(ex)

        if DEBUG:
            print '\n%d symbol(s) found' %len(symbol_list)
            print symbol_list
            
        return symbol_list

    '''
    def save_to_file(self, symbol_list):
        FILE_NAME = 'SymbolList.txt'
        f = open (FILE_NAME, 'w')
        for symbol in symbol_list:
            f.write(symbol+'\n')
        f.close()
        if DEBUG:
            print 'File saved successfully.'

        return FILE_NAME
    '''

    def downloadCSV(self, symbol_list):
        count = 0
        for symbol in symbol_list:
            wget.download(QUANDL_API + symbol + QUANDL_FORMAT)
            count += 1
            if DEBUG:
                print ''

        if DEBUG:
            print '%d csv downloaded'%count
    
if __name__ == "__main__":
    stock = Stocks()
    name_list = stock.create_name_list()
    symbol_list = stock.nameToSymbol(name_list)
    stock.downloadCSV(symbol_list)

        