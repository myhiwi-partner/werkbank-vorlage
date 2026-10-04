# Anruf-Notiz: Format der Anrufliste

Stand 05.10.2026. Die Anrufliste liegt in deinem Drive-Ordner unter `anrufe/anrufe_<JJJJ-MM-TT>.csv`, eine Datei pro Tag. MyHiwi liest sie abends ein, deshalb gilt das Format genau so. UTF-8, Komma als Trenner, Werte mit Komma in Anführungszeichen. Eine Zeile pro Versuch, noch am selben Tag. Nur anhängen, alte Zeilen nie ändern. Eine Korrektur ist eine neue Zeile.

Kopfzeile, genau so:

```
zeit,lead_id,firma,ergebnis,anlass_gesagt,kanal,einwilligung_von,rueckruf_am,notiz
```

## Spalten

| Spalte | Inhalt |
|---|---|
| `zeit` | Zeitpunkt des Anrufs oder Besuchs, `JJJJ-MM-TT HH:MM` |
| `lead_id` | genau aus der Tagesliste übernommen |
| `firma` | Name aus der Tagesliste |
| `ergebnis` | einer der Werte unten |
| `anlass_gesagt` | `ja` oder `nein`: Hast du den Anlass genannt? |
| `kanal` | nur bei Einwilligung: `telefon`, `whatsapp` oder `mail`, sonst leer |
| `einwilligung_von` | wer zugestimmt hat, zum Beispiel Inhaberin oder Büro, sonst leer |
| `rueckruf_am` | vereinbarter Tag, `JJJJ-MM-TT`, nur bei `rueckruf` |
| `notiz` | ein kurzer Satz. Keine Gesundheitsangaben, nichts Privates über Personen |

## Erlaubte Werte für `ergebnis`

| Wert | Bedeutung |
|---|---|
| `nicht_erreicht` | niemand erreicht, keine Nachricht auf der Mailbox. Nach zwei Versuchen ist Schluss. |
| `kein_interesse` | kein Interesse, der Betrieb wird gesperrt |
| `nicht_mehr_anrufen` | will nicht mehr angerufen werden, der Betrieb wird gesperrt |
| `rueckruf` | Rückruf zu einem vereinbarten Tag gewünscht |
| `unterlagen` | möchte Unterlagen über den genannten Kanal |
| `termin` | möchte ein Gespräch |
| `spaeter` | passt gerade nicht, kein Tag vereinbart |
| `falsche_nummer` | Nummer falsch oder Betrieb gibt es nicht mehr, wird gesperrt |

Erlaubte Werte für `anlass_gesagt`: `ja`, `nein`.
Erlaubte Werte für `kanal`: `telefon`, `whatsapp`, `mail` oder leer.

## Besuche

Besuche kommen in dieselbe Tagesdatei, im selben Format. Die Notiz beginnt mit `Besuch:`, so lassen sich Besuche getrennt zählen.

- Ja dazu, dass du dich meldest: `rueckruf` mit Tag, Kanal und wer zugestimmt hat
- Unterlagen oder Gespräch gewünscht: `unterlagen` oder `termin`
- kein Interesse oder nicht mehr anrufen: `kein_interesse` oder `nicht_mehr_anrufen`, der Betrieb wird gesperrt
- kein Ja zum Melden: `spaeter`, dann rufst du nicht an
- niemand angetroffen: `nicht_erreicht`

## Beispiele

```
2026-10-05 10:15,00000000-0000-4000-8000-000000000001,Musterbetrieb Nord,rueckruf,ja,telefon,Inhaberin,2026-10-08,möchte nach 16 Uhr angerufen werden
2026-10-05 10:40,00000000-0000-4000-8000-000000000002,Musterbetrieb Süd,nicht_erreicht,nein,,,,
2026-10-05 11:05,00000000-0000-4000-8000-000000000003,Musterbetrieb Ost,unterlagen,ja,whatsapp,Inhaber,,will Preis und Ablauf lesen
2026-10-06 14:20,00000000-0000-4000-8000-000000000004,Musterbetrieb West,rueckruf,ja,whatsapp,Inhaber,2026-10-13,Besuch: möchte nächste Woche eine Nachricht
```
