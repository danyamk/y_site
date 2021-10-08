from posts.models import Post
from django import forms


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        label = {'text': 'Введите текст', 'group': 'Выберите группу'}
        help_text = {'text': 'Ваши мысли', 'group': 'Из уже существующих'}
