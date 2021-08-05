import MetaTrader5 as mt5
from datetime import datetime

def setLastErrorDescription(description):
    global lasterrordescription
    lasterrordescription = description
    #print(lasterrordescription)

def getLastErrorDescription():
    delMT5Conn()
    return lasterrordescription
    
def getMT5Conn():
# connect to MetaTrader 5
    if not mt5.initialize():
        setLastErrorDescription("initialization failed")
        return None    
    #print('----------------')
    #print(mt5.account_info().server)
    #print('Total de ativos: ' + str(mt5.symbols_total()))
    return mt5

def delMT5Conn():
    # shut down connection to the MetaTrader 5 terminal
    mt5.shutdown()
    
def validatePrice(price):
    if price <=0:
        #dados do ativo ainda não carregados no metatrader
        setLastErrorDescription("symbol data is loading")
        return False
    #else
    return True
    

def normalizeSymbol(symbol):
    global lasterrordescription
    if (type(symbol) != str):
        setLastErrorDescription("symbol must be a string")
        return "ERROR"
    #else
    
    codigoTratado = symbol.strip() #.upper()

    #print("Processando o ativo: " + codigoTratado)
    symbol_info = getMT5Conn().symbol_info(codigoTratado)
    #print(symbol_info)
    
    if symbol_info is None:
        setLastErrorDescription("symbol info not found")
        return "ERROR"

    # if the symbol is unavailable in MarketWatch, add it
    if not symbol_info.visible:
        print(codigoTratado, ": is not visible, trying to switch on")
        if not getMT5Conn().symbol_select(codigoTratado,True):
            setLastErrorDescription("symbol_select failed")
            return "ERROR"
    
    return codigoTratado

def getLastPrice(codigo):
    codigoTratado = normalizeSymbol(codigo)
    if codigoTratado == 'ERROR':
        print(getLastErrorDescription())
        return -1        
    
    #try get last tick
    lastprice = getMT5Conn().symbol_info_tick(codigoTratado).last
    
    if not validatePrice(lastprice):
        # try get last M1 close price 
        lastprice = getMT5Conn().copy_rates_from_pos(codigoTratado, getMT5Conn().TIMEFRAME_M1, 0, 1)[0][4]
        if not validatePrice(lastprice):
            print(getLastErrorDescription())
            return -1        
    #else
    delMT5Conn()
    return lastprice
 
def getRatesByRange(symbol, dth1, dth2, tf):
    codigoTratado = normalizeSymbol(symbol)
    if codigoTratado == 'ERROR':
        print(getLastErrorDescription())
        return -1        
    rates = getMT5Conn().copy_rates_range(codigoTratado, tf, dth1, dth2)
    #else
    delMT5Conn()
    return rates

def getRatesByDth(codigo, dth, count, tf):
    codigoTratado = normalizeSymbol(codigo)
    if codigoTratado == 'ERROR':
        print(getLastErrorDescription())
        return -1        
    rates = getMT5Conn().copy_rates_from(codigoTratado, tf, dth, count)
    #else
    delMT5Conn()
    return rates

'''
TimeFrames Constants
'''
TF_D1 = getMT5Conn().TIMEFRAME_D1

