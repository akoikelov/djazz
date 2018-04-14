

class AbstractBackupHelper(object):

    def __init__(self, db_settings):
        self.db_settings = db_settings


class MySQLBackupHelper(AbstractBackupHelper):
    pass


class SQLiteBackupHelper(AbstractBackupHelper):
    pass