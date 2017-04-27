from django import forms

from Project.models import requestTable , TimeTableEvents
from .models import User


class SignupForm(forms.Form):
    username = forms.CharField(max_length=10, label='ID')
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    type = forms.ChoiceField(choices=(('student', 'STUDENT'), ('faculty', 'FACULTY')), label='CHOICE')
    mobile_number = forms.CharField(max_length=10, label='MOBILE NUMBER')

    def signup(self, request, user):
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.type = self.cleaned_data['type']
        user.mobile_number = self.cleaned_data['mobile_number']
        user.save()


class EventForm(forms.ModelForm):
    block = forms.CharField(label='BLOCK NAME', widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'block_name'}))
    room_number = forms.CharField(label='ROOM NUMBER', widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'room_number'}))
    startDateTime = forms.CharField(label='START DATE', widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'startDateTime'}))
    endDateTime = forms.CharField(label='END DATE', widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'endDateTime'}))
    description = forms.CharField(label='DESCRIPTION', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'description', 'placeholder': 'Enter the description for the event'}))
    granter = forms.ModelChoiceField(label='FACULTY',
                                     widget=forms.Select(attrs={'class': 'form-control', 'id': 'granter'}),
                                     queryset=User.objects.filter(type='faculty'))
    sender = forms.CharField(label='RESERVER', widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'sender'}))
    sender_id = forms.CharField(label='RESERVER ID', widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'sender_id'}))
    booking_status = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = requestTable
        fields = (
        "block", "room_number", "description", "granter", "startDateTime", "endDateTime", "sender_id", "sender")

    def save(self, commit=True):
        form = super(EventForm, self).save(commit=False)
        if commit:
            form.save()
        return form


class EventFormf(forms.ModelForm):
    block = forms.CharField(label='BLOCK NAME', widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'block_name'}))
    room_number = forms.CharField(label='ROOM NUMBER', widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'room_number'}))
    startDateTime = forms.CharField(label='START DATE', widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'startDateTime'}))
    endDateTime = forms.CharField(label='END DATE', widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'endDateTime'}))
    description = forms.CharField(label='DESCRIPTION', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'description', 'placeholder': 'Enter the description for the event'}))
    sender = forms.CharField(label='RESERVER', widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'sender'}))
    sender_id = forms.CharField(label='RESERVER ID', widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'sender_id'}))
    booking_status = forms.HiddenInput()

    class Meta:
        model = requestTable
        fields = ("block", "room_number", "description", "startDateTime", "endDateTime", "sender_id", "sender")

    def save(self, commit=True):
        form = super(EventFormf, self).save(commit=False)
        if commit:
            form.save()
        return form


class TimeTableForm(forms.ModelForm):
    room_number = forms.CharField(label='ROOM NUMBER', widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'room_number'}))
    startTime = forms.CharField(label='START DATE', widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'startDateTime'}))
    endTime = forms.CharField(label='END DATE', widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'endDateTime'}))
    course = forms.CharField(label='COURSE', widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'course', 'placeholder': 'Enter the course name'}))
    lecturer = forms.ModelChoiceField(label='LECTURER',
                                     widget=forms.Select(attrs={'class': 'form-control', 'id': 'lecturer'}),
                                     queryset=User.objects.filter(type='faculty'))
    dayOfWeek = forms.CharField(label='Day Of Week',initial='0', widget=forms.HiddenInput(
        attrs={'class': 'form-control', 'id': 'dow'}))

    class Meta:
        model = TimeTableEvents
        fields = ("room_number","course", "lecturer","startTime","endTime","dayOfWeek")

    def save(self, commit=True):
        form = super(TimeTableForm, self).save(commit=False)
        if commit:
            form.save()
        return form