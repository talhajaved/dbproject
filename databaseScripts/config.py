import os

#default-db is the name of the default database that is running on your postgres
#server. It is used so we can create the new database .
##db is the name you want to give to the new database
db = {
         'host': 'localhost',
         'port':'5432',
         'user': 'postgres',
         'password': 'database',
         'default-db': 'postgres',
         'db':'dbproject'
}

#The path of the folder that contains the csv data files
csv_files_input_directory = '/Users/nyuad/Desktop/csv/outputDir-1k'

#The path of the test file
dn = os.path.dirname(os.path.realpath(__file__))
test_file_path = os.path.join(dn,'input.txt')


