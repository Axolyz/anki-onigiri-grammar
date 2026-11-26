"""Anki note type for five sentence-comprehension cards."""

from pathlib import Path

ROOT = Path(__file__).parent
MODEL_NAME = "おにぎり文法 · 和色版"
FIELDS = [
    "Grammar", "Remark", "Source", "Level", "Category", "Frequency", "Connection",
    "ExplanationJP", "ExplanationCN",
] + [
    f"{field}{slot}" for slot in range(1, 6) for field in ("Example", "Translation", "Audio")
]
THEME_SCRIPT = """<script>
(() => {
    const root = document.documentElement;
    const style = getComputedStyle(root);
    root.dataset.jlptDayTheme = style.getPropertyValue("--jlpt-day-theme").trim();
    root.dataset.jlptNightTheme = style.getPropertyValue("--jlpt-night-theme").trim();
})();
</script>"""


def field(name):
    return "{{" + name + "}}"


def conditional(name, html):
    return field(f"#{name}") + html + field(f"/{name}")


def make_template(slot, *, back):
    jp = field(f"Example{slot}")
    cn = field(f"Translation{slot}")
    audio = conditional(f"Audio{slot}", f'<span class="GrammarAudio">{field(f"Audio{slot}")}</span>')
    answer = field(f"type:Translation{slot}")
    parts = ['<main class="GrammarCard">']
    if not back:
        parts.append('<h1 class="GrammarHeading">理解例句</h1>')
    parts.append(f'<div class="GrammarExample"><p lang="ja" class="GrammarText">{jp}</p>{audio}</div>')
    if back:
        parts.append(f'<p class="GrammarTranslation" lang="zh-Hans">{cn}</p>')
    parts.append(f'<div class="GrammarType">{answer}</div>')
    if back:
        parts.extend((
            '{{#Remark}}<aside class="LocalRemarks">{{Remark}}</aside>{{/Remark}}',
            '<section class="GrammarReference">'
            '<h2 lang="ja">{{Grammar}}</h2>'
            '<p class="GrammarMeta">{{Level}}{{#Category}} · {{Category}}{{/Category}}'
            '{{#Frequency}} · {{Frequency}}{{/Frequency}}</p>'
            '{{#Connection}}<div class="GrammarConnection" lang="ja">{{Connection}}</div>{{/Connection}}'
            '{{#ExplanationCN}}<p lang="zh-Hans">{{ExplanationCN}}</p>{{/ExplanationCN}}'
            '{{#ExplanationJP}}<details><summary>日文说明</summary>'
            '<p lang="ja">{{ExplanationJP}}</p></details>{{/ExplanationJP}}'
            '{{#Source}}<a href="{{Source}}">原文与其他例句</a>{{/Source}}'
            '</section>',
        ))
    parts.extend(["</main>", THEME_SCRIPT])
    return conditional(f"Example{slot}", "\n".join(parts))


def create_model(models):
    model = models.new(MODEL_NAME)
    model["css"] = "\n".join(
        (ROOT / filename).read_text(encoding="utf-8") for filename in ("palette.css", "style.css")
    )
    for name in FIELDS:
        models.add_field(model, models.new_field(name))
    for slot in range(1, 6):
        template = models.new_template(f"例句 {slot} · 理解")
        template["qfmt"] = make_template(slot, back=False)
        template["afmt"] = make_template(slot, back=True)
        models.add_template(model, template)
    return models.add(model).id
