"""
Script to generate the comprehensive MLOps Internal Lab Examination Report in DOCX format.
"""

import os
import json
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_report():
    doc = docx.Document()

    # Set page margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Document Header Title
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = title_p.add_run("MLOps INTERNAL LABORATORY EXAMINATION REPORT")
    run_title.font.name = "Calibri"
    run_title.font.size = Pt(22)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(26, 82, 118) # Deep Blue

    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = sub_p.add_run("Question 4: Develop and Automate an E-Commerce Product Return Prediction System using CI/CD")
    run_sub.font.name = "Calibri"
    run_sub.font.size = Pt(13)
    run_sub.font.bold = True
    run_sub.font.color.rgb = RGBColor(86, 101, 115)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Student Information Table
    student_table = doc.add_table(rows=6, cols=2)
    student_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    metadata = [
        ("Student Name", "Velpuri Bhanu Teja"),
        ("Register Number", "231FA04E85"),
        ("Class & Section", "B.Tech CSE - Section 7"),
        ("Faculty Evaluator", "Dr. Gabbi Reddy Keerthi"),
        ("GitHub Repository", "https://github.com/BhanuTeja33/ecommerce-return-prediction-ci-cd"),
        ("Published GHCR Image", "ghcr.io/bhanuteja33/ecommerce-return-prediction:latest")
    ]
    for idx, (label, val) in enumerate(metadata):
        cell_lbl = student_table.cell(idx, 0)
        cell_val = student_table.cell(idx, 1)
        cell_lbl.width = Inches(2.2)
        cell_val.width = Inches(4.6)
        
        set_cell_background(cell_lbl, "EBF5FB")
        set_cell_background(cell_val, "FAFAFA")
        set_cell_margins(cell_lbl, 80, 80, 120, 120)
        set_cell_margins(cell_val, 80, 80, 120, 120)
        
        p1 = cell_lbl.paragraphs[0]
        r1 = p1.add_run(label)
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = RGBColor(27, 79, 114)
        
        p2 = cell_val.paragraphs[0]
        r2 = p2.add_run(val)
        r2.font.size = Pt(10)
        if "http" in val:
            r2.font.bold = True
            r2.font.color.rgb = RGBColor(41, 128, 185)

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # Section 1: Problem Statement
    h1 = doc.add_heading("1. Problem Statement & Objectives", level=1)
    p = doc.add_paragraph()
    p.add_run(
        "An e-commerce company wants to predict whether a purchased product is likely to be returned based on product category, "
        "price, discount percentage, delivery time, customer ratings, and previous return history. "
        "The company also aims to automate the testing, building, and deployment of its machine learning application "
        "whenever changes are introduced to the source code repository."
    )
    p = doc.add_paragraph()
    p.add_run("The end-to-end implementation satisfies the following examiner requirements:\n")
    requirements = [
        "Load the provided e-commerce dataset (1,200 records) and perform necessary preprocessing (handling missing values, invalid values, categorical encoding).",
        "Perform feature engineering by creating meaningful features: discount percentage, delivery delay, and customer return frequency.",
        "Train at least two machine learning classification models to predict whether a product will be Returned or Not Returned and evaluate performance.",
        "Develop a FastAPI application to serve the best-performing model through /predict and /health endpoints.",
        "Create a GitHub repository containing application code, trained model, dependencies, and configuration files.",
        "Implement an automated CI/CD pipeline using GitHub Actions (dependency installation, code validation, automated testing, application build).",
        "Configure pipeline to build a Docker image and publish to GitHub Container Registry (GHCR) after successful validation.",
        "Modify application code or model configuration, commit and push changes, and demonstrate automatic CI/CD workflow triggering.",
        "Verify successful execution of workflow, inspect build logs, and demonstrate the updated application running from the newly built Docker image."
    ]
    for r in requirements:
        doc.add_paragraph(r, style='List Bullet')

    # Section 2: Tools & Technologies Used
    h2 = doc.add_heading("2. Tools and Technologies Used", level=1)
    tools_table = doc.add_table(rows=8, cols=2)
    tools_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tools_data = [
        ("Component", "Technology / Framework"),
        ("Programming Language", "Python 3.11 / Python 3.13"),
        ("Data Preprocessing & Features", "pandas 2.2+, NumPy 1.26+, scikit-learn 1.4+"),
        ("Machine Learning Models", "Logistic Regression (Balanced), Random Forest Classifier, Gradient Boosting"),
        ("Model Serving API", "FastAPI 0.110+, Uvicorn 0.28+, Pydantic v2"),
        ("Automated Testing Framework", "pytest 8.0+, httpx TestClient"),
        ("Containerization", "Docker Engine 29.8.1, Docker Desktop, Multi-stage Linux Container"),
        ("CI/CD & Container Registry", "GitHub Actions (Ubuntu Runner), GitHub Container Registry (GHCR)")
    ]
    for idx, (c1, c2) in enumerate(tools_data):
        cell1 = tools_table.cell(idx, 0)
        cell2 = tools_table.cell(idx, 1)
        cell1.width = Inches(2.5)
        cell2.width = Inches(4.3)
        if idx == 0:
            set_cell_background(cell1, "1A5276")
            set_cell_background(cell2, "1A5276")
            cell1.paragraphs[0].add_run(c1).font.bold = True
            cell1.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            cell2.paragraphs[0].add_run(c2).font.bold = True
            cell2.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        else:
            set_cell_background(cell1, "F2F4F4" if idx % 2 == 0 else "FFFFFF")
            set_cell_background(cell2, "F2F4F4" if idx % 2 == 0 else "FFFFFF")
            cell1.paragraphs[0].add_run(c1).font.bold = True
            cell2.paragraphs[0].add_run(c2)
        set_cell_margins(cell1, 60, 60, 100, 100)
        set_cell_margins(cell2, 60, 60, 100, 100)

    # Section 3: Data Preprocessing & Feature Engineering
    doc.add_heading("3. Data Preprocessing & Feature Engineering", level=1)
    p = doc.add_paragraph()
    p.add_run(
        "The raw dataset contains 1,200 customer order records. Domain-specific data cleansing was applied to resolve anomalous "
        "and missing values identified during exploratory data analysis:"
    )
    doc.add_paragraph("Handling Invalid Values:", style='List Bullet')
    doc.add_paragraph("• Negative Prices: 3 records with negative prices (e.g. -200 INR) were replaced with NaN and imputed using median price.", style='List Bullet 2')
    doc.add_paragraph("• Out-of-Range Discounts: 2 records with discounts > 100% (e.g. 125%) were converted to NaN and imputed using median discount.", style='List Bullet 2')
    doc.add_paragraph("• Customer Ratings: Clamped between 1.0 and 5.0.", style='List Bullet 2')
    
    doc.add_paragraph("Missing Value Imputation:", style='List Bullet')
    doc.add_paragraph("• Product_Price_INR, Discount_Percent, Customer_Rating_PreOrder: Imputed with training set medians.", style='List Bullet 2')
    doc.add_paragraph("• Actual_Delivery_Days: Imputed using Expected_Delivery_Days as natural operational baseline.", style='List Bullet 2')
    doc.add_paragraph("• Payment_Method: Imputed using mode ('Card').", style='List Bullet 2')

    doc.add_paragraph("Engineered Domain Features:", style='List Bullet')
    doc.add_paragraph("1. delivery_delay = Actual_Delivery_Days - Expected_Delivery_Days (Captures logistics delay signal).", style='List Bullet 2')
    doc.add_paragraph("2. is_delayed = 1 if delivery_delay > 0 else 0 (Binary delay trigger).", style='List Bullet 2')
    doc.add_paragraph("3. customer_return_frequency = Previous_Returns / max(Previous_Orders, 1) (Historical return propensity).", style='List Bullet 2')
    doc.add_paragraph("4. effective_price = Product_Price_INR * (1 - Discount_Percent / 100) (Actual realized revenue per order).", style='List Bullet 2')
    doc.add_paragraph("5. return_risk_score = 0.6 * (return_frequency > 0.25) + 0.4 * (damaged_flag == 'Yes') (Composite risk indicator).", style='List Bullet 2')

    # Section 4: Model Training and Evaluation Results
    doc.add_heading("4. Machine Learning Model Training & Comparative Evaluation", level=1)
    p = doc.add_paragraph()
    p.add_run(
        "Three distinct classification algorithms were implemented, trained, and benchmarked on an 80/20 stratified split. "
        "Due to severe class imbalance in real-world returns (77.4% Not Returned vs 22.6% Returned), models were evaluated on "
        "Accuracy, Precision, Recall, F1-Score, and ROC-AUC:"
    )

    perf_table = doc.add_table(rows=4, cols=6)
    perf_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    perf_data = [
        ("Model", "Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC"),
        ("Logistic Regression (Balanced)", "62.08%", "0.2874", "0.4630", "0.3546", "0.5772"),
        ("Random Forest Classifier", "72.50%", "0.3529", "0.2593", "0.2979", "0.5398"),
        ("Gradient Boosting Classifier", "74.58%", "0.2000", "0.0556", "0.0896", "0.5367"),
    ]
    for idx, row in enumerate(perf_data):
        for c_idx, val in enumerate(row):
            cell = perf_table.cell(idx, c_idx)
            set_cell_margins(cell, 60, 60, 80, 80)
            if idx == 0:
                set_cell_background(cell, "1A5276")
                r = cell.paragraphs[0].add_run(val)
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
            else:
                bg = "E8F8F5" if idx == 1 else ("F8F9F9" if idx % 2 == 0 else "FFFFFF")
                set_cell_background(cell, bg)
                r = cell.paragraphs[0].add_run(val)
                if idx == 1:
                    r.font.bold = True
                    r.font.color.rgb = RGBColor(17, 122, 101)

    p_sel = doc.add_paragraph()
    p_sel.paragraph_format.space_before = Pt(8)
    r_sel = p_sel.add_run(
        "Winning Model Selection: Logistic Regression with Balanced Class Weights was selected as the production model. "
        "In product return prediction, false negatives (failing to identify an order that gets returned) are costly. "
        "The balanced pipeline achieved the highest minority class Recall (46.30%), F1-Score (0.3546), and ROC-AUC (0.5772)."
    )
    r_sel.font.italic = True

    # Embed Evaluation Plots
    if os.path.exists("reports/confusion_matrix.png") and os.path.exists("reports/roc_curve.png"):
        doc.add_paragraph().paragraph_format.space_before = Pt(6)
        img_table = doc.add_table(rows=1, cols=2)
        img_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        c1 = img_table.cell(0, 0)
        c2 = img_table.cell(0, 1)
        c1.paragraphs[0].add_run().add_picture("reports/confusion_matrix.png", width=Inches(3.2))
        c2.paragraphs[0].add_run().add_picture("reports/roc_curve.png", width=Inches(3.2))
        cap = doc.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rcap = cap.add_run("Figure 1: Confusion Matrix and Receiver Operating Characteristic (ROC) Curve of Selected Model")
        rcap.font.size = Pt(9)
        rcap.font.italic = True

    # Section 5: FastAPI Application
    doc.add_heading("5. FastAPI Production Model Serving Application", level=1)
    p = doc.add_paragraph()
    p.add_run(
        "A modular asynchronous REST API was built in app.py utilizing FastAPI, Pydantic data schemas, and CORS middleware. "
        "The application provides the following endpoints:"
    )
    api_items = [
        ("GET /", "Root service info, student metadata, version, and endpoints catalogue."),
        ("GET /health", "Health check endpoint returning service status, model readiness, and version."),
        ("POST /predict", "Single-order return prediction returning prediction label ('Returned' / 'Not Returned'), probability, risk tier ('High' / 'Medium' / 'Low'), delivery delay, customer return frequency, and human-readable reason summary."),
        ("POST /predict/batch", "Batch prediction endpoint for multi-order operational pipelines."),
        ("GET /docs", "Interactive OpenAPI Swagger UI for live parameter testing and validation.")
    ]
    for ep, desc in api_items:
        p_ep = doc.add_paragraph(style='List Bullet')
        r_ep = p_ep.add_run(ep + ": ")
        r_ep.font.bold = True
        p_ep.add_run(desc)

    # Section 6: CI/CD Pipeline & GitHub Actions
    doc.add_heading("6. Automated CI/CD Pipeline Implementation (GitHub Actions)", level=1)
    p = doc.add_paragraph()
    p.add_run(
        "A complete 2-stage automated pipeline was authored in .github/workflows/ci-cd.yml and executed on GitHub's Ubuntu runners:"
    )
    doc.add_paragraph("Stage 1 - ML CI (Continuous Integration):", style='List Bullet')
    doc.add_paragraph("• Code checkout and Python 3.11 environment configuration with pip caching.", style='List Bullet 2')
    doc.add_paragraph("• Dependency installation and syntax verification via py_compile.", style='List Bullet 2')
    doc.add_paragraph("• Automated model training and evaluation execution (python train_model.py).", style='List Bullet 2')
    doc.add_paragraph("• MLOps Quality Gate verification (quality_gate.py: artifact presence, accuracy >= 0.55, ROC-AUC >= 0.50).", style='List Bullet 2')
    doc.add_paragraph("• Automated unit and API testing using pytest (13 test cases passed).", style='List Bullet 2')
    doc.add_paragraph("• Artifact upload preserving models, reports, and metrics.", style='List Bullet 2')

    doc.add_paragraph("Stage 2 - Continuous Delivery & Containerization (GHCR):", style='List Bullet')
    doc.add_paragraph("• Automated login to GitHub Container Registry (ghcr.io) using secrets.GITHUB_TOKEN.", style='List Bullet 2')
    doc.add_paragraph("• Building Docker container image tagged with commit SHA and :latest.", style='List Bullet 2')
    doc.add_paragraph("• In-CI Shift-Left Smoke Testing: Starts container on port 8000, polls /health, and sends live POST /predict request via curl.", style='List Bullet 2')
    doc.add_paragraph("• Publishing verified container image to ghcr.io/bhanuteja33/ecommerce-return-prediction:latest.", style='List Bullet 2')
    doc.add_paragraph("• Emitting detailed step summary into GitHub Actions dashboard.", style='List Bullet 2')

    # Section 7: Verification & Demonstration of Updated Image
    doc.add_heading("7. Workflow Execution Verification & Docker Demonstration", level=1)
    p = doc.add_paragraph()
    p.add_run(
        "Demonstration of Code Change & Automatic Triggering (Task 8 & 9):\n"
        "1. The application code was upgraded to version 1.1.0, adding explainable return reasoning to inference responses.\n"
        "2. The change was committed (SHA: 1aa7a74) and pushed to GitHub main branch.\n"
        "3. GitHub Actions automatically triggered Workflow Run ID: 42199797360.\n"
        "4. Both Stage 1 (ML CI) and Stage 2 (Docker Build & Publish) passed completely.\n"
        "5. The Docker container was started locally on port 8000 from the newly built image (ghcr.io/bhanuteja33/ecommerce-return-prediction:latest) and responded with verified v1.1.0 predictions."
    )

    doc.add_paragraph("Sample Prediction Output from Running Container:", style='List Bullet')
    sample_json = (
        '{\n'
        '  "order_id": "ECOM00004",\n'
        '  "prediction": "Returned",\n'
        '  "predicted_class": 1,\n'
        '  "return_probability": 0.7474,\n'
        '  "risk_level": "High",\n'
        '  "delivery_delay_days": 3,\n'
        '  "customer_return_frequency": 0.3333,\n'
        '  "effective_price_inr": 17291.88,\n'
        '  "return_reason_summary": "Damaged package reported; Delivery delayed by 3 day(s); High historical return rate (33.3%)",\n'
        '  "model_name": "Logistic_Regression",\n'
        '  "model_version": "1.1.0",\n'
        '  "timestamp": "2026-11-06T10:08:11.964593"\n'
        '}'
    )
    p_code = doc.add_paragraph()
    r_code = p_code.add_run(sample_json)
    r_code.font.name = "Consolas"
    r_code.font.size = Pt(8.5)
    p_code.paragraph_format.left_indent = Inches(0.4)

    # Section 8: Faculty Verification Guide
    doc.add_heading("8. Faculty Verification Guide & Execution Instructions", level=1)
    instructions = [
        "Repository Access: Navigate to https://github.com/BhanuTeja33/ecommerce-return-prediction-ci-cd to view full source code, test suites, and workflows.",
        "CI/CD Workflow Verification: Access https://github.com/BhanuTeja33/ecommerce-return-prediction-ci-cd/actions to inspect Run 42199797360 and view green logs.",
        "Container Image Pull: Execute 'docker pull ghcr.io/bhanuteja33/ecommerce-return-prediction:latest' to fetch the published image from GHCR.",
        "Run Local Container: Run 'docker run -d -p 8000:8000 ghcr.io/bhanuteja33/ecommerce-return-prediction:latest'.",
        "Swagger Documentation: Open your browser to http://localhost:8000/docs to interactively execute test predictions on the Swagger UI.",
        "Execute Test Suite: Run 'pytest -v' to execute all 13 unit, feature, model, and API integration tests."
    ]
    for inst in instructions:
        doc.add_paragraph(inst, style='List Number')

    output_path = "231FA04E85_MLOps_Internal_Lab_Report.docx"
    doc.save(output_path)
    print(f"Generated {output_path} successfully!")

if __name__ == "__main__":
    create_report()
