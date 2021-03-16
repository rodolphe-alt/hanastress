#import dbapi
from hdbcli import dbapi
import sys
import random
import util.printUtil
import util.miscUtils
import generators.sql.queries
#import socket
#socket.setdefaulttimeout(90) # sets timeout to 10 seconds

class DatabaseUtils:

    def __init__(self, verbose, connection = False):
        self.connection = connection
        self.printUtil = util.printUtil.PrintUtil(verbose)
        self.miscUtils = util.miscUtils.MiscUtils()
        self.queries = generators.sql.queries.Queries()

    def connect(self, hostname, instance, user, password):

        if not hostname:
            self.printUtil.warn("input needed", "You must supply a hostname to use for a connection")
            return False

        if not instance:
            self.printUtil.warn("input needed", "You must supply a instance to use for a connection")
            return False

        if not user:
            self.printUtil.warn("input needed", "You must supply a user to use for a connection")
            return False

        if not password:
            self.printUtil.warn("input needed", "You must supply a password to use for a connection")
            return False

        #Create the user and grant access to monitoring views
        try:
            #Create the database connetion to HANA
            #self.connection = dbapi.connect(hostname, int('3' + instance + '15'), user, password)
            self.connection = dbapi.connect(hostname, int('3' + instance + '44'), user, password, connectTimeout=0)

            #get a cursor
            self.cursor = self.connection.cursor()

            if not self.testConnection():
                self.printUtil.err("CONNECTION", "Test query failed")
                self.disconnect()
                sys.exit(1)

        except  Exception as e:
            self.printUtil.err("CONNECTION", "Unable to connect to DB")
            print (e)
            sys.exit(1)

        return True

    def testConnection(self):
        if self.select("SELECT 'I WORK' FROM dummy")[0][0] == 'I WORK':
            return True
        return False

    def disconnect(self):
        self.connection.commit()

        # be nice and close the connection
        self.connection.close()

        # self.printUtil.debug("CONNECTION", "disconnected")
        return True

    def createSchema(self, schema_name, user):
        # Get the query for creating schemas
        query = self.queries.createSchema(schema_name, user)

        # Run the query
        if not self.query(query):
            self.printUtil.err("ERROR", "UNABLE TO CREATE SCHEMA '" + schema_name + "' FOR USER '" + user + "'")
            sys.exit(1)

        return True

    def deleteSchema(self, name):
        # Get the query for dropping schemas
        query = self.queries.dropSchema(name)

        # Run the query
        if not self.query(query):
            self.printUtil.err("ERROR", "UNABLE TO DROP SCHEMA '" + schema_name + "'")
            sys.exit(1)
            
        return True

    def createAnarchyTable(self, schema_name, table_name, store_type):
        # Get the query string to create the table with
        query = self.queries.createAnarchyTable(schema_name, table_name, store_type)

        # Run the query
        if not self.query(query):
            self.printUtil.err("ERROR", "UNABLE TO CREATE TABLE '" + schema_name + "'.'" + table_name + "'")
            sys.exit(1)
            
        return True

    def addForiegnKey(self, schema_name, table_name1, table_name2, keyname, column):
        query = self.queries.addForiegnKey(schema_name, table_name1, table_name2, keyname, column)

        # Run the query
        if not self.query(query):
            self.printUtil.err("ERROR", "UNABLE TO CREATE CONSTRAINT BETWEEN '" + schema_name + "'.'" + table_name1 + "' AND '" + schema_name + "'.'" + table_name2 + "'")
            sys.exit(1)
            
        return True


    def createHierarchyTable(self, schema_name, table_name, store_type):
        # Get the query string to create the table with
        query = self.queries.createHierarchyTable(schema_name, table_name, store_type)

        # Run the query
        if not self.query(query):
            self.printUtil.err("ERROR", "UNABLE TO CREATE TABLE '" + schema_name + "'.'" + table_name + "'")
            sys.exit(1)
            
        return True

    def createMasterTable(self, schema_name, table_name, store_type):
        # Get the query string to create the table with
        query = self.queries.createMasterTable(schema_name, table_name, store_type)

        # Run the query
        if not self.query(query):
            self.printUtil.err("ERROR", "UNABLE TO CREATE TABLE '" + schema_name + "'.'" + table_name + "'")
            sys.exit(1)
            
        return True

    def createRelationalTable(self, schema_name, table_name, store_type, master_table):
        # Get the query string to create the table with
        query = self.queries.createRelationalTable(schema_name, table_name, store_type, master_table)

        # Run the query
        if not self.query(query):
            self.printUtil.err("ERROR", "UNABLE TO CREATE TABLE '" + schema_name + "'.'" + table_name + "'")
            sys.exit(1)
            
        return True

    def createSequence(self, schema_name, name):
        query = 'CREATE SEQUENCE "' + schema_name + '"."' + name + '" START WITH 1'

        # Run the query
        if not self.query(query):
            self.printUtil.err("ERROR", "UNABLE TO CREATE SEQUENCE '" + name + "'")
            sys.exit(1)
            
        return True

    def dropSequence(self, schema_name, name):
        query = 'DROP SEQUENCE "' + schema_name + '"."' + name + '"'

        # Run the query
        if not self.query(query):
            self.printUtil.err("ERROR", "UNABLE TO DROP SEQUENCE '" + name + "'")
            sys.exit(1)
            
        return True

    def insertRandomData(self, schema_name, table_name, columns, amount):
        query = self.queries.insertRandomDataBulk(schema_name, table_name, columns, amount)
        
        if not self.query(query):
            self.printUtil.err("ERROR", "ERROR ADDING RANDOM DATA TO TABLE: '" + table_name + "'")
            sys.exit(1)

        return True

    def query(self, query):
        try:
            self.cursor.execute(query)
            return True
        except  dbapi.Error as e:
            print (e)
            sys.exit(1)

    def select(self, query):
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except  dbapi.Error as e:
            print (e)
            sys.exit(1)
