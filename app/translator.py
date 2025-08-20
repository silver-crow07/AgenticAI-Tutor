from googletrans import Translator

def translate_content(text, lang_code):
    try:
        translator = Translator()
        result = translator.translate(text, dest=lang_code)
        return result.text
    except Exception as e:
        return f"Translation Error: {str(e)}"
