from __future__ import unicode_literals
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.db import models
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('id'), max_length=10, blank=False)
    first_name = models.CharField(_('first name'), max_length=30, blank=False)
    last_name = models.CharField(_('last name'), max_length=30, blank=False)
    mobile_number = models.CharField(verbose_name='mobile number', max_length=10, default="")
    type = models.CharField(verbose_name='type', choices=(('student', 'STUDENT'), ('faculty', 'FACULTY')),
                            max_length=10)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'type']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.username], **kwargs)

    def get_username(self):
        return self.username


class requestTable(models.Model):
    time_stamp = models.DateTimeField(verbose_name="time stamp", auto_now_add=True)

    block = models.CharField(
        verbose_name="Building name",
        max_length=20
    )

    room_number = models.CharField(
        verbose_name="Room number",
        max_length=10,
    )

    block_type = models.CharField(
        verbose_name="Block type",
        choices=(('classroom', 'CLASSROOM'), ('lab', 'LAB')),
        max_length=10,
        default='classroom'
    )

    startDateTime = models.CharField(
        verbose_name="startDateTime",
        max_length=30
    )

    endDateTime = models.CharField(
        verbose_name="endDateTime",
        max_length=30,
    )

    sender = models.CharField(
        verbose_name="sender",
        max_length=20,
    )

    sender_id = models.CharField(
        verbose_name="sender_id",
        max_length=20,
        default="",
    )

    granter = models.CharField(
        verbose_name="granter",
        max_length=10, blank=True
    )

    description = models.CharField(
        verbose_name="description",
        max_length=100
    )

    booking_status = models.CharField(
        verbose_name="booking status",
        max_length=5, default='0'
    )


class classroom(models.Model):
    block = models.CharField(
        verbose_name="Building name",
        choices=(('cc1', 'COMPUTER CENTER- 1'), ('cc2', 'COMPUTER CENTER- 2'), ('cc3', 'COMPUTER CENTER- 3'),
                 ('lt', 'LECTURE THEATRE')),
        max_length=20
    )

    room_number = models.CharField(
        verbose_name="Room number",
        max_length=10,
        primary_key=True
    )

    floor_number = models.PositiveIntegerField(
        verbose_name="Floor number"
    )

    maximum_capacity = models.PositiveIntegerField(
        verbose_name="Maximum room size",
    )

    projector = models.BooleanField(
        verbose_name="Projector condition",
        choices=((True, 'WORKING'), (False, 'NOT WORKING')),
        max_length=10
    )

    computer = models.BooleanField(
        verbose_name="Computer condition",
        choices=((True, 'WORKING'), (False, 'NOT WORKING')),
        max_length=10
    )

    air_conditioner = models.BooleanField(
        verbose_name="AC condition",
        choices=((True, 'WORKING'), (False, 'NOT WORKING')),
        max_length=10
    )

    speakers = models.BooleanField(
        verbose_name="Speakes condition",
        choices=((True, 'WORKING'), (False, 'NOT WORKING')),
        max_length=10
    )

    def __str__(self):
        return self.block + " " + self.room_number


class labs(models.Model):
    block = models.CharField(
        verbose_name="Building name",
        choices=(('cc1', 'COMPUTER CENTER- 1'), ('cc2', 'COMPUTER CENTER- 2'), ('cc3', 'COMPUTER CENTER- 3'),
                 ('lt', 'LECTURE THEATRE')),
        max_length=20
    )

    room_number = models.CharField(
        verbose_name="Room number",
        max_length=10,
        primary_key=True
    )

    floor_number = models.CharField(
        verbose_name="Floor number",
        max_length=10
    )

    maximum_capacity = models.CharField(
        verbose_name="Maximum room size",
        max_length=5
    )

    type = models.CharField(
        verbose_name="Type of Lab",
        choices=(('computer', 'COMPUTER'), ('physics', 'PHYSICS'), ('vlsi', 'VLSI')),
        max_length=20
    )

    air_conditioner = models.BooleanField(
        verbose_name="AC condition",
        choices=((True, 'WORKING'), (False, 'NOT WORKING')),
        max_length=10
    )

    def __str__(self):
        return self.block + " " + self.room_number


class TimeTableEvents(models.Model):
    room_number = models.CharField(
        verbose_name="Room number",
        max_length=10
    )

    course = models.CharField(
        verbose_name="course name",
        max_length=25
    )

    startTime = models.CharField(
        verbose_name="start time",
        max_length=30,
        default=''
    )

    endTime = models.CharField(
        verbose_name="end time",
        max_length=30,
        default=''
    )

    dayOfWeek = models.CharField(
        verbose_name="week day",
        max_length=12
    )

    lecturer = models.CharField(
        verbose_name="lecturer",
        max_length=10
    )
