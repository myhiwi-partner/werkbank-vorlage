# Plugins und Dienste

Du bekommst nicht alles auf einmal. Neues kommt dazu, wenn du es brauchst. Woran man das sieht, steht in deinem Lernlog.

## Was du sicher brauchst

| Was | Wofür | Wann |
|---|---|---|
| Codex oder Claude | deine KI in diesem Ordner | Einrichtung |
| Git und GitHub-Kommandozeile `gh` | Werkbank sichern, Hinweise vom Coach lesen | Einrichtung |
| Google Drive für Desktop | Tagesliste, Anrufliste und Preisblatt lesen, ohne sie zu kopieren | Einrichtung |

## Später, wenn du magst

Ein Plugin ist ein Paket mit mehreren Skills. In Claude installierst du es mit `/plugin install <name>@claude-plugins-official` (falls der Marktplatz fehlt, vorher `/plugin marketplace add anthropics/claude-plugins-official`). In Codex fragst du deine KI, wie es dort geht.

| Wann | Plugin | Was es kann |
|---|---|---|
| Stufe 2 | superpowers | Brainstorming, Pläne schreiben, Fehler systematisch suchen |
| Stufe 3 | skill-creator | Eigene Skills schreiben und testen |

## Dienste mit eigenem Konto

Für jeden Dienst hast du ein **eigenes Konto**. Denis' Zugänge nutzt du nie. Kosten sprichst du vorher mit Denis ab.

Ein API-Schlüssel ist ein Passwort für Programme. Wer ihn hat, kann auf deine Kosten den Dienst nutzen. Deshalb:

1. Schlüssel beim Anbieter erzeugen.
2. `.env.example` nach `.env` kopieren und den Schlüssel dort eintragen. **Das machst du selbst im Editor, nicht über den Chat.**
3. Prüfen, dass Git die Datei nicht sieht: `git status` darf `.env` nicht zeigen.
4. Vor einem Skript den Schlüssel laden, ohne ihn anzuzeigen: `set -a; source .env; set +a`

Ist ein Schlüssel doch im Chat oder in einem Commit gelandet: beim Anbieter sofort löschen und einen neuen erzeugen. Das ist kein Drama, nur Routine.
