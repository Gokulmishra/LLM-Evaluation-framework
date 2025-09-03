def score(results):
    """
    Weighted scoring for evaluation results.
    Correctness: 40%
    Code Quality: 20%
    """
    correctness = 1.0 if results["compilation"]["success"] else 0.0
    correctness -= min(results["compilation"]["warnings"], 5) * 0.05

    code_quality = 1.0
    code_quality -= min(results["checkpatch"]["errors"], 5) * 0.1
    code_quality -= min(results["clang_tidy"]["warnings"], 10) * 0.05
    code_quality = max(0.0, code_quality)

    overall = (correctness * 0.4 + code_quality * 0.2) * 100
    return {
        "correctness": round(correctness, 2),
        "code_quality": round(code_quality, 2),
        "overall_score": round(overall, 2)
    }

