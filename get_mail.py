"""Connect to IMAP, find email, return it"""
import email
import email.message
import imaplib
import json
from datetime import date
from datetime import timedelta


# get credentials
with open('config.json') as config_data:
    config = json.load(config_data)['imap']

IMAP_HOST = config['host']
IMAP_PORT = config['port']
IMAP_USER = config['user']
IMAP_PASS = config['password']

def last_sunday():
    today = date.today()
    time_format = "%d-%b-%Y"
    i = 1

    while i <= 7:
        past_day = today + timedelta(days=-i)
        if past_day.weekday() == 6:
            return past_day.strftime(time_format)
        i += 1


def main():
    """Main fuction"""
    imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
    imap.login(IMAP_USER, IMAP_PASS)
    imap.select('Inbox')

    # search email by subject. imap.search return tuple with status and message's numbers. we need only numbers
    data = imap.search(None, '(SUBJECT "PGA TOUR Digital: Operations & Support Schedule" SINCE {})'.format(last_sunday()))[1]
    # get email
    raw_email = imap.fetch(data[0], '(RFC822)')[1]
    # choose part of multipart email
    email_body = raw_email[0][1]
    # convert from bytes. In msg is mail headers and base64-encoded message
    msg = email.message_from_bytes(email_body)

    for part in msg.walk():
        if part.get_content_type() == 'text/plain':
            temp = part.get_payload(decode=True)


    #temp = msg.get_payload(decode=True)
    

    # get 1st part's payload encoded
    msg_base64 = msg.get_payload()[0]
    # decode
    # body_text = msg.get_payload(decode=True)
    # body_text = msg_base64.get_payload(decode=True)
    
    imap.close()
    imap.logout()

    return temp

if __name__ == "__main__":
    print(main())