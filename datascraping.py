#Notifications (reels) are gathered with the help of a shortcut made on my iPhone which uses screenshots and "text on image"
#to scrape all text off the screenshot taken.
#Notifications are then stored in a document (reel-data.txt) so that the program can read them and edit them accordingly.
#We use a different file (results.txt) so that the document that contains all notification information is left intact.
#so that it can continue being used every time new data (notifications) is added to it.
from datetime import datetime, timedelta

def scrape_data():
  f = open("reel-data.txt", "r")
  r = open("results.txt", "r")
  lines = f.readlines()
  
  #your instagram user would go here, along with the [ ] 
  keyword = "[your insta user] "
  date_string = ''
  #start_date is important. it allows us to read dates that are up to one year old
  start_date = datetime.now() - timedelta(days=365)
  end_date = datetime.now()
  accepted_lines = []
  users = []
  curr_date = None
  dates = {}
  
  with open("reel-data.txt", "r") as f:
    for line in lines:
      if keyword in line:
        #we want to get the users who send us media. since i already only
        #screenshot messages that contain the media itself
        #("[{your user}] {user} sent a post/reel by {account}")
        #i only need to check that my instagram user is in the line to count it

        #keep track of all users and all instances of those users sending you media
        accepted_lines.append(line) 

      #we want to get the date that is obtained through the prepared shortcut on the phone. (date on which the screenshot is taken)
      #this is to plot it in a graph later
      try:
        date_string = line[:line.find(' at')]
        date_string = datetime.strptime(date_string, "%b %d, %Y")
        if start_date <= date_string <= end_date:
          formatted_date = date_string.strftime("%Y-%m-%d")
          accepted_lines.append(formatted_date) #keep track of dates
      except ValueError:
        pass
#--------------------------------------------------------------------------------------------------------------------------------------
    #assigning all corresponding users to each date encountered
    for line in accepted_lines:
      if keyword in line:
        user = line.replace(keyword, '') #take your insta user out
        #user = line.replace('\n', '')
        users.append(user)
        if curr_date is not None: #we've enountered a date
          if curr_date not in dates:
            dates[curr_date] = [] #list of users who sent media on that day
          dates[curr_date].extend(users)
          users = []
          curr_date = None
      #you either encounter a date or an empty line
      else:
        try:
          curr_date = datetime.strptime(line, "%Y-%m-%d").date()
        except ValueError:
          #we didnt find a date, meaning there was more than one instance of receiving media in that one screenshot. 
          #we need to find all users that appear in that screenshot (the shortcut uses screenshots to get the reel data)
          curr_date = None
          continue
          
  #retrieves the last date        
  if curr_date is not None:
    if curr_date not in dates:
        dates[curr_date] = []
    dates[curr_date].extend(users)  

  #write all the dates with corresponding users
  with open("results.txt", "w") as r:
    for date, users in dates.items():
      r.write(f"{date}: {users}\n")
