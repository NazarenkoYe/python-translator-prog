import asyncio
import time
from googletrans import Translator, LANGUAGES

def CodeLang(lang: str):
    if not lang:
        return None

    lang = lang.strip().lower()
    if lang in LANGUAGES:
        return LANGUAGES[lang].capitalize()
    for code, name in LANGUAGES.items():
        if name.lower() == lang:
            return code
    return None

async def LangDetect(txt: str):
    try:
        async with Translator() as translator:
            detection = await translator.detect(txt)
            return detection.lang, detection.confidence
    except Exception as e:
        return None, f"Detection error: {e}"

async def TransLate(text: str, lang: str):
    try:
        if lang.lower() in LANGUAGES:
            lang_code = lang.lower()
        else:
            lang_code = None
            for code, name in LANGUAGES.items():
                if name.lower() == lang.lower():
                    lang_code = code
                    break
        if not lang_code:
            return "Error: Unsupported language."
        async with Translator() as translator:
            result = await translator.translate(text, dest=lang_code)
            return result.text
    except Exception as e:
        return f"Translation error: {e}"

def split_into_sentences(text):
    sentences = []
    current = ""
    for char in text:
        current += char
        if char in ".":
            sentences.append(current.strip())
            current = ""
    if current.strip():
        sentences.append(current.strip())
    return sentences

async def main():

    filename = "SteveJobs.txt"
    target_language = "Irish"   
    try:
        with open(filename, "r", encoding="utf-8") as f:
            txt = f.read()
        print(f"Файл: {filename}")
    except Exception as e:
        print(f"Помилка читання файлу: {e}")
        return
    print("Кількість символів:", len(txt))
    sentences = split_into_sentences(txt)
    print("Кількість речень:", len(sentences))
    
    start_time = time.time()
    lang, conf = await LangDetect(txt)
    translated_text = await TransLate(txt, target_language)
    sync_time = time.time() - start_time

    print("\nОригінал:")
    print("Мова:", lang)
    print("Назва мови:", CodeLang(lang))
    print("Confidence:", conf)
    print(txt)

    print("\nПереклад:")
    print("Мова перекладу:", target_language)
    print("Код:", CodeLang(target_language))
    print(translated_text)
    print("\nЧас (синхронний режим):", round(sync_time, 4), "сек")

    start_time = time.time()
    async with Translator() as translator:
        detect_task = translator.detect(txt)
        if target_language.lower() in LANGUAGES:
            lang_code = target_language.lower()
        else:
            lang_code = CodeLang(target_language)
        translate_tasks = [
            translator.translate(sentence, dest=lang_code)
            for sentence in sentences
        ]

        detect_result = await detect_task
        translated_sentences = await asyncio.gather(*translate_tasks)

    async_time = time.time() - start_time
    translated_async_text = " ".join([t.text for t in translated_sentences])

    print("\nАсинхронний переклад:")
    print(translated_async_text)
    print("Час (асинхронний режим):", round(async_time, 4), "сек")

if __name__ == "__main__":
    asyncio.run(main())