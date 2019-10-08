from pyrebase import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyDmv7TUeHMoLSz1sG5a38iE4SdZPBY08Oo",
    "authDomain": "blendr-c1bd5.firebaseapp.com",
    "databaseURL": "https://blendr-c1bd5.firebaseio.com",
    "storageBucket": "blendr-c1bd5.appspot.com",
    "projectId": "blendr-c1bd5",
    "appId": "1:289396306071:web:fe685d0d1278f3c76df9d2"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()
