from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Set up database
engine = create_engine("postgres://aagwkpzqcmjlcp:632797451d6b8c816f564ec9fe08df08ae1278b0d106c5ef0d19649f7db45231@ec2-174-129-33-156.compute-1.amazonaws.com:5432/deln6atfh1l79a")
db = scoped_session(sessionmaker(bind=engine))

class Users:

    def select(self,user,flag):
        self.user = user
        self.flag = flag
        self.user_credential = db.execute("SELECT * from user_credentials where user_username = :user",{"user":self.user}).fetchone()
        if self.flag == 1:
            self.user_id = self.user_credential[0]
            self.user_data = db.execute("SELECT * from user_data where user_id = :user_id",{"user_id":self.user_id}).fetchone()
            self.user_username = self.user_credential[1]
            self.user_password = self.user_credential[2]
            self.user_fname = self.user_data[2]
            self.user_lname = self.user_data[3]
            return (self.user_id,self.user_username,self.user_password,self.user_fname,self.user_lname)
        elif self.flag == 0:
            if self.user_credential == None :
                return False
            else:
                return True
            # return (self.user_data == None)
    
    def insert_user_credentials(self,username,hashed_password,fname, lname, phone_number,country, province, city, postal_code):
        #for adding data in user_credentials table
        db.execute("INSERT into user_credentials(user_username, user_password) VALUES(:user_username, :user_password)",{"user_username":username, "user_password":hashed_password})
        db.commit()
        
        #creating an instance of the class Users
        self.user_data = Users()

        #calling select method to get the user_id
        self.user_id = self.user_data.select(username,1)[0]
        
        # creating local variable for the scope of this assignment
        self.fname = fname
        self.lname = lname
        self.phone_number = phone_number
        self.country = country
        self.province = province
        self.city = city
        self.postal_code = postal_code
        # calling insert method to insert user data into database
        self.user_data.insert_user_data(self.user_id,self.fname, self.lname, self.phone_number, self.country, self.province, self.city, self.postal_code)

    def insert_user_data(self,user_id,fname,lname, phone_number, country, province, city, postal_code):
        self.user_id = user_id
        self.fname = fname
        self.lname = lname
        self.phone_number = phone_number
        self.country = country
        self.province = province
        self.city = city
        self.postal_code = postal_code
        #for adding data in the user_data table
        db.execute("INSERT into user_data(user_id,user_first_name,user_last_name,user_phone_number,user_country,user_province,user_city,user_postal_code) VALUES(:user_id,:fname,:lname,:phone_number,:country,:province,:city,:postal_code)", {"user_id":user_id,"fname":fname,"lname":lname,"phone_number":phone_number,"country":country,"province":province,"city":city,"postal_code":postal_code})
        db.commit()

    
    