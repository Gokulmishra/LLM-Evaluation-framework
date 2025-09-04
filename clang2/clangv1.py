import os
import subprocess
import json
import sys

def run_clang_tidy(folder):
    results = {"errors": 0, "warnings": 0, "log": ""}

    # Detect kernel headers automatically
    uname_r = subprocess.check_output(["uname", "-r"], text=True).strip()
    kernel_includes = [
        f"-I/lib/modules/{uname_r}/build/include",
        f"-I/usr/src/linux-headers-{uname_r}/include",
        f"-I/usr/src/linux-headers-{uname_r}/arch/x86/include",
        f"-I/usr/src/linux-headers-{uname_r}/arch/x86/include/generated",
        f"-I/usr/src/linux-headers-{uname_r}/include/uapi",
        f"-I/usr/src/linux-headers-{uname_r}/arch/x86/include/uapi",
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
            results["log"] += f"\n---- Results for {f} ----\n{log}\n"

    return results


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 run_clang_tidy.py <folder_with_c_files>")
        sys.exit(1)

    folder = sys.argv[1]
    results = run_clang_tidy(folder)
    print(json.dumps(results, indent=2))

