from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ToolLifecycleForm
from .models import DynamicField, FormSubmission, ToolLifecycleReport
import pandas as pd
from datetime import datetime
from django.contrib import messages
import json
import openpyxl
from io import BytesIO
from django.utils import timezone


def lifecycle_form(request):

    dynamic_fields = DynamicField.objects.all()

    if request.method == "POST":
        form = ToolLifecycleForm(request.POST)

        if form.is_valid():

            report = form.save(commit=False)

            # Shift logic
            hour = datetime.now().hour
            if 6 <= hour < 14:
                report.shift = "A"
            elif 14 <= hour < 22:
                report.shift = "B"
            else:
                report.shift = "C"

            # Target life mapping
            tool_map = {
                "T01": 1000, "T02": 1200, "T03": 900, "T04": 1500,
                "T05": 1100, "T06": 1300, "T07": 1250,
                "T08": 1400, "T09": 1600, "T10": 1700,
            }

            if report.tool_no in tool_map:
                report.target_life = tool_map[report.tool_no]

            if report.actual_life < report.target_life:
                reason = request.POST.get("reason_for_tool_change")
                if not reason:
                    form.add_error("reason_for_tool_change", "Required when Actual Life < Target Life")
                    return render(request, "lifecycle_form.html", {
                        "form": form,
                        "dynamic_fields": dynamic_fields
                    })

            required_fields = [
                report.cell_no,
                report.stage,
                report.tool_no,
                report.machine_number,
                report.sap_code,
                report.make,
                report.actual_life,
                report.batch_no,
            ]

            if any(field in [None, ""] for field in required_fields):
                form.add_error(None, "Please fill all required fields")
                return render(request, "lifecycle_form.html", {
                    "form": form,
                    "dynamic_fields": dynamic_fields
                })

            report.save()

            # Save dynamic fields
            for field in dynamic_fields:
                val = request.POST.get(field.field_name)

                # Required validation
                if field.is_required and not val:
                    form.add_error(None, f"{field.field_name} is required")
                    return render(request, "lifecycle_form.html", {
                        "form": form,
                        "dynamic_fields": dynamic_fields
                    })

                if val:
                    FormSubmission.objects.create(
                        report=report,
                        field=field,
                        value=val
                    )

            return redirect("success")

    else:
        form = ToolLifecycleForm()

    return render(request, "lifecycle_form.html", {
        "form": form,
        "dynamic_fields": dynamic_fields
    })


def success_page(request):
    return render(request, "success.html")


# =========================
# ADMIN REPORTS DASHBOARD
# =========================
def reports_table(request):

    reports = ToolLifecycleReport.objects.all().order_by("-date","-serial_no")
    dynamic_fields = DynamicField.objects.all()

    return render(
        request,
        "reports_table.html",
        {
            "reports": reports,
            "dynamic_fields": dynamic_fields
        }
    )


# =========================
# EXCEL EXPORT
# =========================
def export_reports_excel(request):

    reports = ToolLifecycleReport.objects.all().order_by("-date","-serial_no")
    dynamic_fields = DynamicField.objects.all()

    data = []

    for report in reports:

        local_dt = timezone.localtime(report.date) if report.date else None
        naive_dt = local_dt.replace(tzinfo=None) if local_dt else None

        row = {
            "Serial No": report.serial_no,
            "Date": naive_dt,
            "Shift": report.shift,
            "Cell No": report.cell_no,
            "Stage": report.stage,
            "Tool No": report.tool_no,
            "Machine Number": report.machine_number,
            "Stage_Tool": report.stage_tool,
            "SAP Code": report.sap_code,
            "Description": report.description,
            "Make": report.make,
            "Target Life": report.target_life,
            "Actual Life": report.actual_life,
            "Reason for Tool Change": report.reason_for_tool_change,
        }

        # Dynamic fields
        for field in dynamic_fields:
            row[field.field_name] = ""

        submissions = FormSubmission.objects.filter(report=report)

        for s in submissions:
            row[s.field.field_name] = s.value

        # Remaining fields
        row.update({
            "Waiting": report.waiting,
            "Count": report.count,
            "Life Achieved %": report.life_achieved_percent,
            "Batch No": report.batch_no,
            "Remarks": report.remarks,
        })

        data.append(row)

    df = pd.DataFrame(data)

    filename = f"CNC_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    df.to_excel(response, index=False)

    return response


COLUMN_ALIASES = {
    "cell no": "Cell No",
    "cell": "Cell No",

    "stage": "Stage",

    "tool no": "Tool No",
    "tool": "Tool No",

    "machine number": "Machine Number",
    "machine no": "Machine Number",

    "sap code": "SAP Code",
    "sap": "SAP Code",

    "description": "Description",
    "make": "Make",

    "actual life": "Actual Life",

    "reason for tool change": "Reason for Tool Change",
    "reason": "Reason for Tool Change",

    "waiting": "Waiting",
    "count": "Count",

    "batch no": "Batch No",
    "batch": "Batch No",

    "remarks": "Remarks",
}

REQUIRED_COLUMNS = [
    "Cell No", "Stage", "Tool No", "Machine Number",
    "SAP Code", "Description", "Make",
    "Actual Life", "Reason for Tool Change",
    "Waiting", "Count", "Batch No", "Remarks"
]


def upload_excel(request):

    if request.method == "POST":

        # ===== BYPASS CASE =====
        if request.POST.get("bypass") == "true":
            request.session["bypass"] = True
            return redirect("confirm_upload")

        file = request.FILES.get("file")

        if not file:
            messages.error(request, "No file uploaded")
            return redirect("upload_excel")

        try:
            df = pd.read_excel(file)
            for col in df.columns:
                if "date" in col.lower():
                    df[col] = df[col].astype(str)
                    df[col] = df[col].replace(["NaT", "nan", "None"], None)

            df = normalize_columns(df)
            df = normalize_values(df)
        except Exception:
            messages.error(request, "Invalid Excel file")
            return redirect("upload_excel")

        request.session["excel_data"] = df.to_json(orient="records")

        # ===== VALIDATION =====
        missing_columns = []

        for col in REQUIRED_COLUMNS:
            if col not in df.columns:
                missing_columns.append(col)

        # If missing → show warning page
        if missing_columns:
            return render(request, "excel_missing.html", {
                "missing_columns": missing_columns
            })

        # Otherwise go to preview
        preview = df.head(20).to_dict(orient="records")

        return render(request, "excel_preview.html", {
            "preview": preview
        })

    return render(request, "upload_excel.html")


def confirm_upload(request):

    data_json = request.session.get("excel_data")
    bypass = request.session.get("bypass", False)

    if not data_json:
        return redirect("upload_excel")

    data = json.loads(data_json)
    df = pd.DataFrame(data)

    dynamic_fields = DynamicField.objects.all()

    tool_map = {
        "T01": 1000, "T02": 1200, "T03": 900, "T04": 1500,
        "T05": 1100, "T06": 1300, "T07": 1250,
        "T08": 1400, "T09": 1600, "T10": 1700,
    }

    error_rows = []

    for index, row in df.iterrows():

        try:

            tool = row.get("Tool No")

            if not tool:
                raise ValueError("Missing Tool No")

            raw_date = row.get("DATE") or row.get("Date")
            parsed_date = None

            if raw_date and str(raw_date).lower() not in ["nan", "nat", "none"]:
                try:
                    parsed_date = pd.to_datetime(raw_date, unit='ms')
                except:
                    parsed_date = pd.to_datetime(raw_date)

            # Duplicate check
            existing = ToolLifecycleReport.objects.filter(
                cell_no=row.get("Cell No"),
                stage=row.get("Stage"),
                tool_no=tool,
                machine_number=row.get("Machine Number"),
                batch_no=row.get("Batch No"),
            )

            if parsed_date:
                existing = existing.filter(date__date=parsed_date.date())

            if existing.exists():
                continue

            report = ToolLifecycleReport.objects.create(
                shift=calculate_shift(),
                cell_no=row.get("Cell No"),
                stage=row.get("Stage"),
                tool_no=tool,
                machine_number=row.get("Machine Number"),
                sap_code=row.get("SAP Code"),
                description=row.get("Description"),
                make=row.get("Make"),
                target_life=tool_map.get(tool),
                actual_life=row.get("Actual Life"),
                reason_for_tool_change=row.get("Reason for Tool Change"),
                waiting=row.get("Waiting"),
                count=row.get("Count"),
                batch_no=row.get("Batch No"),
                remarks=row.get("Remarks"),
            )

            if parsed_date:
                report.date = parsed_date
                report.save()

            # Dynamic fields
            for field in dynamic_fields:
                if field.field_name in df.columns:
                    val = row.get(field.field_name)
                    if val:
                        FormSubmission.objects.create(
                            report=report,
                            field=field,
                            value=str(val)
                        )

        except Exception as e:

            error_row = row.to_dict()
            error_row["Error"] = str(e)
            error_rows.append(error_row)

            if not bypass:
                continue

    # =========================
    # RETURN ERROR FILE IF ANY
    # =========================
    if error_rows:

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Errors"

        headers = list(error_rows[0].keys())
        ws.append(headers)

        for row in error_rows:
            ws.append([row.get(h) for h in headers])

        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        response = HttpResponse(
            buffer,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename=error_report.xlsx'

        return response

    # cleanup
    request.session.pop("excel_data", None)
    request.session.pop("bypass", None)

    return redirect("reports_table")


def calculate_shift():
    hour = datetime.now().hour
    if 6 <= hour < 14:
        return "A"
    elif 14 <= hour < 22:
        return "B"
    return "C"

def normalize_columns(df):

    normalized_columns = {}

    for col in df.columns:
        clean_col = col.strip().lower()

        # Replace underscores & extra spaces
        clean_col = clean_col.replace("_", " ")

        if clean_col in COLUMN_ALIASES:
            normalized_columns[col] = COLUMN_ALIASES[clean_col]
        else:
            normalized_columns[col] = col  # keep as is (dynamic fields)

    df = df.rename(columns=normalized_columns)

    return df

def normalize_values(df):

    if "Tool No" in df.columns:
        df["Tool No"] = df["Tool No"].astype(str).str.upper().str.strip()

    if "Stage" in df.columns:
        df["Stage"] = df["Stage"].astype(str).str.upper().str.strip()

    if "Cell No" in df.columns:
        df["Cell No"] = df["Cell No"].astype(str).str.strip()

    return df