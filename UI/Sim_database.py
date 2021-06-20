import csv
import datetime
import sqlite3


class Sim_database:
    # Specify the list format and standardize the format of the imported database.
    configuration = [[], [], [], [], [], [], [], [], [], [], [], []]
    sim_process = [[], [], [], []]
    sim_limit = [[], [], [], [], [], [], [], []]

    # This method is used to import a csv file in a specified path, and standardize the format used for the database for
    # the imported file according to the file type.
    def input_csv(self):
        sequence_length = 0
        temp_list = []
        select_mode = input("Please select the type of file you: 1. Configuration; 2. Simulation process; 3. "
                            "Simulation limits: ")
        # Import the corresponding csv template through user options, and limit the length of the list.
        if int(select_mode) == 1:
            sequence_length = 12
            temp_list = self.configuration
        elif int(select_mode) == 2:
            sequence_length = 4
            temp_list = self.sim_process
        elif int(select_mode) == 3:
            sequence_length = 8
            temp_list = self.sim_limit

        else:
            print("Please enter the correct mode!")
            print("CLOSE!")
            return False
        try:
            path = input("Please enter the path of the file you want to open: ")
            print("Open the document path:", path)
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                rows = [row for row in reader]
                # If the import csv format is wrong, the method ends directly and return FALSE.
                if len(rows[0]) != sequence_length:
                    print("Please import or select the correct type of cav file.")
                    return False
                # Because the template has been specified, the data is filled in the temporary list in the specified
                # order by using the for loop with the length of the list.
                break_point = 0
                for i in rows:
                    if break_point == 0:
                        break_point += 1
                    else:
                        count = 0
                        while count < sequence_length:
                            temp_list[count].append(i[count])
                            count += 1
            # Enter the temporary list in a specific format into the class variable by selecting the mode.
            # Returns the type of imported csv (indicated by numbers).
            if int(select_mode) == 1:
                self.configuration = [float(temp_list[0][0]), float(temp_list[1][0]), float(temp_list[2][0]),
                                      float(temp_list[3][0]),
                                      float(temp_list[4][0]), float(temp_list[5][0]), float(temp_list[6][0]),
                                      float(temp_list[7][0]),
                                      float(temp_list[8][0]), float(temp_list[9][0]), float(temp_list[10][0]),
                                      float(temp_list[11][0])]
                print(self.configuration)
                return 1
            elif int(select_mode) == 2:
                self.sim_process = temp_list
                print(self.sim_process)
                return 2
            else:
                self.sim_limit = temp_list
                print(self.sim_limit)
                return 3
        except:
            print("EXIT")
            return False

    # Connect to the database. If there is no library locally, create a new library.
    def connect_database(self):
        conn = sqlite3.connect('sim_database.db')
        print("Opened database successfully")

    # Create a configuration table in the database.
    def create_db_sim_configuration(self):
        conn = sqlite3.connect('sim_database.db')
        print("Opened database successfully")
        c = conn.cursor()
        # ID is automatically created using sqlite's AUTOINCREMENT method.
        c.execute('''CREATE TABLE CONFIGURATION
           (ID            INTEGER       PRIMARY KEY AUTOINCREMENT,
           INPUT_TIME           TIME      NOT NULL,
           START_TEMPERATURE FLOAT      NOT NULL,
           LIMIT_TEMPERATURE FLOAT      NOT NULL,
           START_VIBRATION  FLOAT      NOT NULL,
           LIMIT_VIBRATION   FLOAT      NOT NULL,
           TEST_TIME         FLOAT      NOT NULL,         
           S_TEMP_WARING  FLOAT      NOT NULL,
           S_TEMP_ALARM   FLOAT      NOT NULL,
           S_TEMP_EMERGENCY FLOAT    NOT NULL, 
           S_VIB_WARING  FLOAT NOT NULL,
           S_VIB_ALARM   FLOAT NOT NULL,
           S_VIB_EMERGENCY FLOAT   NOT NULL,
           SENSOR_NUMBER     INT     NOT NULL
          );''')
        print("Table created successfully")
        conn.commit()
        conn.close()

    # Insert configuration data into the database. The data source is the standardized data imported from csv.
    def insert_db_sim_configuration(self):
        conn = sqlite3.connect('sim_database.db')
        c = conn.cursor()
        print("Opened database successfully")
        # Get the current time. This time is the data import time.
        this_time = datetime.datetime.now()
        # Pass the parameter into the SQL statement to be executed through the placeholder "?".
        c.execute("INSERT INTO CONFIGURATION (INPUT_TIME ,START_TEMPERATURE, LIMIT_TEMPERATURE, START_VIBRATION, LIMIT_VIBRATION, TEST_TIME, S_TEMP_WARING ,S_TEMP_ALARM, S_TEMP_EMERGENCY, S_VIB_WARING, S_VIB_ALARM, S_VIB_EMERGENCY,SENSOR_NUMBER) \
                                      VALUES (?, ? , ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (this_time, float(self.configuration[0]), float(self.configuration[1]), float(self.configuration[2]),
                   float(self.configuration[3]),
                   float(self.configuration[4]), float(self.configuration[5]), float(self.configuration[6]),
                   float(self.configuration[7]),
                   float(self.configuration[8]),
                   float(self.configuration[9]), float(self.configuration[10]), float(self.configuration[11])))

        conn.commit()
        print("Records created successfully")
        conn.close()

    def create_db_sim_process_value(self):
        conn = sqlite3.connect('sim_database.db')
        print("Opened database successfully")
        c = conn.cursor()
        c.execute('''CREATE TABLE SIM_PROCESS
           (ID            INTEGER       PRIMARY KEY AUTOINCREMENT,
           INPUT_TIME     TIME          NOT NULL,
           SENSOR_ID      NONE NOT NULL,
           TIMES          NONE  NOT NULL,
           TEMPERATURE    NONE  NOT NULL,
           VIBRATION      NONE  NOT NULL
          );''')
        print("Table created successfully")
        conn.commit()
        conn.close()

    def insert_db_sim_process_value(self):
        conn = sqlite3.connect('sim_database.db')
        c = conn.cursor()
        print("Opened database successfully")
        this_time = datetime.datetime.now()
        print(this_time)
        # Due to the limitation of SQLite on the storage format of the list, the storage format needs to be
        # converted through the .__repr__() method.
        c.execute("INSERT INTO SIM_PROCESS (INPUT_TIME ,SENSOR_ID, TIMES, TEMPERATURE, VIBRATION) \
                                      VALUES (?, ? , ?, ?, ?)",
                  (this_time, self.sim_process[0].__repr__(), self.sim_process[1].__repr__(),
                   self.sim_process[2].__repr__(),
                   self.sim_process[3].__repr__()))

        conn.commit()
        print("Records created successfully")
        conn.close()

    def create_db_sim_process_limit(self):
        conn = sqlite3.connect('sim_database.db')
        print("Opened database successfully")
        c = conn.cursor()
        c.execute('''CREATE TABLE SIM_LIMIT
           (ID              INTEGER       PRIMARY KEY AUTOINCREMENT,
            INPUT_TIME      TIME          NOT NULL,
            SENSOR_ID       INT           NOT NULL,
            TIMES           NONE  NOT NULL,
            TEMP_ALERT      NONE  NOT NULL,
            VIB_ALERT       NONE  NOT NULL,
            TEMP_WARNING    NONE  NOT NULL,
            VIB_WARNING     NONE  NOT NULL,
            TEMP_EMERGENCY  NONE  NOT NULL,
            VIB_EMERGENCY   NONE  NOT NULL
          );''')
        print("Table created successfully")
        conn.commit()
        conn.close()

    def insert_db_sim_process_limit(self):
        conn = sqlite3.connect('sim_database.db')
        c = conn.cursor()
        print("Opened database successfully")
        this_time = datetime.datetime.now()
        print(this_time)
        c.execute("INSERT INTO SIM_LIMIT (INPUT_TIME ,SENSOR_ID, TIMES, TEMP_ALERT, VIB_ALERT, TEMP_WARNING, VIB_WARNING, TEMP_EMERGENCY, VIB_EMERGENCY) \
                                      VALUES (?, ? , ?, ?, ?, ?, ? , ?, ?)",
                  (this_time, self.sim_limit[0].__repr__(), self.sim_limit[1].__repr__(), self.sim_limit[2].__repr__(),
                   self.sim_limit[3].__repr__(), self.sim_limit[4].__repr__(), self.sim_limit[5].__repr__(),
                   self.sim_limit[6].__repr__(), self.sim_limit[7].__repr__()))
        conn.commit()
        print("Records created successfully")
        conn.close()

    def search_database_configuration(self, date):
        # Since the storage time has minutes and seconds, it cannot be directly matched by year, month, and day. The
        # form of date+% can effectively search for results that are associated with keywords in SQL statements. That
        # is, all results within the date.
        date = date + '%'
        conn = sqlite3.connect('sim_database.db')
        c = conn.cursor()
        print("Opened database successfully")
        cursor = c.execute("SELECT * FROM CONFIGURATION where INPUT_TIME LIKE :date", {"date": date})
        for row in cursor:
            print(row)
        print("Operation done successfully")
        conn.close()

    def search_database_sim_value(self, date):
        date = date + '%'
        conn = sqlite3.connect('sim_database.db')
        c = conn.cursor()
        print("Opened database successfully")
        # Pass the parameter into the SQL statement to be executed through the placeholder ":".
        cursor = c.execute("SELECT * FROM SIM_PROCESS where INPUT_TIME LIKE :date", {"date": date})
        for row in cursor:
            print(row)
        print("Operation done successfully")
        conn.close()

    def search_database_sim_limit(self, date):
        date = date + '%'
        conn = sqlite3.connect('sim_database.db')
        c = conn.cursor()
        print("Opened database successfully")
        cursor = c.execute("SELECT * FROM SIM_LIMIT where INPUT_TIME LIKE :date", {"date": date})
        for row in cursor:
            print(row)
        print("Operation done successfully")
        conn.close()

    def del_database(self, table, table_id):
        conn = sqlite3.connect('sim_database.db')
        c = conn.cursor()
        print("Opened database successfully")

        if table == "1":
            c.execute("DELETE from CONFIGURATION where ID=?;", table_id)
        elif table == "2":
            c.execute("DELETE from SIM_PROCESS where ID=?;", table_id)
        elif table == "3":
            c.execute("DELETE from SIM_LIMIT where ID=?;", table_id)
        else:
            print("Please enter the correct table number.")

        conn.commit()
        print("Total number of rows deleted :", conn.total_changes)

        conn.close()


#
if __name__ == '__main__':
    # Create a database operation class.
    s = Sim_database()
    while True:
        # Confirm user selection by input().
        mode = input("What do you want to perform on the database?\n"
                     "1. Import csv data and insert in Database\n"
                     "2. Query data\n"
                     "3. Delete data\n"
                     "4. Connect/create database\n"
                     "5. Create a table\n"
                     "6. quit\n"
                     "Please enter your choice:  ")
        if mode == "1":
            i_value = s.input_csv()
            if not i_value:
                print("false")
            elif i_value == 1:
                s.insert_db_sim_configuration()
                print("\n")
            elif i_value == 2:
                s.insert_db_sim_process_value()
                print("\n")
            elif i_value == 3:
                s.insert_db_sim_process_limit()
                print("\n")
        elif mode == "2":
            search_date = input(
                "Please enter the date you want to query: (format: year-month-day. For example: 2000-06-01)\n")
            select_table = input(
                "Please enter the table you want to query: 1. configuration; 2. simulation process; 3. simulation limit.\n")
            if select_table == "1":
                s.search_database_configuration(search_date)
            elif select_table == "2":
                s.search_database_sim_value(search_date)
            elif select_table == "3":
                s.search_database_sim_limit(search_date)
            else:
                print("Please enter the correct table number!")
            break
        elif mode == "3":
            print(
                "Before using this function, be sure to confirm the correctness of the id to avoid deleting data by mistake.")
            select_table = input(
                "Please enter the table you want to query: 1. configuration; 2. simulation process; 3. simulation limit.\n")
            select_id = input("Please enter the ID to be deleted:\n")
            confirm_operation = input(
                "The operation is about to be performed. If you agree, please enter yes. Or press any key to exit the operation.\n")
            if confirm_operation == "yes":
                s.del_database(select_table, select_id)
            else:
                print("quit")
            break
        elif mode == "4":
            s.connect_database()
            break
        elif mode == "5":
            print(
                "This mode will perform the operation of creating a new table according to the template. If the table "
                "with the same name already exists, please use the sql statement to delete or rename it.")
            create_table = input(
                "Please enter the template you want to create: 1. configuration; 2. simulation process;"
                " 3. simulation limitations.")
            if create_table == "1":
                s.create_db_sim_configuration()
            elif create_table == "2":
                s.create_db_sim_process_value()
            elif create_table == "3":
                s.create_db_sim_process_limit()
            else:
                print("Please enter the correct options number!")
        elif mode == "6":
            print("QUIT!")
            break
        else:
            # continue can be re-entered by looping while true under the premise of illegal input.
            print("Illegal input! Please enter the code correctly.")
            continue
