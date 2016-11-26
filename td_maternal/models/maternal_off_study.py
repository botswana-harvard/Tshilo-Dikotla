from edc_base.model.models import BaseUuidModel, HistoricalRecords
from edc_offstudy.model_mixins import OffstudyModelMixin


class MaternalOffStudy(OffstudyModelMixin, BaseUuidModel):

    """ A model completed by the user on the visit when the mother is taken off-study. """

    history = HistoricalRecords()

    class Meta:
        app_label = 'td_maternal'
        verbose_name = "Maternal Off Study"
        consent_model = 'td_maternal.maternalconsent'
