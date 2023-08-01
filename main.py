#Main file. Recieves the data obtained and datascraping.py and uses the Flask framework to build a site on python.
#Flask documentation: https://flask.palletsprojects.com/en/2.3.x/
import datascraping
from flask import Flask, render_template

datascraping.scrape_data()
f = open("results.txt", "r")  
lines = f.readlines()

#lines reads it as a list. make it a dictionary instead
lines_dict = {}
for line in lines:
    date_str, users_str = line.strip().split(':')
    date = date_str.strip()
    users = []
    for user in eval(users_str.strip()):
        users.append(user.strip())
    lines_dict[date] = users

#keep track of how many reels each user sends per day
reels_per_users = {}
for key, values in lines_dict.items():
  if key not in reels_per_users:
    reels_per_users[key] = {}
  for value in values:
    if value not in reels_per_users[key]:
      reels_per_users[key][value] = 1
    else:
      reels_per_users[key][value] += 1


#HTML SITE CODE
#Flask requires you to make a folder called templates and to put all html files in there. Otherwise, it wont work
#Flase also requires the creation of a folder called static to put all js and css files there. 
#MAKE SURE TO MAKE THESE BEFOREHAND

app = Flask(__name__)
# @app.route('/')
# #main page - displays total amount of reels collectively sent per day
# def home():
#   return render_template('template.html', lines = lines_dict)


@app.route('/')
#users page - displays how many reels each user has sent separated by day in which they sent them
def users():
  return render_template('users.html', freq = reels_per_users)

if __name__ == '__main__':
   app.run(host = "0.0.0.0")
