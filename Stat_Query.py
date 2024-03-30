import sqlite3
from reportlab.pdfgen import canvas
import smtplib
import ssl
from email.message import EmailMessage


#cheat code...
stat_query_results = []

#Connect to the Batting.db database
connection = sqlite3.connect('Batting.db')
cursor= connection.cursor()

#Function that returns a query
def stat_query(stat_category, stat_number):
    global stat_query_results
    cursor = connection.execute(f'''SELECT playerID, yearID, {stat_category} FROM Statistics WHERE {stat_category} >= {stat_number} ORDER BY {stat_category} DESC''')
    stat_query_results = cursor.fetchall()
   
connection.commit()

#Generating a txt file 
def generate_txt_file():
    with open('Stat_query_results.txt', 'w') as file:
        file.write("\n".join(str(item) for item in stat_query_results))


#Generating an email with the query results
def generate_email():
    while True:
        receiver_email = input("Please enter your email address")
        confirm_email = input(f"You entered {receiver_email} is this Correct?  Y | N").upper()
        if confirm_email == "Y":
            break
        else:
            continue 

    sender_email = "real.freddy.peterson@gmail.com"
    password = "thlw xbrk jiud bubq"
    query_results_file = 'stat_query_results.txt'

    with open(query_results_file) as file:
        msg = EmailMessage()
        msg.set_content(file.read())
    
    msg['Subject'] = 'Freddy is ready with your results!'
    msg['From'] = sender_email
    msg['To'] = receiver_email
    print("sending email")
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
    print("success! check your email for results")

#Generate a PDF file, work in progress...
def pdf_file():
    c = canvas.Canvas("results.pdf")
    c.drawString(100,100, stat_query_results)
    c.showPage()
    c.save()


def main():
    while True:
        search_type = input("Select 1 to search the database, Select 2 to see all searchable statistical categories, Select 3 to exit")
        if search_type == "1":
            stat_category = input("Please select the Category of Statistics you'd like to search for").upper()
            stat_number = input(f"Please select the number of {stat_category}'s in a season youd like to search for").upper()
            stat_query(stat_category, stat_number)
            generate_txt_file()
            generate_email()
        if search_type == "2":
            print("The current searchable categories are: \n HR . RBI . R . H . G . AB ")              
        else:
            break
    connection.close()



main()
