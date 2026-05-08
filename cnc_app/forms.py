from django import forms
from .models import ToolLifecycleReport

class ToolLifecycleForm(forms.ModelForm):
    class Meta:
        model = ToolLifecycleReport
        fields = [
            "cell_no", "stage", "tool_no", "machine_number",
            "sap_code", "description", "make", "target_life",
            "actual_life", "reason_for_tool_change", "waiting",
            "count", "batch_no", "remarks",
        ]

        # Adding form-control to all widgets for a professional, uniform look
        widgets = {
            "description": forms.Textarea(attrs={"rows": 1, "class": "form-control"}),
            "actual_life": forms.NumberInput(attrs={"class": "form-control", "id": "id_actual_life"}),
            "waiting": forms.TextInput(attrs={"class": "form-control"}),
            "count": forms.NumberInput(attrs={"class": "form-control"}),
            "batch_no": forms.TextInput(attrs={"class": "form-control"}),
            "remarks": forms.Textarea(attrs={"rows": 1, "class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        target = cleaned_data.get("target_life")
        actual = cleaned_data.get("actual_life")
        reason = cleaned_data.get("reason_for_tool_change")

        if target and actual and actual < target and not reason:
            raise forms.ValidationError(
                "Reason required when actual life is less than target life."
            )
        return cleaned_data