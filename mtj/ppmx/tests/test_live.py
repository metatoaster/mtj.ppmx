import sqlite3

from mtj.ppmx import admin

from .base import ProsodyLiveTestCase


class AddUserProsodyLiveTestCase(ProsodyLiveTestCase):

    def test_add_user(self):
        bot = self.mkBot()
        bot.client.register_plugin('xep_0133')
        admin.add_user(bot, 'dummy@localhost', 'a_password')

        conn = sqlite3.connect(self.sqlitefile)
        c = conn.cursor()

        c.execute("SELECT `value` from `prosody` WHERE `user` = 'dummy'")
        self.assertEqual(c.fetchone(), ('a_password',))
