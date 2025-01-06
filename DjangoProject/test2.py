import pytest
from your_module_name import YourClass  # החלף בשם המחלקה ובקובץ המתאים

def test_init_without_user():
    """בדיקה כאשר לא מועבר משתמש"""
    instance = YourClass()

    # בדיקה שהשדה 'event' אינו מוגדר
    assert "event" in instance.fields  # רק אם השדה קיים כברירת מחדל
    assert instance.fields["event"].queryset is None
