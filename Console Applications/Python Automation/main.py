# pip install schedule
# pip install requests
# textbelt.com

import requests
import schedule
import time

# use key=textbelt to send 1 free text per day (textbelt.com)
# use phone number you want for phone variable
def send_message():
    resp = requests.post('https://textbelt.com/text', {
        'phone': "",
        'message': "Hello. Good morning",
        'key': 'textbelt'
    })
    print(resp.json())

#schedule.every().day.at('06:00').do(send_message())

# schedule.every(10).seconds.do(send_message())
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)