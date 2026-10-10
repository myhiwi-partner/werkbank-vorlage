"""Tests for scripts/werkbank.py, run from the repo root: python3 -m unittest discover tests"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "werkbank.py"


def run(repo, *args):
    return subprocess.run([sys.executable, str(repo / "scripts" / "werkbank.py"), *args],
                          cwd=repo, capture_output=True, text=True)


class RepoCase(unittest.TestCase):
    """Each test works on a fresh copy of the template."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.repo = self.tmp / "werkbank"
        shutil.copytree(ROOT, self.repo, ignore=shutil.ignore_patterns(".git", "__pycache__"))

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def state(self):
        return json.loads((self.repo / "werkbank.json").read_text(encoding="utf-8"))

    def write_state(self, **changes):
        data = self.state()
        data.update(changes)
        (self.repo / "werkbank.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                                                 encoding="utf-8")


class PruefenTest(RepoCase):
    def test_template_passes(self):
        result = run(self.repo, "pruefen")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("OK", result.stdout)

    def test_list_file_fails(self):
        (self.repo / "projekte" / "tagesliste_2026-10-05.csv").write_text("lead_id,firma\n", encoding="utf-8")
        result = run(self.repo, "pruefen")
        self.assertEqual(result.returncode, 1)
        self.assertIn("tagesliste_2026-10-05.csv", result.stdout)

    def test_phone_number_fails(self):
        (self.repo / "projekte" / "notiz.md").write_text("Rückruf unter 030 1234567\n", encoding="utf-8")
        result = run(self.repo, "pruefen")
        self.assertEqual(result.returncode, 1)
        self.assertIn("notiz.md", result.stdout)

    def test_price_fails(self):
        (self.repo / "projekte" / "notiz.md").write_text("Das kostet 1.500 € netto.\n", encoding="utf-8")
        self.assertEqual(run(self.repo, "pruefen").returncode, 1)

    def test_internal_paths_fail(self):
        for text in ("siehe ~/.credentials/x.json", "aus clients.map.json", "Ordner Kunden/Beispiel",
                     "laut Offer Register", "Werkzeug mcp__myhiwi-crm__get_lead", "Provision je Auftrag"):
            (self.repo / "projekte" / "notiz.md").write_text(text + "\n", encoding="utf-8")
            self.assertEqual(run(self.repo, "pruefen").returncode, 1, text)

    def test_dash_in_markdown_fails(self):
        (self.repo / "projekte" / "notiz.md").write_text("Gut — sehr gut.\n", encoding="utf-8")
        self.assertEqual(run(self.repo, "pruefen").returncode, 1)

    def test_unknown_milestone_fails(self):
        data = self.state()
        data["meilensteine"]["gibt_es_nicht"] = {"erreicht": None, "allein_wiederholt": None}
        self.write_state(**data)
        result = run(self.repo, "pruefen")
        self.assertEqual(result.returncode, 1)
        self.assertIn("gibt_es_nicht", result.stdout)

    def test_bad_tool_fails(self):
        self.write_state(werkzeug="notepad")
        self.assertEqual(run(self.repo, "pruefen").returncode, 1)

    def test_phone_formats_are_caught(self):
        for number in ("030-1234567", "+49 30 1234567", "030 123 4567", "0171 23 45 678", "(030) 1234567",
                       "0049 30 1234567", "Tel. 03338 70 99 11", "030/1234567"):
            (self.repo / "projekte" / "notiz.md").write_text("Nummer {}\n".format(number), encoding="utf-8")
            self.assertEqual(run(self.repo, "pruefen").returncode, 1, number)

    def test_numbers_that_are_not_phones_pass(self):
        text = ("Auftrag 0123456 vom 2026-10-05 10:15, lead 00000000-0000-4000-8000-000000000001, "
                "PLZ 16356, Tag 30, Version 1.2.3\n")
        (self.repo / "projekte" / "notiz.md").write_text(text, encoding="utf-8")
        result = run(self.repo, "pruefen")
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_price_formats_are_caught(self):
        for text in ("EUR 1500", "1500 netto", "1.500,- im Jahr", "kostet 90 Euro", "€ 200"):
            (self.repo / "projekte" / "notiz.md").write_text(text + "\n", encoding="utf-8")
            self.assertEqual(run(self.repo, "pruefen").returncode, 1, text)

    def test_drive_path_belongs_in_local_file(self):
        self.write_state(drive_ordner="/Users/x/Library/CloudStorage/GoogleDrive-x@gmail.com/Ordner")
        result = run(self.repo, "pruefen")
        self.assertEqual(result.returncode, 1)
        self.assertIn("werkbank.local.json", result.stdout)

    def test_local_file_is_not_scanned_outside_git(self):
        (self.repo / "werkbank.local.json").write_text(
            '{"drive_ordner": "/Users/x/Library/CloudStorage/GoogleDrive-x@gmail.com/Ordner"}\n', encoding="utf-8")
        self.assertEqual(run(self.repo, "pruefen").returncode, 0)

    def test_broken_state_gives_message_not_traceback(self):
        data = self.state()
        data["meilensteine"]["werkbank_laeuft"] = None
        data["pausen"] = ["kaputt"]
        self.write_state(**data)
        result = run(self.repo, "pruefen")
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("Traceback", result.stdout + result.stderr)
        result = run(self.repo, "status")
        self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_repetition_before_reaching_fails(self):
        data = self.state()
        data["meilensteine"]["werkbank_laeuft"] = {"erreicht": "2026-10-08", "allein_wiederholt": "2026-10-06"}
        self.write_state(**data)
        self.assertEqual(run(self.repo, "pruefen").returncode, 1)

    def test_typographic_quotes_get_a_hint(self):
        (self.repo / "werkbank.json").write_text('{"name": \u201eLena\u201c}\n', encoding="utf-8")
        result = run(self.repo, "pruefen")
        self.assertEqual(result.returncode, 1)
        self.assertIn("typografische Anführungszeichen", result.stdout)
        self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_gitignore_keeps_lists_out(self):
        ignore = (self.repo / ".gitignore").read_text(encoding="utf-8")
        for pattern in (".env", "*.csv", "*.xlsx", "heute/", "anrufe/", "listen/", "werkbank.local.json"):
            self.assertIn(pattern, ignore.splitlines(), pattern)


class StatusTest(RepoCase):
    def test_without_starttag(self):
        result = run(self.repo, "status", "--heute", "2026-10-05")
        self.assertEqual(result.returncode, 0)
        self.assertIn("Stufe 1. Dein Tempo, keine Fristen.", result.stdout)
        self.assertIn("- Werkbank läuft: offen\n", result.stdout)

    def test_no_deadlines_from_starttag(self):
        self.write_state(starttag="2026-10-05")
        out = run(self.repo, "status", "--heute", "2026-12-20").stdout
        self.assertIn("Dabei seit 2026-10-05", out)
        self.assertIn("Werkbank läuft: offen\n", out)
        self.assertNotIn("Frist 20", out)
        self.assertNotIn("überfällig", out)

    def test_every_milestone_is_without_deadline(self):
        strang = json.loads((self.repo / "vertriebsstrang.json").read_text(encoding="utf-8"))
        self.assertEqual({m["frist_tag"] for m in strang["meilensteine"]}, {None})

    def test_own_goal_is_shown(self):
        data = self.state()
        data["meilensteine"]["erste_tagesliste"]["ziel"] = "2026-10-20"
        self.write_state(**data)
        out = run(self.repo, "status", "--heute", "2026-10-10").stdout
        self.assertIn("Erste Tagesliste bearbeitet: offen, dein Ziel 2026-10-20", out)

    def test_passed_goal_is_a_hint_not_overdue(self):
        data = self.state()
        data["meilensteine"]["erste_tagesliste"]["ziel"] = "2026-10-20"
        self.write_state(**data)
        out = run(self.repo, "status", "--heute", "2026-10-25").stdout
        self.assertIn("dein Ziel 2026-10-20 ist vorbei (neu setzen oder streichen", out)
        self.assertNotIn("überfällig", out)

    def test_active_pause_is_shown(self):
        self.write_state(starttag="2026-10-05", pausen=[{"von": "2026-10-06", "bis": "2026-10-20"}])
        out = run(self.repo, "status", "--heute", "2026-10-08").stdout
        self.assertIn("Pause bis 2026-10-20", out)

    def test_crm_milestones_wait_for_coach(self):
        out = run(self.repo, "status", "--heute", "2026-10-06").stdout
        self.assertIn("Erster Abschluss: offen (zählt, wenn der Coach es im CRM sieht)", out)

    def test_milestone_needs_repetition(self):
        data = self.state()
        data["starttag"] = "2026-10-05"
        data["meilensteine"]["werkbank_laeuft"]["erreicht"] = "2026-10-06"
        self.write_state(**data)
        out = run(self.repo, "status", "--heute", "2026-10-09").stdout
        self.assertIn("Werkbank läuft: erreicht am 2026-10-06, allein wiederholen fehlt noch", out)

    def test_closing_milestone_needs_no_repetition(self):
        data = self.state()
        data["starttag"] = "2026-10-05"
        data["meilensteine"]["erster_abschluss"]["erreicht"] = "2026-10-20"
        self.write_state(**data)
        out = run(self.repo, "status", "--heute", "2026-10-21").stdout
        self.assertIn("Erster Abschluss: bestanden am 2026-10-20", out)


class SchreibenTest(RepoCase):
    def test_pause_and_end(self):
        self.write_state(starttag="2026-10-05")
        self.assertEqual(run(self.repo, "pause", "--bis", "2026-10-20", "--heute", "2026-10-08").returncode, 0)
        self.assertEqual(self.state()["pausen"], [{"von": "2026-10-08", "bis": "2026-10-20"}])
        self.assertEqual(run(self.repo, "pause", "--ende", "--heute", "2026-10-12").returncode, 0)
        self.assertEqual(self.state()["pausen"], [{"von": "2026-10-08", "bis": "2026-10-12"}])

    def test_pause_in_the_past_is_refused(self):
        result = run(self.repo, "pause", "--bis", "2026-10-01", "--heute", "2026-10-08")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.state()["pausen"], [])

    def test_second_pause_while_active_is_refused(self):
        run(self.repo, "pause", "--bis", "2026-10-20", "--heute", "2026-10-08")
        result = run(self.repo, "pause", "--bis", "2026-10-25", "--heute", "2026-10-09")
        self.assertEqual(result.returncode, 2)

    def test_milestone_reached_then_repeated(self):
        run(self.repo, "meilenstein", "werkbank_laeuft", "erreicht", "--am", "2026-10-06")
        run(self.repo, "meilenstein", "werkbank_laeuft", "allein", "--am", "2026-10-08")
        self.assertEqual(self.state()["meilensteine"]["werkbank_laeuft"],
                         {"erreicht": "2026-10-06", "allein_wiederholt": "2026-10-08"})

    def test_repetition_before_reaching_is_refused(self):
        result = run(self.repo, "meilenstein", "werkbank_laeuft", "allein", "--am", "2026-10-08")
        self.assertEqual(result.returncode, 2)

    def test_stage_two_after_werkbank_repeated(self):
        run(self.repo, "meilenstein", "werkbank_laeuft", "erreicht", "--am", "2026-10-06")
        run(self.repo, "meilenstein", "werkbank_laeuft", "allein", "--am", "2026-10-08")
        self.assertEqual(self.state()["stufe"], 2)

    def test_repetition_dated_before_reaching_is_refused(self):
        run(self.repo, "meilenstein", "werkbank_laeuft", "erreicht", "--am", "2026-10-08")
        self.assertEqual(run(self.repo, "meilenstein", "werkbank_laeuft", "allein", "--am", "2026-10-06").returncode, 2)

    def test_unknown_milestone_is_refused(self):
        self.assertEqual(run(self.repo, "meilenstein", "foo", "erreicht").returncode, 2)

    def test_goal_set_and_removed(self):
        self.assertEqual(run(self.repo, "ziel", "erste_tagesliste", "--bis", "2026-10-20",
                             "--heute", "2026-10-10").returncode, 0)
        self.assertEqual(self.state()["meilensteine"]["erste_tagesliste"]["ziel"], "2026-10-20")
        self.assertEqual(run(self.repo, "pruefen").returncode, 0)
        self.assertEqual(run(self.repo, "ziel", "erste_tagesliste", "--weg").returncode, 0)
        self.assertNotIn("ziel", self.state()["meilensteine"]["erste_tagesliste"])

    def test_goal_in_the_past_is_refused(self):
        result = run(self.repo, "ziel", "erste_tagesliste", "--bis", "2026-10-01", "--heute", "2026-10-10")
        self.assertEqual(result.returncode, 2)

    def test_bad_goal_date_fails_check(self):
        data = self.state()
        data["meilensteine"]["erste_tagesliste"]["ziel"] = "bald"
        self.write_state(**data)
        self.assertNotEqual(run(self.repo, "pruefen").returncode, 0)


class HookTest(RepoCase):
    """The pre-commit hook is the guard that keeps lists and phone numbers out of the Werkbank."""

    def git(self, *args):
        return subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.com", *args],
                              cwd=self.repo, capture_output=True, text=True)

    def setUp(self):
        super().setUp()
        self.git("init", "-q")
        self.git("config", "core.hooksPath", ".githooks")
        self.git("add", "-A")
        self.assertEqual(self.git("commit", "-qm", "start").returncode, 0)

    def test_list_is_blocked_even_when_forced(self):
        (self.repo / "anrufe_2026-10-05.csv").write_text("zeit,lead_id\n", encoding="utf-8")
        self.git("add", "-f", "anrufe_2026-10-05.csv")
        result = self.git("commit", "-qm", "liste")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("anrufe_2026-10-05.csv", result.stdout + result.stderr)

    def test_phone_number_is_blocked(self):
        (self.repo / "LERNLOG.md").write_text("Rückruf 0171 2345678\n", encoding="utf-8")
        self.git("add", "LERNLOG.md")
        self.assertNotEqual(self.git("commit", "-qm", "notiz").returncode, 0)

    def test_staged_leak_is_blocked_even_if_working_tree_is_clean(self):
        (self.repo / "LERNLOG.md").write_text("Rückruf 0171 2345678\n", encoding="utf-8")
        self.git("add", "LERNLOG.md")
        self.git("checkout", "--", "LERNLOG.md")  # working tree back to clean, index keeps the leak
        self.assertNotEqual(self.git("commit", "-qm", "leak").returncode, 0)

    def test_unstaged_draft_does_not_block_clean_commit(self):
        (self.repo / "projekte" / "entwurf.md").write_text("Rückruf 0171 2345678\n", encoding="utf-8")
        with (self.repo / "LERNLOG.md").open("a", encoding="utf-8") as handle:
            handle.write("\n### 2026-10-05\n\n- **Gebaut:** Einrichtung\n")
        self.git("add", "LERNLOG.md")
        result = self.git("commit", "-qm", "eintrag")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_forced_env_file_is_blocked(self):
        (self.repo / ".env.production").write_text("KEY=abc\n", encoding="utf-8")
        self.git("add", "-f", ".env.production")
        self.assertNotEqual(self.git("commit", "-qm", "env").returncode, 0)

    def test_status_warns_when_the_guard_is_off(self):
        self.write_state(starttag="2026-10-05")
        self.assertNotIn("Commit-Schutz ist aus", run(self.repo, "status", "--heute", "2026-10-06").stdout)
        self.git("config", "core.hooksPath", ".githook")
        self.assertIn("Commit-Schutz ist aus", run(self.repo, "status", "--heute", "2026-10-06").stdout)

    def test_clean_commit_passes(self):
        with (self.repo / "LERNLOG.md").open("a", encoding="utf-8") as handle:
            handle.write("\n### 2026-10-05\n\n- **Gebaut:** Werkbank eingerichtet\n")
        self.git("add", "LERNLOG.md")
        result = self.git("commit", "-qm", "erster Eintrag")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


class SkillsTest(unittest.TestCase):
    """The Stufe 2 skills ship in .agents/skills (Codex) and .claude/skills points there (Claude)."""

    SKILLS = (
        "tagesbriefing", "nachbereitung", "info-nachricht", "gespraech-vorbereiten", "abschluss", "projektdarstellung",
    )

    def test_claude_skills_is_a_link_to_the_shared_folder(self):
        link = ROOT / ".claude" / "skills"
        self.assertTrue(link.is_symlink())
        self.assertEqual(os.readlink(str(link)), "../.agents/skills")

    def test_every_skill_has_matching_front_matter(self):
        for name in self.SKILLS:
            text = (ROOT / ".agents" / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            head = text.split("---")[1]
            self.assertIn("\nname: {}\n".format(name), head)
            self.assertRegex(head, r"\ndescription: .*Use when ")

    def test_no_skill_points_to_a_missing_skill(self):
        known = set(self.SKILLS)
        for name in self.SKILLS:
            text = (ROOT / ".agents" / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            for other in re.findall(r"Skill `([a-z-]+)`", text):
                self.assertIn(other, known, "{} verweist auf {}".format(name, other))


if __name__ == "__main__":
    unittest.main()
