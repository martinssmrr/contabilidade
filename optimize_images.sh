#!/bin/bash

# Script para otimizar imagens usando ImageMagick e cwebp
# Executar no servidor de produção

echo "======================================"
echo "🖼️  Otimização de Imagens - Vetorial"
echo "======================================"

# Instalar ferramentas necessárias
echo "Instalando ferramentas..."
apt-get update && apt-get install -y imagemagick webp

IMG_DIR="/root/vetorial/static/img"
cd $IMG_DIR

# Função para converter e otimizar imagem
optimize_image() {
    local file=$1
    local filename=$(basename "$file" .png)
    local dir=$(dirname "$file")
    
    # Converter para WebP com qualidade 80
    if [[ "$file" == *.png ]]; then
        cwebp -q 80 "$file" -o "${dir}/${filename}.webp" 2>/dev/null
        echo "✓ Convertido: ${filename}.webp"
    fi
}

echo ""
echo "📦 Otimizando imagens grandes..."

# Imagens de benefícios (redimensionar para 300x300)
for img in certificado-digital.png reducao-impostos.png escritorio-virtual.png atendimento-wpp.png; do
    if [ -f "$img" ]; then
        # Criar backup
        cp "$img" "${img}.backup"
        # Redimensionar e comprimir
        convert "$img" -resize 300x300 -quality 85 "$img"
        # Converter para WebP
        cwebp -q 80 "$img" -o "${img%.png}.webp"
        echo "✓ Otimizado: $img"
    fi
done

# Imagem de crescimento (redimensionar para 600x400)
if [ -f "sectioncrecimento.png" ]; then
    cp "sectioncrecimento.png" "sectioncrecimento.png.backup"
    convert "sectioncrecimento.png" -resize 600x400 -quality 85 "sectioncrecimento.png"
    cwebp -q 80 "sectioncrecimento.png" -o "sectioncrecimento.webp"
    echo "✓ Otimizado: sectioncrecimento.png"
fi

# CTA (redimensionar para 1200x600)
if [ -f "cta.png" ]; then
    cp "cta.png" "cta.png.backup"
    convert "cta.png" -resize 1200x600 -quality 80 "cta.png"
    cwebp -q 75 "cta.png" -o "cta.webp"
    echo "✓ Otimizado: cta.png"
fi

# Logos de parceiros (redimensionar para 150x150)
echo ""
echo "📦 Otimizando logos de parceiros..."
for i in {1..19}; do
    if [ -f "${i}.png" ]; then
        cp "${i}.png" "${i}.png.backup"
        convert "${i}.png" -resize 150x150 -quality 85 "${i}.png"
        cwebp -q 80 "${i}.png" -o "${i}.webp"
        echo "✓ Otimizado: ${i}.png"
    fi
done

# Outros ícones pequenos (redimensionar para 100x100)
echo ""
echo "📦 Otimizando ícones..."
for img in brasil.png online.png custo.png atendimento.png; do
    if [ -f "$img" ]; then
        cp "$img" "${img}.backup"
        convert "$img" -resize 100x100 -quality 85 "$img"
        cwebp -q 80 "$img" -o "${img%.png}.webp"
        echo "✓ Otimizado: $img"
    fi
done

# Selos do footer (redimensionar para 80x80)
echo ""
echo "📦 Otimizando selos..."
for img in SELO-RA1000.png googlesiteseguro.png ssl.png pix.png boleto.png mercadopago.png; do
    if [ -f "$img" ]; then
        cp "$img" "${img}.backup"
        convert "$img" -resize 80x80 -quality 85 "$img"
        cwebp -q 80 "$img" -o "${img%.png}.webp"
        echo "✓ Otimizado: $img"
    fi
done

# Logo principal (redimensionar para 150x150)
if [ -f "logo.png" ]; then
    cp "logo.png" "logo.png.backup"
    convert "logo.png" -resize 150x150 -quality 85 "logo.png"
    cwebp -q 80 "logo.png" -o "logo.webp"
    echo "✓ Otimizado: logo.png"
fi

# Avaliação Google
if [ -f "avaliação-google.png" ]; then
    cp "avaliação-google.png" "avaliação-google.png.backup"
    convert "avaliação-google.png" -resize 300x100 -quality 85 "avaliação-google.png"
    cwebp -q 80 "avaliação-google.png" -o "avaliação-google.webp"
    echo "✓ Otimizado: avaliação-google.png"
fi

echo ""
echo "======================================"
echo "✅ Otimização concluída!"
echo "======================================"

# Mostrar economia de espaço
echo ""
echo "📊 Relatório de tamanho:"
du -sh $IMG_DIR
echo ""
echo "Arquivos WebP criados:"
ls -la *.webp 2>/dev/null | head -20
