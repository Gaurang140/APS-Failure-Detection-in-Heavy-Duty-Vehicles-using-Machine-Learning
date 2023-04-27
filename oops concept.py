# oops concept lecture by ineuron

class Data_transformation():
   # initialisation of perticular class 
    def __init__(self, name , suranme , emailid , year_of_birth):
        self.name = name
        self.suranme = suranme
        self.emaiid = emailid
        self.year_of_birth = year_of_birth


    def calculate_age(self , current_year ):
        return current_year-self.year_of_birth 
    
class person :

    def age(self , current_year , year_of_birth):
        return current_year - year_of_birth 
    
    def email_id(self , email_id):
        print("Please enter your email id in this field so we can take this input in this " , email_id)
        
    def ask_name(self):
        name = input("tell me your name")
        return name 
    
    def ask_dob(self):
        dob= input("Input your date of birth in this field")
        
        return dob 


gau = person()





if __name__=='__main__':
   anuj = Data_transformation("anuj" , "bhandari" , "anuj@gmail.com" , "1994")
   print(anuj.year_of_birth)
   print(anuj.name)
   print(anuj.suranme)
