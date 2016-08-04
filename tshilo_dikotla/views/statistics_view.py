import asyncio
import pandas as pd
import json
import pytz
from datetime import date, datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from edc_base.views import EdcBaseViewMixin
from edc_constants.constants import CLOSED
from edc_sync.models.outgoing_transaction import OutgoingTransaction

from call_manager.models import Call

from td_maternal.models import (MaternalConsent, MaternalLabourDel, MaternalOffStudy, MaternalUltraSoundInitial)
from dateutil.relativedelta import relativedelta

tz = pytz.timezone(settings.TIME_ZONE)


class StatisticsView(EdcBaseViewMixin, TemplateView):
    template_name = 'tshilo_dikotla/home.html'

    def __init__(self):
        self._response_data = {}
        self.columns = [
            'offstudy',
            'verified_consents',
            'not_verified_consents',
            'consented',
            'is_verified',
            'delivered',
            'delivered_po',
            'delivered_neg',
            'edd_1week',
            'consented_today',
            'contacted_retry',
            'contacted_today',
            'not_consented',
            'not_contacted',
            'consent_verified',
            'pending_transactions',
            'potential_calls']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            title=settings.PROJECT_TITLE,
            project_name=settings.PROJECT_TITLE,
        )
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StatisticsView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.is_ajax():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop = asyncio.get_event_loop()
            future_a = asyncio.Future()
            future_b = asyncio.Future()
            future_c = asyncio.Future()
            future_d = asyncio.Future()
            future_e = asyncio.Future()
            tasks = [
                self.consent_stats(future_a),
                self.transaction_data(future_b),
                self.pregnant_delivery_stats(future_c),
                self.offstudy_stats(future_d),
                self.weekly_edd_stats(future_e)
            ]
            loop.run_until_complete(asyncio.wait(tasks))
            self.response_data.update(future_a.result())
            self.response_data.update(future_b.result())
            self.response_data.update(future_c.result())
            self.response_data.update(future_d.result())
            self.response_data.update(future_e.result())
            loop.close()
            print('****{}*****'.format(self.response_data))
            return HttpResponse(json.dumps(self.response_data), content_type='application/json')
        return self.render_to_response(context)

    @asyncio.coroutine
    def consent_stats(self, future):
        response_data = {}
        columns = ['id', 'is_verified', 'modified']
        qs = MaternalConsent.objects.values_list(*columns).all()
        consents = pd.DataFrame(list(qs), columns=columns)
        if not consents.empty:
            response_data.update({
                'consented': int(consents['id'].count()),
                'verified_consents': int(consents.query('is_verified == True')['is_verified'].count()),
                'not_verified_consents': int(consents.query('is_verified == False')['is_verified'].count()),
            })
            d = date.today()
            local_date = tz.localize(datetime(d.year, d.month, d.day, 0, 0, 0))
            consented_today = consents[(consents['modified'] >= local_date)]
            response_data.update({
                'consented_today': int(consented_today['id'].count()),
            })
        future.set_result(self.verified_response_data(response_data))

    @asyncio.coroutine
    def pregnant_delivery_stats(self, future):
        response_data = {}
        columns = ['id', 'valid_regiment_duration', 'modified']
        qs = MaternalLabourDel.objects.values_list(*columns).all()
        deliveries = pd.DataFrame(list(qs), columns=columns)
        if not deliveries.empty:
            response_data.update({
                'delivered': int(deliveries['id'].count()),
                'delivered_po': int(deliveries.query(
                    'valid_regiment_duration != N/A')['valid_regiment_duration'].count()),
                'delivered_neg': int(deliveries.query(
                    'valid_regiment_duration == N/A')['valid_regiment_duration'].count()),
            })
        future.set_result(self.verified_response_data(response_data))

    @asyncio.coroutine
    def offstudy_stats(self, future):
        response_data = {}
        columns = ['id', 'modified']
        qs = MaternalOffStudy.objects.values_list(*columns).all()
        deliveries = pd.DataFrame(list(qs), columns=columns)
        if not deliveries.empty:
            response_data.update({
                'offstudy': int(deliveries['id'].count())
            })
        future.set_result(self.verified_response_data(response_data))

    @asyncio.coroutine
    def calling_stats(self):
        pass

    @asyncio.coroutine
    def weekly_edd_stats(self, future):
        response_data = {}
        columns = ['id', 'edd_confirmed', 'modified']
        qs = MaternalUltraSoundInitial.objects.values_list(*columns).all()
        ultrasounds = pd.DataFrame(list(qs), columns=columns)
        d = date.today()
        week_later = d + relativedelta(weeks=1)
        week_before = d - relativedelta(weeks=1)
        weekly_edd = ultrasounds[(ultrasounds['edd_confirmed'] >= week_before)]
        weekly_edd = weekly_edd[(weekly_edd['edd_confirmed'] <= week_later)]
        if not ultrasounds.empty:
            response_data.update({
                'edd_1week': int(weekly_edd['id'].count())
            })
        future.set_result(self.verified_response_data(response_data))

    @asyncio.coroutine
    def transaction_stats(self, future):
        response_data = {}
        tx = OutgoingTransaction.objects.filter(is_consumed_server=False)
        if tx:
            response_data.update(pending_transactions=tx.count())
        future.set_result(self.verified_response_data(response_data))

    #######################
    #STOP
    ######################
    @asyncio.coroutine
    def contact_data(self, future):
        response_data = {}
        calls = Call.objects.filter(call_attempts__gte=1)
        if calls:
            response_data.update(contacted_retry=calls.exclude(call_status=CLOSED).count())
            calls.filter(**self.modified_option)
            if calls:
                response_data.update(contacted_today=calls.count())
        future.set_result(self.verified_response_data(response_data))

    @asyncio.coroutine
    def transaction_data(self, future):
        response_data = {}
        tx = OutgoingTransaction.objects.filter(is_consumed_server=False)
        if tx:
            response_data.update(pending_transactions=tx.count())
        future.set_result(self.verified_response_data(response_data))

    @property
    def modified_option(self):
        d = date.today()
        local_date = tz.localize(datetime(d.year, d.month, d.day, 0, 0, 0))
        return {'modified__gte': local_date}

    def verified_response_data(self, response_data):
        diff = set(response_data.keys()).difference(set(self.response_data.keys()))
        if diff:
            raise KeyError('Invalid key or keys in response data dictionary. Got {}'.format(diff))
        return response_data

    @property
    def response_data(self):
        if not self._response_data:
            self._response_data = dict(zip(self.columns, len(self.columns) * [0]))
        return self._response_data
