from django import forms
from .models import Post,Comment
# from django.db.models import Count
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):

    error_css_class = 'is-invalid'
    def __init__(self,*args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        if self.errors:
            for form_name in self.errors:
                classes = self.fields[form_name].widget.attrs.get("class")
                classes += ' is-invalid'
                self.fields[form_name].widget.attrs['class'] = classes
    # required_css_class = 'required'
    class Meta:
        model = Post
        fields = ('title', 'text','category')
        labels = {
            "title" : "Title",
            "text"  : "Body Blog",
            "category" : "Category",
        }

        widgets = {
            'title' : forms.TextInput(
                attrs = {
                    'class' : 'form-control',
                }
            ),
            'text' : forms.Textarea (
                attrs = {
                    'class' : 'form-control',
                    'rows' : 15
                }
            ),
            'category' : forms.SelectMultiple (
                attrs = {
                    'class' : 'form-control',
                }
            ),
        }
    
    #validasi
    def clean_title(self):
        cleaned_title = self.cleaned_data.get('title')
        check_title = Post.objects.filter(title=cleaned_title)

        if self.instance:
            check_title = check_title.exclude(pk=self.instance.pk)

        if check_title.exists():
            raise ValidationError("This Article already published")

        return cleaned_title


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
        labels = {"text": "Comment"}

        widgets = {
            'text' : forms.Textarea (
                attrs = {
                    'class' : 'form-control',
                    'placeholder' : 'komentar anda',
                    'rows' : 2
                }
            ),
        }