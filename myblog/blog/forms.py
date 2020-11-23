from django import forms
from .models import Post,Comment

class PostForm(forms.ModelForm):

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
    
    def clean_title(self):
        pass

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