from django import forms
from .models import NippoModel

class NippoModelForm(forms.ModelForm):
    
    class Meta:
        model = NippoModel
        exclude = ["user"]
        # fields = "__all__"

    def __init__(self,user=None, *args, **kwargs):
        for field in self.base_fields.values():
            field.widget.attrs["class"] = "form-control"
        self.user = user
        print(self.user)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        nippo_obj = super().save(commit=False)
        if self.user:
            nippo_obj.user = self.user
        if commit:
            nippo_obj.save()
        return nippo_obj


class NippoFormClass(forms.Form):
    title = forms.CharField(label="タイトル", widget=forms.TextInput(attrs={'placeholder':'タイトル...'}))
    content = forms.CharField(label="内容", widget=forms.Textarea(attrs={'placeholder':'内容...'}))
    
    def __init__(self, *args, **kwargs):
        for field in self.base_fields.values():
            field.widget.attrs.update({"class":"form-control"})
        super().__init__(*args, **kwargs)