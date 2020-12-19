#This script schedules and executes the entire program 3x a day
import schedule, time, sys
import scrapeData #main file with all the lesser jobs 

def job():
    scrapeData.main()

def runMulti():
    #Scrape 3x a day - make it every weekday
    schedule.every().day.at("09:00").do(job) # 30 minutes after Market Open
    print("Idle...")
    schedule.every().day.at("12:00").do(job) # Noon
    print("Idle...")
    schedule.every().day.at("15:00").do(job) # Market Close

    while 1:
        schedule.run_pending()
        time.sleep(1)

def main():
    choice = input("1 for Scheduled Job, 2 for whole job right now, 3 for a specific job:")
    if choice == "1":
        runMulti()
    elif choice =="2":
        job()
    #run a input loop to interact with user for which job to run --> have to split main file into multiple functions

if __name__=='__main__':
    main()