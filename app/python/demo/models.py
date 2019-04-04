###########################################################
## File        : Models.py
## Description :

# python app\python\manage.py makemigrations
# python app\python\manage.py migrate

from django.db import models

class PermissionModel(models.Model):
    owner = models.CharField(max_length=256, default='unspecified', editable=False)

    class Meta:
        abstract = True

class AuditModel(models.Model):
    saved_on = models.DateTimeField(blank=True, null=True)
    saved_by = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        abstract = True

class Definition(models.Model):
    category = models.CharField(max_length=64)
    label = models.CharField(max_length=64)
    numeric = models.IntegerField(null=True)
    alphanumeric = models.CharField(max_length=256, null=True)

    class Meta:
        db_table="demo__definition"

class Link(models.Model):
    entity_type = models.IntegerField(blank=True, null=True)
    entity_id = models.IntegerField(blank=True, null=True)
    link_type = models.IntegerField(blank=True, null=True)
    link_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table="demo__link"

class Person(AuditModel):
    first_name = models.CharField(max_length=256, blank=True, null=True)
    last_name = models.CharField(max_length=256, blank=True, null=True)
    email = models.CharField(max_length=256, blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table="demo_person"

    def __unicode__(self):
        return unicode(self.last_name + ', ' + self.first_name)

class PersonAudit(AuditModel):
    person_id = models.IntegerField(blank=True, null=True)
    first_name = models.CharField(max_length=256, blank=True, null=True)
    last_name = models.CharField(max_length=256, blank=True, null=True)
    email = models.CharField(max_length=256, blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table="demo_person_audit"

    def __unicode__(self):
        return unicode(self.last_name + ', ' + self.first_name)

