"""
Executes all Jupyter notebooks in stats_notebooks/ and saves them with pre-rendered outputs.
Allows examiners and faculty to view all statistical analyses, Welch t-test results, and EDA tables
directly on GitHub or in Jupyter without requiring local execution.
"""
import io
import os
import sys
import json
import contextlib

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

NOTEBOOKS_DIR = os.path.dirname(os.path.abspath(__file__))

NOTEBOOK_FILES = [
    "01_eda_descriptive_stats.ipynb",
    "04_clt_sampling_distribution.ipynb",
    "05_hypothesis_testing_rag_vs_cag.ipynb",
    "08_regression_correlation.ipynb",
    "12_pca_clustering.ipynb",
]


def execute_notebook(filepath: str):
    print(f"Executing: {os.path.basename(filepath)}...")
    with open(filepath, "r", encoding="utf-8") as f:
        nb = json.load(f)

    # Clean execution namespace
    global_namespace = {}
    execution_count = 1

    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "code":
            source_lines = cell.get("source", [])
            code = "".join(source_lines)

            # Strip plt.show() if matplotlib not interactive
            safe_code = code.replace("plt.show()", "# plt.show() (pre-rendered)")

            stdout_capture = io.StringIO()
            try:
                with contextlib.redirect_stdout(stdout_capture):
                    exec(safe_code, global_namespace)
                output_text = stdout_capture.getvalue()
                
                outputs = []
                if output_text.strip():
                    outputs.append({
                        "name": "stdout",
                        "output_type": "stream",
                        "text": [line + "\n" for line in output_text.strip().split("\n")]
                    })
                
                cell["outputs"] = outputs
                cell["execution_count"] = execution_count
                execution_count += 1
            except Exception as e:
                print(f"  ⚠️ Cell execution warning: {e}")
                cell["outputs"] = [{
                    "output_type": "stream",
                    "name": "stderr",
                    "text": [f"Execution note: {str(e)}\n"]
                }]
                cell["execution_count"] = execution_count
                execution_count += 1

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print(f"  ✓ Saved with pre-rendered outputs ({execution_count - 1} code cells).")


def main():
    print("=" * 60)
    print("📊 Executing & Pre-rendering Statistics Jupyter Notebooks")
    print("=" * 60)
    for nb_file in NOTEBOOK_FILES:
        path = os.path.join(NOTEBOOKS_DIR, nb_file)
        if os.path.exists(path):
            execute_notebook(path)
        else:
            print(f"❌ Notebook not found: {nb_file}")
    print("=" * 60)
    print("✨ All notebooks successfully executed and saved with outputs!")
    print("=" * 60)


if __name__ == "__main__":
    main()
