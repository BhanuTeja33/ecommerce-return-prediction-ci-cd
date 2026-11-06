"""
Automated Project Document Generator with Embedded Screenshots.
Builds the formal 231FA04E85_MLOps_Internal_Lab_Report.docx.
Automatically scans the screenshots/ folder, normalizes image formats using PIL,
and embeds all available screenshots with professional styling and captions.
"""

import os
import glob
from pathlib import Path
from PIL import Image
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

SCREENSHOTS_DIR = "screenshots"
PRIMARY_DOCX = "231FA04E85_MLOps_Internal_Lab_Report.docx"
FALLBACK_DOCX = "231FA04E85_MLOps_Internal_Lab_Report_Final.docx"


def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>'
    )
    tcPr.append(tcMar)


def add_image_box(doc, image_path, caption_text, width=Inches(6.0)):
    if not os.path.exists(image_path):
        return False
    # Normalize image to PNG via PIL for docx compatibility
    norm_path = image_path
    if not image_path.lower().endswith(".png"):
        norm_path = os.path.splitext(image_path)[0] + "_norm.png"
        try:
            with Image.open(image_path) as im:
                im.convert("RGB").save(norm_path, "PNG")
        except Exception as e:
            print(f"PIL conversion error for {image_path}: {e}")
            norm_path = image_path

    try:
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        run_img = p_img.add_run()
        run_img.add_picture(norm_path, width=width)

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(10)
        run_cap = p_cap.add_run(caption_text)
        run_cap.font.name = "Calibri"
        run_cap.font.size = Pt(9.5)
        run_cap.font.bold = True
        run_cap.font.italic = True
        run_cap.font.color.rgb = RGBColor(41, 128, 185)
        return True
    except Exception as e:
        print(f"Warning: Could not embed {image_path}: {e}")
        return False


def build_document():
    doc = docx.Document()

    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Document Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("MLOps INTERNAL LABORATORY EXAMINATION WORK")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(22)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(26, 82, 118)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("Question 4: Develop and Automate an E-Commerce Product Return Prediction System using CI/CD")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(13)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(86, 101, 115)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # Student Metadata Table
    table = doc.add_table(rows=7, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    metadata = [
        ("Student Name", "Velpuri Bhanu Teja"),
        ("Register Number", "231FA04E85"),
        ("Class & Section", "B.Tech CSE - Section 7"),
        ("GitHub Repository", "https://github.com/BhanuTeja33/ecommerce-return-prediction-ci-cd"),
        ("Live Web Application URL", "https://deviant-controversy-scroll-input.trycloudflare.com/docs"),
        ("Published GHCR Image", "ghcr.io/bhanuteja33/ecommerce-return-prediction:latest"),
        ("Faculty Evaluator", "Dr. Gabbi Reddy Keerthi")
    ]
    for idx, (label, val) in enumerate(metadata):
        c1 = table.cell(idx, 0)
        c2 = table.cell(idx, 1)
        c1.width = Inches(2.2)
        c2.width = Inches(4.6)
        set_cell_background(c1, "EBF5FB")
        set_cell_background(c2, "FAFAFA")
        set_cell_margins(c1)
        set_cell_margins(c2)

        r1 = c1.paragraphs[0].add_run(label)
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = RGBColor(27, 79, 114)

        r2 = c2.paragraphs[0].add_run(val)
        r2.font.size = Pt(10)
        if "http" in val or "ghcr" in val:
            r2.font.bold = True
            r2.font.color.rgb = RGBColor(41, 128, 185)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # 1. Problem Statement
    doc.add_heading("1. Problem Statement & Examination Objectives", level=1)
    p = doc.add_paragraph(
        "An e-commerce enterprise requires an end-to-end Machine Learning system to predict whether customer purchases "
        "will be Returned or Not Returned based on product characteristics, price, discounts, delivery timelines, "
        "customer ratings, package damage, and return history. The company requires full automation of code validation, "
        "model testing, container packaging, and publishing to GitHub Container Registry (GHCR) upon repository push."
    )
    p = doc.add_paragraph("The assignment requires satisfying all 9 tasks:")
    tasks = [
        "Task 1: Load and preprocess e-commerce dataset (1,200 records), handling missing and invalid values, and categorical encoding.",
        "Task 2: Engineer meaningful domain features (discount percentage, delivery delay, customer return frequency).",
        "Task 3: Train at least two classification models and evaluate performance using standard classification metrics.",
        "Task 4: Develop FastAPI service serving the best model via /predict and /health endpoints.",
        "Task 5: Create a public GitHub repository containing code, model artifacts, configuration, and dependencies.",
        "Task 6: Implement an automated CI/CD pipeline using GitHub Actions (dependency install, syntax check, automated testing).",
        "Task 7: Build a Docker container image and publish to GitHub Container Registry (GHCR) after successful validation.",
        "Task 8: Modify application code or model configuration, push changes, and demonstrate automatic workflow triggering.",
        "Task 9: Verify workflow execution, inspect build logs, and demonstrate the updated application running from the new Docker image."
    ]
    for t in tasks:
        doc.add_paragraph(t, style='List Bullet')

    # 2. Tools Used
    doc.add_heading("2. Tools & Technologies Used", level=1)
    t_table = doc.add_table(rows=8, cols=2)
    t_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tools = [
        ("Layer / Component", "Technology / Framework Selected"),
        ("Programming Language", "Python 3.11 / Python 3.13"),
        ("Data Cleaning & Features", "pandas 2.2+, NumPy 1.26+, scikit-learn ColumnTransformer"),
        ("Machine Learning Models", "Logistic Regression (Balanced), Random Forest Classifier, Gradient Boosting"),
        ("Model Serving Framework", "FastAPI 0.110+, Uvicorn 0.28+, Pydantic v2"),
        ("Automated Testing", "pytest 8.0+, httpx TestClient (13 unit and integration tests)"),
        ("Containerization", "Docker Desktop, Docker Engine 29.8.1, Python 3.11-slim base image"),
        ("CI/CD & Container Registry", "GitHub Actions (Ubuntu-latest runner), GitHub Container Registry (GHCR)")
    ]
    for idx, (c1, c2) in enumerate(tools):
        cell1 = t_table.cell(idx, 0)
        cell2 = t_table.cell(idx, 1)
        cell1.width = Inches(2.5)
        cell2.width = Inches(4.3)
        set_cell_margins(cell1)
        set_cell_margins(cell2)
        if idx == 0:
            set_cell_background(cell1, "1A5276")
            set_cell_background(cell2, "1A5276")
            r1 = cell1.paragraphs[0].add_run(c1)
            r2 = cell2.paragraphs[0].add_run(c2)
            r1.font.bold = True
            r2.font.bold = True
            r1.font.color.rgb = RGBColor(255, 255, 255)
            r2.font.color.rgb = RGBColor(255, 255, 255)
        else:
            set_cell_background(cell1, "F2F4F4" if idx % 2 == 0 else "FFFFFF")
            set_cell_background(cell2, "F2F4F4" if idx % 2 == 0 else "FFFFFF")
            cell1.paragraphs[0].add_run(c1).font.bold = True
            cell2.paragraphs[0].add_run(c2)

    # 3. Data Cleansing & Feature Engineering
    doc.add_heading("3. Data Preprocessing & Feature Engineering", level=1)
    doc.add_paragraph(
        "1. Cleansing Invalid Values:\n"
        "   - Negative Prices: 3 records with prices <= 0 (e.g., -200 INR) converted to NaN and imputed with median.\n"
        "   - Out-of-Range Discounts: 2 records with discounts > 100% (e.g., 125%) converted to NaN and imputed with median.\n"
        "   - Customer Ratings: Clamped to valid range [1.0, 5.0].\n"
        "2. Imputing Missing Values:\n"
        "   - Numerical variables (Price, Discount, Rating) imputed via median.\n"
        "   - Actual_Delivery_Days imputed with Expected_Delivery_Days as operational baseline.\n"
        "   - Payment_Method imputed via mode ('Card').\n"
        "3. Feature Engineering:\n"
        "   - delivery_delay = Actual_Delivery_Days - Expected_Delivery_Days\n"
        "   - is_delayed = 1 if delivery_delay > 0 else 0\n"
        "   - customer_return_frequency = Previous_Returns / max(Previous_Orders, 1)\n"
        "   - effective_price = Product_Price_INR * (1 - Discount_Percent / 100)\n"
        "   - return_risk_score = 0.6 * (return_frequency > 0.25) + 0.4 * (damaged == 'Yes')"
    )

    # 4. Model Training & Evaluation
    doc.add_heading("4. Machine Learning Model Training & Evaluation Results", level=1)
    doc.add_paragraph(
        "Three classification pipelines were trained using stratified 80/20 train/test splits. "
        "Due to class imbalance in return data (~22.6% return rate), evaluation prioritized Recall, F1, and ROC-AUC:"
    )

    m_table = doc.add_table(rows=4, cols=6)
    m_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    m_data = [
        ("Model", "Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC"),
        ("Logistic Regression (Balanced)", "62.08%", "0.2874", "0.4630", "0.3546", "0.5772"),
        ("Random Forest Classifier", "72.50%", "0.3529", "0.2593", "0.2979", "0.5398"),
        ("Gradient Boosting Classifier", "74.58%", "0.2000", "0.0556", "0.0896", "0.5367")
    ]
    for idx, row in enumerate(m_data):
        for c_idx, val in enumerate(row):
            cell = m_table.cell(idx, c_idx)
            set_cell_margins(cell, 60, 60, 80, 80)
            if idx == 0:
                set_cell_background(cell, "1A5276")
                r = cell.paragraphs[0].add_run(val)
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
            else:
                set_cell_background(cell, "E8F8F5" if idx == 1 else ("F8F9F9" if idx % 2 == 0 else "FFFFFF"))
                r = cell.paragraphs[0].add_run(val)
                if idx == 1:
                    r.font.bold = True
                    r.font.color.rgb = RGBColor(17, 122, 101)

    doc.add_paragraph(
        "Winning Model Justification: Logistic Regression with Balanced Class Weights achieved the highest minority "
        "return Recall (46.30%), F1-Score (0.3546), and ROC-AUC (0.5772), effectively identifying high-risk returns."
    )

    # Evaluation Plots
    if os.path.exists("reports/confusion_matrix.png") and os.path.exists("reports/roc_curve.png"):
        img_table = doc.add_table(rows=1, cols=2)
        img_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        img_table.cell(0, 0).paragraphs[0].add_run().add_picture("reports/confusion_matrix.png", width=Inches(3.2))
        img_table.cell(0, 1).paragraphs[0].add_run().add_picture("reports/roc_curve.png", width=Inches(3.2))
        cap = doc.add_paragraph("Figure 1: Confusion Matrix and ROC Curve for the Production Model Pipeline")
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap.runs[0].font.italic = True
        cap.runs[0].font.size = Pt(9)

    # 5. FastAPI Application & Live Endpoints
    doc.add_heading("5. FastAPI Production Model Serving Application", level=1)
    doc.add_paragraph(
        "The model is served using FastAPI via high-throughput REST endpoints:\n"
        "• Public Swagger UI: https://deviant-controversy-scroll-input.trycloudflare.com/docs\n"
        "• Health Endpoint: https://deviant-controversy-scroll-input.trycloudflare.com/health\n"
        "• Inference Endpoint: https://deviant-controversy-scroll-input.trycloudflare.com/predict\n"
        "• Local Port: http://localhost:8000/docs"
    )

    # 6. CI/CD Pipeline & GitHub Actions
    doc.add_heading("6. Automated CI/CD Pipeline Implementation (GitHub Actions)", level=1)
    doc.add_paragraph(
        "A dual-stage pipeline was implemented in .github/workflows/ci-cd.yml:\n"
        "• Job 1 (ML CI): Automated code syntax check, training pipeline execution, MLOps Quality Gate verification, and 13 unit tests via pytest.\n"
        "• Job 2 (Continuous Delivery): Builds Docker container image, conducts in-CI live smoke testing on port 8000, and publishes the image to GitHub Container Registry (GHCR)."
    )

    # 7. Verification Screenshots Section
    doc.add_heading("7. System Execution Screenshots & Verification Evidence", level=1)
    doc.add_paragraph(
        "The following screenshots substantiate the complete execution across Docker, GitHub Actions, "
        "Swagger UI, and test validation:"
    )

    # Scan screenshots folder
    screenshot_files = sorted(glob.glob(os.path.join(SCREENSHOTS_DIR, "*.*")))
    embedded_count = 0

    for s_file in screenshot_files:
        if s_file.endswith("_norm.png"):
            continue
        fname = os.path.basename(s_file).lower()
        if "docker" in fname:
            caption = "Figure 2: Docker Desktop Container Dashboard showing Running Container and Username (bhanuteja33)"
        elif "swagger" in fname or "docs" in fname or "api" in fname:
            caption = "Figure 3: FastAPI Interactive Swagger UI Documentation and Live Parameter Testing"
        elif "action" in fname or "workflow" in fname or "github" in fname or "ci" in fname:
            caption = "Figure 4: GitHub Actions CI/CD Pipeline Execution with Green Status for Both Stages"
        elif "test" in fname or "pytest" in fname or "gate" in fname:
            caption = "Figure 5: Automated Test Suite (13 tests passed) and MLOps Quality Gate Verification"
        elif "ghcr" in fname or "package" in fname:
            caption = "Figure 6: GitHub Container Registry (GHCR) Package Dashboard"
        else:
            caption = f"Figure {embedded_count + 2}: Execution Verification Output - {os.path.basename(s_file)}"

        if add_image_box(doc, s_file, caption):
            embedded_count += 1

    # 8. Execution Instructions for Faculty
    doc.add_heading("8. Faculty Verification Guide & Execution Instructions", level=1)
    doc.add_paragraph(
        "1. Public Application URL: Visit https://deviant-controversy-scroll-input.trycloudflare.com/docs to test live predictions on Swagger UI.\n"
        "2. GitHub Repository: Access https://github.com/BhanuTeja33/ecommerce-return-prediction-ci-cd for code, models, and workflows.\n"
        "3. GitHub Actions Workflows: Inspect Run 42199797360 and Run 42200744814 at https://github.com/BhanuTeja33/ecommerce-return-prediction-ci-cd/actions.\n"
        "4. Pull Docker Image: Run 'docker pull ghcr.io/bhanuteja33/ecommerce-return-prediction:latest'.\n"
        "5. Run Local Container: Run 'docker run -d -p 8000:8000 ghcr.io/bhanuteja33/ecommerce-return-prediction:latest'.\n"
        "6. Run Test Suite: Run 'pytest -v' to execute all 13 unit, feature, and integration tests."
    )

    saved_path = None
    for target in [PRIMARY_DOCX, FALLBACK_DOCX]:
        try:
            doc.save(target)
            saved_path = target
            break
        except Exception as e:
            print(f"Could not save to {target}: {e}")

    print(f"Successfully generated {saved_path} with {embedded_count} embedded screenshot(s)!")


if __name__ == "__main__":
    build_document()
