import subprocess, os

def run_docker_cmd(driver_folder, cmd):
    """
    Run a command inside the driver-eval Docker container.
    Mounts the driver folder into /workspace and kernel headers into /lib/modules.
    """
    abs_path = os.path.abspath(driver_folder)
    proc = subprocess.run(
        ["docker", "run", "--rm",
         "-v", f"{abs_path}:/workspace",
         "-v", "/lib/modules:/lib/modules",   # ✅ Mount kernel headers
         "llm-evalv3"] + cmd,
        capture_output=True, text=True
    )
    return proc.stdout + proc.stderr, proc.returncode

