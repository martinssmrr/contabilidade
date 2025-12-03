"""
Testes unitários para o módulo de Documentos de Clientes.

Este módulo testa:
- Criação do modelo DocumentoCliente
- Disparo do signal
- Execução da task de e-mail
- Envio do e-mail

Autor: Sistema Vetorial
Data: 2025-12-02
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from unittest.mock import patch, MagicMock
from apps.documents.models import DocumentoCliente
from apps.documents.tasks import enviar_email_notificacao_documento
from apps.services.email_service import EmailService, notificar_novo_documento

User = get_user_model()


class DocumentoClienteModelTest(TestCase):
    """Testes para o modelo DocumentoCliente."""
    
    def setUp(self):
        """Configurar dados de teste."""
        # Criar cliente
        self.cliente = User.objects.create_user(
            username='cliente_teste',
            email='cliente@example.com',
            first_name='João',
            last_name='Silva',
            is_staff=False
        )
        
        # Criar staff
        self.staff = User.objects.create_user(
            username='staff_teste',
            email='staff@example.com',
            first_name='Maria',
            last_name='Santos',
            is_staff=True
        )
        
        # Criar arquivo fake
        self.arquivo = SimpleUploadedFile(
            name='contrato_teste.pdf',
            content=b'PDF content here',
            content_type='application/pdf'
        )
    
    def test_criar_documento_cliente(self):
        """Testa criação básica do documento."""
        documento = DocumentoCliente.objects.create(
            cliente=self.cliente,
            arquivo=self.arquivo,
            tipo_documento='contrato_social',
            titulo='Contrato Social 2025',
            descricao='Contrato social da empresa XYZ',
            enviado_por=self.staff
        )
        
        self.assertEqual(documento.cliente, self.cliente)
        self.assertEqual(documento.tipo_documento, 'contrato_social')
        self.assertEqual(documento.titulo, 'Contrato Social 2025')
        self.assertFalse(documento.notificacao_enviada)
        self.assertFalse(documento.visualizado)
        self.assertIsNotNone(documento.data_envio)
    
    def test_properties_documento(self):
        """Testa properties do modelo."""
        documento = DocumentoCliente.objects.create(
            cliente=self.cliente,
            arquivo=self.arquivo,
            tipo_documento='certidao_negativa',
            titulo='Certidão Negativa Federal',
            enviado_por=self.staff
        )
        
        # Testar properties
        self.assertIn('.pdf', documento.nome_arquivo.lower())
        self.assertEqual(documento.extensao_arquivo, 'pdf')
        self.assertIn('B', documento.tamanho_arquivo)
        self.assertEqual(documento.tipo_documento_display, 'Certidão Negativa')
        self.assertIsInstance(documento.dias_desde_envio, int)
    
    def test_marcar_como_visualizado(self):
        """Testa marcação de visualização."""
        documento = DocumentoCliente.objects.create(
            cliente=self.cliente,
            arquivo=self.arquivo,
            tipo_documento='guia_impostos',
            titulo='DARF Mensal',
            enviado_por=self.staff
        )
        
        # Marcar como visualizado
        documento.marcar_como_visualizado()
        documento.refresh_from_db()
        
        self.assertTrue(documento.visualizado)
        self.assertIsNotNone(documento.data_visualizacao)
    
    def test_marcar_notificacao_enviada(self):
        """Testa marcação de notificação enviada."""
        documento = DocumentoCliente.objects.create(
            cliente=self.cliente,
            arquivo=self.arquivo,
            tipo_documento='relatorio_contabil',
            titulo='Relatório Mensal',
            enviado_por=self.staff
        )
        
        # Marcar notificação enviada
        documento.marcar_notificacao_enviada()
        documento.refresh_from_db()
        
        self.assertTrue(documento.notificacao_enviada)
        self.assertIsNotNone(documento.data_notificacao)


class DocumentoClienteSignalTest(TestCase):
    """Testes para o signal de notificação."""
    
    def setUp(self):
        """Configurar dados de teste."""
        self.cliente = User.objects.create_user(
            username='cliente_signal',
            email='cliente_signal@example.com',
            first_name='Pedro',
            last_name='Oliveira',
            is_staff=False
        )
        
        self.staff = User.objects.create_user(
            username='staff_signal',
            email='staff_signal@example.com',
            is_staff=True
        )
        
        self.arquivo = SimpleUploadedFile(
            name='documento_signal.pdf',
            content=b'Test content',
            content_type='application/pdf'
        )
    
    @patch('apps.documents.signals.enviar_email_notificacao_documento')
    def test_signal_dispara_task(self, mock_task):
        """Testa se o signal dispara a task do Celery."""
        # Criar documento (deve disparar signal)
        documento = DocumentoCliente.objects.create(
            cliente=self.cliente,
            arquivo=self.arquivo,
            tipo_documento='contrato_social',
            titulo='Teste Signal',
            enviado_por=self.staff
        )
        
        # Verificar se a task foi chamada
        mock_task.delay.assert_called_once_with(documento.id)
    
    @patch('apps.documents.signals.enviar_email_notificacao_documento')
    def test_signal_nao_dispara_em_update(self, mock_task):
        """Testa que signal não dispara em atualizações."""
        # Criar documento
        documento = DocumentoCliente.objects.create(
            cliente=self.cliente,
            arquivo=self.arquivo,
            tipo_documento='alteracao_contratual',
            titulo='Teste Update',
            enviado_por=self.staff
        )
        
        mock_task.reset_mock()
        
        # Atualizar documento
        documento.titulo = 'Título Atualizado'
        documento.save()
        
        # Task não deve ser chamada novamente
        mock_task.delay.assert_not_called()


class EmailServiceTest(TestCase):
    """Testes para o serviço de e-mail."""
    
    @patch('apps.services.email_service.send_mail')
    def test_enviar_email_simples(self, mock_send_mail):
        """Testa envio de e-mail simples."""
        mock_send_mail.return_value = 1
        
        email_service = EmailService()
        sucesso = email_service.enviar_email_simples(
            destinatario='teste@example.com',
            assunto='Teste',
            mensagem='Mensagem de teste'
        )
        
        self.assertTrue(sucesso)
        mock_send_mail.assert_called_once()
    
    @patch('apps.services.email_service.EmailMultiAlternatives')
    def test_enviar_email_com_template(self, mock_email):
        """Testa envio com template."""
        mock_instance = MagicMock()
        mock_email.return_value = mock_instance
        
        email_service = EmailService()
        
        # Mock do template rendering
        with patch('apps.services.email_service.render_to_string') as mock_render:
            mock_render.return_value = '<html>Test</html>'
            
            sucesso = email_service.enviar_email_com_template(
                destinatario='teste@example.com',
                assunto='Teste Template',
                template_html='emails/teste.html',
                contexto={'nome': 'João'}
            )
        
        self.assertTrue(sucesso)
        mock_instance.send.assert_called_once()
    
    @patch('apps.services.email_service.EmailService.enviar_email_com_template')
    def test_notificar_novo_documento(self, mock_enviar):
        """Testa função de notificação de documento."""
        mock_enviar.return_value = True
        
        sucesso = notificar_novo_documento(
            cliente_nome='João Silva',
            cliente_email='joao@example.com',
            tipo_documento='Contrato Social',
            titulo_documento='Contrato Social 2025',
            data_envio='02/12/2025',
            descricao='Descrição do documento'
        )
        
        self.assertTrue(sucesso)
        mock_enviar.assert_called_once()


class EmailTaskTest(TestCase):
    """Testes para as tasks do Celery."""
    
    def setUp(self):
        """Configurar dados de teste."""
        self.cliente = User.objects.create_user(
            username='cliente_task',
            email='cliente_task@example.com',
            first_name='Ana',
            last_name='Costa',
            is_staff=False
        )
        
        self.staff = User.objects.create_user(
            username='staff_task',
            email='staff_task@example.com',
            is_staff=True
        )
        
        arquivo = SimpleUploadedFile(
            name='documento_task.pdf',
            content=b'Task test',
            content_type='application/pdf'
        )
        
        self.documento = DocumentoCliente.objects.create(
            cliente=self.cliente,
            arquivo=arquivo,
            tipo_documento='balanco_patrimonial',
            titulo='Balanço Anual',
            enviado_por=self.staff
        )
    
    @patch('apps.documents.tasks.notificar_novo_documento')
    def test_task_enviar_email(self, mock_notificar):
        """Testa execução da task."""
        mock_notificar.return_value = True
        
        # Executar task diretamente (sem Celery)
        resultado = enviar_email_notificacao_documento(self.documento.id)
        
        self.assertTrue(resultado)
        mock_notificar.assert_called_once()
        
        # Verificar se documento foi atualizado
        self.documento.refresh_from_db()
        self.assertTrue(self.documento.notificacao_enviada)
    
    @patch('apps.documents.tasks.notificar_novo_documento')
    def test_task_documento_nao_existe(self, mock_notificar):
        """Testa task com documento inexistente."""
        resultado = enviar_email_notificacao_documento(99999)
        
        self.assertFalse(resultado)
        mock_notificar.assert_not_called()
    
    @patch('apps.documents.tasks.notificar_novo_documento')
    def test_task_cliente_sem_email(self, mock_notificar):
        """Testa task com cliente sem e-mail."""
        # Cliente sem e-mail
        cliente_sem_email = User.objects.create_user(
            username='sem_email',
            email='',
            is_staff=False
        )
        
        arquivo = SimpleUploadedFile(
            name='doc.pdf',
            content=b'test',
            content_type='application/pdf'
        )
        
        documento = DocumentoCliente.objects.create(
            cliente=cliente_sem_email,
            arquivo=arquivo,
            tipo_documento='outros',
            titulo='Documento Teste',
            enviado_por=self.staff
        )
        
        resultado = enviar_email_notificacao_documento(documento.id)
        
        self.assertFalse(resultado)
        mock_notificar.assert_not_called()


class IntegrationTest(TestCase):
    """Testes de integração completos."""
    
    def setUp(self):
        """Configurar dados de teste."""
        self.cliente = User.objects.create_user(
            username='cliente_integration',
            email='integration@example.com',
            first_name='Carlos',
            last_name='Mendes',
            is_staff=False
        )
        
        self.staff = User.objects.create_user(
            username='staff_integration',
            email='staff_integration@example.com',
            is_staff=True
        )
    
    @patch('apps.documents.tasks.enviar_email_notificacao_documento')
    @patch('apps.services.email_service.notificar_novo_documento')
    def test_fluxo_completo(self, mock_notificar, mock_task):
        """Testa fluxo completo: criação -> signal -> task -> e-mail."""
        mock_notificar.return_value = True
        mock_task.delay.return_value = MagicMock()
        
        arquivo = SimpleUploadedFile(
            name='fluxo_completo.pdf',
            content=b'Integration test',
            content_type='application/pdf'
        )
        
        # Criar documento (dispara signal)
        documento = DocumentoCliente.objects.create(
            cliente=self.cliente,
            arquivo=arquivo,
            tipo_documento='declaracao_ir',
            titulo='Declaração IR 2025',
            descricao='Declaração completa',
            enviado_por=self.staff
        )
        
        # Verificar se documento foi criado corretamente
        self.assertIsNotNone(documento.id)
        self.assertEqual(documento.cliente, self.cliente)
        self.assertFalse(documento.notificacao_enviada)
        
        # Verificar se task foi agendada
        mock_task.delay.assert_called_once_with(documento.id)
