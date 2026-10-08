---
name: tagesbriefing
description: Bereitet morgens jeden Betrieb der heutigen Tagesliste oder Besuchsroute vor, mit sichtbarem Anlass, erstem Satz und möglichen Einwänden. Use when die Person „Guten Morgen“, „Briefing“, „Tagesliste“, „wen rufe ich heute an“ oder „Besuchsroute“ sagt.
---

# Tagesbriefing

Ergebnis ist ein Kurzbriefing je Betrieb der heutigen Liste, nur im Chat. Die Person ist danach auf jeden Anruf und Besuch vorbereitet.

## Ablauf

1. **Liste finden.** Heutiges Datum bestimmen, `drive_ordner` aus `werkbank.local.json` lesen und dort `heute/tagesliste_<JJJJ-MM-TT>.csv` öffnen. An Besuchstagen heißt die Datei `besuchsroute_<JJJJ-MM-TT>.csv`.
   Gibt es keine Datei von heute: sagen, dass die Liste fehlt, und vorschlagen, im Coach-Issue Bescheid zu geben. Nie eine ältere Liste verwenden.
   Fertig, wenn die Liste von heute offen ist.

2. **Vorgeschichte prüfen.** Für jede `lead_id` in `anrufe/` nachsehen, ob es schon Zeilen gibt.
   - Steht dort ein `rueckruf`, ist der Anruf zugesagt: im Briefing „Zugesagter Rückruf“ mit Datum und Notiz, Einstieg „Sie hatten um einen Rückruf gebeten“.
   - Steht nach dem `rueckruf` schon ein `nicht_erreicht`, ist das der letzte Versuch.
   - Steht ein gesperrtes Ergebnis (`kein_interesse`, `nicht_mehr_anrufen`, `falsche_nummer`) oder steht der Betrieb auf der Sperrliste: nicht briefen, sondern sagen, dass er nicht angerufen wird.

3. **Briefing je Betrieb**, in der Reihenfolge der Liste, höchstens fünf Zeilen:
   - Firma, Branche, Ort, Entfernung.
   - Der Anlass: genau der Satz aus der Spalte `anlass_satz`, kein anderer.
   - Der erste Satz nach `wissen/pitch.md` mit diesem Anlass (an der Tür die 30-Sekunden-Fassung).
   - Ein bis zwei wahrscheinliche Einwände mit der Antwort aus `wissen/einwaende.md`.
   - Prüfhinweis: vor dem Anruf den Maps-Link öffnen und die Öffnungszeiten ansehen. Stimmt der Anlass nicht, nicht anrufen und als `spaeter` mit Notiz „Anlass stimmt nicht“ eintragen.

4. **Abschluss.** Fragen, mit welchem Betrieb die Person anfängt. Nach jedem Gespräch übernimmt der Skill `nachbereitung`.

## Erstes Mal

Das erste Briefing ist ein neuer Handgriff. Die Person öffnet die Liste im Finder selbst und liest dir den Dateinamen vor, du erklärst, warum nur die Liste von heute zählt. Danach Lernlog-Eintrag anbieten. Hat sie Briefing und Nachbereitung für eine ganze Liste gemacht, ist der Meilenstein `erste_tagesliste` erreicht (`python3 scripts/werkbank.py meilenstein erste_tagesliste erreicht`).

## Leitplanken

- Briefings bleiben im Chat. Nie in eine Datei in diesem Repo schreiben, auch nicht in `projekte/`, denn sie sind ein Auszug aus der Liste.
- Keine Telefonnummer im Chat wiederholen; die Person wählt aus der Liste.
- Kein Anlass außer dem aus der Liste, keine Vermutungen über den Betrieb.
- `wissen/leitplanken-telefon.md` gilt für jedes Briefing.
