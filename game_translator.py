from deepl_translator import DeepLTranslator
from file_handler import FileHandler
from language_codes import LanguageCodes
from datetime import datetime


class GameTranslator:
    API_KEY_FILE_NAME = "api_key.txt"
    TRANSLATIONS_FILE_NAME = "Translations"
    OUTPUT_FILE_NAME = "Output"
    FILE_EXTENSION = ".txt"
    TRANSLATIONS_SEPARATOR = " TRANSLATED: "

    def __init__(self, input_file: str, output_language_code: str, deepl_key: str):
        self.language_codes = LanguageCodes()
        self.deepl_phraser = DeepLTranslator(deepl_key, output_language_code)
        self.input_file = FileHandler(input_file, "r")

    # returns found phrases in text. phrases are separated by a new line.
    # a phrase is always after the "m_Localized": " string.
    # already found phrases can start with "KEY: ", anything before that should be removed.
    # the phrase ends with "," at the end of the line which should not be a part of the string.
    # the phrase is always between \" characters, they should not be a part of the string.
    @staticmethod
    def get_phrases(text: str):
        phrases = []
        for line in text.splitlines():
            if "m_Localized" in line:
                phrase = line.split("m_Localized\": \"")[1].split("\",")[0]
                if "KEY: " in phrase:
                    phrase = phrase.split("KEY: ")[1]
                phrases.append(phrase)
        return phrases

    # reads translations from the file and returns them as a list of tuples (phrase, translation)
    @staticmethod
    def read_translations(file_name: str):
        translations = []
        file = FileHandler(file_name, "r")
        text = file.read()
        for line in text.splitlines():
            print(line)
            phrase, translation = line.split(GameTranslator.TRANSLATIONS_SEPARATOR)
            translations.append((phrase, translation))
        return translations

    # reads translation from file and replaces phrases in input file with translations
    def translate_from_file(self, translations_file: str):
        input_text = self.input_file.read()
        translations = self.read_translations(translations_file)

        for phrase, translation in translations:
            input_text = self.replace_phrase(input_text, phrase, translation)

        output_file = FileHandler(self.create_output_file(self.OUTPUT_FILE_NAME), "w")
        output_file.overwrite(input_text)

    # writes translations to a file. after getting all phrases displays the amount of characters and asks if proceeded.
    # while translating, displays the progress.
    def translate_to_file(self):
        input_text = self.input_file.read()
        phrases = self.get_phrases(input_text)

        translations_file = FileHandler(self.create_output_file(self.TRANSLATIONS_FILE_NAME), "a")

        total_characters = len(input_text)
        print("Number of characters: " + str(total_characters))
        if not GameTranslator.proceed():
            return

        character_translated = 0
        for phrase in phrases:
            characters_in_phrase = len(phrase)
            translation = self.deepl_phraser.translate(phrase)
            translations_file.append(phrase + GameTranslator.TRANSLATIONS_SEPARATOR + translation + "\n")
            character_translated += characters_in_phrase
            print("Progress: " + str(character_translated) + "/" + str(total_characters))

    # replaces first found phrase in text with a translated phrase
    @staticmethod
    def replace_phrase(text: str, phrase: str, translated_phrase: str):
        return text.replace(phrase, translated_phrase, 1)

    # displays "Proceed? (y/n)" and waits for user input. If user inputs "y", returns True, otherwise returns False.
    @staticmethod
    def proceed():
        proceed = input("Proceed? (y/n): ")
        if proceed == "y":
            return True
        else:
            return False

    # creates output file with a given name and extension. If extension is not provided, it uses FILE_EXTENSION.
    # Adds to the name a suffix with ac actual date and time, the date and time are separated by a dash.
    # Returns the name of the file.
    @staticmethod
    def create_output_file(file_name: str, extension: str = None):
        if extension is None:
            extension = GameTranslator.FILE_EXTENSION

        now = datetime.now()
        now_string = now.strftime("%Y-%m-%d-%H-%M-%S")
        return file_name + "-" + now_string + extension
