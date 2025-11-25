// Configuração do TinyMCE para o editor WYSIWYG
tinymce.init({
    selector: 'textarea.tinymce',
    
    api_key: '4jflbxct8s4d4w36ycp1onm75pou65ujw0y7qokhl5omiesn',
    // Para obter uma chave gratuita: https://www.tiny.cloud/auth/signup/
    // api_key: 'sua-api-key-aqui',
    
    height: 500,
    menubar: true,
    plugins: [
        'advlist', 'autolink', 'lists', 'link', 'image', 'charmap', 'preview',
        'anchor', 'searchreplace', 'visualblocks', 'code', 'fullscreen',
        'insertdatetime', 'media', 'table', 'code', 'help', 'wordcount'
    ],
    toolbar: 'undo redo | formatselect | bold italic underline strikethrough | ' +
        'alignleft aligncenter alignright alignjustify | ' +
        'bullist numlist outdent indent | link image media | ' +
        'forecolor backcolor | removeformat | code fullscreen preview',
    content_style: 'body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; font-size: 14px }',
    
    // Permitir tags HTML
    valid_elements: '*[*]',
    extended_valid_elements: '*[*]',
    
    // Configurações de imagem
    image_advtab: true,
    automatic_uploads: true,
    file_picker_types: 'image',
    
    // Configurações de link
    link_assume_external_targets: true,
    
    // Idioma
    language: 'pt_BR',
    
    // Toolbar mode
    toolbar_mode: 'sliding',
    
    // Formato de conteúdo
    formats: {
        h1: { block: 'h1' },
        h2: { block: 'h2' },
        h3: { block: 'h3' },
        h4: { block: 'h4' },
        h5: { block: 'h5' },
        h6: { block: 'h6' },
        p: { block: 'p' },
        div: { block: 'div' }
    }
});
