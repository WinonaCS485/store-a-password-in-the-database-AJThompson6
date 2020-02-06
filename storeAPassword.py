import hashlib
import uuid
import pymysql.cursors

def generateSalt():
    frontSalt = str(uuid.uuid4())
    return frontSalt

def createConnection():
    # Connect to the database
    connection = pymysql.connect(host='mrbartucz.com',
                                 user='jp6884xv',
                                 password='Baseball.6',
                                 db='jp6884xv_passwordHash',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

# encryptPassword method to salt and encrypt password
def encryptPassword(password, prefixSalt):
    # Combine password and salt
    saltedPassword = prefixSalt+password
    # Hash the salted password
    hashedAndSalted = hashlib.sha256(saltedPassword.encode())
    return hashedAndSalted


# Insert the salt and hashed password into the table
def insertIntoTable(username, prefixSalt, hashedPassword):
    connection = createConnection()
    try:
        with connection.cursor() as cursor:
            sql = """INSERT INTO loginCredentials(username, salt, hash) VALUES("%s", "%s", "%s")""" % (username, prefixSalt, hashedPassword.hexdigest())
            cursor.execute(sql)   # Execute the SQL command
            connection.commit()   # Commit to save your changes.
    finally:
        connection.close()
            

def checkPassword(secondUsername, testPassword):
    connection = createConnection() 
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM loginCredentials"
            cursor.execute(sql)
            for row in cursor:
                db_username = row['username']
                if(secondUsername == db_username):
                    salt = row['salt']
                    hash = row['hash']
                    saltedPassword = salt + testPassword
                    hashedPassword = hashlib.sha256(saltedPassword.encode())
                    if hashedPassword.hexdigest() == hash:
                        print("Username and password found")
                    else:
                        print("You entered an incorrect password")
    finally:
        connection.close()
        
            
# Get user input for a password to send
username = input("Enter your username: ")
password = input("Enter a password to be stored: ")

# Generate salt
prefixSalt = generateSalt()
hashedPassword = encryptPassword(password, prefixSalt)

# Insert the data into a table
insertIntoTable(username, prefixSalt, hashedPassword)

secondUsername = input("Enter your username again please: ")
# Have the user type in the password in again to see if it is correct
testPassword = input("Enter your password again please: ")
checkPassword(secondUsername, testPassword)