from django.db.models import Manager


class PackingListManager(Manager):

    def get_by_natural_key(self, timestamp):
        return self.get(timestamp=timestamp)


class PackingListItemManager(Manager):

    def get_by_natural_key(self, item_reference):
        return self.get(item_reference=item_reference)
