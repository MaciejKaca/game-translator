class FileHandler:
    def __init__(self, file_name, mode):
        self.file_obj = open(file_name, mode)

    def __enter__(self):
        return self.file_obj

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file_obj.close()

    def append(self, text):
        self.file_obj.write(text)

    def read(self):
        return self.file_obj.read()

    def overwrite(self, text):
        self.file_obj.seek(0)
        self.file_obj.write(text)
        self.file_obj.truncate()
