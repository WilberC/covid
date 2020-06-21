from django.views.generic import TemplateView
from decimal import Decimal
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *


def save_responses(model_name, list_answers, question_number, geolocation_person):
    model_name = SurveyAnswer(geolocation_person=geolocation_person)
    model_name.question_number = question_number
    for answer in list_answers:
        model_name.answer = int(answer)
        model_name.save()
        model_name.id = None
    pass


def valid_result_from_fr(fr, ss, sm, sl):
    if 0 < fr <= 0.6:
        if 0 < ss or sm <= 0.5:
            return 2
        else:
            return 2
    elif fr == 0 and sm >= 0.4:
        return 3
    elif fr >= 1:
        if sl > 0.2 or sm > 0 or ss >= 0:
            return 4
        else:
            return 4
    else:
        return 1


class SurveyTemplateView(TemplateView):
    template_name = "survey.html"
    person_model = SurveyedPerson
    geolocation_model = GeolocationPerson
    answer_model = SurveyAnswer

    def post(self, request, *args, **kwargs):
        data = self.request.POST
        # ----------------------
        name = data.get('name')
        identity_number = data.get('identity_number')
        latitude = Decimal(data.get('latitude'))
        longitude = Decimal(data.get('longitude'))
        # ----------------------
        person = self.person_model.objects.get_or_create(name=name, identity_number=identity_number)
        # ----------------------
        q_one = data.getlist('q-1')
        q_two = data.getlist('q-2')
        q_three = data.getlist('q-3')
        q_fourth = data.getlist('q-4')
        q_five = data.getlist('q-5')
        q_six = data.getlist('q-6')
        # ----------------------
        all_responses = q_one + q_two + q_three + q_fourth + q_five + q_six
        # ----------------------
        fr = 0
        # ----------------------
        if 1 in q_two:
            fr += 1
        if 2 in q_two:
            fr += 1
        # ----------------------
        if 1 in q_three:
            fr += 1
        if 2 in q_three:
            fr += 0.6
        # ----------------------
        ss = 0
        if 1 in q_fourth:
            ss += 0.9
        if 2 in q_fourth:
            ss += 0.4
        if 3 in q_fourth:
            ss += 0.8
        # ----------------------
        sm = 0
        if 1 in q_five:
            sm += 0.4
        if 2 in q_five:
            sm += 0.5
        # ----------------------
        sl = 0
        if 1 in q_six:
            sl += 0.15
        if 2 in q_six:
            sl += 0.14
        if 3 in q_six:
            sl += 0.12
        if 4 in q_six:
            sl += 0.06
        if 5 in q_six:
            sl += 0.17
        # ----------------------
        result = valid_result_from_fr(fr, ss, sm, sl)
        survey_number = len(self.geolocation_model.objects.filter(surveyed_person=person[0])) + 1
        geolocation_person = self.geolocation_model.objects.create(surveyed_person=person[0],
                                                                   survey_number=survey_number,
                                                                   latitude=latitude, longitude=longitude,
                                                                   result=result)
        # ----------------------
        for i, rpt in enumerate(all_responses):
            save_responses(self.answer_model, rpt, (i + 1), geolocation_person)
        # print('-------------------')
        # print('Info')
        # print('-------------------')
        # print(name)
        # print(identity_number)
        # print(latitude)
        # print(longitude)
        # print('-------------------')
        # print('Questions')
        # print('-------------------')
        # print(q_one)
        # print(q_two)
        # print(q_three)
        # print(q_fourth)
        # print(q_five)
        # print(q_six)
        # print('-------------------')
        return redirect(reverse('survey_result') + '?identity_number={}'.format(identity_number))


class SurveyResultTemplateView(TemplateView):
    template_name = "survey_result.html"
    person = SurveyedPerson
    geolocation = GeolocationPerson
    answers = SurveyAnswer

    def get_context_data(self, **kwargs):
        context = super(SurveyResultTemplateView, self).get_context_data(**kwargs)
        identity_number = self.request.GET.get('identity_number')
        context['person'] = self.person.objects.get(identity_number=identity_number)
        context['geolocation'] = self.geolocation.objects.filter(surveyed_person=context['person'])
        return context
