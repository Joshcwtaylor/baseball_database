import sqlite3
from fpdf import FPDF
import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime 
import shutil
import pandas as pd


#globals
time = datetime.now()
dt_string = time.strftime("%m_%d_%Y_%H_%M_%S")
stat_info_string = ''

connection = sqlite3.connect('Batting.db')
cursor = connection.cursor

#Function that returns all the Categories 
def getCategories():
    global stat_query_results
    cursor = connection.execute('''SELECT c.name FROM pragma_table_info('Statistics') c;''')
    stat_query_results = cursor.fetchall()
    connection.commit()

#Function that returns the all time leaders in a specific stat category for a specific team 
def all_time_team_leaders():
    global stat_info_string
    team_ID = input("Please enter the Team ").upper()
    stat_category = input("Please select the Stat category ")
    query = (f'''SELECT playerID, teamID, sum({stat_category}) FROM Statistics WHERE teamID = '{team_ID}' GROUP BY playerID ORDER BY sum({stat_category}) DESC LIMIT 10''')
    df = pd.read_sql_query(query, connection)
    stat_info_string = (f"Here are the All time {stat_category} leaders for {team_ID}")
    with open('Stat_query_results.txt', 'w') as file:
        df_string = df.to_string(index= False)
        file.write(df_string)
    


#Function that returns the team leaders in a specific category in a specific year 
def individual_team_leaders_year():
    global stat_info_string
    team_ID = input("Please enter the Team ").upper()
    team_ID = (f"'{team_ID}'")
    year_ID = input("Please enter a year ")
    stat_category = input("Please enter a Stat Category ")
    query = (f'''SELECT playerID, yearID, teamID, {stat_category} FROM Statistics WHERE teamID = {team_ID} and yearID = {year_ID} ORDER BY {stat_category} DESC LIMIT 10''')
    df = pd.read_sql_query(query, connection)
    stat_info_string = (f"Here are the Team Leaders in {stat_category}s for {team_ID} in {year_ID}")
    with open('Stat_query_results.txt', 'w') as file:
        df_string = df.to_string(index= False)
        file.write(df_string)
    


#Function that returns the league leaders in a specific category in a specific year
def league_leaders_year():
    global stat_info_string
    year_ID = input("Please enter the Year ")
    stat_category = input("Please select the Stat Category ")
    query = (f'''SELECT playerID, yearID, teamID, {stat_category} FROM Statistics WHERE yearID = {year_ID} ORDER BY {stat_category} DESC LIMIT 10''')
    df = pd.read_sql_query(query, connection)
    stat_info_string = (f"Here are the League Leaders in {stat_category}s in {year_ID}.")
    with open('Stat_query_results.txt', 'w') as file:
        df_string = df.to_string(index= False)
        file.write(df_string)
    


#Function that returns the all time Leaders in a specific stat category 
def all_time_MLB_leaders():
    global stat_info_string
    stat_category = input("Please select the Stat Category ")
    query = (f'''SELECT playerID, sum({stat_category}) FROM Statistics GROUP BY playerID ORDER BY sum({stat_category}) DESC LIMIT 10''')
    df = pd.read_sql_query(query, connection)
    stat_info_string = (f"Here are the All Time Leaders in {stat_category}s in Major League Baseball")
    with open('Stat_query_results.txt', 'w') as file:
        df_string = df.to_string(index= False)
        file.write(df_string)
    
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
def generate_pdf():
    global dt_string
    global stat_info_string
    pdf = FPDF()
    pdf.add_page(orientation= 'P')
    pdf.set_font("Arial", size = 15)
    file = open("stat_query_results.txt", "r")
    pdf.cell(200, 10, txt = stat_info_string, ln = 2, align= "L")
    for line in file:
        pdf.cell(200, 10, txt = line, ln = 3, align= 'L')
    pdf.output(f"BD_results_{dt_string}.pdf")
    file_name = (f'BD_results_{dt_string}.pdf')
    folder = 'c:/Users/joshc/OneDrive/Desktop/Database_Results'
    shutil.copy(file_name, folder)

    

def main():
    while True:
        search_type = input("Select 1 to search the database, Select 2 to see all searchable statistical categories, Select 3 to exit" )
        if search_type == "1":
            type_of_query = input("***********************************************\n 1) All Time Team Leaders \n 2) Team Yearly Leaders \n 3) Season Leaders \n 4) All Time MLB Leaders" )
            if type_of_query == "1":
                all_time_team_leaders()
                generate_pdf()
            elif type_of_query == "2":
                individual_team_leaders_year()
                generate_pdf()
            elif type_of_query == "3":
                league_leaders_year()
                generate_pdf()
            elif type_of_query == "4":
                all_time_MLB_leaders()
                generate_pdf()
            email_option = input("Would you like your search results emailed to you? Y | N")
            if email_option == "Y":
                generate_email()
            else:
                continue            
        if search_type == "2":
            getCategories()
            generate_pdf()              
        else:
            break
    connection.close()



main()
