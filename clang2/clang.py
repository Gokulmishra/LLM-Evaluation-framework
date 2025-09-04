import os
import subprocess
import sys

def run_clang_tidy(folder):
    results = {"errors": 0, "warnings": 0, "logs": {}}

    # Kernel includes (keep as is, even if incomplete)
    uname_r = subprocess.check_output(["uname", "-r"], text=True).strip()
    kernel_includes = [
        f"-I/lib/modules/{uname_r}/build/include",
        f"-I/usr/src/linux-headers-{uname_r}/include",
    ]

    for f in os.listdir(folder):
        if f.endswith(".c"):
            filepath = os.path.join(folder, f)

            cmd = [
                "clang-tidy",
                filepath,
                "-checks=clang-analyzer-*,bugprone-*,performance-*",
                "--"
            ] + kernel_includes

            try:
                log = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
            except subprocess.CalledProcessError as e:
                log = e.output

            results["warnings"] += log.count("warning:")
            results["errors"] += log.count("error:")
            results["logs"][f] = log.strip()

    return results


def pretty_print(results):
    print("\n=== Clang-Tidy Analysis Summary ===")
    print(f"Errors   : {results['errors']}")
    print(f"Warnings : {results['warnings']}\n")

    for fname, log in results["logs"].items():
        print(f"---- Results for {fname} ----")
        for line in log.splitlines():
            if "error:" in line:
                print(line.strip())
            elif "warning:" in line:
                print(line.strip())
            else:
                continue
        print()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 run_clang_tidy.py <folder_with_c_files>")
        sys.exit(1)

    folder = sys.argv[1]
    results = run_clang_tidy(folder)
    pretty_print(results)

