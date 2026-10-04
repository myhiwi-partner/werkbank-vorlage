# Vertriebsstrang

Dein Weg vom Starttag bis zum ersten Abschluss. Der Starttag steht in Denis' Einladung und ist Tag 0; Tag 2 ist also zwei Kalendertage danach. Die Meilensteine zeigen dir, wie guter Fortschritt aussieht. Eine verpasste Frist bedeutet ein Gespräch im Wochentermin, nie eine automatische Folge.

## Meilensteine

| Meilenstein | Stufe | bestanden, wenn | Frist ab Starttag |
|---|---|---|---|
| Werkbank läuft | 1 | erster eigener Commit mit Lernlog-Eintrag | Tag 2 |
| Erste Tagesliste bearbeitet | 2 | Briefing abgerufen, Anrufnotizen von der Werkbank in die Anrufliste geschrieben | Tag 7 |
| Erstes Gespräch gebucht | 2 | Interessent im CRM, Termin mit Denis steht | keine |
| Erster Abschluss | 2 | Abschlussmeldung im CRM (begleiteter Auftrag) | Tag 30 |

Ein Meilenstein zählt erst, wenn du ihn einmal ohne Hilfe wiederholt hast. Beim ersten Abschluss gilt das nicht, der zählt sofort. Die ersten beiden trägst du mit deiner KI selbst ein. Gespräch und Abschluss sieht der Coach im CRM und bestätigt sie dir im Coach-Issue. Deinen Stand zeigt `python3 scripts/werkbank.py status`. Die maschinenlesbare Fassung dieser Tabelle steht in `vertriebsstrang.json`.

Die ersten drei Aufträge sind **begleitet**: Du buchst das Kundengespräch mit Denis und danach deinen eigenen Termin. Ab dem vierten schließt du allein ab.

## Der Coach

Der KI-Coach hat zwei Teile.

- **In deiner Werkbank** ist deine KI Lernbegleiter und Verkaufshilfe.
- **Von außen** schaut eine KI von MyHiwi einmal am Tag auf deine Anrufliste, dein Lernlog und das CRM. Sie stellt fest, welche Meilensteine erreicht sind, und bereitet den Wochentermin vor.

Der Coach erreicht dich über das Issue „Coach“ (Label `coach`) in deinem Auftrags-Repo. GitHub schickt dir dazu eine Mail, und deine KI spricht offene Hinweise beim nächsten Start an.

| Lage | Was der Coach tut |
|---|---|
| Werkbank läuft an Tag 2 noch nicht | Tag 3: „Wo hängt's?“ mit dem nächsten kleinen Schritt der Einrichtung |
| Kein Kundenkontakt bis Tag 7 | Tag 8: ein fertiges Briefing für drei Betriebe |
| Danach 5 Werktage ohne Aktivität | eine Nachricht mit einem konkreten Mini-Schritt |
| Kein Abschluss bis Tag 30 | keine Nachricht, ihr geht im Wochentermin den Trichter durch |

Höchstens eine Nachricht je Lage, keine Wiederholungsschleifen.

**Was als Aktivität zählt:** Einträge in der Anrufliste (Anrufe und Besuche), Notizen und Abschlussmeldungen im CRM, Kommentare in deinen Aufträgen. Ein Lernlog-Eintrag zählt nur in Stufe 1.

## Wochentermin

Einmal pro Woche, höchstens 30 Minuten mit Denis. Die Agenda kommt fertig vom Coach: die Zahlen der Woche aus deinem Trichter, wo es hängt, und ein echtes Gespräch der Woche, das ihr gemeinsam nachbesprecht. Der Coach stellt fest, ob ein Meilenstein bestanden ist, Denis bestätigt nur.

Denis wird erst direkt informiert, wenn zwei Wochentermine nacheinander ohne Aktivität waren oder wenn du nach ihm fragst. Fragen kannst du jederzeit im Coach-Issue.

## Pause

Brauchst du eine Pause, sag deiner KI „Pause bis …“. Sie trägt sie ein, committet und pusht. Während der Pause ruhen Fristen und Coach-Nachrichten, danach verlängern sich die Fristen um die Tage der Pause. Eine Frist, die vor der Pause schon verpasst war, bleibt verpasst. Kommst du früher zurück, sag es einfach.

## Ende

Eine Aktivierung endet nie automatisch. Ein Ende vereinbaren du und Denis offen im Gespräch. Die Werkbank bleibt dann bei dir. Offene Aufträge übernimmt Denis, und der Zugang zum MyHiwi-Drive endet.
