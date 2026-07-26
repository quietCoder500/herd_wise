import csv
import io
import zipfile
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from apps.portal.models import AnimalGroup, Animal, RecordTemplate, LivestockRecord
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from zoneinfo import ZoneInfo  # Built-in in Python 3.9+
from django.utils import timezone

EASTERN_TZ = ZoneInfo("America/New_York")


def export_herd_weights_zip(request, template_slug, herd_slug):
    # Fetch the template and the herd (AnimalGroup)
    template = get_object_or_404(RecordTemplate, slug=template_slug)
    group = get_object_or_404(AnimalGroup, slug=herd_slug)

    # Create an in-memory buffer for the ZIP
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        # Fetch all animals belonging to this group
        animals = Animal.objects.filter(group=group)

        for animal in animals:
            # LivestockRecord uses report_link which is a FK to ReportableModel.
            # Because Animal inherits from ReportableModel, they share the same ID.
            records = LivestockRecord.objects.filter(
                report_link_id=animal.id,  # type: ignore
                template=template,
            ).order_by("created_at")

            if not records.exists():
                continue

            # Buffer for this specific animal's CSV
            csv_buffer = io.StringIO()
            writer = csv.writer(csv_buffer)

            # Write CSV Headers
            writer.writerow(["Record ID", "Date Recorded", "Weight", "ADG (per day)"])

            prev_record = None
            for record in records:
                daily_gain = ""

                # IMPORTANT: Adjust "weight" to match the actual key in your JSON schema
                current_weight = float(record.data.get("weight", 0.0))

                if prev_record:
                    prev_weight = float(prev_record.data.get("weight", 0.0))

                    # Calculate time difference in days using total_seconds
                    # (Prevents DivisionByZero if weighed twice in one day)
                    time_diff = record.created_at - prev_record.created_at
                    days_diff = time_diff.total_seconds() / 86400.0

                    weight_diff = current_weight - prev_weight

                    if days_diff > 0:
                        adg = weight_diff / days_diff
                        daily_gain = round(adg, 3)
                    else:
                        daily_gain = 0.0

                writer.writerow(
                    [
                        record.public_id,
                        record.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        current_weight,
                        daily_gain,
                    ]
                )

                prev_record = record

            # Add the CSV to the zip file using a safe filename
            safe_name = "".join(
                c for c in animal.formatted_name if c.isalnum() or c in (" ", "-", "_")
            ).strip()
            filename = f"animal_{animal.id}_{safe_name}.csv"  # type: ignore
            zip_file.writestr(filename, csv_buffer.getvalue())

    # Rewind the buffer
    zip_buffer.seek(0)

    # Return the ZIP file as a download
    response = HttpResponse(zip_buffer.getvalue(), content_type="application/zip")
    response["Content-Disposition"] = (
        f'attachment; filename="{group.slug}_{template.slug}_export.zip"'
    )

    return response


def export_herd_weights_pdf(request, template_slug, herd_slug):
    """Exports a multi-page PDF containing weight tables for each animal."""
    template = get_object_or_404(RecordTemplate, slug=template_slug)
    group = get_object_or_404(AnimalGroup, slug=herd_slug)
    animals = Animal.objects.filter(group=group)

    birds_data = []

    for animal in animals:
        records = LivestockRecord.objects.filter(
            report_link_id=animal.id,  # type: ignore
            template=template,  # type: ignore
        ).order_by("created_at")

        if not records.exists():
            continue

        bird_rows = []
        prev_record = None

        for record in records:
            current_weight = float(record.data.get("weight", 0.0))
            daily_gain = 0.0

            if prev_record:
                prev_weight = float(prev_record.data.get("weight", 0.0))
                time_diff = record.created_at - prev_record.created_at
                days_diff = time_diff.total_seconds() / 86400.0

                if days_diff > 0:
                    daily_gain = round((current_weight - prev_weight) / days_diff, 3)

            est_created_at = timezone.localtime(record.created_at, EASTERN_TZ)
            bird_rows.append(
                {
                    "record_id": record.public_id,
                    "date": est_created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "weight": current_weight,
                    "adg": daily_gain,
                }
            )

            prev_record = record

        birds_data.append({"animal": animal, "rows": bird_rows})

    context = {"group": group, "template": template, "birds_data": birds_data}

    # Render HTML string
    html_string = render_to_string("export_templates/pdf_herd_weights.html", context)

    # Create an in-memory buffer for the PDF
    pdf_buffer = io.BytesIO()

    # Generate the PDF
    pisa_status = pisa.CreatePDF(html_string, dest=pdf_buffer)

    # Check for errors
    if pisa_status.err:  # type: ignore
        return HttpResponse("We had some errors <pre>" + html_string + "</pre>")

    # Reposition buffer to the beginning
    pdf_buffer.seek(0)

    # Serve the PDF
    response = HttpResponse(pdf_buffer, content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="{group.slug}_{template.slug}_pdf_export.pdf"'
    )

    return response
