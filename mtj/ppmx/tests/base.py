from unittest import TestCase, TestSuite

from time import sleep
import random
import shutil
from os.path import join, dirname
from os import mkdir
import subprocess
import tempfile
import sqlite3

from sleekxmpp import ClientXMPP


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
        self.port = random.randint(15200, 15300)

        # deleting users require data_path in prosody???
        self.localhost_path = mkdir(join(self.tempdir, 'localhost'))

        self.cfgfile = join(self.tempdir, 'prosody.cfg.lua')
        self.pidfile = join(self.tempdir, 'prosody.pid')
        self.sqlitefile = join(self.tempdir, 'prosody.sqlite')
        self.prosody_logfile = join(self.tempdir, 'prosody.log')
        self.init_prosody_db(self.sqlitefile)

        with open(filepath('prosody.cfg.lua.template')) as f:
            template = f.read()

        cfg = template % {
            'sqlite3': self.sqlitefile,
            'pidfile': self.pidfile,
            'prosody_logfile': self.prosody_logfile,
            'prosody_datapath': self.tempdir,
            'port': self.port,
        }

        with open(self.cfgfile, 'w') as f:
            f.write(cfg)

        self.p = subprocess.Popen(['prosody', '--config', self.cfgfile])
        sleep(0.1)  # to allow the server to start

    def make_client(self):
        jid = 'admin@localhost'
        password = 'password'
        client = ClientXMPP(jid, password)

        [client.register_plugin(plugin) for plugin in [
            'xep_0030',  # Service discovery
            'xep_0199',  # XMPP Ping
            'xep_0133',  # Adhoc admin
        ]]

        client.connect(address=('localhost', self.port))
        client.process(block=False)
        self.client = client
        return client

    def tearDown(self):
        try:
            self.client.disconnect()
        except:
            # no bot, who cares.
            pass
        self.p.terminate()
        shutil.rmtree(self.tempdir)
