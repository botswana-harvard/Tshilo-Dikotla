from edc_lab.lab_packing.forms import BasePackingListForm, BasePackingListItemForm

from ..models import MaternalRequisition, PackingList, PackingListItem, Aliquot


class PackingListForm (BasePackingListForm):

    def clean(self):
        self.requisition = [MaternalRequisition, Aliquot]
        return super(PackingListForm, self).clean()

    class Meta:
        model = PackingList
        fields = '__all__'


class PackingListItemForm (BasePackingListItemForm):

    def clean(self):
        self.requisition = [MaternalRequisition, Aliquot]
        return super(BasePackingListItemForm, self).clean()

    class Meta:
        model = PackingListItem
        fields = '__all__'
