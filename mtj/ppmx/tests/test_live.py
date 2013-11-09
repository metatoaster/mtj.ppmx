import sqlite3

from mtj.ppmx import admin

from .base import ProsodyLiveTestCase


class AddUserProsodyLiveTestCase(ProsodyLiveTestCase):

    def test_add_user_delete_user(self):
        client = self.make_client()
        admin.add_user(client, 'dummy@localhost', 'a_password')

        conn = sqlite3.connect(self.sqlitefile)
        c = conn.cursor()

        c.execute("SELECT `value` from `prosody` WHERE `user` = 'dummy'")
        self.assertEqual(c.fetchone(), ('a_password',))

        admin.delete_user(client, 'dummy@localhost')

        c.execute("SELECT `value` from `prosody` WHERE `user` = 'dummy'")
        self.assertEqual(len(c.fetchall()), 0)

    def test_delete_disable_multi_user(self):
        client = self.make_client()
        admin.add_user(client, 'dummy1@localhost', 'a_password')
        admin.add_user(client, 'dummy2@localhost', 'a_password')
        admin.add_user(client, 'dummy3@localhost', 'a_password')

        conn = sqlite3.connect(self.sqlitefile)
        c = conn.cursor()
        c.execute("SELECT `value` from `prosody`")
        self.assertEqual(len(c.fetchall()), 4)

        admin.delete_user(client, ['dummy1@localhost', 'dummy3@localhost'])

        c.execute("SELECT `value` from `prosody`")
        self.assertEqual(len(c.fetchall()), 2)
