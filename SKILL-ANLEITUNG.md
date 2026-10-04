# So ist ein Skill gebaut

Ein Skill ist eine Arbeitsanleitung für deine KI. Statt jedes Mal neu zu erklären, wie du etwas gemacht haben willst, schreibst du es einmal auf. Die KI liest die Anleitung, wenn die Aufgabe passt.

## Wo Skills liegen

```
.claude/skills/
└── projektdarstellung/        ← ein Ordner pro Skill
    ├── SKILL.md               ← die Anleitung (Pflicht)
    └── references/            ← Zusatzwissen, das die KI bei Bedarf liest (optional)
        └── gliederung.md
```

Bei Claude liegen Skills in `.claude/skills/` und gelten nur in diesem Repo. Codex sucht Skills an einem eigenen Ort; den richtet deine KI mit dir ein, wenn in Stufe 2 die ersten Skills dazukommen.

## Die Datei SKILL.md

Sie hat zwei Teile.

**1. Der Kopf (zwischen den `---`):**

```markdown
---
name: projektdarstellung
description: Erstellt für einen Betrieb eine Projektdarstellung aus öffentlichen Angaben. Use when the user „Projektdarstellung“ sagt oder einen Betrieb nennt.
---
```

- `name`: kurz, klein geschrieben, mit Bindestrichen. Gleich wie der Ordnername.
- `description`: Das Wichtigste am ganzen Skill. Die KI entscheidet nur anhand dieses Satzes, ob sie den Skill benutzt. Schreib rein, **was** der Skill macht und **wann** er dran ist, mit den Worten, die du wirklich sagst.

**2. Der Inhalt (darunter):** Die eigentliche Anleitung in Markdown. Bewährt hat sich:

- Ein Satz, was am Ende herauskommt.
- Nummerierte Schritte. Bei jedem Schritt: woran man merkt, dass er fertig ist.
- Leitplanken: was nie passieren darf.
- Verweise auf Dateien in `references/`, wenn es lang wird. Dann bleibt `SKILL.md` kurz.

## Gute Skills

- **Kurz.** Was die KI ohnehin weiß, musst du nicht erklären. Schreib nur auf, was bei dir anders ist.
- **Konkret.** „Höchstens drei Hebel, sortiert von klein nach groß“ schlägt „gib gute Empfehlungen“.
- **Mit Beispiel.** Ein gutes Ergebnis als Datei in `references/` zeigt mehr als jede Regel.
- **Getestet.** Probier den Skill in einer neuen Sitzung aus. Wenn die KI ihn nicht von selbst startet, ist meistens die `description` zu vage.

## Dein erster eigener Skill (Stufe 3)

Nimm etwas, das du jede Woche gleich machst, zum Beispiel die Vorbereitung auf eine bestimmte Branche. Geh so vor:

1. Ordner für den Skill anlegen und `SKILL.md` mit Kopf schreiben. Das machst du selbst.
2. Die Schritte aufschreiben, die du heute im Kopf hast.
3. Ein gutes Ergebnis als Beispiel nach `references/` legen, nur mit öffentlichen Angaben.
4. In einer neuen Sitzung testen: Sag das, was du sonst sagen würdest, und schau, ob der Skill startet.
5. `python3 scripts/werkbank.py pruefen`, dann Lernlog-Eintrag und Commit.

Für Skills, die du oft brauchst, gibt es das Plugin `skill-creator`. Siehe `wissen/plugins-und-dienste.md`.
