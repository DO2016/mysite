from __future__ import unicode_literals
from django.db import models
from django import forms

# Create your models here.

class ModelTable(models.Model):
    col1 = models.CharField(max_length=200)



class Author(models.Model):
    author_fio = models.CharField(max_length=256)

    def get_full_name(self):
        return self.author_fio


class Editor(models.Model):
    editor_fio = models.CharField(max_length=256)

    def get_full_name(self):
        return self.editor_fio


class Post(models.Model):
    description = models.TextField()
    category = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author) # many posts -> many editor
    editor = models.ForeignKey(Editor, default=0)  # many posts -> one editor



class PostForm(forms.ModelForm):
    description = forms.CharField(widget=forms.TextInput(attrs={ 'class':'special' }))
    category = forms.CharField(widget=forms.TextInput(attrs={ 'class':'special' }))

    class Meta:
        model = Post
        fields = ['description', 'category']


class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()


class UserModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()

class BookForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea(attrs={ 'class':'special' }))
    category = forms.CharField(widget=forms.TextInput(attrs={ 'class':'special' }))
    editor = UserModelChoiceField(queryset=Editor.objects.all())
    authors = UserModelMultipleChoiceField(queryset=Author.objects.all())