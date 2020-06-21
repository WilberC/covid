from django.db import models
from covid.model_layout import AuditFields


class SurveyedPerson(AuditFields):
    name = models.CharField(max_length=1000)
    identity_number = models.CharField(max_length=300)

    class Meta:
        managed = True
        ordering = ['identity_number']


class GeolocationPerson(AuditFields):
    POSSIBLE_RESULTS = [
        (1, 'How good!, please take this survey again in one week.'),
        (2, 'Please isolate yourself for prevention and take the survey again in three days.'),
        (3, 'Please isolate yourself for prevention and take the survey again in three days.'),
        (4, 'You have symptoms of covid19, please contact with a hospital as soon as possible.')
    ]
    surveyed_person = models.ForeignKey(SurveyedPerson, on_delete=models.CASCADE)
    survey_number = models.IntegerField()
    latitude = models.DecimalField(max_digits=15, decimal_places=8)
    longitude = models.DecimalField(max_digits=15, decimal_places=8)
    result = models.IntegerField(choices=POSSIBLE_RESULTS)

    class Meta:
        managed = True
        ordering = ['survey_number']


class SurveyAnswer(AuditFields):
    geolocation_person = models.ForeignKey(GeolocationPerson, on_delete=models.CASCADE)
    question_number = models.IntegerField()
    answer = models.IntegerField()

    class Meta:
        managed = True
        ordering = ['id']
