"""
Comando de gerenciamento para popular o banco de dados com CNAEs organizados por categoria
Uso: python manage.py popular_cnaes
"""
from django.core.management.base import BaseCommand
from apps.services.models import CategoriaCNAE, CNAE


class Command(BaseCommand):
    help = 'Popula o banco de dados com categorias e CNAEs de exemplo'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando população de CNAEs...'))
        
        # Dados das categorias e seus CNAEs
        dados_cnaes = {
            'Consultoria': [
                ('7020-4/00', 'Atividades de consultoria em gestão empresarial'),
                ('7490-1/04', 'Atividades de consultoria em gestão empresarial, exceto consultoria técnica específica'),
                ('7112-0/00', 'Serviços de engenharia'),
                ('7119-7/03', 'Serviços de desenho técnico relacionados à arquitetura e engenharia'),
                ('7020-4/00', 'Consultoria em tecnologia da informação'),
                ('6204-0/00', 'Consultoria em tecnologia da informação'),
                ('7490-1/99', 'Outras atividades profissionais, científicas e técnicas não especificadas anteriormente'),
                ('8299-7/99', 'Outras atividades de serviços prestados principalmente às empresas não especificadas anteriormente'),
            ],
            'Software': [
                ('6201-5/00', 'Desenvolvimento de programas de computador sob encomenda'),
                ('6202-3/00', 'Desenvolvimento e licenciamento de programas de computador customizáveis'),
                ('6203-1/00', 'Desenvolvimento e licenciamento de programas de computador não customizáveis'),
                ('6204-0/00', 'Consultoria em tecnologia da informação'),
                ('6209-1/00', 'Suporte técnico, manutenção e outros serviços em tecnologia da informação'),
                ('6311-9/00', 'Tratamento de dados, provedores de serviços de aplicação e serviços de hospedagem na internet'),
                ('6319-4/00', 'Portais, provedores de conteúdo e outros serviços de informação na internet'),
                ('5820-1/00', 'Edição de programas de computador'),
            ],
            'Educação e Cursos': [
                ('8599-6/04', 'Treinamento em desenvolvimento profissional e gerencial'),
                ('8599-6/05', 'Cursos preparatórios para concursos'),
                ('8511-2/00', 'Educação infantil - creche'),
                ('8512-1/00', 'Educação infantil - pré-escola'),
                ('8520-1/00', 'Ensino médio'),
                ('8531-7/00', 'Educação superior - graduação'),
                ('8541-4/00', 'Educação profissional de nível técnico'),
                ('8599-6/03', 'Treinamento em informática'),
                ('8599-6/99', 'Outras atividades de ensino não especificadas anteriormente'),
                ('8592-9/03', 'Ensino de idiomas'),
            ],
            'Administrativo': [
                ('8211-3/00', 'Serviços combinados de escritório e apoio administrativo'),
                ('8219-9/01', 'Fotocópias'),
                ('8219-9/99', 'Preparação de documentos e serviços especializados de apoio administrativo não especificados anteriormente'),
                ('8230-0/01', 'Serviços de organização de feiras, congressos, exposições e festas'),
                ('8230-0/02', 'Casas de festas e eventos'),
                ('8291-1/00', 'Atividades de cobranças e informações cadastrais'),
                ('8292-0/00', 'Envasamento e empacotamento sob contrato'),
                ('8299-7/01', 'Medição de consumo de energia elétrica, gás e água'),
            ],
            'Advogados': [
                ('6911-7/01', 'Serviços advocatícios'),
                ('6911-7/02', 'Atividades auxiliares da justiça'),
                ('6911-7/03', 'Agente de propriedade industrial'),
                ('6912-5/00', 'Cartórios'),
            ],
            'Engenharia': [
                ('7112-0/00', 'Serviços de engenharia'),
                ('7119-7/01', 'Serviços de cartografia, topografia e geodésia'),
                ('7119-7/02', 'Atividades de estudos geológicos'),
                ('7119-7/03', 'Serviços de desenho técnico relacionados à arquitetura e engenharia'),
                ('7119-7/04', 'Serviços de perícia técnica relacionados à segurança do trabalho'),
                ('4313-4/00', 'Obras de terraplenagem'),
                ('4321-5/00', 'Instalação e manutenção elétrica'),
                ('7120-1/00', 'Testes e análises técnicas'),
            ],
            'Tecnologia': [
                ('6201-5/00', 'Desenvolvimento de programas de computador sob encomenda'),
                ('6204-0/00', 'Consultoria em tecnologia da informação'),
                ('6209-1/00', 'Suporte técnico, manutenção e outros serviços em tecnologia da informação'),
                ('9511-8/00', 'Reparação e manutenção de computadores e de equipamentos periféricos'),
                ('9512-6/00', 'Reparação e manutenção de equipamentos de comunicação'),
                ('6110-8/01', 'Serviços de telefonia fixa comutada - STFC'),
                ('6110-8/02', 'Serviços de redes de transporte de telecomunicações - SRTT'),
                ('6190-6/01', 'Provedores de acesso às redes de comunicações'),
            ],
            'Serviços Médicos': [
                ('8610-1/01', 'Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências'),
                ('8621-6/01', 'UTI móvel'),
                ('8621-6/02', 'Serviços móveis de atendimento a urgências, exceto por UTI móvel'),
                ('8630-5/01', 'Atividade médica ambulatorial com recursos para realização de procedimentos cirúrgicos'),
                ('8630-5/02', 'Atividade médica ambulatorial com recursos para realização de exames complementares'),
                ('8630-5/99', 'Atividades de atenção ambulatorial não especificadas anteriormente'),
                ('8640-2/01', 'Laboratórios de anatomia patológica e citológica'),
                ('8640-2/02', 'Laboratórios clínicos'),
                ('8650-0/01', 'Atividades de enfermagem'),
                ('8650-0/02', 'Atividades de profissionais da nutrição'),
                ('8650-0/03', 'Atividades de psicologia e psicanálise'),
                ('8650-0/04', 'Atividades de fisioterapia'),
                ('8650-0/05', 'Atividades de terapia ocupacional'),
                ('8650-0/06', 'Atividades de fonoaudiologia'),
                ('8650-0/07', 'Atividades de terapia de nutrição enteral e parenteral'),
                ('8650-0/99', 'Atividades de profissionais da área de saúde não especificadas anteriormente'),
                ('8660-7/00', 'Atividades de apoio à gestão de saúde'),
                ('8690-9/01', 'Atividades de práticas integrativas e complementares em saúde humana'),
                ('8690-9/99', 'Outras atividades de atenção à saúde humana não especificadas anteriormente'),
                ('8711-5/01', 'Clínicas e residências geriátricas'),
                ('8711-5/02', 'Instituições de longa permanência para idosos'),
                ('8720-4/01', 'Atividades de centros de assistência psicossocial'),
            ],
            'Publicidade': [
                ('7311-4/00', 'Agências de publicidade'),
                ('7312-2/00', 'Agenciamento de espaços para publicidade, exceto em veículos de comunicação'),
                ('7319-0/01', 'Criação e montagem de estandes para feiras e exposições'),
                ('7319-0/02', 'Promoção de vendas'),
                ('7319-0/03', 'Marketing direto'),
                ('7319-0/04', 'Consultoria em publicidade'),
                ('7319-0/99', 'Outras atividades de publicidade não especificadas anteriormente'),
                ('7320-3/00', 'Pesquisas de mercado e de opinião pública'),
                ('7410-2/01', 'Design'),
                ('7410-2/02', 'Design de interiores'),
                ('7410-2/03', 'Design de produto'),
            ],
            'Turismo': [
                ('7911-2/00', 'Agências de viagens'),
                ('7912-1/00', 'Operadores turísticos'),
                ('7990-2/00', 'Serviços de reservas e outros serviços de turismo não especificados anteriormente'),
                ('5510-8/01', 'Hotéis'),
                ('5510-8/02', 'Apart-hotéis'),
                ('5590-6/01', 'Albergues, exceto assistenciais'),
                ('5590-6/02', 'Campings'),
                ('5590-6/03', 'Pensões (alojamento)'),
                ('7721-7/00', 'Aluguel de equipamentos recreativos e esportivos'),
                ('9319-1/01', 'Produção e promoção de eventos esportivos'),
            ],
            'Arquitetura': [
                ('7111-1/00', 'Serviços de arquitetura'),
                ('7119-7/03', 'Serviços de desenho técnico relacionados à arquitetura e engenharia'),
                ('4120-4/00', 'Construção de edifícios'),
                ('7410-2/02', 'Design de interiores'),
                ('4330-4/01', 'Impermeabilização em obras de engenharia civil'),
                ('4330-4/99', 'Outras obras de acabamento da construção'),
            ],
            'Medico': [
                ('8630-5/01', 'Atividade médica ambulatorial com recursos para realização de procedimentos cirúrgicos'),
                ('8630-5/02', 'Atividade médica ambulatorial com recursos para realização de exames complementares'),
                ('8630-5/99', 'Atividades de atenção ambulatorial não especificadas anteriormente'),
                ('8610-1/01', 'Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências'),
                ('8610-1/02', 'Atividades de atendimento em pronto-socorro e unidades hospitalares para atendimento a urgências'),
                ('8621-6/01', 'UTI móvel'),
                ('8621-6/02', 'Serviços móveis de atendimento a urgências, exceto por UTI móvel'),
            ],
            'Corretagem de Imoveis': [
                ('6821-8/01', 'Corretagem na compra e venda e avaliação de imóveis'),
                ('6821-8/02', 'Corretagem no aluguel de imóveis'),
                ('6822-6/00', 'Gestão e administração da propriedade imobiliária'),
                ('6810-2/01', 'Compra e venda de imóveis próprios'),
                ('6810-2/02', 'Aluguel de imóveis próprios'),
                ('6831-8/00', 'Intermediação na compra, venda e aluguel de imóveis'),
            ],
            'Outros': [
                # Categoria vazia conforme solicitado
            ],
        }
        
        # Limpar dados existentes
        self.stdout.write('Removendo CNAEs e categorias existentes...')
        CNAE.objects.all().delete()
        CategoriaCNAE.objects.all().delete()
        
        # Criar categorias e CNAEs
        total_cnaes = 0
        for ordem, (categoria_nome, cnaes_lista) in enumerate(dados_cnaes.items(), start=1):
            self.stdout.write(f'\nCriando categoria: {categoria_nome}')
            
            categoria, created = CategoriaCNAE.objects.get_or_create(
                nome=categoria_nome,
                defaults={'ordem': ordem}
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Categoria "{categoria_nome}" criada'))
            else:
                self.stdout.write(self.style.WARNING(f'  ⚠ Categoria "{categoria_nome}" já existia'))
            
            # Adicionar CNAEs da categoria
            for codigo, descricao in cnaes_lista:
                cnae, created = CNAE.objects.get_or_create(
                    codigo=codigo,
                    defaults={
                        'descricao': descricao,
                        'categoria': categoria,
                        'ativo': True
                    }
                )
                
                if created:
                    total_cnaes += 1
                    self.stdout.write(f'    + {codigo} - {descricao[:60]}...')
        
        # Resumo final
        total_categorias = CategoriaCNAE.objects.count()
        total_cnaes_db = CNAE.objects.count()
        
        self.stdout.write('\n' + '=' * 70)
        self.stdout.write(self.style.SUCCESS(f'✓ População concluída com sucesso!'))
        self.stdout.write(self.style.SUCCESS(f'✓ Total de categorias: {total_categorias}'))
        self.stdout.write(self.style.SUCCESS(f'✓ Total de CNAEs: {total_cnaes_db}'))
        self.stdout.write('=' * 70)
        
        # Estatísticas por categoria
        self.stdout.write('\n📊 CNAEs por categoria:')
        for cat in CategoriaCNAE.objects.all():
            count = cat.cnaes.count()
            self.stdout.write(f'  • {cat.nome}: {count} CNAEs')
