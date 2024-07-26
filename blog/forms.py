from django import forms


class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label="Comment")
    rating = forms.IntegerField(label="Rating", min_value=1, max_value=5)

