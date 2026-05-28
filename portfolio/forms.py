from django import forms
from .models import Portfolio, Feedback

class PortfolioForm(forms.ModelForm):
    
    # Explicitly defining FileFields without using them inside widgets
    puc_marks = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'accept': '.pdf,.jpg,.png,.jpeg'}))
    certificates = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'accept': '.pdf,.jpg,.png,.jpeg'}))
    profile_image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    resume = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'accept': '.pdf'}))

    class Meta:
        model = Portfolio
        fields = [
            'full_name', 'bio', 'skills', 'experience', 'projects', 
            'school', 'college', 'linkedin_url', 'puc_marks', 
            'profile_image', 'certificates', 'resume'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'skills': forms.TextInput(attrs={'class': 'form-control'}),
            'experience': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'projects': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'school': forms.TextInput(attrs={'class': 'form-control'}),  
            'college': forms.TextInput(attrs={'class': 'form-control'}),  
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control'}),
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }
