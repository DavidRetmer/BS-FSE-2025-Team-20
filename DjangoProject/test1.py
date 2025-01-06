import pytest
from unittest.mock import MagicMock
from your_module_name import YourClass  # החלף בשם המחלקה ובקובץ המתאים
from your_app.models import Event  # החלף בשם המודול והמודל שלך

@pytest.fixture
def mock_user():
    """יצירת אובייקט מדומה עבור המשתמש"""
    user = MagicMock()
    user.email = "test_user@example.com"
    return user

@pytest.fixture
def mock_event_queryset():
    """יצירת אובייקט מדומה עבור ה-QuerySet"""
    mock_queryset = MagicMock()
    return mock_queryset

def test_init_with_user(mock_user, mock_event_queryset, monkeypatch):
    """בדיקה כאשר מועבר משתמש"""
    # ליצירת QuerySet מדומה
    mock_filter = MagicMock(return_value=mock_event_queryset)
    monkeypatch.setattr(Event.objects, "filter", mock_filter)

    # קריאה לקונסטרקטור
    instance = YourClass(user=mock_user)

    # בדיקה שהשדה 'event' משתמש ב-QuerySet המתאים
    assert instance.fields["event"].queryset == mock_event_queryset

    # בדיקה ש-Event.objects.filter נקרא עם הפרמטר הנכון
    mock_filter.assert_called_once_with(members_email_icontains=mock_user.email)
