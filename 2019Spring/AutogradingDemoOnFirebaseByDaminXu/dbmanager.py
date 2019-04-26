import pyrebase

class firebaseManager(object):
    """docstring for ClassName"""
    def __init__(self, config):
        self.config = config
        self.firebase = pyrebase.initialize_app(config)
        self.database = self.firebase.database()
        self.storage = self.firebase.storage() 

    def newGrads(self, testName, grades):
        for name, score in grades.items():
            self.database.child("GRADES").child(testName).child(name).set(score)



if __name__ == '__main__':
    config = {
              "apiKey": "AIzaSyCVL9P3X4pDhr0xXwgikOm7eabBr-u0U40",
              "authDomain": "autograding-47061.firebaseapp.com",
              "databaseURL": "https://autograding-47061.firebaseio.com",
              "storageBucket": "autograding-47061.appspot.com",
              "serviceAccount": "privateKey.json"
            }
    firebase = firebaseManager(config)
    grades = {
        "aaa": 89,
        "bbb": 90,
        "ccc": 60,
        "ddd": 100
        }
    firebase.newGrads("Test1",grades )