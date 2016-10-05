import factory

from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from edc_constants.constants import CONTINUOUS
from .registered_subject_factory import RegisteredSubjectFactory
from edc_constants.choices import YES, NO, POS, NEG, NOT_APPLICABLE

from td_maternal.models import MaternalLifetimeArvHistory
from tshilo_dikotla.constants import LIVE, STILL_BIRTH

from ..factories import MaternalVisitFactory


class MaternalArvHistoryFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalLifetimeArvHistory

    maternal_visit = MaternalVisitFactory
    report_datetime = timezone.now()
    haart_start_date = datetime.today() - relativedelta(months=9)
    is_date_estimated = '-'
    preg_on_haart = YES
    haart_changes = 0
    prior_preg = CONTINUOUS
    #prior_arv: [prior_arv.id],