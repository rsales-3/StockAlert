#This script contains the web scrapping, data manipulation and flow control of the jobs
#Create actual functions to then place into the main function AND to allow using certain 
#functions singly or 2 of the 3 and so on if needed IN OTHER scripts that import this file
import numpy as np
from bs4 import BeautifulSoup
import requests, time, yfinance  as yf
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import createCharts 
import sendCharts
import send_SMS

### WEB SCRAPE -------------- START
def main():
    url='https://finance.yahoo.com/most-active' #defaults to US Mid/Large/Mega Cap, with volume greater than 5million (25 results/companies)
    response=requests.get(url) 
    time.sleep(5)
    #print(response)

    symbols = [] # list of ticker symbols scraped 
    names = [] # list of company names
    prices = [] # list of prices 
    changePrice = [] #list of price change
    percentChange = [] # list of % change associated
    soup=BeautifulSoup(response.content,'lxml')

    for item in soup.select('.simpTblRow'): # 
        try:#append scraped elements to lists
            symbols.append(item.select('[aria-label=Symbol]')[0].get_text())
            names.append(item.select('[aria-label=Name]')[0].get_text())
            prices.append(item.select('[aria-label*=Price]')[0].get_text())
            changePrice.append(item.select('[aria-label=Change]')[0].get_text())
            percentChange.append(item.select('[aria-label="% Change"]')[0].get_text())
            
        except Exception as e:
            raise e
            print('')

    ### WEB SCRAPE -------------- END



    ### DATA MANIPULATION ------- START
    #convert all strings to floats
    float_prices = []
    for item in prices:
        float_prices.append(float(item))

    float_changePrice = []
    for item in changePrice:
        float_changePrice.append(float(item))

    #remove % sign from string 
    withoutSign = []
    for item in percentChange:
        withoutSign.append(item.replace("%", ""))
    #to then convert str to float
    float_percentChange = []
    for item in withoutSign:
        float_percentChange.append(float(item))

    #merge the data to make tuples of each row 
    merged_data = list(map(lambda v,w,x,y,z: (v,w,x,y,z), symbols, names, float_prices, float_changePrice, float_percentChange))

    #sort the list of tuples based on the % change
    merged_data.sort(key = lambda z: z[4]) #This sort is ascending by default
    #print(merged_data)

    #slice to get top 3 / bot 3 movers
    top3 = merged_data[:-4:-1] #top 3 is the last 3 of this list - reverse order
    bot3 = merged_data[:3] #bot 3 is the first 3 of this list

    ### DATA MANIPULATION ------- END



    ### OUT PUT JOBS ------------ START

    ###     createCharts START
    for (v,w,x,y,z) in top3:
        createCharts.main(v) # calling createCharts with v (ticker symbol) in top3 list

    for (v,w,x,y,z) in bot3:
        createCharts.main(v) # calling createCharts with v (ticker symbol) in bot3 list
    ###     createCharts END

    ###     sendCharts      ###png files are now in directory ready to send thru email
    sendCharts.main() #sends charts as attachments of email

    ###     send_SMS START
    #finally send the user SMS about stocks and their % change
    stringToSend =''
    for item in top3:
        stringToSend += str("Ticker {} is MOONING at +{}% change on the day!\n".format(item[0], item[4]))
    stringToSend = stringToSend + "and here are the 3 worst:\n"

    for item in bot3:
        stringToSend += str("Ticker {} is BOMBING on the day at {}% change !\n".format(item[0], item[4]))

    send_SMS.main(stringToSend)
    ###     send_SMS END

    ### OUT PUT JOBS ------------ END

if __name__=='__main__':
    main()