
import psycopg2

################################################################################
#  SQL database entry point
################################################################################

class PSQLEntry:
    """ PostgreSQL server wrapping utility, used to ease connections with the
    remote database. This class is called from both file wrappers and
    filesystem hierarchy wrappers.

    Users should provide the following information while creating the database,
    while not provided they default to their original values. """

    def __init__(self, host='127.0.0.1', port=5432, database='postgres',
            user='admin', password='', url=None,
            disable_exceptions=True):
        """ __init__(host, port, database, user, password) / __init__(url):
        While url is not provided, arguments should be passed separately. If
        the url is provided then it would override the rest.

        If disable_exceptions is set to false, exceptions would be passed on
        instead of caught and printed.

        The url should take the following form:
        .....................
        """
        if url != None:
            raise NotImplementedError('Not yet implemented')
            ...
            pass
        self.connect_params = dict(
            host=host,
            port=port,
            database=database,
            user=ser,
            password=password
        )
        self.disable_exceptions=True
        psycopg2.extras.register_uuid()
        return

    def execute_deprecated(self, command, *args, fetch_func='all'):
        """ execute_deprecated(command, ..., fetch_func='all'):
        Executes the SQL command with variables as arguments. If fetch_func is
        set to 'all', then all results satisfying the condition would be taken.
        If fetch_func is set to 'one', then only one result would be fetched.

        This function is deprecated, and might remove in the near future.
        """

        f_res = None
        with self.connect() as pg_db:
            with pg_db.cursor() as pg_csr:
                # Executing operation
                try:
                    pg_csr.execute(command, args)
                except psycopg2.ProgrammingError as err:
                    if self.disable_exceptions:
                        print('Exception occured in SQL database while executing command:\n'\
                            '    %s: %s\n    %s\n' % (type(err), err, command))
                    else:
                        raise err
                # Retrieving results
                try:
                    if fetch_func == 'one':
                        f_res = pg_csr.fetchone()
                    elif fetch_func == 'all':
                        f_res = pg_csr.fetchall()
                    else:
                        f_res = None
                except Exception as err:
                    if self.disable_exceptions:
                        print('Exception occured in SQL database while fetching result:\n'\
                            '    %s: %s\n    %s\n' % (type(err), err, command))
                    else:
                        raise err
                # Returning results
        return f_res

    def connect(self):
        """ connect():
        Returns a connection to the database. This can be used for customized
        functions acted towards it.
        """
        return psycopg2.connect(**self.connect_params)
    pass

################################################################################
#  Logical Block Manager
################################################################################

class LogicalBlockManager:
    """ Logical Block Manager dynamically managers the data and scatters the
    data throughout the dedicated rows. Concurrency is guaranteed through a
    mathematical expectation of collision. Mostly this collision would be very
    rare, and would affect performance subtly.

    The maximum connections and dedicated rows should be provided if this is the
    first time this database initializes.

    The table name is concatencated with additional metadata, such as 'psqlfs'
    as a table name would yield 'psqlfs_master' et al, which should be avoided as
    much as possible."""

    def __init__(self, db, initialize=None):
        """ __init__(db):
        Uses created database as *the base*, and takes 'psqlfs...' as table
        prefix. The argument 'initialize' is used or not used, depending on
        whether it is initialized for the first time.

        If this is the first time this FS is created, arguments should be set
        in initialize as a dict() type, which should contain the following
        datum:

          - max_rows - int(), Maximum rows dedicated to this file system.
          - max_conns - int(), Maximum connections allowed.

        If this is not the first time, LBM would automatically read the config
        from the master table.
        """
        self.db = db
        self.table_prefix = table_name
        # Set default values
        if not initialize:
            props = {}
            with self.db.connect() as p_db:
                with p_db.cursor() as p_csr:
                    # Takes the JSON string out.
                    p_csr.execute("""
                        SELECT * FROM psqlfs_master WHERE tag = 'properties'
                    """, ())
                    # Fetch only one item / as JSON.
                    j_res = p_csr.fetchone()
                    # Parsing to dict()
                    props = json.loads(j_res)
            # Attaching conditions
            self.max_rows = props['max_rows']
            self.max_conns = props['max_conns']
        # Create a new table.
        elif initialize:
            self.create(initialize)
            self.max_rows = initialize['max_rows']
            self.max_conns = initialize['max_conns']
        # Finished, not testing
        pass
    pass
