from twilio.rest import Client
import schedule, time, sys
#This part of the script requires you to have a Twilio (Trial) Account to communicate through the API to a user
client = Client("", "")

def main(arg):
    client.messages.create(to="",
                           from_="",
                           body="Hello! Here's the best 3 stocks right now: "+ arg)
    print("Thank you for sending!")                      

if __name__=="__main__":
    main(arg)