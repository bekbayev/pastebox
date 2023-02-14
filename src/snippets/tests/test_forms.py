from freezegun import freeze_time

from django.test import SimpleTestCase
from django.utils import timezone

from ..forms import SnippetForm

ONE_DAY_IN_SECONDS = 24 * 60 * 60
TIME_CODES = {
    "10": 10 * 60,
    "1H": 60 * 60,
    "1D": ONE_DAY_IN_SECONDS,
    "1W": 7 * ONE_DAY_IN_SECONDS,
    "1M": 30 * ONE_DAY_IN_SECONDS,
    "6M": 183 * ONE_DAY_IN_SECONDS,
    "1Y": 366 * ONE_DAY_IN_SECONDS,
}


class SnippetFormTest(SimpleTestCase):
    @freeze_time(timezone.now())
    def test_clean_expiration_returns_datetime_by_timecode(self) -> None:
        for time_code, expected_expiration in TIME_CODES.items():
            form = SnippetForm({"expiration": time_code})
            form.is_valid()  # calls SnippetForm.clean_expiration method
            expiration = form.cleaned_data.get("expiration", None)
            expiration -= timezone.now()  # get only duration
            self.assertEquals(expiration.total_seconds(), expected_expiration)
