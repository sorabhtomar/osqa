"""
Custom Django DB backend based on postgresql_psycopg2.
Adds a 'connection_statement' option which (if present) is executed when a
new DB connection is created.
"""


from django.db.backends.postgresql_psycopg2.base import DatabaseWrapper as BaseDatabaseWrapper


class DatabaseWrapper(BaseDatabaseWrapper):
    def __init__(self, settings_dict, alias='default'):
        settings_dict = settings_dict.copy()
        options = settings_dict['OPTIONS'].copy()
        settings_dict['OPTIONS'] = options

        self.connect_statement = options.pop('connection_statement', None)
        super(DatabaseWrapper, self).__init__(settings_dict, alias)

    def create_cursor(self, *args, **kwargs):
        cursor = super(DatabaseWrapper, self).create_cursor(*args, **kwargs)
        if self.connect_statement:
            cursor.execute(self.connect_statement)
        return cursor

