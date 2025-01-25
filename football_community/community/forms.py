from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Event, Rating, Post, Comment, Message

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name', 
            'email', 
            'bio', 
            'skill_level',
            'availability_days',
            'availability_time_slots',
            'location_latitude',
            'location_longitude'
        ]
        widgets = {
            'location_latitude': forms.HiddenInput(),
            'location_longitude': forms.HiddenInput(),
            'availability_days': forms.SelectMultiple(choices=[
                ('monday', 'Monday'),
                ('tuesday', 'Tuesday'),
                ('wednesday', 'Wednesday'),
                ('thursday', 'Thursday'),
                ('friday', 'Friday'),
                ('saturday', 'Saturday'),
                ('sunday', 'Sunday'),
            ]),
            'availability_time_slots': forms.SelectMultiple(choices=[
                ('morning', 'Morning (6AM-12PM)'),
                ('afternoon', 'Afternoon (12PM-5PM)'),
                ('evening', 'Evening (5PM-10PM)'),
            ]),
        }

    def clean(self):
        cleaned_data = super().clean()
        lat = cleaned_data.get('location_latitude')
        lng = cleaned_data.get('location_longitude')

        # If one coordinate is provided, both must be provided
        if (lat is not None and lng is None) or (lat is None and lng is not None):
            raise forms.ValidationError("Both latitude and longitude must be provided together.")

        # Validate latitude range
        if lat is not None and (float(lat) < -90 or float(lat) > 90):
            raise forms.ValidationError("Latitude must be between -90 and 90 degrees.")

        # Validate longitude range
        if lng is not None and (float(lng) < -180 or float(lng) > 180):
            raise forms.ValidationError("Longitude must be between -180 and 180 degrees.")

        return cleaned_data

class EventForm(forms.ModelForm):
    def clean_location_latitude(self):
        latitude = self.cleaned_data.get('location_latitude')
        if latitude is not None:
            lat_float = float(latitude)
            if lat_float < -90 or lat_float > 90:
                raise forms.ValidationError("Latitude must be between -90 and 90 degrees.")
            return lat_float
        return latitude

    def clean_location_longitude(self):
        longitude = self.cleaned_data.get('location_longitude')
        if longitude is not None:
            lon_float = float(longitude)
            if lon_float < -180 or lon_float > 180:
                raise forms.ValidationError("Longitude must be between -180 and 180 degrees.")
            return lon_float
        return longitude

    class Meta:
        model = Event
        fields = [
            'title', 'description', 'location',
            'location_latitude', 'location_longitude',
            'datetime', 'max_players', 'skill_level_filter'
        ]
        widgets = {
            'datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score', 'feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 4}),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'content': 'Your Comment'
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type your message here...'}),
        } 