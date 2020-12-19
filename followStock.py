#Recently FuelCell Energy has popped off (100+% the last 4-5 trading days)
#I want to track it and notify myself when it is red
#Create functionality that alerts when below a certain number or above, or % change
#--> next level would be if it's above/below MA5, etc
#--> VWAP??? RSI???
import yfinance as yf
import requests,re
from bs4 import BeautifulSoup

url = "https://finance.yahoo.com/quote/fcel"
response = requests.get(url)
data = response.text
soup = BeautifulSoup(data, "html.parser")

price = soup.find('span', attrs={'data-reactid':"50"}).text
#print(price)

change = soup.find('span', attrs={'data-reactid':"51"}).text
decimal, percentage = change.split()
#print(decimal)
#want to convert str to int/float to then compare/analyze
percentage = re.search(r'\((.*?)\)', percentage).group(1) #parse text from parentheses 
percentage = float(percentage.strip("%"))
#e=m.strip("%");f=float(e);return f/100if e!=m else str(f*100)+"%"
#percentage = percentage[:-1]
#print(percentage) 

#Create alert system that informs user when ticker sees a red percentage on the day



#initialize ticker to analyze
#ticker = yf.Ticker("FCEL")

#get historical market data
#hist = ticker.history(period="max")
#print(hist) #DF of max history

#Show some recommendations
#print(ticker.recommendations[-1::]) #prints most recent recommendation

#Show next event
#print(ticker.calendar)

#Show options expirations
#print(ticker.options) #list of next expiry

#Get options chain for a specific expiry
#opt = ticker.option_chain('2021-01-15')
#use opt.calls or opt.puts to view them
#print(opt.calls)
#print(opt.puts)