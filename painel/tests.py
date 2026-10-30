from decimal import Decimal
from unittest.mock import MagicMock, patch

import requests
from django.test import TestCase
from django.urls import reverse

from .models import RegistroCotacao


def resposta_falsa(json_data, status=200):
    resposta = MagicMock()
    resposta.json.return_value = json_data
    if status >= 400:
        resposta.raise_for_status.side_effect = requests.exceptions.HTTPError(
            f'HTTP {status}'
        )
    return resposta


class ConsultarCotacaoTest(TestCase):
    @patch('painel.views.requests.get')
    def test_sucesso_salva_registro(self, get):
        get.return_value = resposta_falsa({'USDBRL': {'bid': '5.1234'}})
        resposta = self.client.get(reverse('consultar'))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'Cotação registrada')
        registro = RegistroCotacao.objects.get()
        self.assertEqual(registro.valor, Decimal('5.1234'))
        self.assertEqual(get.call_args.kwargs['timeout'], 5)

    @patch('painel.views.requests.get', side_effect=requests.exceptions.Timeout())
    def test_timeout_nao_quebra_a_pagina(self, get):
        resposta = self.client.get(reverse('consultar'))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'Não foi possível consultar')
        self.assertEqual(RegistroCotacao.objects.count(), 0)

    @patch('painel.views.requests.get')
    def test_erro_http_500_da_api(self, get):
        get.return_value = resposta_falsa({}, status=500)
        resposta = self.client.get(reverse('consultar'))
        self.assertContains(resposta, 'Não foi possível consultar')
        self.assertEqual(RegistroCotacao.objects.count(), 0)

    @patch('painel.views.requests.get')
    def test_formato_inesperado(self, get):
        get.return_value = resposta_falsa({'outra': 'coisa'})
        resposta = self.client.get(reverse('consultar'))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'formato inesperado')
        self.assertEqual(RegistroCotacao.objects.count(), 0)

    def test_template_usa_fetch_e_catch(self):
        with patch(
            'painel.views.requests.get',
            side_effect=requests.exceptions.ConnectionError(),
        ):
            resposta = self.client.get(reverse('consultar'))
        self.assertContains(resposta, "fetch('/api/historico/')")
        self.assertContains(resposta, '.catch(')

class HistoricoAPITest(TestCase):
    def test_ordem_do_mais_recente_ao_mais_antigo(self):
        registro_antigo = RegistroCotacao.objects.create(
            valor=Decimal('5.0000')
        )
        registro_meio = RegistroCotacao.objects.create(
            valor=Decimal('5.1000')
        )
        registro_recente = RegistroCotacao.objects.create(
            valor=Decimal('5.2000')
        )
        resposta = self.client.get(reverse('api-historico'))
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(
            [item['id'] for item in resposta.json()],
            [registro_recente.id, registro_meio.id, registro_antigo.id],
        )

    def test_somente_leitura(self):
        resposta = self.client.post(reverse('api-historico'), {'valor': '1'})
        self.assertEqual(resposta.status_code, 405)

    def test_lista_vazia(self):
        self.assertEqual(
            self.client.get(reverse('api-historico')).json(),
            [],
        )