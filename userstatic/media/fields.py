# -*- coding: utf-8 -*-
from django import forms

from invite.models import Invite


class InviteField(forms.CharField):
    def clean(self, value):
        value = super(InviteField, self).clean(value)
        try:
            invite = Invite.objects.get(pk=value, accepted=None)
        except Invite.DoesNotExist:
            raise forms.ValidationError(u'Некорректный код. Возможно, приглашение уже использовано.')
        else:
            return invite
