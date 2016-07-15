from django.db.models import Manager


class OrderManager(Manager):

    def get_by_natural_key(self, order_identifier):
        return self.get(order_identifier=order_identifier)


class OrderItemManager(Manager):

    def get_by_natural_key(self, order_identifier):
        return self.get(order_identifier=order_identifier)
