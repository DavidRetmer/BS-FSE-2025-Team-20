from django.conf import settings
from django.http import HttpResponse
from django.views import View
from .models import Messages, Complaint
from django.shortcuts import render, redirect
from .forms import SendMailForm
from .forms import ContactForm, CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib import messages

from django.shortcuts import redirect
from django.contrib.auth import logout
from django.http import HttpResponseForbidden
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')  # Redirect to login page after logout
    return HttpResponseForbidden("Forbidden: Only POST requests are allowed.")

def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('username')
            form.save()
            messages.success(request, f'Account was created for {user}')
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)
@login_required
def welcome(request):
    return render(request, 'welcome.html', {'user': request.user})


from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages


def loginPage(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('welcome')  # הפניה לדף ברוך הבא של המשתמש
            else:
                messages.error(request, 'Invalid username or password.')
                return render(request, 'accounts/login.html', {'form': form})
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

# Admin Welcome Page
@login_required
def welcome_admin(request):
    return render(request, 'welcome_admin.html', {'user': request.user})
def login_admin(request):
    if request.method == 'POST':
        admin_password = request.POST.get('admin_password')

        if admin_password == '1234':  # הסיסמה האדמין
            # חיבור האדמין
            user = authenticate(username="admin", password="admin")  # הוספת שם משתמש וסיסמת אדמין לאמיתיים
            if user:
                login(request, user)
                messages.success(request, 'Welcome Admin!')
                return redirect('welcome_admin')  # הפניה לדף ברוך הבא של האדמין
            else:
                messages.error(request, 'Admin credentials are incorrect.')
                return redirect('login_admin')  # הפניה חזרה לדף כניסת האדמין
        else:
            messages.error(request, 'Incorrect admin password.')
            return redirect('login_admin')  # הפניה חזרה לדף כניסת האדמין
    return render(request, 'accounts/login_admin.html')

@login_required  # Ensure the user is logged in to access the welcome page
def welcome(request):
    return render(request, 'welcome.html', {'user': request.user})

def index(request):
    return render(request, 'index.html')
# views.py

from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import Event

def delete_event(request, event_id):
    # אם הבקשה היא DELETE (כמו ששלחנו מה-JavaScript)
    if request.method == 'DELETE':
        event = get_object_or_404(Event, id=event_id)
        event.delete()  # מוחק את האירוע
        return JsonResponse({'message': 'Event deleted successfully'}, status=200)

    return JsonResponse({'message': 'Invalid request method'}, status=400)

def about(request):
    return render(request, 'about.html')

def events(request):
    return render(request, 'events.html')

def join(request):
    return render(request, 'join.html', {'form': SendMailForm()})


# main_app/views.py
from django.shortcuts import render
from .models import Event


def events_view(request):
    # שליפת כל האירועים מהמסד נתונים
    events = Event.objects.all()

    # החזרת התבנית עם האירועים
    return render(request, 'events_view.html', {'events': events})


from django.shortcuts import render
from .models import Event

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Event

# View for displaying events on the map
def events_map(request):
    events = Event.objects.all()
    return render(request, 'accounts/events_map.html', {'events': events})
# main_app/views.py
from django.shortcuts import render

# main_app/views.py
from django.shortcuts import render

def rate_complaint(request):
    # אם יש צורך, תוכל לשלוף נתונים שקשורים לדירוג ממסד הנתונים
    # לדוגמה:
    # complaints = Complaint.objects.all()  # רק אם יש לך מודל כזה

    return render(request, 'accounts/rate_complaint.html')  # הדף שתציג למשתמש


# main_app/views.py
from django.shortcuts import render, redirect
from .models import ComplaintRating





def rate_complaint(request):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        complaint_id = request.POST.get('complaint_id')  # אם יש ID של תלונה שצריך לדירוג
        complaint = Complaint.objects.get(id=complaint_id)

        # יצירת דירוג חדש
        ComplaintRating.objects.create(complaint=complaint, rating=rating)

        return redirect('events_map')  # אחרי שהדירוג נשלח, נחזור לדף המפה

    return render(request, 'main_app/rate_complaint.html')


# View for deleting an event
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return JsonResponse({'status': 'success'})


def contact(request):
    if request.method == 'GET':
        return render(request, 'contact.html', {'form': ContactForm()})
    else:
        Messages.objects.create(
            title=request.POST.get('title', ''),
            description=request.POST.get('description', '')
        )
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EventForm
from .models import Event

def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event added successfully!')
            return redirect('events')  # Redirect to events page or event list page
    else:
        form = EventForm()

    context = {'form': form}
    return render(request, 'add_event.html', context)

def events(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events})

def index(request):
    # You can return some basic content or render a template
    return render(request, 'index.html')
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
# views.py

from django.shortcuts import render, redirect

def admin_login(request):
    if request.method == 'POST':
        admin_password = request.POST.get('admin_password')

        if admin_password == 'Salh9999':
            return redirect('welcome_admin')  # הפנייה לדף המנהל לאחר התחברות מוצלחת
        else:
            return render(request, 'welcome_admin.html', {'error_message': 'Incorrect password. Please try again.'})

    return render(request, 'admin_login.html')


from django.shortcuts import render

from django.shortcuts import render

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

# views.py

from django.shortcuts import render

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

from django.shortcuts import render, redirect

def admin_login(request):
    # תמיד להעביר לדף הניהול ללא קשר לסיסמה
    return redirect('admin_dashboard')


@login_required  # נוודא רק משתמשים מחוברים יכולים לגשת לדף ניהול
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


class MapView:
    pass