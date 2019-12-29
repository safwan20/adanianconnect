from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput
from django.core.validators import RegexValidator

from .models import Profile

class UserRegisterForm(UserCreationForm) :
    alphanumeric = RegexValidator(r'^[a-zA-Z]*$', 'Only Letters are allowed.')
    username = forms.CharField()
    email = forms.EmailField()
    first_name = forms.CharField(validators=[alphanumeric])
    last_name = forms.CharField(validators=[alphanumeric])

    class Meta :
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']


class ProfileUpdateForm(forms.ModelForm):
    T_choices = (
        ('WEB DEVELOPMENT','WEB DEVELOPMENT'),
        ('MOBILE APP DEVELOPMENT', 'MOBILE APP DEVELOPMENT'),
        ('SOFTWARE DEVELOPMENT', 'SOFTWARE DEVELOPMENT'),
        ('COMPETETIVE PROGRAMMING', 'COMPETETIVE PROGRAMMING'),
        ('GAME DEVELOPMENT', 'GAME DEVELOPMENT'),
        ('MACHINE LEARNING', 'MACHINE LEARNING'),
        ('DEEP LEARNING', 'DEEP LEARNING'),
        ('ARTIFICIAL INTELLIGENT', 'ARTIFICIAL INTELLIGENT'),
        ('ROBOTICS', 'ROBOTICS'),
        ('FRONT END DEVELOPMENT', 'FRONT END DEVELOPMENT'),
        ('BACK END DEVELOPMENT', 'BACK  END DEVELOPMENT'),
        ('UI UX DESIGNING', 'UI UX DESIGNING'),
        ('GRAPHIC DESIGNING', 'GRAPHIC DESIGNING'),
        ('CLOUD TECHNOLOGY', 'CLOUD TECHNOLOGY'),
        ('DATABASE MANAGEMENT', 'DATABASE MANAGEMENT'),
        ('IOT', 'IOT'),
        )

    L_choices = (
        ('C++', 'C++'),
        ('Java', 'Java'),
        ('Python', 'Python'),
        ('C#', 'C#'),
        ('C', 'C'),
        ('Andriod', 'Andriod'),
        ('Flutter', 'Flutter'),
        ('Django', 'Django'),
        ('Flask', 'Flask'),
        ('Java Script', 'Java Script'),
        ('Jquery', 'Jquery'),
        ('Html', 'Html'),
        ('R', 'R'),
        ('Kotlin', 'Kotlin'),
        ('Css', 'Css'),
        ('Golang', 'Golang'),
        ('Pygame', 'Pygame'),
        ('Ruby', 'Ruby'),
        ('Objective C', 'Objective C'),
        ('Php', 'Php'),
        ('Swift', 'Swift'),
        ('Mysql', 'Mysql'),
        ('Sql', 'Sql'),
        ('Perl', 'Perl'),
        ('Lua', 'Lua'),
        ('Erlang', 'Erlang'),
        ('MATLAB', 'MATLAB'),
        ('React Native', 'React Native'),
     )

    hj = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
    )

    tech = forms.MultipleChoiceField(choices=T_choices, widget=forms.CheckboxSelectMultiple,required=False)
    lang = forms.MultipleChoiceField(choices=L_choices, widget=forms.CheckboxSelectMultiple,required=False)
    link = forms.URLField(required=False,label="Github Link")
    skills = forms.CharField(required=False,label="Skills (i.e reading,coding,etc)")
    sem = forms.ChoiceField(choices=hj,required=False)
    linkin = forms.URLField(required=False,label="linkedin Link for people to connect")
    stop = forms.URLField(required=False, label="If you select the competitive programming then add ( STOPSTALK ) profile link, its a very cool website for competitive programmer ")

    class Meta:
        model = Profile
        fields = ['tech','lang','link','linkin','stop','skills','sem','image']



class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name','last_name','email']
