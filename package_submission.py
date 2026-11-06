"""
Packaging script for MLOps Internal Examination Submission.
Generates: RegisterNumber_MLOps_Internal.zip (231FA04E85_MLOps_Internal.zip)
"""
import os
import zipfile
import shutil
import tempfile

ZIP_NAME = "231FA04E85_MLOps_Internal.zip"
REPORT_FINAL = "231FA04E85_MLOps_Internal_Lab_Report_Final.docx"
REPORT_STANDARD_NAME = "231FA04E85_MLOps_Internal_Lab_Report.docx"

EXCLUDE_DIRS = {".git", ".pytest_cache", "__pycache__", "venv", ".cloudflared"}
EXCLUDE_FILES = {
    ZIP_NAME,
    "cloudflared.exe",
    "config.yml",
    "package_submission.py"
}

def package_project():
    if os.path.exists(ZIP_NAME):
        os.remove(ZIP_NAME)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Copy the latest finalized docx to the canonical report name in tmp
        canonical_report = os.path.join(tmpdir, REPORT_STANDARD_NAME)
        if os.path.exists(REPORT_FINAL):
            shutil.copyfile(REPORT_FINAL, canonical_report)

        with zipfile.ZipFile(ZIP_NAME, "w", zipfile.ZIP_DEFLATED) as zipf:
            # Add canonical report
            if os.path.exists(canonical_report):
                zipf.write(canonical_report, arcname=REPORT_STANDARD_NAME)
                print(f"Added {REPORT_STANDARD_NAME} (from {REPORT_FINAL})")

            # Add all project files
            for root, dirs, files in os.walk("."):
                # Filter out unwanted directories in-place
                dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith(".")]
                
                for f in files:
                    if f in EXCLUDE_FILES or f.endswith(".zip") or f.endswith(".exe"):
                        continue
                    # Skip the locked docx if any, since we wrote the updated one above
                    if f == REPORT_STANDARD_NAME:
                        continue
                    
                    full_path = os.path.join(root, f)
                    rel_path = os.path.relpath(full_path, ".")
                    zipf.write(full_path, arcname=rel_path)

    size_mb = os.path.getsize(ZIP_NAME) / (1024 * 1024)
    print(f"Successfully packaged {ZIP_NAME} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    package_project()
