import argparse
import os

from deepl_translator import DeepLTranslator
from game_translator import GameTranslator


def validate_args(args):
    # validates if input_file exists
    if not os.path.exists(args.input_file):
        print("Input file does not exist")
        return

    # if deepl_key is not provided, it tries to get it from API_KEY_FILE_NAME. If key is not found in file,
    # it throws an exception
    if args.deepl_key is None:
        args.deepl_key = DeepLTranslator.get_api_key_from_file(GameTranslator.API_KEY_FILE_NAME)
        if args.deepl_key is None:
            raise Exception("Provide DeepL API key as argument or put it in file")


def main():
    parser = argparse.ArgumentParser(description="Tool for translating game files")
    parser.add_argument("--translations", type=str, help="Translations file", default=None)
    parser.add_argument("--deepl_key", type=str, help="DeepL api key", default=None)
    parser.add_argument(
        "-i",
        "--input_file",
        required=True,
        type=str,
        help="File to translate",
    )
    parser.add_argument(
        "-l",
        "--output_language_code",
        required=True,
        type=str,
        help="Output language",
    )

    args = parser.parse_args()
    validate_args(args)

    deepl_key = args.deepl_key
    input_file = args.input_file
    output_language_code = args.output_language_code
    translations_file = args.translations

    game_translator = GameTranslator(input_file, output_language_code, deepl_key)

    if translations_file is None:
        game_translator.translate_to_file()
    else:
        game_translator.translate_from_file(translations_file)


if __name__ == "__main__":
    main()
