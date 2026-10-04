# Einrichtung

Du richtest deine Werkbank selbst ein. Plane etwa eine Stunde ein. Die Schritte 1 bis 4 machst du im Browser, ab Schritt 5 führt dich deine KI.

**Für die KI:** Führe Schritt für Schritt, immer nur einen Schritt auf einmal. Sag vorher in einem Satz, was passiert und warum. Die Person tippt Befehle selbst, du zeigst sie. Prüfe nach jedem Schritt das „Fertig, wenn“. Hängt ein Schritt, such mit ihr den kleinsten nächsten Schritt. Klappt er auch beim zweiten Versuch nicht, notiert ihr es im Lernlog unter „Hängt“, und sie fragt Denis im Wochentermin oder per Antwort auf seine Einladung. Ist alles fertig, ist der Meilenstein „Werkbank läuft“ erreicht.

## Im Browser

**1. GitHub-Konto mit Zwei-Faktor.** Hast du noch kein GitHub-Konto, leg eins auf github.com an. Schalte unter Settings, Password and authentication, die Zwei-Faktor-Anmeldung ein. MyHiwi verlangt das. Schick Denis dann deinen GitHub-Namen und die Google-Adresse, mit der du Google Drive nutzt.
Fertig, wenn GitHub die Zwei-Faktor-Anmeldung als aktiv zeigt und Denis deinen GitHub-Namen hat.

**2. Einladungen annehmen.** Denis schickt dir zwei Einladungen: eine zu deinem Auftrags-Repo `myhiwi-partner/<name>` auf GitHub (dort siehst du später deine Aufträge und die Hinweise vom Coach) und eine zu deinem Drive-Ordner „MyHiwi Webseiten-Vertrieb <Vorname>“. In seiner Nachricht steht dein **Starttag**. Ab ihm zählen die Fristen im Vertriebsstrang.
Fertig, wenn du beide Einladungen angenommen hast.

**3. Werkbank erzeugen.** Öffne `https://github.com/myhiwi-partner/werkbank-vorlage`, klick auf „Use this template“, dann „Create a new repository“. Besitzer: dein eigenes Konto. Name: `werkbank`. Sichtbarkeit: Private.
Fertig, wenn `github.com/<dein-name>/werkbank` existiert.

**4. Denis einladen.** In deiner Werkbank unter Settings, Collaborators, „Add people“: `deniskaliberda`. So kann Denis dein Lernlog lesen und der Coach deinen Fortschritt sehen.
Fertig, wenn die Einladung verschickt ist.

## Mit deiner KI

**5. Werkzeuge installieren.** Wähle deine KI: Codex oder Claude (Desktop-App, Bereich Code). Dazu brauchst du Git, die GitHub-Kommandozeile `gh` und Python 3. Die KI prüft, was schon da ist, und zeigt dir die Befehle für den Rest. Danach meldest du `gh` an: `gh auth login`.
Mit Codex: Erlaube Codex für diesen Ordner den Netzwerkzugriff (in der Codex-Konfiguration `network_access = true` im Abschnitt `sandbox_workspace_write`). Sonst kann deine KI die Hinweise vom Coach nicht lesen. Die KI zeigt dir, wo das bei deiner Codex-Version steht.
Fertig, wenn `git --version`, `gh auth status` und `python3 --version` ohne Fehler antworten und die KI `gh issue list -R myhiwi-partner/<name>` ausführen kann.

**6. Werkbank auf deinen Rechner holen.** `gh repo clone <dein-name>/werkbank`, dann den Ordner in deiner KI öffnen. Nur auf deinem eigenen Rechner, nie auf dem Laptop eines Arbeitgebers.
Fertig, wenn deine KI diese Datei im geöffneten Ordner lesen kann.

**7. Prüfung vor jedem Commit einschalten.** Im Werkbank-Ordner: `git config core.hooksPath .githooks`. Ab jetzt prüft jeder Commit, dass keine Liste, keine Telefonnummer und kein Schlüssel hineinrutscht. GitHub prüft jeden Push zusätzlich.
Fertig, wenn `git config core.hooksPath` die Antwort `.githooks` gibt.

**8. Google Drive für Desktop.** Installieren und mit der Google-Adresse aus Schritt 1 anmelden. Deinen Ordner „MyHiwi Webseiten-Vertrieb <Vorname>“ unter „Für mich freigegeben“ suchen und als Verknüpfung in „Meine Ablage“ legen. Dann liegt er auch auf deinem Rechner. Die KI hilft dir, den Pfad zu finden.
Fertig, wenn die KI den Ordner `heute/` darin sehen kann. Sie öffnet dabei keine Liste.

**9. Deinen Stand eintragen.** Gemeinsam mit der KI:
- `werkbank.local.example.json` nach `werkbank.local.json` kopieren und dort `drive_ordner` auf den Pfad aus Schritt 8 setzen. Diese Datei bleibt auf deinem Rechner und wird nie hochgeladen.
- In `werkbank.json`: `name` (dein Vorname), `github` (dein GitHub-Name), `werkzeug` (`codex` oder `claude`), `starttag` (das Datum aus Denis' Nachricht, als `JJJJ-MM-TT`), `auftrags_repo` (`myhiwi-partner/<name>`, wie in der Einladung). Den Rest lässt du, wie er ist.

Fertig, wenn `python3 scripts/werkbank.py pruefen` mit „OK“ endet und `python3 scripts/werkbank.py status` deinen Starttag zeigt.

**10. Erster Lernlog-Eintrag und erster Commit.** Schreib in `LERNLOG.md` deinen ersten Eintrag: was du heute eingerichtet hast und wo es gehakt hat. Dann selbst: `git add LERNLOG.md werkbank.json`, `git commit -m "<ein Satz, was sich geändert hat>"`, `git push`. Die KI trägt danach den Meilenstein ein: `python3 scripts/werkbank.py meilenstein werkbank_laeuft erreicht`, und ihr committet und pusht das auch.
Fertig, wenn dein Commit auf GitHub zu sehen ist und dort die Prüfung grün ist. Damit ist „Werkbank läuft“ erreicht.

**11. Allein wiederholen.** An einem der nächsten Tage machst du einen Lernlog-Eintrag mit Commit und Push ganz ohne Hilfe. Dann trägt die KI ein: `python3 scripts/werkbank.py meilenstein werkbank_laeuft allein`. Damit ist Stufe 1 bestanden, und es geht mit Stufe 2 weiter.

## Danach

Der erste Wochentermin mit Denis ist euer Start. Bring mit, was im Lernlog unter „Hängt“ steht. Wie es weitergeht, steht in `VERTRIEBSSTRANG.md`.
