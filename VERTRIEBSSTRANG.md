# Vertriebsstrang

Dein Weg zum ersten Abschluss, als Teil von etwas Größerem: Du lernst an echten MyHiwi-Produkten, eine eigene KI-Agentur zu führen. Die acht Kompetenzen dafür stehen in `LERNLOG.md`, der erste vollständige Lernfall in `wissen/lernfaelle/webseite.md`.

Tempo und Reihenfolge bestimmst du. Es gibt keine Fristen, keine Pflichtstunden und keine Quoten. Das Ziel bleibt trotzdem klar: Du kommst bei den nächsten Schritten ohne Denis weiter, mit deiner KI, guten Tickets und gezielt geholter Hilfe.

## Meilensteine

| Meilenstein | Stufe | bestanden, wenn |
|---|---|---|
| Werkbank läuft | 1 | erster eigener Commit mit Lernlog-Eintrag |
| Erste Tagesliste bearbeitet | 2 | Briefing abgerufen, Anrufnotizen von der Werkbank in die Anrufliste geschrieben |
| Erstes Gespräch gebucht | 2 | Interessent im CRM, Termin mit Denis steht |
| Erster Abschluss | 2 | Abschlussmeldung im CRM (begleiteter Auftrag) |

Bestanden ist ein Meilenstein erst, wenn du ihn einmal ohne Hilfe wiederholt hast. Beim ersten Abschluss gilt das nicht, der zählt sofort. Die ersten beiden trägst du mit deiner KI selbst ein. Gespräch und Abschluss sieht der Coach im CRM und bestätigt sie dir im Coach-Issue. Deinen Stand zeigt `python3 scripts/werkbank.py status`. Die maschinenlesbare Fassung dieser Tabelle steht in `vertriebsstrang.json`.

**Eigene Ziele, wenn du magst.** Willst du dir selbst ein Datum setzen, sag es deiner KI: `python3 scripts/werkbank.py ziel <id> --bis JJJJ-MM-TT`. Ist es vorbei, zeigt der Status das als Hinweis. Neu setzen oder streichen (`--weg`) ist beides in Ordnung.

Die ersten drei Aufträge sind **begleitet**: Du buchst das Kundengespräch mit Denis und danach deinen eigenen Termin. Ab dem vierten schließt du allein ab. Das ist eine Regel für die Qualität beim Kunden, kein Lernmaßstab: Ob du es kannst, zeigt der zweite ähnliche Fall, den du selbst führst.

## Der Coach

Der KI-Coach hat zwei Teile.

- **In deiner Werkbank** ist deine KI Lernbegleiter und Verkaufshilfe.
- **Von außen** schaut eine KI von MyHiwi auf deine Anrufliste, dein Lernlog und das CRM. Sie bestätigt Meilensteine und bereitet ein Gespräch mit Denis vor, wenn du eins willst.

Der Coach erreicht dich über das Issue „Coach“ (Label `coach`) in deinem Auftrags-Repo. GitHub schickt dir dazu eine Mail, und deine KI spricht offene Hinweise beim nächsten Start an.

Der Coach meldet sich nur, wenn es dir hilft: wenn er einen Meilenstein bestätigt, wenn ein Ziel, das du selbst gesetzt hast, vorbei ist (einmal, mit einem kleinen nächsten Schritt), oder wenn du ihn fragst. Er drängt nicht und wiederholt sich nicht.

## Hilfe von Denis

Am Anfang hilft Denis so viel wie nötig. Frag im Coach-Issue, jederzeit. Willst du reden, verabredet ihr eine **Sprechstunde**; der Coach legt dafür eine kurze Agenda an (was du geschafft hast, wo es hängt, ein echtes Gespräch zum Nachbesprechen). Wie oft, entscheidest du.

Jede Frage, bei der Denis helfen musste, ist auch für ihn ein Hinweis: Dort fehlt in der Werkbank eine Erklärung, eine Vorlage oder ein Werkzeug. Das kommt zurück in die Vorlage, damit es beim nächsten Mal ohne ihn geht.

## Pause

Brauchst du eine Pause, sag deiner KI „Pause bis …“. Sie trägt sie ein, committet und pusht. Während der Pause ruhen Erinnerungen und Coach-Nachrichten. Kommst du früher zurück, sag es einfach.

## Ende

Es gibt keinen festen Ausstieg und keinen automatischen. Ein Ende vereinbaren du und Denis offen im Gespräch, und spätere Zusammenarbeit bleibt möglich. Die Werkbank bleibt bei dir. Offene Aufträge übernimmt Denis, und der Zugang zum MyHiwi-Drive endet.
