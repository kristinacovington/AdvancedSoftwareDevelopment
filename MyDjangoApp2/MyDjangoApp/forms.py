from django import forms
from .models import Profile
from django.contrib.auth.models import User, Group



class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        required=True,
        label='Username',
        max_length=32
    )
    email = forms.EmailField(
        required=True,
        label='Email',
        max_length=32,
    )
    password = forms.CharField(
        required=True,
        label='Password',
        max_length=32,
        widget=forms.PasswordInput()
    )
    first_name = forms.CharField(
        required=True,
        label='First name',
        max_length=32,
    )
    last_name = forms.CharField(
        required=True,
        label='Last name',
        max_length=32,
    )
    company = forms.BooleanField(
        required=False,
        label='Company',
    )


class UserLoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label='Username',
        max_length=32
    )
    password = forms.CharField(
        required=True,
        label='Password',
        max_length=32,
        widget=forms.PasswordInput()
    )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'location')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class CreateGroupForm(forms.Form):
    name = forms.CharField(
        required=True,
        label='Group Name',
        max_length=32
    )
    #users = User.objects.all()
    usernames = []
    #tup = ('','')
    #usernames.append(tup)
    #for u in users:
    #    tup = (u.username, u.username)
    #    usernames.append(tup)
    members = forms.CharField(
        required=False,
        label='Add member',
        max_length=100,
    )



class RemoveMemberForm(forms.Form):
    '''
    PART_CHOICES = (
        ('No', 'No'),
        ('Yes', 'Yes'),)
    remove = forms.ChoiceField(choices = PART_CHOICES,required = False, label = 'Remove yourself from group')
    '''

    #users = User.objects.all()
    usernames = []
    #tup = ('','')
    #usernames.append(tup)
    #for u in users:
    #    tup = (u.username, u.username)
    #    usernames.append(tup)
    remove = forms.CharField(
        required=False,
        label='Remove a member. (Verify username if not site manager)',
        max_length=100,

    )
    members = forms.CharField(
        required=False,
        label='Add member',
        max_length=100,

    )


class SearchReportForm(forms.Form):
    keyword = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Search"}), required=True,
                              label='Keyword', max_length=100)


class ManageUserAccessForm(forms.Form):
    #users = User.objects.all()
    usernames = []
    #tup = ('','')
    #usernames.append(tup)
    #for u in users:
    #    tup = (u.username, u.username)
    #    usernames.append(tup)
    members = forms.CharField(
        required=True,
        label='Member',
        max_length=100,
    )
    PART_CHOICES = (
        ('No', 'No'),
        ('Yes', 'Yes'),)
    block = forms.ChoiceField(choices=PART_CHOICES, required=False, label='Block')
