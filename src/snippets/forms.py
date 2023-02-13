from datetime import timedelta

from django import forms
from django.utils import timezone

from .models import Snippet


class SnippetForm(forms.ModelForm):
    TIME_LIMITS = [
        ("", "Never"),
        ("10", "10 Minutes"),
        ("1H", "1 Hour"),
        ("1D", "1 Day"),
        ("1W", "1 Week"),
        ("1M", "1 Month"),
        ("6M", "6 Months"),
        ("1Y", "1 Year"),
    ]
    expiration = forms.ChoiceField(choices=TIME_LIMITS, required=False)

    class Meta:
        model = Snippet
        fields = ("title", "body", "syntax", "expiration")
        widgets = {"body": forms.Textarea()}

    def clean_expiration(self) -> timezone.datetime | None:
        """Returns datetime object with time limit otherwise None.

        The time limit is defined in the TIME_LIMITS list
        by the first element of each tuple.
        """
        time_code = self.cleaned_data["expiration"]
        match time_code:
            case "10":
                time_limit = timedelta(minutes=10)
            case "1H":
                time_limit = timedelta(hours=1)
            case "1D":
                time_limit = timedelta(days=1)
            case "1W":
                time_limit = timedelta(weeks=1)
            case "1M":
                time_limit = timedelta(days=30)
            case "6M":
                time_limit = timedelta(days=183)
            case "1Y":
                time_limit = timedelta(days=366)
            case _:
                return None

        return timezone.now() + time_limit
