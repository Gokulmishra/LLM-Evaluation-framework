import os
import subprocess
from docker_utils import run_docker_cmd

def get_kernel_release():
    """Get the kernel release inside the container."""
    result = subprocess.run(["uname", "-r"], capture_output=True, text=True)
    return result.stdout.strip()

def clang_tidy_in_docker(driver_folder):
    """
    Run clang-tidy on all .c files in driver folder.
    """
    results = {"errors": 0, "warnings": 0, "log": ""}

    kernel_release = get_kernel_release()
    include_paths = [
        f"-I/lib/modules/{kernel_release}/build/include",
        f"-I/lib/modules/{kernel_release}/build/arch/x86/include"
    ]

    for f in os.listdir(driver_folder):
        if f.endswith(".c"):
            log, code = run_docker_cmd(
                driver_folder,
                ["clang-tidy", f"/workspace/{f}", "--", *include_paths]
            )
            results["warnings"] += log.count("warning:")
            results["errors"] += log.count("error:")
            results["log"] += f"\n---- Results for {f} ----\n{log}\n"
    return results

