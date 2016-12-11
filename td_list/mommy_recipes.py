from .models import WhoAdultDiagnosis, AdultDiagnoses, DeliveryComplications
from edc_constants.constants import NOT_APPLICABLE
from model_mommy.recipe import Recipe, seq

whoadultdiagnosis = Recipe(
    WhoAdultDiagnosis,
    name=NOT_APPLICABLE,
    short_name=NOT_APPLICABLE,
    display_index=seq(1),
)

adultdiagnoses = Recipe(
    AdultDiagnoses,
    name=NOT_APPLICABLE,
    short_name=NOT_APPLICABLE,
    display_index=seq(1),
)


deliverycomplications = Recipe(
    DeliveryComplications,
    name=NOT_APPLICABLE,
    short_name=NOT_APPLICABLE)