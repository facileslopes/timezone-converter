import datetime as dt
import requests

def get_utc_offset(tz):
    #Converts the given time zone to an offset from UTC
    if tz != None:
        offset = requests.get("http://worldtimeapi.org/api/timezone/" + tz)
        offset_json = offset.json()
        utc_offset = offset_json['utc_offset']
        return utc_offset

def tz_diff(offset1, offset2):
    #Finds the time difference between two time zones
    fset1 = offset1.split(":")    
    fset2 = offset2.split(":")
    if fset1[0][0] == "+":
        mins1 = int(fset1[0][1:]) * 60  + int(fset1[1]) 
    elif fset1[0][0] == "-":
        mins1 = - ( int(fset1[0][1:]) * 60 + int(fset1[1]) )  
    if fset2[0][0] == "+":
        mins2 = int(fset2[0][1:]) * 60  + int(fset2[1] )
    elif fset2[0][0] == "-":
        mins2 = - ( int(fset2[0][1:]) *60  + int(fset2[1] ) )
    return mins1-mins2
              
def main():
    event_date = input("Enter the date of the event(YYYY-MM-DD): ") #Entered in the given format
    event_time = input("Enter the time of the event(HH:MM:SS): ")#Hours are between 1-24; no PM
    event = dt.datetime( int(event_date[0:4]) , int(event_date[5:7]), int(event_date[8:])
                               ,int(event_time[0:2]), int(event_time[3:5]), int(event_time[6:])  )
    choice1 = input("Do you wish to enter the UTC offsets directly, or do you want to enter the timezones first?(UTC/TimeZone) ")
    if choice1 == "UTC":
        event_utc = input("Enter the UTC offset of the event's timezone: ")
        user_utc = input("Enter the UTC offset of your timezone: ")
    elif choice1 == "TimeZone":
        event_timezone = input("Enter the timezone of your event: ")# Check http://worldtimeapi.org/timezones for the list of valid timezones
        event_utc = get_utc_offset(event_timezone)
        user_timezone = input("Enter your timezone: ")
        user_utc = get_utc_offset(user_timezone)
    else:
        print("Invalid choice")
    diff = tz_diff(event_utc,user_utc)
    tdelta = dt.timedelta(minutes=diff)
    translated_t = event - tdelta
    print(translated_t.strftime("%d %B %Y, %I:%M:%S %p"))
    
if __name__ == "__main__":
    main()
