from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Cliente, Chamado


class ChamadoFlowTest(TestCase):
    """Testa fluxo básico: criar perfil de cliente e abrir um chamado."""

    def setUp(self):
        User = get_user_model()
        # criar usuário cliente
        self.user = User.objects.create_user(username='cliente1', email='cli@example.com', password='pass1234')
        # criar usuário contador (staff)
        self.contador = User.objects.create_user(username='contador1', email='cont@example.com', password='pass1234', is_staff=True)

        # criar perfil Cliente
        self.cliente = Cliente.objects.create(user=self.user, contador_responsavel=self.contador)

        self.client = Client()

    def test_criar_chamado_via_model(self):
        chamado = Chamado.objects.create(
            cliente=self.cliente,
            titulo='Solicitação de NF',
            tipo_solicitacao='nota_fiscal',
            descricao='Preciso emitir nota fiscal para venda X.'
        )
        self.assertIn(chamado, self.cliente.chamados.all())

    def test_abrir_chamado_via_view(self):
        # login do cliente
        logged = self.client.login(username='cliente1', password='pass1234')
        self.assertTrue(logged)

        url = reverse('support:abrir_chamado')
        data = {
            'titulo': 'Pedido de Documentos',
            'tipo_solicitacao': 'documentos',
            'descricao': 'Por favor, envie os documentos da empresa.'
        }
        resp = self.client.post(url, data, follow=True)
        self.assertEqual(resp.status_code, 200)

        # verificar que foi criado
        chamados = self.cliente.chamados.filter(titulo='Pedido de Documentos')
        self.assertTrue(chamados.exists())
from django.test import TestCase

# Create your tests here.
