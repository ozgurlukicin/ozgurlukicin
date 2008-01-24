from django import newforms as forms

class SearchForm(forms.Form):
    term = forms.CharField(label='Anahtar kelime', required=True, widget=forms.TextInput(attrs={'size': '40',}))
	
class CommentForm(forms.Form):
    """ The comment thngyy add validation please..."""
    yorum=forms.CharField(label="Yorum",required=True,max_length=100,widget=forms.Textarea())
