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

    def f(self, q):
        print '*********'
        print q

    def f2(self, **q):
        print '*********'
        print q

    def g(self, key1=None, key2=None):
        print '*********'
        print key1
        print key2

    def g2(self, k1=None, k2=None):
        print '*********'
        print k1
        print k2


    def g3(self, *t1):
        print '*********'
        print t1

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['class'] = 'special2'

        kwargs = { 'key1' : 'val1', 'key2' : 'val2' }
        self.f(kwargs)   # {u'key2': u'val2', u'key1': u'val1'}
        #self.f2(kwargs) # TypeError: f2() takes exactly 1 argument (2 given)
        self.g(**kwargs) # val1 val2
        self.g2(*kwargs) # key2 key1
        self.g3(*kwargs) # (u'key2', u'key1')
