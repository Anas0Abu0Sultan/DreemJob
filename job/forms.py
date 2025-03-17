from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from job.models import freelancer, job, apply


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=255, required=True, widget=forms.EmailInput())
    name_job = forms.CharField(max_length=100, required=False, help_text="Optional. Enter your job title.")
    country = forms.CharField(max_length=100, required=True, help_text="Required. Enter your country.")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2",  "name_job", "country"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create a freelancer profile for the user
            freelancer.objects.create(
                user=user,
                name_job=self.cleaned_data['name_job'],
                country=self.cleaned_data['country'],
            )
        return user


# class CustomerForm(forms.ModelForm):
#     class Meta:
#         model = customer
#         fields = ['card', 'country', 'image']




class JobForm(forms.ModelForm):
    deadline = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    class Meta:
        model = job
        
        fields = ['title','deadline','salary','category','cover','job_nature','description']


class ApplyForm(forms.ModelForm):
    class Meta:
        model = apply
        fields = ['link', 'cv', 'coverletter']

        widgets = {
            'coverletter': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your cover letter here...'}),
            'link': forms.URLInput(attrs={'placeholder': 'Portfolio or relevant link'}),
        }

    def clean_cv(self):
        cv = self.cleaned_data.get('cv')

        if cv:
            # Restrict file size (e.g., max 5MB)
            max_size = 5 * 1024 * 1024  # 5MB
            if cv.size > max_size:
                raise forms.ValidationError("CV file size must not exceed 5MB.")

            # Restrict file extensions
            allowed_extensions = ['pdf', 'doc', 'docx']
            if not cv.name.split('.')[-1].lower() in allowed_extensions:
                raise forms.ValidationError("Only PDF, DOC, or DOCX files are allowed.")

        return cv

    def clean_link(self):
        link = self.cleaned_data.get('link')

        if link and not link.startswith(('http://', 'https://')):
            raise forms.ValidationError("Please enter a valid URL (starting with http:// or https://).")

        return link

    def clean_coverletter(self):
        coverletter = self.cleaned_data.get('coverletter')

        # Restrict cover letter length
        if len(coverletter.split()) < 20:  # Minimum 20 words
            raise forms.ValidationError("Cover letter must be at least 20 words long.")

        return coverletter