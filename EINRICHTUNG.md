# Einrichtung

Du richtest deine Werkbank selbst ein. Plane ein bis zwei Stunden ein, am besten an einem ruhigen Vormittag. Teil A machst du im Browser, Teil B am Mac nach dieser Liste, ab Teil C führt dich deine KI im fertigen Ordner.

Hängst du in Teil A oder B, öffne Claude oder ChatGPT im normalen Chat, füge diese Seite ein und schreib, bei welchem Schritt du bist. Die KI hilft dir dann weiter.

**Für die KI (ab Teil C):** Prüfe zuerst das „Fertig, wenn“ jedes Schritts von oben nach unten und mach beim ersten offenen weiter. Führe immer nur einen Schritt auf einmal. Sag vorher in einem Satz, was passiert und warum. Neue Befehle tippt die Person selbst ins Terminal, du zeigst sie. Hängt ein Schritt, such mit ihr den kleinsten nächsten Schritt. Klappt er auch beim zweiten Versuch nicht, notiert ihr es im Lernlog unter „Hängt“, und sie fragt Denis im Coach-Issue oder per Antwort auf seine Einladung.

## Teil A: im Browser

**A1. GitHub-Konto mit Zwei-Faktor.** Hast du noch kein GitHub-Konto, leg eins auf github.com an. Schalte unter Settings, Password and authentication, die Zwei-Faktor-Anmeldung ein. MyHiwi verlangt das. Schick Denis dann deinen GitHub-Namen und die Google-Adresse, mit der du Google Drive nutzt.
Fertig, wenn GitHub die Zwei-Faktor-Anmeldung als aktiv zeigt und Denis deinen GitHub-Namen hat.

**A2. Einladungen annehmen.** Denis schickt dir zwei Einladungen: eine zu deinem Auftrags-Repo `myhiwi-partner/<name>` auf GitHub (dort siehst du später deine Aufträge und die Hinweise vom Coach) und eine zu deinem Drive-Ordner „MyHiwi Webseiten-Vertrieb <Vorname>“. In seiner Nachricht stehen der Name deines Auftrags-Repos und dein **Starttag**. Er ist nur der Tag, an dem es losgeht; Fristen gibt es keine.
Fertig, wenn du beide Einladungen angenommen hast und `github.com/myhiwi-partner/<name>` im Browser öffnen kannst.

**A3. Werkbank erzeugen.** Öffne `https://github.com/myhiwi-partner/werkbank-vorlage`, klick auf „Use this template“, dann „Create a new repository“. Besitzer: dein eigenes Konto. Name: `werkbank`. Sichtbarkeit: Private.
Fertig, wenn `github.com/<dein-name>/werkbank` existiert.

**A4. Denis einladen.** In deiner Werkbank unter Settings, Collaborators, „Add people“: `deniskaliberda`. So kann Denis dein Lernlog lesen und der Coach deinen Fortschritt sehen.
Fertig, wenn die Einladung verschickt ist.

**A5. Deine KI.** Du brauchst Claude (Desktop-App, Bereich „Code“) oder Codex. Beides braucht ein bezahltes Abo. Welches du nimmst und wer es bezahlt, klärst du vorher mit Denis.
Fertig, wenn die App installiert ist und du angemeldet bist.

## Teil B: am Mac vorbereiten

Befehle tippst du in die App **Terminal**: Cmd und Leertaste drücken, „Terminal“ tippen, Enter. Ein Befehl ist eine Zeile; du tippst sie ab und drückst Enter. Fragt das Terminal nach deinem Mac-Passwort, siehst du beim Tippen nichts. Das ist normal, tipp es trotzdem und drück Enter.

**B1. Git und Python.** Tipp `git --version`. Erscheint ein Fenster „Befehlszeilenentwickler-Tools installieren?“, klick auf Installieren und warte, bis es fertig ist (das kann zehn Minuten dauern). Dann `git --version` noch einmal und `python3 --version`.
Fertig, wenn beide Befehle eine Versionsnummer zeigen.

**B2. GitHub-Werkzeug `gh`.** Lade auf `https://cli.github.com` das Installationspaket für macOS herunter, öffne es und folge dem Installer. Danach im Terminal: `gh --version`.
Fertig, wenn `gh --version` eine Versionsnummer zeigt.

**B3. Bei GitHub anmelden.** Tipp `gh auth login`. Es kommen Fragen auf Englisch. Antworten: „GitHub.com“, „HTTPS“, „Yes“ (bei „Authenticate Git with your GitHub credentials?“), „Login with a web browser“. Das Terminal zeigt dann einen Code; Enter öffnet den Browser, dort gibst du den Code ein und bestätigst.
Fertig, wenn `gh auth status` „Logged in to github.com“ zeigt.

**B4. Deinen Namen für Git.** Git schreibt zu jeder Änderung, wer sie gemacht hat. Auf GitHub unter Settings, Emails findest du eine Adresse, die auf `@users.noreply.github.com` endet. Dann:
`git config --global user.name "<Vorname>"` und `git config --global user.email "<diese Adresse>"`.
Fertig, wenn `git config --global user.email` diese Adresse zeigt.

**B5. Werkbank auf deinen Rechner holen.** Tipp `cd ~` (das bringt dich in deinen Benutzerordner), dann `gh repo clone <dein-name>/werkbank`. Danach liegt deine Werkbank im Benutzerordner unter `werkbank`. Nur auf deinem eigenen Rechner, nie auf dem Laptop eines Arbeitgebers.
Fertig, wenn es den Ordner `werkbank` in deinem Benutzerordner gibt.

**B6. Ordner in der KI öffnen.** Claude: Desktop-App, Bereich „Code“, Ordner `werkbank` auswählen. Codex: den Ordner `werkbank` als Projekt öffnen. Schreib dann: „Führe mich durch die Einrichtung.“ Ab hier führt dich deine KI.

## Teil C: mit deiner KI

Deine KI fragt dich, bevor sie einen Befehl ausführt oder eine Datei liest. Lies kurz, was dasteht, und erlaube es, wenn es zu dem passt, was ihr gerade macht.

**C1. Codex: Netzwerk erlauben.** Nur mit Codex: In der Datei `~/.codex/config.toml` gehört im Abschnitt `[sandbox_workspace_write]` die Zeile `network_access = true`. Sonst kann die KI die Hinweise vom Coach nicht lesen. Die KI zeigt dir, wie du die Datei öffnest. Die Einstellung gilt für alle deine Codex-Projekte.
Fertig, wenn die KI `gh auth status` ausführen kann. Mit Claude ist dieser Schritt erledigt.

**C2. Prüfung vor jedem Commit einschalten.** Im Terminal im Werkbank-Ordner (`cd ~/werkbank`): `git config core.hooksPath .githooks`. Ab jetzt prüft jeder Commit, dass keine Liste, keine Telefonnummer und kein Schlüssel hineinrutscht. GitHub prüft jeden Push zusätzlich.
Fertig, wenn `git config core.hooksPath` genau `.githooks` antwortet, mit s am Ende. Ein Tippfehler schaltet den Schutz still ab.

**C3. Auftrags-Repo erreichen.** Die KI führt `gh issue list -R myhiwi-partner/<name>` aus.
Fertig, wenn der Befehl ohne Fehler antwortet (eine leere Liste ist richtig). Meldet er „Could not resolve to a Repository“, prüf im Browser, ob du `github.com/myhiwi-partner/<name>` öffnen kannst und ob der Name stimmt. Klappt es dann noch nicht, schreib es ins Lernlog unter „Hängt“ und mach mit C4 weiter. Den Rest kann Denis lösen.

**C4. Google Drive für Desktop.** Installieren und mit der Google-Adresse aus A1 anmelden. Deinen Ordner „MyHiwi Webseiten-Vertrieb <Vorname>“ unter „Für mich freigegeben“ suchen und als Verknüpfung in „Meine Ablage“ legen. Dann liegt er auch auf deinem Rechner, meist unter `Benutzerordner/Library/CloudStorage/GoogleDrive-<deine Adresse>/Meine Ablage/MyHiwi Webseiten-Vertrieb <Vorname>` (auf Englisch „My Drive“). Die KI sucht den genauen Pfad mit dir. Fragt dein Mac, ob die KI auf Google Drive zugreifen darf: erlauben.
Fertig, wenn die KI den Ordner sehen kann. `heute/` kann am ersten Tag noch fehlen. Sie öffnet dabei keine Liste.

**C5. Deinen Stand eintragen.** Du sagst die Werte, die KI trägt sie ein, du liest gegen:
- `werkbank.local.json` (aus `werkbank.local.example.json`): `drive_ordner` ist der Pfad aus C4. Diese Datei bleibt auf deinem Rechner und wird nie hochgeladen.
- `werkbank.json`: `name` (dein Vorname), `github` (dein GitHub-Name), `werkzeug` (`codex` oder `claude`), `starttag` (das Datum aus Denis' Nachricht, als `JJJJ-MM-TT`), `auftrags_repo` (`myhiwi-partner/<name>`). Den Rest lässt du, wie er ist.

Fertig, wenn `python3 scripts/werkbank.py pruefen` mit „OK“ endet und `python3 scripts/werkbank.py status` „Dabei seit“ mit deinem Starttag zeigt.

**C6. Erster Lernlog-Eintrag und erster Commit.** Du erzählst, was du heute eingerichtet hast und wo es gehakt hat; die KI schreibt den Eintrag in `LERNLOG.md`, du liest gegen. Dann tippst du selbst im Terminal:
`git add LERNLOG.md werkbank.json`, dann `git commit -m "Werkbank eingerichtet"`, dann `git push`.
Die KI trägt danach den Meilenstein ein (`python3 scripts/werkbank.py meilenstein werkbank_laeuft erreicht`), und ihr committet und pusht das auch. Schlägt die Prüfung beim Commit an, sagt sie dir, in welcher Zeile was nicht stimmt.
Fertig, wenn dein Commit auf GitHub zu sehen ist und die Prüfung dort grün ist (die KI sieht das mit `gh run list --limit 1`). Damit ist „Werkbank läuft“ erreicht.

**C7. Allein wiederholen.** An einem der nächsten Tage machst du einen Lernlog-Eintrag mit Commit und Push ganz ohne Hilfe. Dann trägt die KI ein: `python3 scripts/werkbank.py meilenstein werkbank_laeuft allein`. Damit ist Stufe 1 bestanden, und es geht mit Stufe 2 weiter.

## Danach

Wenn du magst, verabredest du jetzt eine erste Sprechstunde mit Denis. Bring mit, was im Lernlog unter „Hängt“ steht. Wie es weitergeht, steht in `VERTRIEBSSTRANG.md`.
