import googletrans as gt

translator = gt.Translator()

txt = "Доброго дня. Як справи?"
lang = "en"

def LangDetect(txt):
    inf = translator.detect(txt)
    return f"Detected(lang={inf.lang}, confidence={round(inf.confidence)})"

def TransLate(txt, lang):
    if lang.lower() not in gt.LANGUAGES:
        for code, name in gt.LANGUAGES.items():
            if name.lower() == lang.lower():
                lang = code
                break
    tr = translator.translate(txt, dest=lang)
    return tr.text

def CodeLang(lang):
    lang = lang.lower()
    if lang in gt.LANGUAGES:
        return gt.LANGUAGES[lang].capitalize()
    for code, name in gt.LANGUAGES.items():
        if name.lower() == lang:
            return code
    return "Language not found"

x = int(input('Введіть текст'))
for i in range(x):
    print(i, end='')

print(txt)
print(LangDetect(txt))
print(TransLate(txt, lang))
print(CodeLang("En"))
print(CodeLang("English"))