import datetime
import os
timedate = datetime.datetime.now()
speak = timedate.strftime("%Y %m %d, and the time is %H:%M")
os.system(f"espeak 'The current date is {speak}'")
