import sqlite3
import pandas as pd
import shutil
from datetime import datetime
from fpdf import FPDF


class StatQuery:
    dataFrame = None

    def __init__(self, sql) -> None:
        self.sql = sql


class QueryBuilder:

    #String to be added to the Generated PDF explaining the SQL Query 
    stat_info_string = ""
    
    #Method that returns the all time leaders in a specific stat category for a specific team 
    def get_all_time_team_leaders(stat_category, team_ID):
        QueryBuilder.stat_info_string = (f"Here are the All time {stat_category} leaders for {team_ID}")
        return StatQuery(f'''SELECT playerID, teamID, sum({stat_category}) FROM Statistics WHERE teamID = '{team_ID}' GROUP BY playerID ORDER BY sum({stat_category}) DESC LIMIT 10''')

    #Method that returns the all time leaders in a category in MLB history
    def get_all_time_MLB_leaders(stat_category):
        QueryBuilder.stat_info_string = (f"Here are the All Time {stat_category} leaders in MLB history")
        return StatQuery(f'''SELECT playerID, sum({stat_category}) FROM Statistics GROUP BY playerID ORDER BY sum({stat_category}) DESC LIMIT 10''')

    #Method that returns the team leaders in a specific category in a specific year 
    def get_individual_team_leaders_year(stat_category, team_ID, year_ID):
        QueryBuilder.stat_info_string = (f"Here are the {stat_category}, for {team_ID} in {year_ID}")
        return StatQuery(f'''SELECT playerID, yearID, teamID, {stat_category} FROM Statistics WHERE teamID = '{team_ID}' and yearID = {year_ID} ORDER BY {stat_category} DESC LIMIT 10''')

    #Method that returns the league leaders in a specific category in a specific year
    def get_league_leaders_year(stat_category, year_ID):
        QueryBuilder.stat_info_string = (f"Here are the League Leaders in {stat_category} in {year_ID}")
        return StatQuery(f'''SELECT playerID, yearID, teamID, {stat_category} FROM Statistics WHERE yearID = {year_ID} ORDER BY {stat_category} DESC LIMIT 10''')


class Repository:
    database_name = "Batting.db"

    @staticmethod
    def run_query_and_get_dataframe(stat_query):
        connection = sqlite3.connect(Repository.database_name)
        
        #Get the data frame when running the SQL query
        df = pd.read_sql(stat_query.sql, connection)
        with open('Stat_query_results.txt', 'w') as file:
            df_string = df.to_string(index= False)
            file.write(df_string)
        # Close the connection
        connection.close()

        # Print the DataFrame
        print(df)
        return df

class Generate_PDF:
    
    time = datetime.now()
    dt_string = time.strftime("%m_%d_%Y_%H_%M_%S")

    def get_pdf():

        pdf = FPDF()
        pdf.add_page(orientation= 'P')
        pdf.set_font("Arial", size = 15)
        file = open("stat_query_results.txt", "r")
        pdf.cell(200, 10, txt = QueryBuilder.stat_info_string, ln = 2, align= "L")
        for line in file:
            pdf.cell(200, 10, txt = line, ln = 3, align= 'L')
        pdf.output(f"BD_results_{Generate_PDF.dt_string}.pdf")
        file_name = (f'BD_results_{Generate_PDF.dt_string}.pdf')
        folder = 'c:/Users/joshc/OneDrive/Desktop/Database_Results'
        shutil.copy(file_name, folder)


def display_menu():
    menu_choice = -1
    while menu_choice < 0 and menu_choice < 4:
        print("===== Menu =====")
        print("1) All Time Team Leaders")
        print("2) Team Yearly Leaders")
        print("3) Season Leaders")
        print("4) All Time MLB Leaders")
        print("0) Quit")
        print("================")

        menu_choice = int(input("Enter choice:"))
    
    return menu_choice

def main():
    print("===== Stats Application =====")

    #instantiates the StatQuery class and passes a SQL string to the constructor. Not using it except as an example
    #sq = StatQuery("SELECT age FROM database", "test")
    #sq.show()

    #Keep running the application and allow the user to make queries until they choose to exit
    menu_choice = -1
    while menu_choice != 0:
    
        menu_choice = display_menu()

        if menu_choice == 0:
            # Exit application
            print("Have a great day!")
            return
        elif menu_choice == 1:
            team_ID = input("Please enter the Team: ").upper()
            stat_category = input("Please select the Stat Category").upper()
            selectedQuery = QueryBuilder.get_all_time_team_leaders(stat_category, team_ID)
        elif menu_choice == 2:
            team_ID = input("Please enter the Team: ").upper()
            year_ID = input("Please enter the year: ")
            stat_category = input("Please enter the Stat Category").upper()
            selectedQuery = QueryBuilder.get_individual_team_leaders_year(stat_category, team_ID, year_ID)
        elif menu_choice == 3:
            year_ID = input("Please enter the Year: ")
            stat_category = input("Please enter the Stat Category: ").upper()
            selectedQuery = QueryBuilder.get_league_leaders_year(stat_category, year_ID)
        elif menu_choice == 4:
            stat_category = input("Please enter the Stat Category: ").upper()
            selectedQuery = QueryBuilder.get_all_time_MLB_leaders(stat_category)

        selectedQuery.dataFrame = Repository.run_query_and_get_dataframe(stat_query=selectedQuery)
        Generate_PDF.get_pdf()


#Automatically calls main() when you run this script
if __name__ == "__main__":
    main()