from edc_base.model.models import ListModelMixin


class DiseasesAtEnrollment (ListModelMixin):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Diseases At Enrollment"
        verbose_name_plural = "Diseases At Enrollment"
