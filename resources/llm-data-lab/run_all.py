"""Run every experiment and keep what it printed in results/.

    uv run python run_all.py          # all of them
    uv run python run_all.py 03 07    # only some
"""
import glob
import subprocess
import sys

if __name__ == "__main__":
    wanted = sys.argv[1:]
    for script in sorted(glob.glob("[0-9][0-9]_*.py")):
        if wanted and script[:2] not in wanted:
            continue
        print(f"\n######## {script}")
        done = subprocess.run([sys.executable, script], capture_output=True, text=True)
        output = done.stdout + (f"\nERROR:\n{done.stderr[-1500:]}" if done.returncode else "")
        print(output)
        with open(f"results/{script[:-3]}.txt", "w", encoding="utf-8") as f:
            f.write(output)
