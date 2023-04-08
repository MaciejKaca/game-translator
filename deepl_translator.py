import requests
from language_codes import LanguageCodes


class DeepLTranslator:
    API_KEY_FORMAT = "DEEPL_API_KEY:"

    def __init__(self, api_key: str, target_lang_code):
        self.language_codes = LanguageCodes()
        # checks if language code is valid. If not, throws an exception and lists all available.
        if self.language_codes.get_language_name(target_lang_code) is None:
            raise Exception(
                "Invalid language code. Available codes are:"
                + str(self.language_codes.language_codes)
            )

        print("Your DeepL API key is:" + api_key)
        self.target_lang_code = target_lang_code
        self.api_key: str = api_key

    def translate(self, text: str):
        print("Text: " + text)

        result = requests.post(
            url="https://api-free.deepl.com/v2/translate",
            data={
                "target_lang": self.target_lang_code,
                "auth_key": self.api_key,
                "text": text
            },
        )

        translated_text = result.json()["translations"][0]["text"]
        print("Text translated: " + translated_text + "\n")
        return translated_text

    # Gets API key from file from the line where it is defined.
    # The file should follow this format:
    # OPENAI_API_KEY:<API_KEY>
    # returns only the API key without the format and blank spaces
    @staticmethod
    def get_api_key_from_file(file_name: str):
        with open(file_name, "r") as file:
            for line in file:
                if DeepLTranslator.API_KEY_FORMAT in line:
                    return line.replace(DeepLTranslator.API_KEY_FORMAT, "").strip()
        return None
