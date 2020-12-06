import mysql.connector
import os
from dotenv import load_dotenv


class Database():
    
    """
    This function will read from .env file the required variables used to interact with the mysql database
    """

    def __init__(self):
        load_dotenv()
        self.host = os.getenv('HOST_DB')
        self.port = os.getenv('PORT_DB')
        self.user = os.getenv('USER_DB')
        self.password = os.getenv('PASSWORD_DB')
        self.database = os.getenv('DATABASE')

    """
    This function will connect to the mysql database
    """
        
    def __connect__(self): 
        self.db = mysql.connector.connect(host=self.host, port=self.port, user=self.user, password=self.password, database=self.database)
        self.cursor = self.db.cursor()

    """
    This function will disconnect to the mysql database
    """

    def __disconnect__(self):
        self.db.disconnect()

    """
    This function will return a list of words given the name of the tag 
    """

    def get_words_by_tag(self, tag):
        self.__connect__()
        sql = "SELECT wordname FROM `words` WHERE id IN (SELECT `id-words` FROM `tags-words` WHERE `id-tags` IN (SELECT id FROM tags WHERE tagname = %s))"
        self.cursor.execute(sql, [tag])
        # the db returns a list of tuples, with this magic we will translate it to a list of words
        result = [(lambda x: x[0])(row)for row in self.cursor.fetchall()]
        self.__disconnect__()
        return result
