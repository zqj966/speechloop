import subprocess
import sys


def test_cli_version():
    r = subprocess.run([sys.executable, "-m", "speechloop.cli", "--version"],
                       capture_output=True, text=True)
    assert r.returncode == 0
    assert r.stdout.strip()


def test_cli_init_and_run(tmp_path):
    target = tmp_path / "demo"
    r = subprocess.run([sys.executable, "-m", "speechloop.cli", "init", str(target)],
                       capture_output=True, text=True)
    assert r.returncode == 0
    suite = target / "suite.yaml"
    assert suite.exists()
    r2 = subprocess.run([sys.executable, "-m", "speechloop.cli", "run", str(suite),
                         "--format", "json"], capture_output=True, text=True)
    # WER 阈值故意宽松，应通过
    assert r2.returncode == 0, r2.stderr
    assert '"schema": 1' in r2.stdout
