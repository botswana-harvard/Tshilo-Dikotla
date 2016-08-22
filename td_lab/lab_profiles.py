from edc_lab.lab_profile.classes import site_lab_profiles

from edc_lab.lab_profile.classes import LabProfile

from .models import (Aliquot, AliquotType, Receive, MaternalRequisition, InfantRequisition,
                     AliquotProfile, AliquotProfileItem, Panel)


class BaseTshiloDikotlaProfile(LabProfile):
    aliquot_model = Aliquot
    aliquot_type_model = AliquotType
    profile_model = AliquotProfile
    profile_item_model = AliquotProfileItem
    receive_model = Receive
    panel_model = Panel


class MaternalProfile(BaseTshiloDikotlaProfile):
    requisition_model = MaternalRequisition
    name = MaternalRequisition._meta.object_name
site_lab_profiles.register(MaternalProfile)


class InfantProfile(BaseTshiloDikotlaProfile):
    requisition_model = InfantRequisition
    name = InfantRequisition._meta.object_name
site_lab_profiles.register(InfantProfile)
