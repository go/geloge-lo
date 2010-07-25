import fcntl
import pickle

class DataQueue:
    def __init__(self, filename):
        self.filename = filename

    def __open(self, flag='r'):
        self.file = open(self.filename, flag)

    def dump(self, obj):
        self.__open('w')
        pickle.dump(obj, self.file)

    def load(self):
        self.__open()
        return pickle.load(self.file)

    def lock(self):
        self.__open('a')
        fcntl.flock(self.file.fileno(), fcntl.LOCK_EX)

    def unlock(self):
        self.__open()
        fcntl.flock(self.file.fileno(), fcntl.LOCK_UN)

class GeloDataQueue(DataQueue):
    def __init__(self, filename):
        DataQueue.__init__(self, filename)

    def __clear(self):
        data = []
        self.dump(data)
        return data

    def __load_gelodata(self):
        data = None
        try:
            data = self.load()
        except Exception, e:
            data = self.__clear()
        return data

    def append(self, new_data):
        self.lock()

        try:
            current_data = self.__load_gelodata()                
            current_data.append(new_data)
            self.dump(current_data)
        finally:
            self.unlock()

    def get_all(self, readonly = False):
        self.lock()
        data = None

        try:
            data = self.__load_gelodata()                
            if not readonly:
                self.__clear()
        finally:
            self.unlock()

        return data

