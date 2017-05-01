from django.db import models
from django.forms import ModelForm, Textarea, CheckboxInput
from django import forms
from django.contrib.auth.models import Group, User
from .report_to_pdf import convert
import hashlib

# Create your models here.
sector_choices = [
    ('GenTech', 'General Technology'),
    ('HthTech', 'Health Technology'),
    ('SpcTech', 'Space Technology'),
    ('AITech', 'Artificial Intelligence Technology'),
    ('RobTech', 'Robot Technology')
]

industry_choices = [
    ('Tech', 'Technology'),
    ('ArHu', 'Arts and Humanities')
]

class Report(models.Model):
    #creator = models.ForeignKey(User, on_delete=models.CASCADE)
    create_datetime = models.DateTimeField(auto_now_add=True, editable=False)

    report_name = models.CharField(max_length=50, unique=True, null=False)#, editable=False)
    company_name = models.CharField(max_length=50, null=False)
    phone_number = models.CharField(max_length=15, null=False)
    company_location = models.CharField(max_length=20, null=False)
    company_country = models.CharField(max_length=20, null=False)

    sector = models.CharField(max_length=7, choices=sector_choices, null=False)
    industry = models.CharField(max_length=4, choices=industry_choices, null=False)

    current_projects = models.CharField(max_length=500, null=False)
    isprivate = models.BooleanField(default=True)
    isencrypted = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group)
    hash = models.CharField(max_length=40, null=True, blank=True, unique=True)

    def __str__(self):
        return self.report_name + " created on " + str(self.create_datetime.date())

    def return_info(self):
        info = "Report Title: " + self.report_name + "\n"+\
               "Company: "+self.company_name + ", located at " +self.company_location +", "+ self.company_country+"\n"+\
               "Sector: " + self.sector + ",\t" + "Industry: " + self.industry + "\n"+\
               "Report created on " + str(self.create_datetime.date())
        return info

    #returns a date obejct for the date the report was created on
    def get_date(self):
        return self.create_datetime.date()

    def set_hash(self):
        self.hash = self.__hash__()
        self.save()

    def __hash__(self):
        return hash(convert(self))

class Attachment(models.Model):
    seqid = models.IntegerField(null=True)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    file = models.FileField(upload_to="attachments") #read documentation on FileField
    hash = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return self.file.name

    def set_hash(self):
        self.hash = self.__hash__()
        self.save()

    def __hash__(self):
        f = self.file
        hash = hashlib.sha1()

        for chunk in iter(lambda: f.read(64000), b''):
            hash.update(chunk)

        f.close()
        return hash.hexdigest()


class ReportForm(ModelForm):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple':True}),required=False)
    groups = forms.MultipleChoiceField(label='Groups', required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Report
        fields = ['report_name','company_name','phone_number','company_location','company_country','sector','industry',\
                  'current_projects','isprivate','isencrypted']
        widgets = {
            'current_projects': Textarea(),
        }