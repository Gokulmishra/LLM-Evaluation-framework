import os
from docker_utils import run_docker_cmd

def checkpatch_in_docker(driver_folder):
    """
    Run Linux checkpatch.pl on all .c files in driver folder.
    """
    results = {"errors": 0, "warnings": 0, "log": ""}
    for f in os.listdir(driver_folder):
        if f.endswith(".c"):
            log, _ = run_docker_cmd(driver_folder,
                ["checkpatch.pl", "--no-tree", "--file", f"/workspace/{f}"])
            results["errors"] += log.count("ERROR")
            results["warnings"] += log.count("WARNING")
            results["log"] += f"\n---- Results for {f} ----\n{log}\n"
    return results

