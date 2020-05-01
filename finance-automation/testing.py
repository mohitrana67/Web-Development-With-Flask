from datetime import date
import hashlib, binascii, os
today = date.today()
import csv
# print(f"Today is {today}")

def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

#unhashing the password and check
def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


def read_csv(file_path):
    with open(file_path) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        counter = 0
        sheet = {"Account Type":[],
                 "Account Number":[],
                 "Transaction Date":[],
                 "Cheque Number":[],
                 "Description 1":[],
                 "Description 2":[],
                 "CAD$":[],
                 "USD$":[]}
        sheet_updated = []
        for row in readCSV:
            if counter >= 0:
                sheet["Account Type"].append(row[0])
                sheet["Account Number"].append(row[1])
                sheet["Transaction Date"].append(row[2])
                sheet["Cheque Number"].append(row[3])
                sheet["Description 1"].append(row[4])
                sheet["Description 2"].append(row[5])
                sheet["CAD$"].append(row[6])
                sheet["USD$"].append(row[7])
                
                temp_array = []
                totalNoOfFields = len(row)
                for i in range(0,totalNoOfFields):
                    temp_array.append(row[i])
                # temp_array.append(row[0])
                # temp_array.append(row[1])
                # temp_array.append(row[2])
                # temp_array.append(row[3])
                # temp_array.append(row[4])
                # temp_array.append(row[5])
                # temp_array.append(row[6])
                # temp_array.append(row[7])

                sheet_updated.append(temp_array)
                
            # else:
            #     print(f"Column Name is {str(row[0])}")
            
            counter += 1 
        
        header = sheet_updated[0]
        data = sheet_updated[1:]
        return data

sheet = read_csv("test.csv")
print(sheet)
# out = read_csv("test.csv")
# print(out)
# janFeb = read_csv("jan-feb.csv")
# mar = read_csv("march.csv")
# mar_2019 = read_csv("mar-2019.csv")
# totalJanFeb = 0
# totalMar = 0
# totalmar2019 = 0
# for i in mar_2019['CAD$']:
#     # print(f'{i} is a {type(i)}')

#     if i != "":
#         value = float(i)
#         if value >= 0:
#             totalJanFeb = totalJanFeb+value
#         else:
#             pass

# for i in mar['CAD$']:
#     # print(f'{i} is a {type(i)}')

#     if i != "":
#         value = float(i)
#         if value >= 0:
#             totalMar = totalMar+value
#         else:
#             pass

# print(totalJanFeb)
# print(totalMar)

# perc = ((totalJanFeb - totalMar)/totalJanFeb)*100


