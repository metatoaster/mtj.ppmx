from unittest import TestCase, TestSuite

from time import sleep
import shutil
from os.path import join, dirname
import subprocess
import tempfile
import sqlite3

from mtj.jibber.core import BotCore


def filepath(name):
    return join(dirname(__file__), name)


class ProsodyLiveTestCase(TestCase):
    """
    Launch a live Prosody instance and run a basic test.
    """

    def init_prosody_db(self, sqlite_filename):
        conn = sqlite3.connect(sqlite_filename)
        c = conn.cursor()
        c.execute('CREATE TABLE `prosody` ('
            '`host` TEXT, `user` TEXT, `store` TEXT, `key` TEXT, '
            '`type` TEXT, `value` TEXT'
        ')')
        c.execute('CREATE INDEX `prosody_index` ON `prosody` ('
            '`host`, `user`, `store`, `key`)')
        c.execute("INSERT INTO `prosody` VALUES ("
            "'localhost', 'admin', 'accounts', 'password', "
            "'string', 'password')")
        conn.commit()
        conn.close()

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

        self.cfgfile = join(self.tempdir, 'prosody.cfg.lua')
        self.pidfile = join(self.tempdir, 'prosody.pid')
        self.sqlitefile = join(self.tempdir, 'prosody.sqlite')
        self.init_prosody_db(self.sqlitefile)

        with open(filepath('prosody.cfg.lua.template')) as f:
            template = f.read()

        cfg = template % {
            'sqlite3': self.sqlitefile,
            'pidfile': self.pidfile,
        }

        with open(self.cfgfile, 'w') as f:
            f.write(cfg)

        self.p = subprocess.Popen(['prosody', '--config', self.cfgfile])
        sleep(0.1)  # to allow the server to start

    def mkBot(self):
        self.bot = BotCore()
        self.bot.jid = 'admin@localhost'
        self.bot.password = 'password'
        self.bot.host = 'localhost'
        self.bot.connect()
        return self.bot

    def tearDown(self):
        try:
            self.bot.disconnect()
        except:
            # no bot, who cares.
            pass
        self.p.terminate()
        shutil.rmtree(self.tempdir)
