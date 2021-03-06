from django.contrib import admin

from ..models import MaternalContraception
from ..forms import MaternalContraceptionForm

from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalContraceptionAdmin(BaseMaternalModelAdmin):

    form = MaternalContraceptionForm

    fields = ('maternal_visit',
              'more_children',
              'next_child',
              'contraceptive_partner',
              'contraceptive_relative',
              'contraceptive_relative_other',
              'influential_decision_making',
              'influential_decision_making_other',
              'uses_contraceptive',
              'contraceptive_startdate',
              'contr',
              'contr_other',
              'another_pregnancy',
              'pregnancy_date',
              'pap_smear',
              'pap_smear_date',
              'pap_smear_estimate',
              'pap_smear_result',
              'pap_smear_result_status',
              'pap_smear_result_abnormal',
              'date_notified',
              'srh_referral')
    radio_fields = {'more_children': admin.VERTICAL,
                    'next_child': admin.VERTICAL,
                    'contraceptive_partner': admin.VERTICAL,
                    'influential_decision_making': admin.VERTICAL,
                    'uses_contraceptive': admin.VERTICAL,
                    'another_pregnancy': admin.VERTICAL,
                    'pap_smear': admin.VERTICAL,
                    'pap_smear_estimate': admin.VERTICAL,
                    'pap_smear_result': admin.VERTICAL,
                    'pap_smear_result_status': admin.VERTICAL,
                    'srh_referral': admin.VERTICAL}
    filter_horizontal = ('contraceptive_relative', 'contr',)

admin.site.register(MaternalContraception, MaternalContraceptionAdmin)
