#!/usr/bin/env python3
"""Werkbank helper: check the repo, show the Vertriebsstrang, set a pause, record milestones.

Usage (from the repo root):
  python3 scripts/werkbank.py pruefen [--staged]
  python3 scripts/werkbank.py status
  python3 scripts/werkbank.py pause --bis JJJJ-MM-TT | --ende
  python3 scripts/werkbank.py meilenstein <id> erreicht|allein [--am JJJJ-MM-TT]

werkbank.json holds the person's state, vertriebsstrang.json the shared milestone definitions,
werkbank.local.json (git-ignored) the machine-specific Drive path and the last-read marker.
The KI-Coach reads werkbank.json and vertriebsstrang.json; only this script and the Werkbank
agent write werkbank.json. Standard library only, Python 3.9+.
"""
import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "werkbank.json"
STRANG = ROOT / "vertriebsstrang.json"

REQUIRED = ("README.md", "AGENTS.md", "CLAUDE.md", "EINRICHTUNG.md", "VERTRIEBSSTRANG.md", "LERNLOG.md",
            "werkbank.json", "vertriebsstrang.json", ".gitignore", ".githooks/pre-commit",
            "wissen/anruf-notiz.md")
IGNORED = (".env", "*.csv", "*.xlsx", "heute/", "anrufe/", "listen/", "werkbank.local.json")
LIST_SUFFIXES = (".csv", ".xlsx", ".xls", ".ods", ".tsv", ".numbers", ".gsheet")
TEXT_SUFFIXES = (".md", ".json", ".txt", ".yaml", ".yml", ".py", ".sh", ".html")
TOOLS = ("", "codex", "claude")
STATE_KEYS = ("schema", "name", "github", "werkzeug", "starttag", "auftrags_repo", "stufe", "pausen",
              "meilensteine")
# Files that must spell out the forbidden patterns to check for them.
SCAN_EXEMPT = ("scripts/werkbank.py", "tests/test_werkbank.py")

# Phone numbers: find number-like runs, strip separators, then test the German shape.
PHONE_CANDIDATE = re.compile(r"(?<![\w.-])(?:\+|\(?0)[\d \t/()\-]{5,}\d")
PHONE_SHAPE = re.compile(r"^(?:\+49|0049|0)[1-9]\d{6,13}$")

# Bereinigungsregel: nothing internal, no prices, no personal contact data in the Werkbank.
FORBIDDEN = (
    (re.compile(r"\.credentials"), "Pfad zu Zugangsdaten"),
    (re.compile(r"clients\.map\.json"), "interne Kundenliste"),
    (re.compile(r"(?<![\w-])Kunden/"), "interner Kundenordner"),
    (re.compile(r"Offer[ _]Register", re.I), "internes Preisregister"),
    (re.compile(r"mcp__"), "internes CRM-Werkzeug"),
    (re.compile(r"Provision", re.I), "Vergütungsregeln gehören in den Vertrag"),
    (re.compile(r"\d[\d.,]*\s?(?:€|Euro\b|EUR\b)|(?:€|EUR)\s?\d|\d[\d.]*,-|\d[\d.,]*\s?netto\b", re.I),
     "Preis oder Betrag"),
    (re.compile(r"[\w.+-]+@(?!example\.(?:com|org|de)\b)[\w-]+\.[a-z]{2,}", re.I), "E-Mail-Adresse"),
)
DASHES = re.compile("[–—]")


class Broken(Exception):
    """werkbank.json or vertriebsstrang.json cannot be used."""


def today(value=None):
    return dt.date.fromisoformat(value) if value else dt.date.today()


def parse_date(value, label):
    try:
        return dt.date.fromisoformat(value)
    except (TypeError, ValueError):
        raise ValueError("{}: kein Datum im Format JJJJ-MM-TT: {!r}".format(label, value))


def load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise Broken("{} unlesbar: {}".format(path.name, error))


def save_state(state):
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def milestones():
    return load(STRANG)["meilensteine"]


def pause_days(pause):
    return (parse_date(pause["bis"], "bis") - parse_date(pause["von"], "von")).days + 1


def deadline(start, days, pauses):
    """Day `days` after the Starttag (Tag 0), pushed back by every pause that begins on or before
    the running deadline, by the pause's length in days (both ends included)."""
    due = start + dt.timedelta(days=days)
    for pause in sorted(pauses, key=lambda p: p["von"]):
        if parse_date(pause["von"], "von") <= due:
            due += dt.timedelta(days=pause_days(pause))
    return due


def active_pause(pauses, day):
    for pause in pauses:
        if parse_date(pause["von"], "von") <= day <= parse_date(pause["bis"], "bis"):
            return pause
    return None


# --- pruefen -----------------------------------------------------------------------------------

def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)


def in_git():
    return git("rev-parse", "--is-inside-work-tree").stdout.strip() == "true"


def candidate_files(staged):
    """(relative path, text reader) pairs: the staged snapshot, the repo's files, or the folder."""
    if staged:
        names = git("diff", "--cached", "--name-only", "--relative", "--diff-filter=ACMR").stdout.splitlines()
        return [(Path(n), lambda n=n: git("show", ":./" + n).stdout) for n in names]
    if in_git():
        names = git("ls-files", "--cached", "--others", "--exclude-standard").stdout.splitlines()
    else:
        names = [p.relative_to(ROOT).as_posix() for p in sorted(ROOT.rglob("*"))
                 if p.is_file() and not {".git", "__pycache__"} & set(p.relative_to(ROOT).parts)
                 and p.name != "werkbank.local.json"]
    return [(Path(n), lambda n=n: (ROOT / n).read_text(encoding="utf-8", errors="replace"))
            for n in names if (ROOT / n).is_file()]


def scan_line(line):
    reasons = [reason for pattern, reason in FORBIDDEN if pattern.search(line)]
    for match in PHONE_CANDIDATE.finditer(line):
        if PHONE_SHAPE.match(re.sub(r"[ \t/()\-]", "", match.group())):
            reasons.append("Telefonnummer")
            break
    return reasons


def check_state(state, defs):
    if not isinstance(state, dict):
        return ["werkbank.json: kein JSON-Objekt"]
    problems = ["werkbank.json: Feld fehlt: {}".format(k) for k in STATE_KEYS if k not in state]
    if problems:
        return problems
    if "drive_ordner" in state:
        problems.append("werkbank.json: drive_ordner gehört in werkbank.local.json (wird nie hochgeladen)")
    if state["werkzeug"] not in TOOLS:
        problems.append("werkbank.json: werkzeug muss codex oder claude sein, nicht {!r}".format(state["werkzeug"]))
    if state["stufe"] not in (1, 2, 3, 4):
        problems.append("werkbank.json: stufe muss 1 bis 4 sein")
    if state["starttag"] is not None:
        try:
            parse_date(state["starttag"], "starttag")
        except ValueError as error:
            problems.append("werkbank.json: {}".format(error))
    if not isinstance(state["pausen"], list):
        problems.append("werkbank.json: pausen muss eine Liste sein")
    else:
        for pause in state["pausen"]:
            try:
                if pause_days(pause) < 1:
                    problems.append("werkbank.json: Pause endet vor ihrem Beginn: {}".format(pause))
            except (KeyError, TypeError, ValueError) as error:
                problems.append("werkbank.json: Pause unlesbar: {} ({})".format(pause, error))
    known = {m["id"] for m in defs}
    if not isinstance(state["meilensteine"], dict):
        return problems + ["werkbank.json: meilensteine muss ein Objekt sein"]
    for key, value in state["meilensteine"].items():
        if key not in known:
            problems.append("werkbank.json: unbekannter Meilenstein: {}".format(key))
            continue
        if not isinstance(value, dict):
            problems.append("werkbank.json: Meilenstein {} muss ein Objekt sein".format(key))
            continue
        dates = {}
        for field in ("erreicht", "allein_wiederholt"):
            if value.get(field) is not None:
                try:
                    dates[field] = parse_date(value[field], "{}.{}".format(key, field))
                except ValueError as error:
                    problems.append("werkbank.json: {}".format(error))
        if "allein_wiederholt" in dates and ("erreicht" not in dates or dates["allein_wiederholt"] < dates["erreicht"]):
            problems.append("werkbank.json: {}: allein wiederholt vor dem Erreichen".format(key))
    for key in known - set(state["meilensteine"]):
        problems.append("werkbank.json: Meilenstein fehlt: {}".format(key))
    return problems


def pruefen(staged=False):
    problems = []
    files = candidate_files(staged)
    if not staged:
        for name in REQUIRED:
            if not (ROOT / name).is_file():
                problems.append("Datei fehlt: {}".format(name))
        ignore = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines() if (ROOT / ".gitignore").is_file() else []
        for pattern in IGNORED:
            if pattern not in ignore:
                problems.append(".gitignore: Eintrag fehlt: {}".format(pattern))
    for rel, read in files:
        if rel.suffix.lower() in LIST_SUFFIXES:
            problems.append("{}: Listen gehören in den Drive, nie in die Werkbank".format(rel))
            continue
        if rel.name == ".env" or (rel.name.startswith(".env.") and rel.name != ".env.example"):
            problems.append("{}: Schlüsseldateien gehören nie ins Repo".format(rel))
            continue
        if rel.name == "werkbank.local.json":
            problems.append("{}: lokale Datei, gehört nie ins Repo".format(rel))
            continue
        if rel.suffix.lower() not in TEXT_SUFFIXES or rel.as_posix() in SCAN_EXEMPT:
            continue
        for number, line in enumerate(read().splitlines(), 1):
            for reason in scan_line(line):
                problems.append("{}:{}: {}".format(rel, number, reason))
            if rel.suffix == ".md" and DASHES.search(line):
                problems.append("{}:{}: Gedankenstrich, bitte Punkt oder Komma".format(rel, number))
    try:
        state = json.loads(git("show", ":./werkbank.json").stdout) if staged and any(
            r.as_posix() == "werkbank.json" for r, _ in files) else load(STATE)
        problems += check_state(state, milestones())
    except (Broken, ValueError, KeyError, TypeError) as error:
        problems.append("werkbank.json oder vertriebsstrang.json unlesbar: {}".format(error))
    for problem in problems:
        print(problem)
    if problems:
        print("{} Problem(e). Bitte beheben, dann erneut prüfen.".format(len(problems)))
        return 1
    print("OK")
    return 0


# --- status ------------------------------------------------------------------------------------

def status(day):
    state = load(STATE)
    if check_state(state, milestones()):
        print("werkbank.json hat Fehler. Bitte zuerst `python3 scripts/werkbank.py pruefen`.")
        return 1
    if not state["starttag"]:
        print("Der Starttag ist noch nicht gesetzt. Er steht in Denis' Einladung, siehe EINRICHTUNG.md.")
        return 0
    start = parse_date(state["starttag"], "starttag")
    if day < start:
        print("Der Starttag ist {}. Bis dahin laufen keine Fristen.".format(start))
        return 0
    print("Starttag {}, heute Tag {}, Stufe {}.".format(start, (day - start).days, state["stufe"]))
    pause = active_pause(state["pausen"], day)
    if pause:
        print("Pause bis {}. Fristen und Coach-Nachrichten ruhen.".format(pause["bis"]))
    for m in milestones():
        record = state["meilensteine"][m["id"]]
        reached, repeated = record.get("erreicht"), record.get("allein_wiederholt")
        if reached and (repeated or not m["wiederholung"]):
            line = "bestanden am {}".format(repeated or reached)
        elif reached:
            line = "erreicht am {}, allein wiederholen fehlt noch".format(reached)
        elif m["frist_tag"] is None:
            line = "offen, ohne Frist"
        else:
            due = deadline(start, m["frist_tag"], state["pausen"])
            line = "überfällig seit {}".format(due) if day > due else "offen, Frist {}".format(due)
        if m.get("quelle") == "crm" and not reached:
            line += " (zählt, wenn der Coach es im CRM sieht)"
        print("- {}: {}".format(m["name"], line))
    return 0


# --- writing -----------------------------------------------------------------------------------

def pause(bis, end, day):
    state = load(STATE)
    current = active_pause(state["pausen"], day)
    if end:
        if not current:
            print("Es läuft gerade keine Pause.")
            return 2
        current["bis"] = day.isoformat()
    else:
        until = parse_date(bis, "bis")
        if until < day:
            print("Das Ende der Pause liegt in der Vergangenheit.")
            return 2
        if current:
            print("Es läuft schon eine Pause bis {}. Erst beenden, dann neu setzen.".format(current["bis"]))
            return 2
        state["pausen"].append({"von": day.isoformat(), "bis": until.isoformat()})
    save_state(state)
    print("Gespeichert. Bitte committen und pushen, damit der Coach es sieht.")
    return 0


def meilenstein(key, what, day):
    state = load(STATE)
    if key not in state["meilensteine"]:
        print("Unbekannter Meilenstein {}. Möglich: {}".format(key, ", ".join(state["meilensteine"])))
        return 2
    record = state["meilensteine"][key]
    if what == "allein":
        if not record.get("erreicht"):
            print("Erst erreichen, dann allein wiederholen.")
            return 2
        if day < parse_date(record["erreicht"], "erreicht"):
            print("Die Wiederholung kann nicht vor dem Erreichen liegen.")
            return 2
    record["erreicht" if what == "erreicht" else "allein_wiederholt"] = day.isoformat()
    # Stufe 1 is passed once the Werkbank runs and was repeated alone.
    if key == "werkbank_laeuft" and what == "allein" and state["stufe"] == 1:
        state["stufe"] = 2
        print("Stufe 1 bestanden, ab jetzt Stufe 2.")
    save_state(state)
    print("Gespeichert. Bitte committen und pushen, damit der Coach es sieht.")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    p_check = sub.add_parser("pruefen")
    p_check.add_argument("--staged", action="store_true", help="only what is staged for the next commit")
    p_status = sub.add_parser("status")
    p_status.add_argument("--heute")
    p_pause = sub.add_parser("pause")
    group = p_pause.add_mutually_exclusive_group(required=True)
    group.add_argument("--bis")
    group.add_argument("--ende", action="store_true")
    p_pause.add_argument("--heute")
    p_ms = sub.add_parser("meilenstein")
    p_ms.add_argument("id")
    p_ms.add_argument("was", choices=("erreicht", "allein"))
    p_ms.add_argument("--am")
    args = parser.parse_args(argv)
    try:
        if args.command == "pruefen":
            return pruefen(args.staged)
        if args.command == "status":
            return status(today(args.heute))
        if args.command == "pause":
            return pause(args.bis, args.ende, today(args.heute))
        return meilenstein(args.id, args.was, today(args.am))
    except (Broken, ValueError) as error:
        print(error)
        return 2


if __name__ == "__main__":
    sys.exit(main())
