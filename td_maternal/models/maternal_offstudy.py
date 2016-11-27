from edc_base.model.models import BaseUuidModel, HistoricalRecords
from edc_offstudy.model_mixins import OffstudyModelMixin

from edc_offstudy.model_mixins import OffstudyModelManager


class MaternalOffstudy(OffstudyModelMixin, BaseUuidModel):

    """ A model completed by the user on the visit when the mother is taken off-study. """

    objects = OffstudyModelManager()

    history = HistoricalRecords()

    class Meta:
        app_label = 'td_maternal'
        verbose_name = "Maternal Offstudy"
        consent_model = 'td_maternal.maternalconsent'
