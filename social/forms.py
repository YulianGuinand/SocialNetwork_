from django import forms
from .models import Post, Comment, MessageModel, Story, HelpPost, Meeting


class PostForm(forms.ModelForm):
    title = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '1',
                   'class': "creatPost",
                   'placeholder': "give it a title...",
                   'type': 'text'}
        )
        )
    body = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '5',
                   'class': "creatPost",
                   'placeholder': "what's on your mind ?",
                   'type': 'text'}
        )
        )
    image = forms.ImageField(required=False,
                             widget=forms.FileInput(attrs={
                                "id" : "image_field" ,
                                "class":"hidden",
                            }), label='image',)
    
    class Meta:
        model = Post
        fields = ['title', 'body', 'image' ]

class HelpPostForm(forms.ModelForm):
    title = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '1',
                   'class': "creatPost",
                   'placeholder': "give it a title...",
                   'type': 'text'}
        )
        )
    body = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '5',
                   'class': "creatPost",
                   'placeholder': "How can you help ?",
                   'type': 'text'}
        ))
    
    class Meta:
        model = HelpPost
        fields = ['title', 'body']

class CreateRdvForm(forms.ModelForm):
    date = forms.DateField(
        label='Date',
        widget=forms.DateInput(
            attrs={'type': 'date'}
        )
    )
    time = forms.TimeField(
        label='Time',
        widget=forms.TimeInput(
            attrs={'type': 'time'}
        )
    )
    class Meta:
        model = Meeting
        fields = ['date', 'time']

class StoryForm(forms.ModelForm):
    image = forms.ImageField(required=True,
                             widget=forms.FileInput(attrs={
                                "id" : "image_field" ,
                                "class":"hidden",
                            }), label="image",)
    class Meta:
        model = Story
        fields = ['image']

class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '1',
                   'class':'creatPost',
                   'placeholder': 'Say Something...',
                   
                   }
        ))

    class Meta:
        model = Comment
        fields = ['comment']

class ThreadForm(forms.Form):
    username = forms.CharField(label='', max_length=20, widget=forms.Textarea(
        attrs={
            'rows': '1',
            'type':"search",
            'placeholder' :"search message",
            'class':"message-search",
            'style': 'width: 100%;'
        }
    ))

class MessageForm(forms.ModelForm):
    body = forms.CharField(label='', max_length=1000,widget=forms.Textarea(
            attrs={'rows': '1',
                   'placeholder': "what's on your mind ?",
                    'type': 'text',}))
    
    image = forms.ImageField(required=False,
                             widget=forms.FileInput(attrs={
                                "id" : "image_field" ,
                                "class":"hidden",
                            }), label='image',)
    
    class Meta:
        model = MessageModel
        fields = ['body', 'image']
        
class ShareForm(forms.Form):
    body = forms.CharField(
        label="",
        widget= forms.Textarea(attrs={
            'rows': 1,
            'placeholder': "Say Something",
        })
    )

class ExploreForm(forms.Form):
    query = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Explore tags'
        })
    )