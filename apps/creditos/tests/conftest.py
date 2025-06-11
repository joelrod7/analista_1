# creditos/tests/conftest.py
import pytest
import factory
from django.contrib.auth.models import User
from apps.genericas.models import Valores_generica
from creditos.models import Credito, Estado, Adjunto, Solicitud
from personas.models import Persona

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda o: f'{o.username}@test.com')
    password = factory.PostGenerationMethodCall('set_password', '1234')

class PersonaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Persona

    identificacion = factory.Sequence(lambda n: f'12345{n}')
    nombre = "Joel Rodríguez"
    estado = 1
    telefono = "1234567"
    celular = "3000000000"
    correo = factory.LazyAttribute(lambda o: f'{o.nombre.lower().replace(" ", "_")}@test.com')

class ValoresGenericaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Valores_generica

    codigo = factory.Sequence(lambda n: f'codigo{n}')
    nombre = factory.Sequence(lambda n: f'Nombre {n}')
    estado = 1
    valora = "icetex"

@pytest.fixture
def usuario(db):
    user = UserFactory()
    PersonaFactory(pk=user.id)  # Persona relacionada con ID de usuario
    return user

@pytest.fixture
def estado_credito(db):
    return ValoresGenericaFactory(codigo='Cre_Env')

@pytest.fixture
def periodo(db):
    return ValoresGenericaFactory(codigo='Per_Cre', nombre='2025-1')

@pytest.fixture
def tipo_credito_icetex(db):
    return ValoresGenericaFactory(codigo='sol_cred', valora='icetex')
