#Import necessary modules
import sqlite3
import csv

#Connect to the Batting.csv file
connection = sqlite3.connect('Batting.db')
cursor= connection.cursor()


# Table Definition
        
cursor.execute('''CREATE TABLE IF NOT EXISTS Statistics (
               playerID text, 
               yearID integer, 
               stint INTEGER, 
               teamID TEXT, 
               lgID INTEGER,
               G INTEGER, 
               AB INTEGER, 
               R INTEGER, 
               H INTEGER, 
               doubles INTEGER,
               tripples INTEGER, 
               HR INTEGER, 
               RBI INTEGER, 
               SB INTEGER, 
               CS INTEGER,
               BB INTEGER, 
               SO INTEGER, 
               IBB INTEGER, 
               HBP INTEGER, 
               SH INTEGER,
               SF INTEGER,   
               GIDP INTEGER
               );''')


# reading data from the CSV file
with open('Batting.csv', "r") as csv_file:
   no_records = 0
   for row in csv_file:
      cursor.execute('''INSERT INTO Statistics VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', row.split(','))
      connection.commit()
      no_records += 1
connection.close()


