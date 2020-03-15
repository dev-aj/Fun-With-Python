import requests
from bs4 import BeautifulSoup
import re
import smtplib, ssl
import time

#link = 'https://www.flipkart.com/mobiles/~iphone-xs-64gb/pr?sid=tyy%2C4io&sort=price_asc&param=0612&otracker=clp_banner_1_10.banner.BANNER_mobiles-big-shopping-days-sneak-peek-o9i8e4-store_VTPHRXKX37QY'
user_ag = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0" 
User_Agent = ""
Product_Name = ""

link = input('Enter the link of the product(Flipkart): ')
sender_email = input('Enter your Sender Gmail account: ')
receiver_email = input('Enter Receiver account: ')
password = input("Type your password and press enter:")
frequency = int(input('Enter valid Frequency of tracker in seconds: '))
user_agent = input('Enter your user agent(Get it by typing my user agent in browser): ')
desired_price = float(input('Enter the desired price: ').strip())

def sendMail():
    port = 587  # For starttls vgzpefrbaifkytso
    smtp_server = "smtp.gmail.com"
    subject= " "
    body  = 'Hi there,\n' + 'This Email is regarding the product : ' + Product_Name + '\nCheck out The Link: \n' + link

    message = """\
        Subject: Email From Price Tracker"""+ '\n'+ body

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        server.quit()
    print("Email has been sent!!")
    #server.quit()

def price_Tracker():
    if(user_agent == ""):
        User_Agent = user_ag
    else:
        User_Agent = user_agent
    
    headers = {
        "User-Agent" : User_Agent
    }
    res = requests.get(link, headers = headers)

    soup = BeautifulSoup(res.content, 'html.parser')
    title = soup.select('._2yAnYN')
    Product_Name = title[0].text
    print('\n\n************************\t',Product_Name,'**************************\n')

    ProductList = soup.select('._3wU53n')

    PriceList = soup.find_all("div", "_1vC4OE _2rQ-NK")
    flag = False
    for product, price in zip(ProductList, PriceList):
        print(product.text+" \t:\t Rs."+price.text[1:])
        price_list = re.findall(r'\d+', price.text[1:])
        price = ("".join(i for i in price_list))

        if(float(price) <= desired_price):
            flag = True
    
    if(flag):
        sendMail()


#to run the tracker at desired frequency
while(True):
    price_Tracker()
    time.sleep(frequency)
