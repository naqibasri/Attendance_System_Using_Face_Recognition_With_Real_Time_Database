import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://faceattendencerealtime-9bd47-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

ref = db.reference('Staff')

data = {
    "123456":{
        'Name': "Naqib",
        'Position': "AI Engineer",
        "starting_year": 2024,
        "total_attendence": 6,
        "last_attendence_time": "2024-01-01 00:54:34"
    },
        "456789":{
        'Name': "Elon Musk",
        'Position': "BOD",
        "starting_year": 2016,
        "total_attendence": 20,
        "last_attendence_time": "2024-01-01 00:23:34"
    },
        "678901":{
        'Name': "Hillary Clinton",
        'Position': "Human Resource",
        "starting_year": 2018,
        "total_attendence": 16,
        "last_attendence_time": "2024-01-01 00:44:34"
    },
        "987654":{
        'Name': "Bill Gates",
        'Position': "DOB",
        "starting_year": 2016,
        "total_attendence": 21,
        "last_attendence_time": "2024-01-01 00:11:34"
    }
}

for key,value in data.items():
    ref.child(key).set(value)