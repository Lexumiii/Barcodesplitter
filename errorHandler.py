import configparser

class CreateMessage:
    def __init__(self):
        self.msg = ''
        # initialize config with error messages
        self.configHandler = configparser.ConfigParser()
        
        self.configHandler.read('./config.ini')
        self.language = self.configHandler.get('Options', 'language')
        
    def create(self, args):
        errorHandler = configparser.ConfigParser()
        errorHandler.read("./error.ini")
        self.msg = errorHandler.get("MESSAGES", args)
        return self.msg