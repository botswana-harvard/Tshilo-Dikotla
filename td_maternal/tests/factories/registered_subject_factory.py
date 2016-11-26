import factory

from td.models import RegisteredSubject


class RegisteredSubjectFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = RegisteredSubject

    identity = factory.Sequence(lambda n: '11111111{0}'.format(n))
    identity_type = 'OMANG'
    subject_type = 'subject'
