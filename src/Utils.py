import datetime 

def getDate(date):
    return datetime.datetime.strptime(date,"%Y-%m-%d")

def getAgeGroup(birthyear, currentyear):
    age = int(currentyear) - birthyear

    if(age < 5):
        return "Child"
    elif(age < 18):
        return "Minor"
    elif(age < 60):
        return "Adult"
    else:
        return "Senior Citizen"

