"""
Packaging script for MLOps Internal Examination Submission.
Generates: RegisterNumber_MLOps_Internal.zip (231FA04E85_MLOps_Internal.zip)
"""
import os
import zipfile
import shutil
import tempfile

ZIP_NAME = "231FA04E85_MLOps_Internal.zip"
REPORT_SOURCES = [
    "231FA04E85_MLOps_Internal_Project_Document.docx",
    "231FA04E85_MLOps_Internal_Lab_Report_Final.docx",
    "231FA04E85_MLOps_Internal_Lab_Report.docx"
]
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
        # Pick the newest/largest report file
        best_report_src = None
        for cand in REPORT_SOURCES:
            if os.path.exists(cand):
                best_report_src = cand
                break
        
        canonical_report = os.path.join(tmpdir, REPORT_STANDARD_NAME)
        if best_report_src:
            shutil.copyfile(best_report_src, canonical_report)
            print(f"Copied {best_report_src} -> {canonical_report}")

        with zipfile.ZipFile(ZIP_NAME, "w", zipfile.ZIP_DEFLATED) as zipf:
            # Add canonical report as top-level docx
            if os.path.exists(canonical_report):
                zipf.write(canonical_report, arcname=REPORT_STANDARD_NAME)
                print(f"Added {REPORT_STANDARD_NAME} to ZIP archive")

            # Add all project files
            for root, dirs, files in os.walk("."):
                dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith(".")]
                
                for f in files:
                    if f in EXCLUDE_FILES or f.endswith(".zip") or f.endswith(".exe"):
                        continue
                    # Skip any duplicate docx to keep zip clean
                    if f.endswith(".docx") and f != REPORT_STANDARD_NAME:
                        continue
                    if f == REPORT_STANDARD_NAME:
                        continue
                    
                    full_path = os.path.join(root, f)
                    rel_path = os.path.relpath(full_path, ".")
                    zipf.write(full_path, arcname=rel_path)

    size_mb = os.path.getsize(ZIP_NAME) / (1024 * 1024)
    print(f"Successfully packaged {ZIP_NAME} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    package_project()
