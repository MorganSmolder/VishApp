import unittest
from flask import Flask
from flask_testing import TestCase
from api import bind_api
from database import setup_session, create_all, drop_all
from database import JournalEntry, User

app = Flask(__name__)
app.config['TESTING'] = True

db_session = setup_session('sqlite:///:memory:')
bind_api(app, db_session)

get_streak_endpoint = '/getStreak'

class TestFlaskApp(TestCase):
    def create_app(self):
        return app

    def setUp(self):
        create_all()
        user1 = User(Name='x', Password='x', JoinPoint=0)
        db_session.add(user1)
        db_session.commit()


    def tearDown(self):
        drop_all()

    def test_streak_2_start_yesterday(self):
        entry_1 = JournalEntry(UserId=1,Year=2000,Month=1,Day=1,LastModified=0, Content="")
        entry_2 = JournalEntry(UserId=1,Year=2000,Month=1,Day=2,LastModified=0, Content="")
        db_session.add(entry_1)
        db_session.add(entry_2)
        db_session.commit()

        response = self.client.post(get_streak_endpoint, json={
            'key':'1-2000-1-3'
        })
        self.assertEqual(response.status_code, 200)
        streak = response.json['streak']
        self.assertEqual(streak, 2)
        
    def test_streak_2_start_today(self):
        entry_1 = JournalEntry(UserId=1,Year=2000,Month=1,Day=2,LastModified=0, Content="")
        entry_2 = JournalEntry(UserId=1,Year=2000,Month=1,Day=3,LastModified=0, Content="")
        db_session.add(entry_1)
        db_session.add(entry_2)
        db_session.commit()

        response = self.client.post(get_streak_endpoint, json={
            'key':'1-2000-1-3'
        })
        self.assertEqual(response.status_code, 200)
        streak = response.json['streak']
        self.assertEqual(streak, 2)
        
    def test_streak_0(self):
        entry_1 = JournalEntry(UserId=1,Year=2000,Month=1,Day=1,LastModified=0, Content="")
        entry_2 = JournalEntry(UserId=1,Year=2000,Month=1,Day=2,LastModified=0, Content="")
        db_session.add(entry_1)
        db_session.add(entry_2)
        db_session.commit()

        response = self.client.post(get_streak_endpoint, json={
            'key':'1-2000-1-4'
        })
        self.assertEqual(response.status_code, 200)
        streak = response.json['streak']
        self.assertEqual(streak, 0)

    def test_streak_2_start_last_month(self):
        entry_1 = JournalEntry(UserId=1,Year=2023,Month=12,Day=31,LastModified=0, Content="")
        entry_2 = JournalEntry(UserId=1,Year=2024,Month=1,Day=1,LastModified=0, Content="")
        db_session.add(entry_1)
        db_session.add(entry_2)
        db_session.commit()

        response = self.client.post(get_streak_endpoint, json={
            'key':'1-2024-1-1'
        })
        self.assertEqual(response.status_code, 200)
        streak = response.json['streak']
        self.assertEqual(streak, 2)
        
    def test_streak_1_cross_month(self):
        entry_1 = JournalEntry(UserId=1,Year=2023,Month=12,Day=30,LastModified=0, Content="")
        entry_2 = JournalEntry(UserId=1,Year=2024,Month=1,Day=1,LastModified=0, Content="")
        db_session.add(entry_1)
        db_session.add(entry_2)
        db_session.commit()

        response = self.client.post(get_streak_endpoint, json={
            'key':'1-2024-1-1'
        })
        self.assertEqual(response.status_code, 200)
        streak = response.json['streak']
        self.assertEqual(streak, 1)



if __name__ == '__main__':
    unittest.main()