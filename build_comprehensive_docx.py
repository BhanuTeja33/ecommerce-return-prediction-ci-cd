"""
Comprehensive Word Document Lab Report Generator for MLOps Internal Laboratory Examination.
Student: Velpuri Bhanu Teja (231FA04E85)
Question 4: E-Commerce Product Return Prediction System with Automated CI/CD
"""

import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
from PIL import Image

PRIMARY_DOCX = "231FA04E85_MLOps_Internal_Lab_Report.docx"
FINAL_DOCX = "231FA04E85_MLOps_Internal_Lab_Report_Final.docx"

NAVY_HEX = "1A5276"
BLUE_HEX = "2980B9"
LIGHT_BLUE_HEX = "EBF5FB"
LIGHT_GRAY_HEX = "F8F9F9"
BORDER_GRAY_HEX = "BDC3C7"
GREEN_HEX = "27AE60"
LIGHT_GREEN_HEX = "E8F8F5"

COLOR_NAVY = RGBColor(26, 82, 118)
COLOR_BLUE = RGBColor(41, 128, 185)
COLOR_DARK = RGBColor(44, 62, 80)
COLOR_MUTED = RGBColor(127, 140, 141)
COLOR_GREEN = RGBColor(39, 174, 96)


def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>'
    )
    tcPr.append(tcMar)


def add_callout(doc, text, title="NOTE"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = tbl.cell(0, 0)
    c.width = Inches(6.8)
    set_cell_background(c, LIGHT_BLUE_HEX)
    set_cell_margins(c, 120, 120, 160, 160)
    
    tcPr = c._element.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="{NAVY_HEX}"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    r_t = p.add_run(f"[{title}] ")
    r_t.font.name = "Calibri"
    r_t.font.size = Pt(10)
    r_t.font.bold = True
    r_t.font.color.rgb = COLOR_NAVY
    
    r_b = p.add_run(text)
    r_b.font.name = "Calibri"
    r_b.font.size = Pt(9.5)
    r_b.font.color.rgb = COLOR_DARK
    
    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_after = Pt(4)


def add_image_figure(doc, img_path, fig_title, width=Inches(6.2)):
    if not os.path.exists(img_path):
        print(f"Warning: Image file not found: {img_path}")
        return False

    # Ensure format compatibility via PIL
    safe_path = img_path
    if img_path.lower().endswith(('.jpg', '.jpeg')):
        safe_path = os.path.splitext(img_path)[0] + "_converted.png"
        try:
            with Image.open(img_path) as im:
                im.convert("RGB").save(safe_path, "PNG")
        except Exception as e:
            print(f"Conversion error: {e}")
            safe_path = img_path

    try:
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(10)
        p_img.paragraph_format.space_after = Pt(3)
        run_img = p_img.add_run()
        run_img.add_picture(safe_path, width=width)

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(12)
        run_cap = p_cap.add_run(fig_title)
        run_cap.font.name = "Calibri"
        run_cap.font.size = Pt(9.5)
        run_cap.font.bold = True
        run_cap.font.italic = True
        run_cap.font.color.rgb = COLOR_NAVY
        return True
    except Exception as e:
        print(f"Error embedding image {img_path}: {e}")
        return False


def build_lab_report():
    doc = docx.Document()

    # Configure Margins (0.75 in)
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    # -------------------------------------------------------------
    # DOCUMENT HEADER & TITLE
    # -------------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING\nARTIFICIAL INTELLIGENCE & MACHINE LEARNING")
    r_inst.font.name = "Calibri"
    r_inst.font.size = Pt(11)
    r_inst.font.bold = True
    r_inst.font.color.rgb = COLOR_MUTED

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(4)
    p_title.paragraph_format.space_after = Pt(2)
    r_title = p_title.add_run("MLOps INTERNAL LABORATORY EXAMINATION WORK")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(20)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_NAVY

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(10)
    r_sub = p_sub.add_run("Question 4: Develop and Automate an E-Commerce Product Return Prediction System using CI/CD")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(12)
    r_sub.font.bold = True
    r_sub.font.color.rgb = COLOR_BLUE

    # -------------------------------------------------------------
    # CANDIDATE & SUBMISSION METADATA TABLE
    # -------------------------------------------------------------
    meta_table = doc.add_table(rows=6, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Candidate Name", "VELPURI BHANU TEJA"),
        ("Register Number", "231FA04E85"),
        ("Course / Examination", "Machine Learning Operations (MLOps) Laboratory Internal"),
        ("Academic Section / Set", "Section 7 (Set 4, Question 4)"),
        ("GitHub Profile & Account", "https://github.com/BhanuTeja33 (Username: BhanuTeja33)"),
        ("Submission ZIP Archive", "231FA04E85_MLOps_Internal.zip")
    ]
    for idx, (label, val) in enumerate(meta_data):
        c1 = meta_table.cell(idx, 0)
        c2 = meta_table.cell(idx, 1)
        c1.width = Inches(2.2)
        c2.width = Inches(4.6)
        set_cell_margins(c1, 50, 50, 100, 100)
        set_cell_margins(c2, 50, 50, 100, 100)
        set_cell_background(c1, "F2F4F4")
        set_cell_background(c2, "FFFFFF")
        
        r1 = c1.paragraphs[0].add_run(label)
        r1.font.name = "Calibri"
        r1.font.size = Pt(9.5)
        r1.font.bold = True
        r1.font.color.rgb = COLOR_NAVY
        
        r2 = c2.paragraphs[0].add_run(val)
        r2.font.name = "Calibri"
        r2.font.size = Pt(9.5)
        if idx in (0, 1):
            r2.font.bold = True
            r2.font.color.rgb = COLOR_NAVY

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # 1. VERIFICATION DIRECTORY & LIVE LINKS
    # -------------------------------------------------------------
    h1 = doc.add_heading("1. Executive Summary & Faculty Verification Directory", level=1)
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(4)

    p_intro = doc.add_paragraph(
        "This laboratory project implements a complete, end-to-end, production-grade Machine Learning Operations (MLOps) "
        "system for predicting e-commerce product returns. The solution encompasses automated data validation, domain-specific "
        "feature engineering, multi-model benchmark evaluation, an asynchronous FastAPI model serving layer, automated testing "
        "via pytest with strict quality gates, Docker containerization, publication to GitHub Container Registry (GHCR), and "
        "dual-stage automated Continuous Integration / Continuous Deployment (CI/CD) pipelines powered by GitHub Actions. "
        "In accordance with examination guidelines, the application is deployed with a live HTTPS public URL accessible from any system."
    )
    p_intro.paragraph_format.line_spacing = 1.15

    link_table = doc.add_table(rows=6, cols=3)
    link_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    links = [
        ("Resource / Service", "Access URL / Target", "Faculty Verification Description"),
        ("Live Interactive Swagger UI", "https://deviant-controversy-scroll-input.trycloudflare.com/docs", "Public interactive API documentation & real-time inference testing"),
        ("Live Operational Health API", "https://deviant-controversy-scroll-input.trycloudflare.com/health", "Live operational readiness check & student verification"),
        ("GitHub Repository", "https://github.com/BhanuTeja33/ecommerce-return-prediction-ci-cd", "Complete source code, unit tests, models, and CI/CD workflows"),
        ("Published Docker Image (GHCR)", "ghcr.io/bhanuteja33/ecommerce-return-prediction:latest", "Production container image published to GitHub Container Registry"),
        ("GitHub Actions Pipeline Runs", "https://github.com/BhanuTeja33/ecommerce-return-prediction-ci-cd/actions", "Dual-stage CI/CD execution history and automated build logs")
    ]
    for idx, (col1, col2, col3) in enumerate(links):
        c1 = link_table.cell(idx, 0)
        c2 = link_table.cell(idx, 1)
        c3 = link_table.cell(idx, 2)
        c1.width = Inches(2.1)
        c2.width = Inches(2.8)
        c3.width = Inches(1.9)
        set_cell_margins(c1, 60, 60, 80, 80)
        set_cell_margins(c2, 60, 60, 80, 80)
        set_cell_margins(c3, 60, 60, 80, 80)
        if idx == 0:
            set_cell_background(c1, NAVY_HEX)
            set_cell_background(c2, NAVY_HEX)
            set_cell_background(c3, NAVY_HEX)
            for c, txt in zip([c1, c2, c3], [col1, col2, col3]):
                r = c.paragraphs[0].add_run(txt)
                r.font.name = "Calibri"
                r.font.size = Pt(9.5)
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
        else:
            set_cell_background(c1, LIGHT_GRAY_HEX if idx % 2 == 1 else "FFFFFF")
            set_cell_background(c2, LIGHT_GRAY_HEX if idx % 2 == 1 else "FFFFFF")
            set_cell_background(c3, LIGHT_GRAY_HEX if idx % 2 == 1 else "FFFFFF")
            r1 = c1.paragraphs[0].add_run(col1)
            r1.font.name = "Calibri"
            r1.font.size = Pt(9)
            r1.font.bold = True
            
            r2 = c2.paragraphs[0].add_run(col2)
            r2.font.name = "Consolas"
            r2.font.size = Pt(8.5)
            r2.font.color.rgb = COLOR_BLUE
            
            r3 = c3.paragraphs[0].add_run(col3)
            r3.font.name = "Calibri"
            r3.font.size = Pt(8.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # 2. PROBLEM STATEMENT & ARCHITECTURE
    # -------------------------------------------------------------
    h2 = doc.add_heading("2. Problem Statement & System Architecture", level=1)
    h2.paragraph_format.space_before = Pt(10)
    
    doc.add_paragraph(
        "In e-commerce logistics, reverse logistics and customer returns represent substantial operational costs. "
        "The objective of this project is to develop and operationalize an automated Machine Learning pipeline to predict "
        "whether an e-commerce order will be Returned or Not Returned based on product characteristics, pricing, delivery performance, "
        "and historical customer purchasing patterns, while establishing a robust CI/CD pipeline to automate testing, building, "
        "and container deployment whenever code modifications occur."
    )

    arch_text = (
        "+---------------------------------------------------------------------------------------------------------+\n"
        "|                                       END-TO-END MLOps ARCHITECTURE                                      |\n"
        "+---------------------------------------------------------------------------------------------------------+\n"
        "  1. DATA INGESTION & CLEANSING\n"
        "     Raw Dataset (1,200 rows) --> Negative Price Cleaning --> Discount Clamping --> Median/Mode Imputation\n"
        "                                               |\n"
        "  2. FEATURE ENGINEERING\n"
        "     delivery_delay | is_delayed | customer_return_frequency | effective_price | return_risk_score\n"
        "                                               |\n"
        "  3. MULTI-MODEL BENCHMARKING & QUALITY GATE\n"
        "     Logistic Regression (Balanced) vs. Random Forest vs. Gradient Boosting --> Quality Gate (ROC-AUC >= 0.50)\n"
        "                                               |\n"
        "  4. FASTAPI INFERENCE MICROSERVICE (v1.1.0)\n"
        "     GET /health | GET / | POST /predict (Single Order) | POST /predict/batch (Batch Ingestion)\n"
        "                                               |\n"
        "  5. CONTINUOUS INTEGRATION (GitHub Actions - Job 1: ML CI)\n"
        "     Code Checkout --> Python 3.11 Setup --> Pipeline Execution --> Quality Gate Check --> pytest (13 tests)\n"
        "                                               |\n"
        "  6. CONTINUOUS DELIVERY (GitHub Actions - Job 2: CD & GHCR Publishing)\n"
        "     Docker Build --> In-CI Container Smoke Test (port 8000) --> Publish to ghcr.io/bhanuteja33/...:latest\n"
        "                                               |\n"
        "  7. PRODUCTION DEPLOYMENT & VERIFICATION\n"
        "     Public Live HTTPS Endpoint (Cloudflare Tunnel) + Local Docker Container Execution\n"
        "+---------------------------------------------------------------------------------------------------------+"
    )
    p_arch = doc.add_paragraph()
    r_arch = p_arch.add_run(arch_text)
    r_arch.font.name = "Consolas"
    r_arch.font.size = Pt(7.5)
    p_arch.paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # 3. TOOLS & TECHNOLOGIES
    # -------------------------------------------------------------
    h3 = doc.add_heading("3. Tools and Technologies Utilized", level=1)
    t_table = doc.add_table(rows=7, cols=2)
    t_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tools_data = [
        ("Layer / Component", "Technology / Framework and Version"),
        ("Programming Language", "Python 3.11 / Python 3.13 (x64)"),
        ("Machine Learning & Data Processing", "scikit-learn 1.4+, pandas 2.2+, numpy 1.26+, joblib 1.3+"),
        ("API & Serving Framework", "FastAPI 0.110+, Uvicorn 0.28+, Pydantic v2"),
        ("Automated Testing Framework", "pytest 8.0+, httpx TestClient (13 automated test cases)"),
        ("Containerization Platform", "Docker Desktop, Docker Engine 29.8.1, Python 3.11-slim base image"),
        ("CI/CD & Container Registry", "GitHub Actions (Ubuntu-latest runner), GitHub Container Registry (GHCR)")
    ]
    for idx, (col1, col2) in enumerate(tools_data):
        c1 = t_table.cell(idx, 0)
        c2 = t_table.cell(idx, 1)
        c1.width = Inches(2.5)
        c2.width = Inches(4.3)
        set_cell_margins(c1, 50, 50, 80, 80)
        set_cell_margins(c2, 50, 50, 80, 80)
        if idx == 0:
            set_cell_background(c1, NAVY_HEX)
            set_cell_background(c2, NAVY_HEX)
            r1 = c1.paragraphs[0].add_run(col1)
            r2 = c2.paragraphs[0].add_run(col2)
            r1.font.bold = True
            r2.font.bold = True
            r1.font.color.rgb = RGBColor(255, 255, 255)
            r2.font.color.rgb = RGBColor(255, 255, 255)
        else:
            set_cell_background(c1, LIGHT_GRAY_HEX if idx % 2 == 1 else "FFFFFF")
            set_cell_background(c2, LIGHT_GRAY_HEX if idx % 2 == 1 else "FFFFFF")
            r1 = c1.paragraphs[0].add_run(col1)
            r1.font.bold = True
            r2 = c2.paragraphs[0].add_run(col2)
            r1.font.name = "Calibri"
            r2.font.name = "Calibri"
            r1.font.size = Pt(9)
            r2.font.size = Pt(9)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # 4. TASK 1: DATA PREPROCESSING & CLEANSING
    # -------------------------------------------------------------
    doc.add_heading("4. Task 1: Data Ingestion, Cleansing & Preprocessing", level=1)
    doc.add_paragraph(
        "The raw dataset consists of 1,200 purchase records with 14 attributes. Rigorous domain validation and cleaning "
        "were implemented in src/data_preprocessing.py:\n\n"
        "• Invalid Negative / Zero Prices: In e-commerce systems, product prices <= 0 represent database anomalies or refund bugs. "
        "Identified 3 negative price records (e.g. -200 INR) and set them to NaN, followed by median imputation (INR 2,246.72).\n"
        "• Out-of-Range Discounts: Identified 2 records with discounts > 100% (e.g. 125%), replaced with NaN and imputed with the median discount (15.0%).\n"
        "• Rating Clamping: Pre-order customer ratings were verified and clamped to the valid domain scale of [1.0, 5.0].\n"
        "• Actual Delivery Days Imputation: Orders with missing actual delivery days were imputed using Expected_Delivery_Days as the operational baseline.\n"
        "• Categorical Imputation & Encoding: Missing Payment_Method values were imputed using mode ('Card'). Nominal features "
        "(Product_Category, Payment_Method, Package_Size) were One-Hot Encoded, while binary flags (Damaged_Package_Flag, Promotion_Active) were mapped to binary integers {0, 1}."
    )

    # -------------------------------------------------------------
    # 5. TASK 2: FEATURE ENGINEERING
    # -------------------------------------------------------------
    doc.add_heading("5. Task 2: Domain-Driven Feature Engineering", level=1)
    doc.add_paragraph(
        "To empower classification models with predictive signals, five domain features were engineered in src/feature_engineering.py:"
    )
    
    feat_table = doc.add_table(rows=6, cols=3)
    feat_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    feat_info = [
        ("Feature Name", "Mathematical Formulation", "Business & Operational Rationale"),
        ("delivery_delay", "Actual_Delivery_Days - Expected_Delivery_Days", "Positive values indicate delayed delivery; severe delay strongly correlates with cancellation and return."),
        ("is_delayed", "1 if delivery_delay > 0 else 0", "Binary indicator isolating late shipments for direct linear weighting."),
        ("customer_return_frequency", "Previous_Returns / max(Previous_Orders, 1)", "Captures the customer's historical propensity to return items, normalized against order volume."),
        ("effective_price", "Product_Price_INR * (1 - Discount_Percent / 100)", "Represents the net transaction amount paid by the customer after promotional discount deductions."),
        ("return_risk_score", "0.6 * (return_freq > 0.25) + 0.4 * (damaged == 'Yes')", "Composite operational risk heuristic combining customer habit and package damage indicators.")
    ]
    for idx, (f_name, f_form, f_desc) in enumerate(feat_info):
        c1 = feat_table.cell(idx, 0)
        c2 = feat_table.cell(idx, 1)
        c3 = feat_table.cell(idx, 2)
        c1.width = Inches(1.8)
        c2.width = Inches(2.6)
        c3.width = Inches(2.4)
        set_cell_margins(c1, 50, 50, 80, 80)
        set_cell_margins(c2, 50, 50, 80, 80)
        set_cell_margins(c3, 50, 50, 80, 80)
        if idx == 0:
            set_cell_background(c1, NAVY_HEX)
            set_cell_background(c2, NAVY_HEX)
            set_cell_background(c3, NAVY_HEX)
            for c, txt in zip([c1, c2, c3], [f_name, f_form, f_desc]):
                r = c.paragraphs[0].add_run(txt)
                r.font.bold = True
                r.font.size = Pt(9.5)
                r.font.color.rgb = RGBColor(255, 255, 255)
        else:
            set_cell_background(c1, LIGHT_GRAY_HEX if idx % 2 == 1 else "FFFFFF")
            set_cell_background(c2, LIGHT_GRAY_HEX if idx % 2 == 1 else "FFFFFF")
            set_cell_background(c3, LIGHT_GRAY_HEX if idx % 2 == 1 else "FFFFFF")
            r1 = c1.paragraphs[0].add_run(f_name)
            r1.font.bold = True
            r1.font.name = "Consolas"
            r1.font.size = Pt(8.5)
            
            r2 = c2.paragraphs[0].add_run(f_form)
            r2.font.name = "Consolas"
            r2.font.size = Pt(8.5)
            r2.font.color.rgb = COLOR_NAVY
            
            r3 = c3.paragraphs[0].add_run(f_desc)
            r3.font.name = "Calibri"
            r3.font.size = Pt(8.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # 6. TASK 3: MULTI-MODEL ML BENCHMARK & EVALUATION
    # -------------------------------------------------------------
    doc.add_heading("6. Task 3: Machine Learning Model Benchmark & Selection", level=1)
    doc.add_paragraph(
        "Three distinct classification algorithms were implemented and trained using an 80/20 stratified train/test split. "
        "In real-world e-commerce return datasets, class distributions exhibit strong imbalance (~22.6% return rate; 929 Not Returned vs. 271 Returned). "
        "Standard unweighted models optimize trivial majority-class accuracy at the expense of nearly 0% minority recall. "
        "Consequently, evaluation prioritized minority Return Recall, F1-Score, and Area Under the ROC Curve (ROC-AUC):"
    )

    model_table = doc.add_table(rows=4, cols=6)
    model_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    m_benchmark = [
        ("Classification Algorithm", "Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC"),
        ("Logistic Regression (Balanced Weights)", "62.08%", "0.2874", "46.30%", "0.3546", "0.5772"),
        ("Random Forest Classifier (Balanced)", "72.50%", "0.3529", "25.93%", "0.2979", "0.5398"),
        ("Gradient Boosting Classifier", "74.58%", "0.2000", "05.56%", "0.0896", "0.5367")
    ]
    for idx, row in enumerate(m_benchmark):
        for c_idx, val in enumerate(row):
            c = model_table.cell(idx, c_idx)
            set_cell_margins(c, 50, 50, 70, 70)
            if idx == 0:
                set_cell_background(c, NAVY_HEX)
                r = c.paragraphs[0].add_run(val)
                r.font.bold = True
                r.font.size = Pt(9.5)
                r.font.color.rgb = RGBColor(255, 255, 255)
            else:
                set_cell_background(c, LIGHT_GREEN_HEX if idx == 1 else (LIGHT_GRAY_HEX if idx % 2 == 1 else "FFFFFF"))
                r = c.paragraphs[0].add_run(val)
                r.font.size = Pt(9)
                if idx == 1:
                    r.font.bold = True
                    r.font.color.rgb = COLOR_GREEN

    add_callout(
        doc,
        "PRODUCTION WINNER SELECTION: The Balanced Logistic Regression pipeline was selected as the production model. "
        "It achieved the highest Return Recall (46.30%), F1-Score (0.3546), and ROC-AUC (0.5772). Identifying 46.3% of true return "
        "risks enables the e-commerce company to proactively engage customers and prevent unnecessary shipping expenses, "
        "whereas unweighted Gradient Boosting caught only 5.56% of returns.",
        title="MODEL SELECTION RATIONALE"
    )

    # Embedding Evaluation Plots
    if os.path.exists("reports/confusion_matrix.png") and os.path.exists("reports/roc_curve.png"):
        doc.add_paragraph("Figure 1 illustrates the Confusion Matrix and ROC Curve generated by the model evaluation pipeline:")
        img_tbl = doc.add_table(rows=1, cols=2)
        img_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        img_tbl.cell(0, 0).paragraphs[0].add_run().add_picture("reports/confusion_matrix.png", width=Inches(3.2))
        img_tbl.cell(0, 1).paragraphs[0].add_run().add_picture("reports/roc_curve.png", width=Inches(3.2))
        p_c = doc.add_paragraph("Figure 1: Confusion Matrix and ROC-AUC Curve for Production Logistic Regression Model")
        p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c.runs[0].font.name = "Calibri"
        p_c.runs[0].font.size = Pt(9)
        p_c.runs[0].font.bold = True
        p_c.runs[0].font.italic = True
        p_c.runs[0].font.color.rgb = COLOR_NAVY

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # 7. TASK 4: FASTAPI APPLICATION ARCHITECTURE
    # -------------------------------------------------------------
    doc.add_heading("7. Task 4: FastAPI Model Serving Application", level=1)
    doc.add_paragraph(
        "The model is wrapped in a production FastAPI microservice (app.py) operating under an asynchronous lifespan architecture. "
        "It features Pydantic v2 data contract validation and returns explainable inference summaries:\n\n"
        "• GET /: Root service metadata, candidate identity, version, and routing index.\n"
        "• GET /health: Operational readiness check verifying that the model pipeline is loaded in memory.\n"
        "• POST /predict: Real-time single order prediction returning binary classification, probability, risk level (High, Moderate, Low), "
        "and human-readable return_reason_summary explaining factors like delivery delay and customer history.\n"
        "• POST /predict/batch: High-throughput batch inference accepting arrays of orders with aggregate batch statistics.\n"
        "• GET /docs & GET /redoc: Interactive Swagger UI and OpenAPI documentation."
    )

    # -------------------------------------------------------------
    # 8. TASK 5, 6, 7: CI/CD PIPELINE & GHCR DOCKERIZATION
    # -------------------------------------------------------------
    doc.add_heading("8. Tasks 5, 6 & 7: GitHub Repository, CI/CD Pipeline & GHCR Publishing", level=1)
    doc.add_paragraph(
        "A dual-stage CI/CD pipeline was implemented using GitHub Actions in .github/workflows/ci-cd.yml and pushed to GitHub: "
        "https://github.com/BhanuTeja33/ecommerce-return-prediction-ci-cd\n\n"
        "1. Job 1: ML CI - Validate, Train, Quality Gate & Test (Runs on Ubuntu-latest):\n"
        "   - Checks out repository source code and provisions Python 3.11 with pip caching.\n"
        "   - Performs static syntax and compilation validation.\n"
        "   - Executes train_model.py, building the preprocessor, feature transformer, and serialized model artifact.\n"
        "   - Runs quality_gate.py, enforcing automated checks (ROC-AUC >= 0.50, Accuracy >= 0.55, smoke test validation).\n"
        "   - Executes pytest -v across 13 unit and integration tests (tests/test_preprocessing.py, tests/test_features.py, tests/test_model.py, tests/test_api.py).\n"
        "   - Preserves artifacts (models/, metrics.json, reports/) across workflow jobs.\n\n"
        "2. Job 2: Continuous Delivery & Container Registry Publishing:\n"
        "   - Downloads validated model artifacts from Job 1.\n"
        "   - Builds the production Docker image using Dockerfile.\n"
        "   - Shift-Left In-CI Smoke Testing: Launches container on port 8000 inside the CI runner, queries /health and /predict, and verifies live responses.\n"
        "   - Authenticates to GitHub Container Registry using GITHUB_TOKEN and publishes ghcr.io/bhanuteja33/ecommerce-return-prediction:latest."
    )

    # -------------------------------------------------------------
    # 9. TASK 8 & 9: CODE MODIFICATION & AUTOMATIC TRIGGER DEMO
    # -------------------------------------------------------------
    doc.add_heading("9. Tasks 8 & 9: Code Modification, Automatic CI/CD Trigger & Container Verification", level=1)
    doc.add_paragraph(
        "To satisfy Tasks 8 and 9, the application was upgraded to version 1.1.0 with explainable return reason analysis. "
        "The code was committed and pushed to the main branch:\n\n"
        "1. Automatic Workflow Trigger: GitHub Actions immediately recognized the push event and automatically triggered Workflow Run 42199797360 and Run 42208434215.\n"
        "2. Build Logs Inspection: Both Job 1 (ML CI) and Job 2 (Docker Build & Publish) executed cleanly to completion (SUCCESS) within 1m 35s.\n"
        "3. Live Execution from Newly Built Image: The updated image was pulled and launched locally via Docker:\n"
        "   docker pull ghcr.io/bhanuteja33/ecommerce-return-prediction:latest\n"
        "   docker run -d -p 8000:8000 ghcr.io/bhanuteja33/ecommerce-return-prediction:latest\n"
        "   The health check confirmed operational status with version 1.1.0 and candidate identification: Velpuri Bhanu Teja (231FA04E85)."
    )

    # -------------------------------------------------------------
    # 10. VERIFICATION SCREENSHOTS (ALL 8 FIGURES EMBEDDED)
    # -------------------------------------------------------------
    doc.add_heading("10. System Execution Screenshots and Visual Verification", level=1)
    doc.add_paragraph(
        "The following figures provide comprehensive verification evidence demonstrating successful execution across "
        "FastAPI Swagger UI, GitHub Repository, Live Health Check, PowerShell Docker Execution, GitHub Actions CI/CD runs, and Docker Desktop:"
    )

    screenshots_to_embed = [
        ("screenshots/fig01_swagger_ui_overview.png", "Figure 2: Interactive FastAPI Swagger UI (/docs) showing API endpoints, schemas, and live parameter execution interface"),
        ("screenshots/fig02_github_repository.png", "Figure 3: GitHub Repository (BhanuTeja33/ecommerce-return-prediction-ci-cd) showing complete project structure and GHCR packages"),
        ("screenshots/fig03_api_health_check.png", "Figure 4: FastAPI Operational Health Check (/health) showing model status, version 1.1.0, and Candidate Name/Register Number"),
        ("screenshots/fig04_docker_terminal_pull_run.png", "Figure 5: Windows PowerShell Terminal showing docker pull and run execution from ghcr.io/bhanuteja33/ecommerce-return-prediction:latest"),
        ("screenshots/fig05_github_actions_workflow_run.png", "Figure 6: GitHub Actions Workflow Run #5 Details showing successful completion of both ML CI and CD jobs with summary table"),
        ("screenshots/fig06_github_actions_build_details.png", "Figure 7: GitHub Actions Workflow Run #3 Build Details demonstrating automated testing, smoke tests, and GHCR container push"),
        ("screenshots/fig07_github_actions_runs_list.png", "Figure 8: GitHub Actions Workflow Run History showing consecutive successful (green) CI/CD pipeline executions on main branch"),
        ("screenshots/fig08_docker_desktop_account.png", "Figure 9: Docker Desktop Container Dashboard showing container status and verified personal account (bhanuteja33)"),
        ("screenshots/04_pytest_results.png", "Figure 10: Automated Testing Suite Execution showing 13/13 unit and integration tests passing with MLOps Quality Gate verification")
    ]

    fig_count = 0
    for path, caption in screenshots_to_embed:
        if add_image_figure(doc, path, caption, width=Inches(6.2)):
            fig_count += 1

    # -------------------------------------------------------------
    # 11. FACULTY VERIFICATION & REPRODUCIBILITY GUIDE
    # -------------------------------------------------------------
    doc.add_heading("11. Faculty Verification Guide & Execution Instructions", level=1)
    doc.add_paragraph(
        "Faculty can verify this project through any of the three standardized approaches below:\n\n"
        "A. Live Public HTTPS Application Testing (Zero Installation Required):\n"
        "1. Open any browser and navigate to: https://deviant-controversy-scroll-input.trycloudflare.com/docs\n"
        "2. Click on 'POST /predict' -> 'Try it out' -> 'Execute' to perform real-time model inference.\n"
        "3. Navigate to https://deviant-controversy-scroll-input.trycloudflare.com/health to verify service status and candidate identification.\n\n"
        "B. Run Deployed Container Image via Docker:\n"
        "1. Pull published image: docker pull ghcr.io/bhanuteja33/ecommerce-return-prediction:latest\n"
        "2. Launch container: docker run -d --name return-api -p 8000:8000 ghcr.io/bhanuteja33/ecommerce-return-prediction:latest\n"
        "3. Access local interface at: http://localhost:8000/docs\n\n"
        "C. Run Complete Pipeline Locally from Source:\n"
        "1. Unzip 231FA04E85_MLOps_Internal.zip and navigate into the project directory.\n"
        "2. Install requirements: pip install -r requirements.txt\n"
        "3. Execute training pipeline: python train_model.py\n"
        "4. Validate quality gate: python quality_gate.py\n"
        "5. Run full test suite: pytest -v\n"
        "6. Start FastAPI service: uvicorn app:app --host 0.0.0.0 --port 8000 --reload"
    )

    # -------------------------------------------------------------
    # 12. CONCLUSION
    # -------------------------------------------------------------
    doc.add_heading("12. Conclusion & Summary of Deliverables", level=1)
    doc.add_paragraph(
        "All requirements specified for Question 4 of the MLOps Internal Laboratory Examination were successfully accomplished:\n\n"
        "✓ Domain data preprocessing handled negative prices, out-of-range discounts, and missing delivery timelines.\n"
        "✓ Feature engineering captured delivery delay, return frequency, and composite return risk heuristics.\n"
        "✓ Multi-model benchmarking selected Balanced Logistic Regression achieving 46.30% return recall and 0.5772 ROC-AUC.\n"
        "✓ Production FastAPI service deployed with real-time inference, batch prediction, and health monitoring.\n"
        "✓ Automated CI/CD pipeline in GitHub Actions tested, validated, built, and published container images to GHCR.\n"
        "✓ Automated workflow trigger demonstrated upon code upgrade to v1.1.0 with verified build logs.\n"
        "✓ Deployed with live, publicly accessible HTTPS links and packaged as 231FA04E85_MLOps_Internal.zip."
    )

    # Save document
    saved_doc = None
    for target in [PRIMARY_DOCX, FINAL_DOCX]:
        try:
            doc.save(target)
            saved_doc = target
            print(f"Successfully saved document to: {target}")
            break
        except Exception as e:
            print(f"Notice: Could not write directly to {target} (likely open in Word): {e}")

    if not saved_doc:
        doc.save(FINAL_DOCX)
        saved_doc = FINAL_DOCX
        print(f"Saved document to fallback: {FINAL_DOCX}")

    print(f"Total figures embedded: {fig_count}")
    return saved_doc


if __name__ == "__main__":
    build_lab_report()
