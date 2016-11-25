from edc_consent.managers import ConsentManager


class MaternalConsentManager(ConsentManager):

    def get_by_natural_key(self, subject_identifier, identity, version):
        return self.get(subject_identifier=subject_identifier, identity=identity, version=version)
