from django.db import models

from ..maternal_choices import POS_NEG_IND

class RapidTestMixin(models.Model):
    
    last_rapid_test_date = models.DateField(
        verbose_name='What was the date of the last HIV Rapid Test of the participant?'
    )

    rapid_test_result = models.CharField(
        choices=POS_NEG_IND,
        verbose_name="What was the result of the last HIV Rapid Test of the participant?",
        max_length=100,
        help_text="If positive or indeterminate notify study coordinator. Mother should be taken off "
            "study if >33 weeks. If indeterminate, complete PRN lab requisition for Maternal HIV ELISA.")

    class Meta:
        abstract = True