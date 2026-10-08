---
name: nachbereitung
description: Macht aus dem, was die Person nach einem Anruf oder Besuch erzählt oder diktiert, genau eine Zeile für die Anrufliste im Drive. Use when die Person sagt, wie ein Anruf oder Besuch lief, eine Sprachnotiz diktiert oder „Nachbereitung“, „trag ein“ oder „Anruf notieren“ sagt.
---

# Nachbereitung

Ergebnis ist genau eine neue Zeile in `anrufe/anrufe_<JJJJ-MM-TT>.csv` von heute im Drive-Ordner, nach dem Format in `wissen/anruf-notiz.md`.

## Ablauf

1. **Zuhören.** Die Person erzählt oder diktiert kurz, wie es lief. Eine Sprachnotiz tippt sie mit der Diktierfunktion ihres Rechners oder Handys ins Chatfenster; Aufnahmen von Gesprächen gibt es nie.
   Fehlt etwas, das die Zeile braucht (Ergebnis, Anlass genannt, bei Rückruf der Tag, bei Unterlagen Kanal und wer zugestimmt hat), fragst du genau danach.

2. **Zeile bauen.** `lead_id` und `firma` genau aus der heutigen Tagesliste oder Besuchsroute. `ergebnis`, `anlass_gesagt` und `kanal` nur mit den erlaubten Werten aus `wissen/anruf-notiz.md`. Bei einem Besuch beginnt die Notiz mit `Besuch:`. Die Notiz ist ein kurzer Satz: keine Gesundheitsangaben, nichts Privates über Personen.

3. **Vorlesen.** Du zeigst die Zeile und schreibst erst nach ihrem Okay.

4. **Anhängen.** In `anrufe/anrufe_<JJJJ-MM-TT>.csv` von heute. Gibt es die Datei noch nicht, legst du sie mit der Kopfzeile aus `wissen/anruf-notiz.md` an. Nur anhängen, alte Zeilen nie ändern; eine Korrektur ist eine neue Zeile.
   Fertig, wenn die Zeile in der Datei steht und du sie einmal zurückgelesen hast.

5. **Folgen nennen.**
   - `kein_interesse`, `nicht_mehr_anrufen`, `falsche_nummer`: Der Betrieb ist ab jetzt gesperrt.
   - `rueckruf`: Der Rückruf steht am vereinbarten Tag im Briefing.
   - `unterlagen`: Weiter mit dem Skill `info-nachricht`, über genau den genannten Kanal.
   - `termin`: Weiter mit dem Skill `gespraech-vorbereiten`. Bei den ersten drei Aufträgen bucht die Person das Gespräch mit Denis.
   - Fallen Beschwerde, Widerspruch, Anwalt oder Abmahnung: Das Wort kommt in die Notiz, und die Person gibt Denis noch heute Bescheid.

## Erstes Mal

Die erste Zeile ist ein neuer Handgriff. Du zeigst sie, die Person öffnet die Datei selbst und prüft, dass sie richtig angekommen ist. Danach Lernlog-Eintrag anbieten: was gut lief, was beim nächsten Anruf anders wird.

## Leitplanken

- Die Anrufliste liegt nur im Drive-Ordner. Nie eine Kopie, einen Auszug oder eine Telefonnummer in dieses Repo, ins Lernlog oder in einen Commit.
- Keine Aufnahme, kein Mithören. Du arbeitest nach dem Gespräch.
- Nichts erfinden: Was die Person nicht gesagt hat, steht nicht in der Zeile.
