from django import forms
from .models import CustomUser, BlogsDetails, Comment
from django.contrib.auth.forms import UserCreationForm


class LogInForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "fadeIn"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "fadeIn"}))


class DateInput(forms.DateInput):
    input_type = "date"


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "username",
            "date_of_birth",
            "is_role",
            "email",
        )
        widgets = {"is_role": forms.RadioSelect(), "date_of_birth": DateInput()}
        help_texts = {
            "first_name" : None,
            "last_name" : None,
            "username" : None,
            "date_of_birth" : None,
            "is_role" : None,
            "email" : None,
            "password" : None,
            # "password2" : None
        }

    """
    Click on submit form come hear and validet data and at that time it's data save in memory.
    'commit = False' is stop data in memory and add or update them.
    save(commit=False)
    """

    def save(self):
        user = super(SignUpForm, self).save(commit=False)
        # print(type(user)) # <class 'blogs.models.CustomUser'>
        user.is_role = self.cleaned_data["is_role"]

        if user.is_role == "Reader":
            user.is_reader = True
            user.is_blogger = False

        if user.is_role == "Bloger":
            user.is_reader = False
            user.is_blogger = True

        user.save()
        return user


class UserUpdateForm(UserCreationForm):
    password1 = None
    password2 = None

    # def __init__(self, *args, **kwargs):
    #    super(UserUpdateForm, self).__init__(*args, **kwargs)
    #    del self.fields['password1']
    #    del self.fields['password2']

    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "username",
            "date_of_birth",
            "is_role",
            "email",
        )
        widgets = {"is_role": forms.RadioSelect(), "date_of_birth": DateInput()}

    def save(self):
        user = super(UserUpdateForm, self).save(commit=False)
        user.is_role = self.cleaned_data["is_role"]

        if user.is_role == "Reader":
            user.is_reader = True
            user.is_blogger = False

        if user.is_role == "Bloger":
            user.is_reader = False
            user.is_blogger = True

        user.save()
        return user


class ProfileUpdateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "username",
            "date_of_birth",
            "is_role",
            "email",
        )
        widgets = {"is_role": forms.RadioSelect(), "date_of_birth": DateInput()}

    def save(self):
        user = super(ProfileUpdateForm, self).save(commit=False)
        user.is_role = self.cleaned_data["is_role"]

        if user.is_role == "Reader":
            user.is_reader = True
            user.is_blogger = False

        if user.is_role == "Bloger":
            user.is_reader = False
            user.is_blogger = True

        user.save()
        return user


class BlogsDetailsForm(forms.ModelForm):
    class Meta:
        model = BlogsDetails
        fields = ("id","blog_title", "blog_content")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("comment",)


class BlogUpdateForm(forms.ModelForm):
    class Meta:
        model = BlogsDetails
        fields = ("blog_title", "blog_content")


class CommentUpdateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("comment",)
