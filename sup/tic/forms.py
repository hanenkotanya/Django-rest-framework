from django.forms import ModelForm
from .models import Ticket


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['subject','body']

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class EditRoleForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['kind']

    def __init__(self, *args, **kwargs):
        super(EditRoleForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})