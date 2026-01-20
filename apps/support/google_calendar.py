import os
import logging
from django.conf import settings
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/calendar']

class GoogleCalendarService:
    def __init__(self):
        self.creds = None
        self.service = None
        self.calendar_id = getattr(settings, 'GOOGLE_CALENDAR_ID', 'primary')
        self._authenticate()

    def _authenticate(self):
        """Autentica usando o arquivo de credenciais da conta de serviço"""
        creds_path = getattr(settings, 'GOOGLE_CALENDAR_CREDENTIALS', None)
        
        if not creds_path or not os.path.exists(creds_path):
            logger.warning(f"Arquivo de credenciais do Google Calendar não encontrado: {creds_path}")
            return

        try:
            self.creds = service_account.Credentials.from_service_account_file(
                creds_path, scopes=SCOPES
            )
            self.service = build('calendar', 'v3', credentials=self.creds)
        except Exception as e:
            logger.error(f"Erro ao autenticar no Google Calendar: {e}")

    def create_event(self, agenda_item):
        """Cria um evento no Google Calendar e retorna o ID e Link"""
        if not self.service:
            return None, None

        event_body = self._build_event_body(agenda_item)

        try:
            event = self.service.events().insert(
                calendarId=self.calendar_id, 
                body=event_body,
                # conferenceDataVersion=1  # Removido pois gera erro 400 em contas não-workspace
            ).execute()
            
            logger.info(f"Evento criado no Google Calendar: {event.get('htmlLink')}")
            return event.get('id'), event.get('htmlLink')
        
        except HttpError as error:
            logger.error(f"Erro ao criar evento no Google Calendar ({self.calendar_id}): {error}")
            return None, None

    def update_event(self, agenda_item):
        """Atualiza um evento existente"""
        if not self.service or not agenda_item.google_event_id:
            return False

        event_body = self._build_event_body(agenda_item)
        
        try:
            self.service.events().update(
                calendarId=self.calendar_id, 
                eventId=agenda_item.google_event_id, 
                body=event_body
            ).execute()
            return True
        except HttpError as error:
            logger.error(f"Erro ao atualizar evento {agenda_item.google_event_id}: {error}")
            return False

    def delete_event(self, google_event_id):
        """Remove um evento"""
        if not self.service or not google_event_id:
            return False
            
        try:
            self.service.events().delete(
                calendarId=self.calendar_id, 
                eventId=google_event_id
            ).execute()
            return True
        except HttpError as error:
            # Se já foi deletado (404), cosiderar sucesso ou ignorar
            if error.resp.status == 404:
                return True
            logger.error(f"Erro ao deletar evento {google_event_id}: {error}")
            return False

    def list_events(self, max_results=50):
        """Lista os eventos do Google Calendar (30 dias passados + futuros)"""
        if not self.service:
            return []
            
        try:
            # Pega eventos de 30 dias atrás para frente
            start_date = (datetime.utcnow() - timedelta(days=30)).isoformat() + 'Z'
            
            events_result = self.service.events().list(
                calendarId=self.calendar_id, 
                timeMin=start_date,
                maxResults=max_results, 
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            return events_result.get('items', [])
        
        except HttpError as error:
            logger.error(f"Erro ao listar eventos do Google Calendar: {error}")
            # Retorna lista vazia mas loga erro
            return []

    def _build_event_body(self, agenda_item):
        """Monta o corpo do JSON para a API"""
        start_time = agenda_item.data_inicio.isoformat()
        if agenda_item.data_fim:
            end_time = agenda_item.data_fim.isoformat()
        else:
            # Se não tiver fim, assume 1 hora de duração
            end_time = (agenda_item.data_inicio + timedelta(hours=1)).isoformat()

        event = {
            'summary': agenda_item.titulo,
            'description': agenda_item.descricao or '',
            'start': {
                'dateTime': start_time,
                'timeZone': 'America/Sao_Paulo', # Ajuste conforme settings.TIME_ZONE
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'America/Sao_Paulo',
            },
            # 'conferenceData': {
            #    'createRequest': {
            #        'requestId': f"meet-{agenda_item.id}-{int(datetime.now().timestamp())}",
            #        'conferenceSolutionKey': {'type': 'hangoutsMeet'}
            #    }
            # }
        }

        # Convidados: 
        # ATENÇÃO: Contas de serviço NÃO PODEM convidar pessoas via "attendees" sem Domain-Wide Delegation.
        # Também não podem criar conferências Meet em contas @gmail.com comuns facilmente.
        # Workaround: Adicionar info na DESCRIÇÃO.
        desc_extra = []
        if agenda_item.responsavel and agenda_item.responsavel.email:
             desc_extra.append(f"Responsável: {agenda_item.responsavel.email}")
        
        # desc_extra.append("Link da Reunião: (Adicionar no Google Calendar)")

        if desc_extra:
             event['description'] += "\n\n---\n" + "\n".join(desc_extra)

        return event
