from django import forms


#
#   Search
#
class GlobalSearchForm(forms.Form):
    search_query = forms.CharField()


#
# Records
#


# Add a record
class DynamicRecordForm(forms.Form):
    def __init__(self, *args, **kwargs) -> None:
        self.template = kwargs.pop("template", None)
        self.model_options = kwargs.pop("model_options", None)
        super().__init__(*args, **kwargs)
        if self.template and self.template.schema and self.model_options:
            # add initial link model
            self.fields["report_link"] = forms.ModelChoiceField(
                self.model_options, required=True
            )

            for field_def in self.template.schema:
                field_name = field_def["name"]
                field_label = field_def["label"]
                field_type = field_def["type"]
                field_required = field_def.get("required", False)

                if field_type == "number":
                    self.fields[field_name] = forms.FloatField(
                        label=field_label, required=field_required
                    )
                elif field_type == "date":
                    self.fields[field_name] = forms.DateField(
                        label=field_label,
                        required=field_required,
                        widget=forms.DateInput(attrs={"type": "date"}),
                    )
                elif field_type == "boolean":
                    self.fields[field_name] = forms.BooleanField(
                        label=field_label, required=field_required
                    )
                elif field_type == "char":
                    self.fields[field_name] = forms.CharField(
                        label=field_label, required=field_required, max_length=255
                    )
                elif field_type == "text":
                    self.fields[field_name] = forms.CharField(
                        label=field_label,
                        required=field_required,
                        widget=forms.Textarea,
                        max_length=1000,
                    )
                else:
                    raise ValueError(
                        f"Dynamic Record Form generation encountered unknown field_type {str(field_type)}"
                    )


class SchemaFieldForm(forms.Form):
    label = forms.CharField(max_length=100)
    name = forms.CharField(max_length=100)
    field_type = forms.ChoiceField(
        choices=[
            ("number", "Number"),
            ("date", "Date"),
            ("boolean", "Checkbox"),
            ("char", "Short Text"),
            ("text", "Long Text"),
        ],
        initial="text",
    )
    required = forms.BooleanField(initial=True)


SchemaFieldFormSet = forms.formset_factory(SchemaFieldForm, extra=1, can_order=True)
