import json


class LanguageCodes:
    def __init__(self):
        self.language_codes_file_name = "languages.json"
        self.language_codes = self.read_language_codes(self.language_codes_file_name)

    # reads a language.json file where the language codes are stored in format: "language_code": "language_name".
    # If file doesn't exist, it throws an exception.
    @staticmethod
    def read_language_codes(file_name):
        with open(file_name, "r") as file:
            return json.load(file)

    # returns a language code for a given language name, language code is considered as key and language name as value.
    # If language code doesn't exist, returns None.
    def get_language_code(self, lang_name):
        for code, language_name in self.language_codes.items():
            if language_name == lang_name:
                return code
        return None

    # returns a language name for a given language code. If language name doesn't exist, returns None.
    def get_language_name(self, language_code):
        for code, language_name in self.language_codes.items():
            if code == language_code:
                return language_name
        return None
