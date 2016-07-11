from django.contrib import admin

from .models import (
    ChronicConditions, Contraceptives, DiseasesAtEnrollment, HouseholdGoods,
    PriorArv, AutopsyInfoSource, Supplements, InfantVaccines,
    HealthCond, DelComp, ObComp, LabDelDx, MaternalRelatives, MaternalMedications, Rations, Foods,
    Malformations, MaternalDiagnoses, DeliveryComplications, MaternalHospitalization)


class RationsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Rations, RationsAdmin)


class FoodsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Foods, FoodsAdmin)


class ChronicConditionsAdmin(admin.ModelAdmin):
    pass
admin.site.register(ChronicConditions, ChronicConditionsAdmin)


class DeliveryComplicationsAdmin (admin.ModelAdmin):
    pass
admin.site.register(DeliveryComplications, DeliveryComplicationsAdmin)


class ContraceptivesAdmin(admin.ModelAdmin):
    pass
admin.site.register(Contraceptives, ContraceptivesAdmin)


class DiseasesAtEnrollmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(DiseasesAtEnrollment, DiseasesAtEnrollmentAdmin)


class HouseholdGoodsAdmin(admin.ModelAdmin):
    pass
admin.site.register(HouseholdGoods, HouseholdGoodsAdmin)


class MaternalMedicationsAdmin(admin.ModelAdmin):
    pass
admin.site.register(MaternalMedications, MaternalMedicationsAdmin)


class PriorArvAdmin(admin.ModelAdmin):
    pass
admin.site.register(PriorArv, PriorArvAdmin)


class AutopsyInfoSourceAdmin(admin.ModelAdmin):
    pass
admin.site.register(AutopsyInfoSource, AutopsyInfoSourceAdmin)


class SupplementsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Supplements, SupplementsAdmin)


class InfantVaccinesAdmin(admin.ModelAdmin):
    pass
admin.site.register(InfantVaccines, InfantVaccinesAdmin)


class HealthCondAdmin(admin.ModelAdmin):
    pass
admin.site.register(HealthCond, HealthCondAdmin)


class DelCompAdmin(admin.ModelAdmin):
    pass
admin.site.register(DelComp, DelCompAdmin)


class ObCompAdmin(admin.ModelAdmin):
    pass
admin.site.register(ObComp, ObCompAdmin)


class LabDelDxAdmin(admin.ModelAdmin):
    pass
admin.site.register(LabDelDx, LabDelDxAdmin)


class MaternalRelativesAdmin(admin.ModelAdmin):
    pass
admin.site.register(MaternalRelatives, MaternalRelativesAdmin)


class MalformationsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Malformations, MalformationsAdmin)


class MaternalDiagnosesAdmin(admin.ModelAdmin):
    pass
admin.site.register(MaternalDiagnoses, MaternalDiagnosesAdmin)


class MaternalHospitalizationAdmin(admin.ModelAdmin):
    pass
admin.site.register(MaternalHospitalization, MaternalHospitalizationAdmin)
