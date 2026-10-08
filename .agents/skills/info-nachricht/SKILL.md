---
name: info-nachricht
description: Schreibt einen Entwurf für eine Info-Nachricht per Mail oder WhatsApp an einen Betrieb, der ausdrücklich Unterlagen haben wollte. Use when die Person „Info-Nachricht“, „Unterlagen schicken“, „schick ihm was“ sagt oder in der Anrufliste `unterlagen` steht.
---

# Info-Nachricht

Ergebnis ist ein Entwurf im Chat, den die Person selbst verschickt. Du verschickst nie etwas.

## Vorher prüfen

Ein Entwurf entsteht nur, wenn in der Anrufliste für diesen Betrieb eine Zeile mit `ergebnis` = `unterlagen` steht, mit `kanal` und `einwilligung_von`. Fehlt das, schreibst du keinen Entwurf. Dann erklärst du, warum: Erstkontakt nur am Telefon oder an der Tür, Unterlagen nur, wenn der Betrieb sie ausdrücklich möchte, und nur über den Kanal, den er genannt hat. Kam der Wunsch erst jetzt, baut ihr zuerst die Zeile mit dem Skill `nachbereitung`.

## Ablauf

1. **Kanal nehmen.** Genau den aus der Zeile (`mail` oder `whatsapp`). Adresse oder Nummer gibt die Person beim Senden selbst ein; sie steht nicht im Entwurf und nicht im Chat.

2. **Entwurf schreiben.**
   - WhatsApp: höchstens sechs kurze Zeilen. Mail: Betreff plus höchstens zwölf Zeilen.
   - Anrede wie im Gespräch. Bezug auf das Gespräch („wie heute am Telefon besprochen“).
   - Was das Angebot ist, nach `wissen/webseiten-angebot.md` und `wissen/pitch.md`. Den Betrag nur so, wie er im Preisblatt im Drive-Ordner steht; steht er dort nicht, lässt du ihn weg.
   - Die zweite Hälfte erst nach der Freigabe, das erste Jahr Betreuung ist dabei.
   - Ein nächster Schritt als Frage, zum Beispiel ein kurzes Gespräch.
   - Absender: Vorname der Person, „ein Angebot von MyHiwi aus Ahrensfelde“.

3. **Gegenlesen.** Die Person liest und ändert, bis es passt.
   Fertig, wenn sie sagt, dass sie den Text so schickt.

4. **Danach.** Erinnern, dass höchstens zweimal nachgefasst wird. Ein vereinbartes Nachfassen ist eine neue Zeile in der Anrufliste mit `rueckruf` und Tag.

## Leitplanken

- Du sendest nie selbst, auch nicht über ein verbundenes Werkzeug.
- Keine Zusagen zu Google-Platz, Anfragen, Umsatz oder Liefertermin. Keine Rabatte, kein Sonderumfang.
- Gegenüber Betrieben heißt es „Webseite“. KI kommt nicht vor.
- Keine Beispiele mit Kundennamen, solange Denis sie nicht freigegeben hat.
- Entwürfe bleiben im Chat und kommen nicht in dieses Repo.
