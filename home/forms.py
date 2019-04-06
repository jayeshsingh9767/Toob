from django import forms
from django.core.exceptions import ValidationError
from .models import Posts


choice = (
        (1, ("Question")),
        (2, ("Creative Idea")),
        (3, ("Innovation")),
        (4, ("Nightmare")),
        (5, ("Thought"))
    )


class WriteThought(forms.Form):
    # p = ("a", "b")
    title = forms.CharField(
        max_length=250,
        widget=forms.Textarea({
                'attrs': 'content',
                'rows': '1',
                'id': 'title-box',
                'placeholder': 'Title: Short and Descriptive'
            }),
        )

    content = forms.CharField(
        max_length=15000,
        widget=forms.Textarea({
            'attrs': 'content',
            'placeholder': 'Explain Your Thought in Details'
        })
    )
    image = forms.ImageField(required=False)
    type = forms.ChoiceField(
        widget=forms.RadioSelect({'attr': 'type', 'id': 'type'}),
        choices=choice,
    )
    tags = forms.CharField(
        max_length=250,
        help_text="Use Space for seperating tags",
    )

    def clean_title(self, *args, **kwargs):
        post = Posts.objects.get(title=self.title)
        if post:
            raise ValidationError("The title Exixts, Try other relevent Title")
        else:
            return self.title
