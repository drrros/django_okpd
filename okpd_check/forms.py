from django import forms


class OkpdForm(forms.Form):
    check_groups = forms.BooleanField(label='Проверять группы', required=False)
    okpd_list = forms.CharField(
        label='Список ОКПД',
        required=True,
        max_length=80000,
        min_length=8,
        widget=forms.Textarea,
        error_messages={
            'required': "Поле не может быть пустым",
            'max_length':"Поле должно быть не более 80000 символов",
            'min_length':"Поле должно быть не менее 8 символов"
        }
    )
    okpd_list.widget.attrs['class'] = 'form-control'
    okpd_list.widget.attrs['rows'] = '15'
    okpd_list.widget.attrs['cols'] = '20'
    # okpd_list.label.widget.attrs['class'] = 'form-control-label'
    # submit = SubmitField('Проверить')
