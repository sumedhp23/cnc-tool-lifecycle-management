from django.db import models


class ToolLifecycleReport(models.Model):

    # Auto fields
    serial_no = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    shift = models.CharField(max_length=1)

    # Dropdown fields
    cell_no = models.CharField(max_length=50)
    stage = models.CharField(max_length=50)
    tool_no = models.CharField(max_length=10)
    machine_number = models.CharField(max_length=50)
    stage_tool = models.CharField(max_length=100)

    sap_code = models.CharField(max_length=100)

    # Text fields
    description = models.TextField(blank=True, null=True)

    make = models.CharField(max_length=100)

    # Lifecycle
    target_life = models.IntegerField()
    actual_life = models.IntegerField()

    reason_for_tool_change = models.CharField(max_length=200, blank=True, null=True)

    waiting = models.IntegerField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)

    life_achieved_percent = models.FloatField(blank=True, null=True)

    batch_no = models.CharField(max_length=100)

    remarks = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):

        # Auto Stage_Tool
        self.stage_tool = f"{self.stage}_{self.tool_no}"

        # Auto Life %
        if self.target_life and self.actual_life:
            self.life_achieved_percent = (
                self.actual_life / self.target_life
            ) * 100

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.stage_tool} - {self.date}"


# KEEP THESE UNCHANGED

FIELD_TYPES = [
    ("text", "Text"),
    ("number", "Number"),
    ("alphanumeric", "Alphanumeric"),
    ("dropdown", "Dropdown"),
]

class DynamicField(models.Model):
    field_name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    is_required = models.BooleanField(default=False)

    def __str__(self):
        return self.field_name


class FieldOption(models.Model):
    field = models.ForeignKey(DynamicField, on_delete=models.CASCADE)
    option = models.CharField(max_length=100)
    def __str__(self): return self.option


class FormSubmission(models.Model):
    report = models.ForeignKey(ToolLifecycleReport, on_delete=models.CASCADE)
    field = models.ForeignKey(DynamicField, on_delete=models.CASCADE)
    value = models.CharField(max_length=200)