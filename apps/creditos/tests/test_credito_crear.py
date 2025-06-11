import io
import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from apps.genericas.models import Valores_generica
from personas.models import Persona
from creditos.models import Credito


@pytest.mark.django_db
def test_credito_crear_icetex_valido(usuario, estado_credito, periodo, tipo_credito_icetex):
    client = APIClient()
    client.force_authenticate(user=usuario)

    archivo = io.BytesIO(b"archivo de prueba")
    archivo.name = "archivo.pdf"

    entidad_icetex = Valores_generica.objects.create(codigo='Ent_Def', estado=1, valora='icetex')

    data = {
        "telefono": "1234567",
        "celular": "3000000000",
        "tipo": tipo_credito_icetex.id,
        "categoria": "1",
        "total": "0",  # No requiere archivos
        "archivo0": archivo,
        "solicitudes": "",
        "codigo_icetex_dev": "",
        "nombre_titular_dev": "",
        "numero_documento_dev": "",
        "nombre_entidad_dev": "",
        "solicitud_estado_finan": ""
    }

    response = client.post("/api/creditos/crear/", data, format='multipart')

    assert response.status_code == 200
    assert "titulo" in response.data
    assert response.data["titulo"] == "Datos Enviados"


@pytest.mark.django_db
def test_credito_crear_falta_celular(usuario, estado_credito, periodo, tipo_credito_icetex):
    client = APIClient()
    client.force_authenticate(user=usuario)

    archivo = io.BytesIO(b"archivo de prueba")
    archivo.name = "archivo.pdf"

    Valores_generica.objects.create(codigo='Ent_Def', estado=1, valora='icetex')

    data = {
        "telefono": "1234567",
        "celular": "",  # Celular vacío
        "tipo": tipo_credito_icetex.id,
        "categoria": "1",
        "total": "1",
        "archivo0": archivo,
        "solicitudes": ""
    }

    response = client.post("/api/creditos/crear/", data, format='multipart')
    assert response.status_code == 302
    assert response.data["titulo"] == "Ingrese numero de celular."


@pytest.mark.django_db
def test_credito_crear_celular_no_numerico(usuario, estado_credito, periodo, tipo_credito_icetex):
    client = APIClient()
    client.force_authenticate(user=usuario)

    archivo = io.BytesIO(b"archivo de prueba")
    archivo.name = "archivo.pdf"

    Valores_generica.objects.create(codigo='Ent_Def', estado=1, valora='icetex')

    data = {
        "telefono": "1234567",
        "celular": "abcd123",  # No es numérico
        "tipo": tipo_credito_icetex.id,
        "categoria": "1",
        "total": "1",
        "archivo0": archivo,
        "solicitudes": ""
    }

    response = client.post("/api/creditos/crear/", data, format='multipart')
    assert response.status_code == 302
    assert response.data["titulo"] == "Ingrese numero de celular."


@pytest.mark.django_db
def test_credito_crear_falta_documentos_sin_icetex(usuario, estado_credito, periodo):
    client = APIClient()
    client.force_authenticate(user=usuario)

    tipo = Valores_generica.objects.create(codigo='sol_cred', estado=1, valora='otra')

    data = {
        "telefono": "1234567",
        "celular": "3000000000",
        "tipo": tipo.id,
        "categoria": "1",
        "total": "0",  # Se esperan documentos pero no hay
        "solicitudes": ""
    }

    response = client.post("/api/creditos/crear/", data, format='multipart')
    assert response.status_code == 302
    assert response.data["titulo"] == "Debe cargar los documentos para continuar."


@pytest.mark.django_db
def test_credito_crear_credito_ya_existente(usuario, estado_credito, periodo, tipo_credito_icetex):
    # Se crea un crédito activo que simula conflicto
    Credito.objects.create(
        usuario_registro_id=usuario.id,
        estado_actual=Valores_generica.objects.create(codigo="Cre_Pen", estado=1),
        tipo=tipo_credito_icetex,
        estado=1,
        periodo=periodo.nombre,
    )

    client = APIClient()
    client.force_authenticate(user=usuario)

    archivo = io.BytesIO(b"archivo de prueba")
    archivo.name = "archivo.pdf"

    Valores_generica.objects.create(codigo='Ent_Def', estado=1, valora='icetex')

    data = {
        "telefono": "1234567",
        "celular": "3000000000",
        "tipo": tipo_credito_icetex.id,
        "categoria": "1",
        "total": "0",
        "solicitudes": ""
    }

    response = client.post("/api/creditos/crear/", data, format='multipart')
    assert response.status_code == 302
    assert "solicitud pendiente" in response.data["titulo"]
