import sqlite3

from mtj.ppmx import admin

from .base import ProsodyLiveTestCase


class AddUserProsodyLiveTestCase(ProsodyLiveTestCase):

    def test_add_user(self):
        client = self.make_client()
        admin.add_user(client, 'dummy@localhost', 'a_password')

        conn = sqlite3.connect(self.sqlitefile)
        c = conn.cursor()

        c.execute("SELECT `value` from `prosody` WHERE `user` = 'dummy'")
        self.assertEqual(c.fetchone(), ('a_password',))
