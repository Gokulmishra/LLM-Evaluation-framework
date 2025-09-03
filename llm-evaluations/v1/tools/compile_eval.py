import re
from docker_utils import run_docker_cmd

def compile_in_docker(driver_folder):
    """
    Compile driver using provided Makefile inside Docker.
    Returns success, errors, warnings, and logs.
    """
    log, code = run_docker_cmd(driver_folder, ["make", "-C", "/workspace"])
    success = (code == 0)
    errors = len(re.findall(r": error:", log))
    warnings = len(re.findall(r": warning:", log))
    return {"success": success, "errors": errors, "warnings": warnings, "log": log}

