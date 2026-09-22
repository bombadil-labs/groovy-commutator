"""A corrupted output/witness must not pass the public certificate commands."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CertificateRejection(unittest.TestCase):
    def rejects(self, name, mutate, expected_error):
        data = json.loads((ROOT / "results" / f"{name}_20260921.json").read_text())
        mutate(data)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tampered.json"
            path.write_text(json.dumps(data))
            proc = subprocess.run([sys.executable, str(ROOT / "scripts" / f"verify_{name}.py"),
                                   "--check", str(path)], capture_output=True, text=True, timeout=30)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn(expected_error, proc.stderr)

    def test_periodic_tail_tampering(self):
        def mutate(data):
            data["cases"]["C"]["full_line_witness"]["left_cycle_word"]["x"] = "1011"
        self.rejects("representation_case_studies", mutate, "certificate differs from exact replay")

    def test_whole_field_output_tampering(self):
        def mutate(data):
            data["rules"]["110"]["candidates"][0]["witness"]["next_current"] = ["00000", "00000"]
        self.rejects("nakamura_retention", mutate, "incorrect output bits")

    def test_local_neighbourhood_tampering(self):
        def mutate(data):
            data["rules"]["110"]["candidates"][0]["witness"]["observed_neighbourhood"] = [99, 99, 99]
        self.rejects("nakamura_local_retention", mutate, "local observations differ")


if __name__ == "__main__":
    unittest.main()
