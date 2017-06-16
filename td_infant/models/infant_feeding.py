from django.db import models

from edc_base.model.fields.custom_fields import OtherCharField
from edc_base.model.validators import date_not_future
from edc_constants.choices import YES_NO, YES_NO_NA, YES_NO_UNSURE_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_visit_schedule.models import VisitDefinition

from tshilo_dikotla.choices import COWS_MILK, TIMES_BREASTFED, WATER_USED

from .infant_crf_model import InfantCrfModel


class InfantFeeding(InfantCrfModel):

    """ A model completed by the user on the infant's feeding. """

    last_att_sche_visit = models.DateField(
        verbose_name=("When was the last attended scheduled visit where an infant feeding form"
                      " was completed? "),
        blank=True,
        null=True)

    other_feeding = models.CharField(
        verbose_name=("Since the last attended scheduled visit where an infant feeding form"
                      " was completed, has the child received any formula milk or "
                      " liquids other than breast-milk? "),
        max_length=3,
        choices=YES_NO,
        help_text="If Formula Feeding or received any other foods or liquids answer YES.")

    formula_intro_occur = models.CharField(
        verbose_name=(
            "Since the last attended scheduled visit has the child received any solid foods?"),
        max_length=3,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE)

    formula_intro_date = models.DateField(
        verbose_name=("Date participant first received formula milk (or other foods or liquids)"
                      "since last attended scheduled visit where an infant feeding form"
                      " was completed"),
        blank=True,
        null=True)

    took_formula = models.CharField(
        verbose_name="Since the last attended scheduled visit where an infant feeding form was completed "
                     "did the participant take Formula?",
        max_length=10,
        choices=YES_NO_UNSURE_NA,
        help_text="If formula feeding since last visit answer YES",
        default=NOT_APPLICABLE)

    is_first_formula = models.CharField(
        verbose_name="Is this the first reporting of infant formula use?",
        max_length=15,
        choices=YES_NO,
        blank=True,
        null=True,)

    date_first_formula = models.DateField(
        verbose_name="Date infant formula introduced?",
        validators=[date_not_future, ],
        blank=True,
        null=True,
        help_text="provide date if this is first reporting of infant formula")

    est_date_first_formula = models.CharField(
        verbose_name="Is date infant formula introduced estimated?",
        max_length=15,
        choices=YES_NO,
        blank=True,
        null=True,
        help_text="provide date if this is first reporting of infant formula")

    water = models.CharField(
        verbose_name="Since the last attended scheduled visit where an infant feeding form was completed did "
                     "the participant take Water?",
        max_length=10,
        choices=YES_NO_UNSURE_NA,
        help_text="Not as part of formula milk",
        default=NOT_APPLICABLE)

    juice = models.CharField(
        verbose_name="Since the last attended scheduled visit where an infant feeding form was completed "
                     "did the participant take Juice?",
        max_length=10,
        choices=YES_NO_UNSURE_NA,
        help_text="If you answered YES to Q3 you must answer YES, NO or NOT SURE to this question, "
                  "you may not answer \'Not Applicable\'.",
        default=NOT_APPLICABLE)

    cow_milk = models.CharField(
        verbose_name="Since the last attended scheduled visit where an infant feeding form was completed "
                     "did the participant take Cow's milk?",
        max_length=15,
        choices=YES_NO_UNSURE_NA,
        default=NOT_APPLICABLE)

    cow_milk_yes = models.CharField(
        verbose_name="If 'Yes', cow's milk was...",
        max_length=25,
        choices=COWS_MILK,
        default=NOT_APPLICABLE)

    other_milk = models.CharField(
        verbose_name="Since the last attended scheduled visit where an infant feeding form was "
                     "completed did the participant take Other animal milk?",
        max_length=15,
        choices=YES_NO_UNSURE_NA,
        default=NOT_APPLICABLE)

    other_milk_animal = OtherCharField(
        verbose_name="If 'Yes' specify which animal:",
        max_length=35,
        blank=True,
        null=True)

    milk_boiled = models.CharField(
        verbose_name="Was milk boiled?",
        max_length=10,
        choices=YES_NO_UNSURE_NA,
        default=NOT_APPLICABLE)

    fruits_veg = models.CharField(
        verbose_name="Since the last attended scheduled visit where an infant feeding form was completed "
                     "did the participant take Fruits/vegetables",
        max_length=10,
        choices=YES_NO_UNSURE_NA,
        default=NOT_APPLICABLE)

    cereal_porridge = models.CharField(
        verbose_name="Since the last attended scheduled visit where an infant feeding form was completed "
                     "did the participant take Cereal/porridge?",
        max_length=12,
        choices=YES_NO_UNSURE_NA,
        default=NOT_APPLICABLE)

    solid_liquid = models.CharField(
        verbose_name="Since the last attended scheduled visit where an infant feeding form was "
                     "completed did the participant take Other solids and liquids",
        max_length=10,
        choices=YES_NO_UNSURE_NA,
        default=NOT_APPLICABLE)

    rehydration_salts = models.CharField(
        verbose_name="Since the last attended scheduled visit where an infant feeding form was completed "
                     "did the participant take Oral rehydaration salts",
        max_length=12,
        choices=YES_NO_UNSURE_NA,
        default=NOT_APPLICABLE)

    water_used = models.CharField(
        verbose_name="What water do you usually use to prepare the participant's milk?",
        max_length=50,
        choices=WATER_USED,
        default=NOT_APPLICABLE)

    water_used_other = OtherCharField(
        verbose_name="If 'other', specify",
        max_length=35,
        blank=True,
        null=True)

    ever_breastfeed = models.CharField(
        verbose_name="Since the last attended scheduled visit,did the infant ever breast-feed",
        max_length=3,
        choices=YES_NO)

    complete_weaning = models.CharField(
        verbose_name="If 'NO', did complete weaning from breast milk take place before the last "
                     "attended scheduled visit?",
        max_length=3,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE)

    weaned_completely = models.CharField(
        verbose_name=("Is the participant currently completely weaned from breast milk"
                      " (at least 72 hours without breast feeding,no intention to re-start)?"),
        max_length=3,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE)

    most_recent_bm = models.DateField(
        verbose_name="Date of most recent breastfeeding ",
        blank=True,
        null=True)

    times_breastfed = models.CharField(
        max_length=50,
        verbose_name=("Between the last attended scheduled visit where an infant feeding form"
                      " was completed and date of most recent breastfeeding,how often did"
                      " the participant receive breast milk for feeding?"),
        choices=TIMES_BREASTFED,
        default=NOT_APPLICABLE)

    comments = models.TextField(
        max_length=200,
        verbose_name="List any comments about participant's feeding that are not answered above",
        blank=True,
        null=True)

    def save(self, *args, **kwargs):
        if self.previous_infant_feeding:
            self.last_att_sche_visit = self.previous_infant_feeding
        super(InfantFeeding, self).save(*args, **kwargs)

    def previous_infant_instance(self, infant_visit):
        """ Returns previous infant visit. """
        from .infant_visit import InfantVisit
        from edc_appointment.models import Appointment
        visit = ['2000', '2010', '2030', '2060', '2090', '2120']
        try:
            registered_subject = infant_visit.appointment.registered_subject
            previous_visit_code = visit[
                visit.index(self.infant_visit.appointment.visit_definition.code) - 1]
            previous_appointment = Appointment.objects.get(registered_subject=registered_subject,
                                                           visit_definition__code=previous_visit_code)
            return InfantVisit.objects.get(appointment=previous_appointment)
        except Appointment.DoesNotExist:
            return None
        except InfantVisit.DoesNotExist:
            return None
        except AttributeError:
            return None

    @property
    def previous_infant_feeding(self):
        """ Return previous infant feeding from. """
        visit_def = VisitDefinition.objects.all()
        visit = []
        for x in visit_def:
            visit.append(x.code)

        if not (self.infant_visit.appointment.visit_definition.code in ['2000', '2010']):
            prev_visit_index = visit.index(
                self.infant_visit.appointment.visit_definition.code) - 1
            registered_subject = self.infant_visit.appointment.registered_subject
            while prev_visit_index > 0:
                infant_feeding = InfantFeeding.objects.filter(
                    infant_visit__appointment__registered_subject=registered_subject,
                    infant_visit__appointment__visit_definition__code=visit[
                        prev_visit_index]
                ).order_by('-created', '-infant_visit__appointment__visit_instance').first()
                if infant_feeding:
                    return infant_feeding.report_datetime.date()
                prev_visit_index = prev_visit_index - 1
        return None

    class Meta:
        app_label = 'td_infant'
        verbose_name = "Infant Feeding"
        verbose_name_plural = "Infant Feeding"
