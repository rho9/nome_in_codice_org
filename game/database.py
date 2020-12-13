import mysql.connector
import os
from dotenv import load_dotenv
from util.exception import NotAllowedCommand


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
    This function fill execute the commit transaction on the db. It's required when inserting values in the tables
    """

    def __commit__(self):
        self.db.commit()

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
    
    """
    This function will get all tags and languages in the db
    """

    def get_tags(self):
        self.__connect__()
        sql = "SELECT tagname, lang  FROM `tags`"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        self.__disconnect__()
        if result is None:
            return []
        else:
            return result

    """
    This function will insert a tag and a language in the db
    """

    def add_tag(self, tag, lang):
        if self.get_tag_id(tag) is None:
            self.__connect__()
            sql = "INSERT INTO `tags` (`id`, `tagname`, `lang`, `modifiable`) VALUES (NULL, %s, %s, '1')"
            value = [tag, lang]
            self.cursor.execute(sql, value)
            self.__commit__()
            self.__disconnect__()
        else:
            raise NotAllowedCommand("tag already present")

    """
    This function will return the id of a single tag
    """

    def get_tag_id(self, tag):
        self.__connect__()
        sql = "SELECT id FROM `tags` WHERE `tagname` LIKE %s "
        self.cursor.execute(sql, [tag])
        result = self.cursor.fetchone() # returns a tuple
        self.__disconnect__()
        if result is None:
            return None
        else:
            return result[0]

    """
    This function will return the id of a single word
    """

    def get_word_id(self, word):
        self.__connect__()
        sql = "SELECT id FROM `words` WHERE `wordname` LIKE %s "
        self.cursor.execute(sql, [word])
        result = self.cursor.fetchone()
        self.__disconnect__()
        if result is None:
            return None
        else:
            return result[0]

    """
    This function will insert a word or a list of words in the db and will bind it with an existing tag
    """

    def add_words(self, words, tag):
        tag_id = self.get_tag_id(tag)
        for word in words:
            word_id = self.get_word_id(word)
            if word_id is None:
                self.__connect__()
                sql = "INSERT INTO `words` (`id`, `wordname`) VALUES (NULL, %s)"
                self.cursor.execute(sql, [word])
                self.__commit__()
                word_id = self.cursor.lastrowid
                self.__disconnect__()
            # improvement: batch insert in tags-words table
            self.__connect__()
            sql = "INSERT INTO `tags-words` (`id`, `id-tags`, `id-words`) VALUES (NULL, %s, %s)"
            self.cursor.execute(sql, [tag_id, word_id])
            self.__commit__()
            self.__disconnect__()