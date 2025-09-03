import os, json
from compile_eval import compile_in_docker
from checkpatch_eval import checkpatch_in_docker
from clang_tidy_eval import clang_tidy_in_docker
from scoring import score

def evaluate_driver(driver_folder):
    comp = compile_in_docker(driver_folder)
    checkpatch = checkpatch_in_docker(driver_folder)
    tidy = clang_tidy_in_docker(driver_folder)

    results = {
        "compilation": comp,
        "checkpatch": checkpatch,
        "clang_tidy": tidy
    }
    results["scores"] = score(results)
    return results

def batch_evaluate(root="drivers"):
    leaderboard = {}
    for run in os.listdir(root):
        folder = os.path.join(root, run)
        if os.path.isdir(folder):
            print(f"Evaluating {folder} ...")
            leaderboard[run] = evaluate_driver(folder)
    return leaderboard

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        folder = sys.argv[1]
        results = evaluate_driver(folder)
        print(json.dumps(results, indent=2))
    else:
        results = batch_evaluate("drivers")
        print(json.dumps(results, indent=2))

