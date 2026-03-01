from django import forms
class ArticleForm(forms.Form):
    title = forms.CharField(label="мақала тақырыбы", max_length=70)
    description=forms.CharField(label="сипаттама", max_length=150)
    content=forms.CharField(widget=forms.Textarea,label="мазмұны",min_length=100, max_length=2000)
    release=forms.DateField(label="жарияланған күні")
    author=forms.CharField(label="автор")