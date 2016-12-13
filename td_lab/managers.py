from django.db import models


class AliquotProcessingManager(models.Manager):

    def get_by_natural_key(self, aliquot_identifier, profile_name):
        return self.get(aliquot__aliquot_identifier=aliquot_identifier, profile__name=profile_name)


class OrderManager(models.Manager):

    def get_by_natural_key(self, order_identifier):
        return self.get(order_identifier=order_identifier)


class OrderItemManager(models.Manager):

    def get_by_natural_key(self, order_identifier):
        return self.get(order_identifier=order_identifier)


class PackingListManager(models.Manager):

    def get_by_natural_key(self, timestamp):
        return self.get(timestamp=timestamp)


class PackingListItemManager(models.Manager):

    def get_by_natural_key(self, item_reference):
        return self.get(item_reference=item_reference)


class PanelManager(models.Manager):

    def get_by_natural_key(self, name):
        return self.get(name=name)


class ProfileManager(models.Manager):

    def get_by_natural_key(self, name):
        return self.get(name=name)


class ResultManager(models.Manager):

    def get_by_natural_key(self, result_identifier, subject_identifier):
        return self.get(result_identifier=result_identifier, subject_identifier=subject_identifier)


class ReceiveManager(models.Manager):

    def get_by_natural_key(self, receive_identifier):
        return self.get(receive_identifier=receive_identifier)


class ResultItemManager(models.Manager):

    def get_by_natural_key(self, subject_identifier):
        return self.get(subject_identifier=subject_identifier)
