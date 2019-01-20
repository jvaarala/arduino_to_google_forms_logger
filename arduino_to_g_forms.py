import serial
import requests
from bs4 import BeautifulSoup

form_url = str(input('Enter URL to Google Form: '))
serial_port = str(input('Enter your Arduino serial port address: '))
data_rate_baud = str(input('Enter your data rate from Arduino in baud: '))

def get_entry():
    page = requests.get(form_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    return (soup.input['name'])


def get_form_response():
    page = requests.get(form_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    return (soup.form['action'])


# print(get_formResponse())
# print(get_entry())


entry = get_entry()
formResponse_url = get_form_response()


url = formResponse_url
form_data = {entry: '', 'draftResponse':[], 'pageHistory':0}
user_agent = {'Referer': form_url, 'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:10.0) Gecko/20100101 Firefox/10.0"}


ser = serial.Serial(serial_port, data_rate_baud)

n = 0
while n < 10:
    data = float(ser.readline())
    form_data[entry] = str(data)
    print("add datapoint", data, "to google forms")
    r = requests.post(url, data=form_data, headers=user_agent)
    n = n+1
