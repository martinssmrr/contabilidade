import io
import base64
from django.utils import timezone
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

def generate_contract_pdf(processo):
    """
    Gera o PDF do contrato de prestação de serviços
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=20*mm, leftMargin=20*mm,
                            topMargin=20*mm, bottomMargin=20*mm)
    
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, leading=14))
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER, leading=14, spaceAfter=20))
    
    story = []
    
    # Título
    story.append(Paragraph("<b>CONTRATO DE PRESTAÇÃO DE SERVIÇOS CONTÁBEIS</b>", styles['Center']))
    story.append(Spacer(1, 10*mm))
    
    # Dados do Contratante
    nome = processo.nome_completo or "____________________"
    cpf = processo.cpf or "____________________"
    endereco = f"{processo.endereco or ''}, {processo.numero or ''}, {processo.bairro or ''}, {processo.cidade or ''}-{processo.estado or ''}"
    
    texto_contratante = f"""
    <b>CONTRATANTE:</b> {nome}, CPF {cpf}, residente e domiciliado em {endereco}.
    """
    story.append(Paragraph(texto_contratante, styles['Justify']))
    story.append(Spacer(1, 5*mm))
    
    # Dados da Contratada
    texto_contratada = """
    <b>CONTRATADA:</b> VETORIAL CONTABILIDADE LTDA, CNPJ 00.000.000/0001-00, 
    estabelecida em Av Marginal B, Ed Aguas Claras, Sala 201 C, Vila Juracy, Luziania Goias.
    """
    story.append(Paragraph(texto_contratada, styles['Justify']))
    story.append(Spacer(1, 5*mm))
    
    # Cláusulas
    clausulas = [
        "<b>CLÁUSULA PRIMEIRA - DO OBJETO</b><br/>O presente contrato tem por objeto a prestação de serviços de abertura de empresa e assessoria contábil, conforme as normas brasileiras de contabilidade e a legislação vigente.",
        "<b>CLÁUSULA SEGUNDA - DAS OBRIGAÇÕES DA CONTRATADA</b><br/>I - Elaborar o contrato social e demais documentos necessários para o registro da empresa;<br/>II - Protocolar os documentos nos órgãos competentes (Junta Comercial, Receita Federal, Prefeitura, etc.);<br/>III - Manter o CONTRATANTE informado sobre o andamento do processo.",
        "<b>CLÁUSULA TERCEIRA - DAS OBRIGAÇÕES DO CONTRATANTE</b><br/>I - Fornecer documentos e informações verdadeiras e dentro do prazo solicitado;<br/>II - Pagar as taxas governamentais e os honorários da CONTRATADA;<br/>III - Responsabilizar-se pela veracidade dos documentos enviados.",
        "<b>CLÁUSULA QUARTA - DA ASSINATURA DIGITAL</b><br/>As partes reconhecem a validade jurídica da assinatura digital/eletrônica aposta neste documento, nos termos da MP 2.200-2/2001."
    ]
    
    for clausula in clausulas:
        story.append(Paragraph(clausula, styles['Justify']))
        story.append(Spacer(1, 5*mm))
    
    story.append(Spacer(1, 10*mm))
    
    # Data e Local
    cidade = processo.cidade or "Luziânia"
    estado = processo.estado or "GO"
    data_hoje = timezone.now().strftime("%d/%m/%Y")
    story.append(Paragraph(f"{cidade}-{estado}, {data_hoje}", styles['Center']))
    story.append(Spacer(1, 10*mm))
    
    # Assinaturas
    # Processar assinatura digital (Base64)
    if processo.assinatura_digital:
        try:
            # Remover cabeçalho do data URI se existir (ex: "data:image/png;base64,")
            img_data = processo.assinatura_digital.split(',')[1] if ',' in processo.assinatura_digital else processo.assinatura_digital
            img_bytes = base64.b64decode(img_data)
            img_io = io.BytesIO(img_bytes)
            
            # Adicionar imagem da assinatura
            img = Image(img_io, width=50*mm, height=25*mm)
            story.append(img)
            story.append(Paragraph("____________________________________________", styles['Center']))
            story.append(Paragraph(f"<b>{nome}</b><br/>CONTRATANTE", styles['Center']))
        except Exception as e:
            story.append(Paragraph(f"[Erro ao carregar assinatura: {str(e)}]", styles['Center']))
    else:
        story.append(Paragraph("____________________________________________", styles['Center']))
        story.append(Paragraph(f"<b>{nome}</b><br/>CONTRATANTE (Pendente de Assinatura)", styles['Center']))
        
    story.append(Spacer(1, 10*mm))
    
    # Assinatura da Contratada (Placeholder ou imagem fixa se tivesse)
    story.append(Paragraph("____________________________________________", styles['Center']))
    story.append(Paragraph("<b>VETORIAL CONTABILIDADE LTDA</b><br/>CONTRATADA", styles['Center']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer
