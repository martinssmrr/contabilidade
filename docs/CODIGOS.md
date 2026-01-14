/* Contabilidade Facil Section */ CSS QUE VAI NO HOME.HTML


    #contabilidade-facil {
        background: linear-gradient(135deg, #4a148c 0%, #0d47a1 100%);
        position: relative;
        overflow: hidden;
    }
    #contabilidade-facil .section-bg-overlay {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        width: 50%;
        background: linear-gradient(to right, transparent, rgba(0,0,0,0.5));
        opacity: 0.1;
        pointer-events: none;
    }
    #contabilidade-facil .text-highlight {
        color: #ffeb3b;
        font-weight: bold;
    }
    #contabilidade-facil .feature-card {
        background: #fff;
        border-radius: 10px;
        padding: 1rem;
        color: #333;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        justify-content: center;
        min-height: 110px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    #contabilidade-facil .feature-card:hover {
        transform: translateY(-5px);
    }
    #contabilidade-facil .feature-card i {
        color: #0c63d1;
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
    }
    #contabilidade-facil .feature-card p {
        font-size: 0.9rem;
        margin: 0;
        font-weight: 600;
        line-height: 1.2;
    }
    #contabilidade-facil .feature-card-tall {
        grid-row: span 2;
        background-color: #fff;
        justify-content: center;
    }
    #contabilidade-facil .btn-white-primary {
        background-color: #fff;
        color: #0c63d1;
        font-weight: bold;
        padding: 12px 30px;
        border-radius: 50px;
        text-decoration: none;
        display: inline-block;
        transition: all 0.3s ease;
        border: 2px solid #fff;
    }
    #contabilidade-facil .btn-white-primary:hover {
        background-color: transparent;
        color: #fff;
    }
    .features-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 15px;
    }
    @media (max-width: 991.98px) {
        .features-grid {
            grid-template-columns: repeat(2, 1fr);
        }
        #contabilidade-facil .section-bg-overlay {
            width: 100%;
        }
    }
    @media (max-width: 575.98px) {
        .features-grid {
            grid-template-columns: 1fr;
        }
        #contabilidade-facil .feature-card-tall {
            grid-row: span 1;
        }
    }

    .btn-purple {
        background-color: #2ed66b;
        color: white;
        border: none;
        transition: background-color 0.3s ease;
    }
    .btn-purple:hover {
        background-color: #59359a;
        color: white;
    }
    .service-card {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .service-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 1rem 3rem rgba(0,0,0,.175)!important;
    }
--------------------------------------------------------------------------------------------------------------
CODIGO HTML QUE VAI NO HOME.HTML
<!-- Contabilidade Facil Section -->
<section id="contabilidade-facil" class="py-5 position-relative text-white">
    <div class="section-bg-overlay"></div>
    <div class="container position-relative z-1">
        <div class="row g-5 align-items-center">
            <!-- Left Column -->
            <div class="col-lg-7">
                <h2 class="display-5 fw-bold mb-4">
                    Tornamos a contabilidade fácil, <span class="text-highlight">rápida e tecnológica!</span>
                </h2>
                <div class="mb-4">
                    <p class="lead mb-3">Simplifique a gestão do seu negócio com nossa plataforma intuitiva. Deixe a burocracia conosco e foque no que realmente importa: o crescimento da sua empresa.</p>
                    <p>Oferecemos soluções completas para MEIs, MEs e EPPs, com atendimento personalizado e tecnologia de ponta para garantir sua tranquilidade fiscal e contábil.</p>
                </div>
                
                <!-- Grid of Features -->
                <div class="features-grid">
                    <div class="feature-card">
                        <i class="fa-solid fa-store"></i>
                        <p>Abertura de empresa grátis</p>
                    </div>
                    <div class="feature-card">
                        <i class="fa-solid fa-rotate"></i>
                        <p>Troca de contador</p>
                    </div>
                    <div class="feature-card">
                        <i class="fa-solid fa-chart-line"></i>
                        <p>Migração de MEI</p>
                    </div>
                    <div class="feature-card feature-card-tall">
                        <i class="fa-solid fa-hand-holding-dollar"></i>
                        <p>Aqui você não paga 13º</p>
                    </div>
                    <div class="feature-card">
                        <i class="fa-solid fa-file-invoice-dollar"></i>
                        <p>Emissão de notas</p>
                    </div>
                    <div class="feature-card">
                        <i class="fa-solid fa-coins"></i>
                        <p>Gestão financeira</p>
                    </div>
                    <div class="feature-card">
                        <i class="fa-solid fa-headset"></i>
                        <p>Atendimento humanizado</p>
                    </div>
                    <div class="feature-card">
                        <i class="fa-solid fa-check-double"></i>
                        <p>Impostos em dia</p>
                    </div>
                </div>
            </div>
            
            <!-- Right Column (CTA) -->
            <div class="col-lg-5">
                <div class="cta-content ps-lg-4">
                    <h3 class="h2 fw-bold mb-4">
                        Uma plataforma digital preparada para o <span class="text-highlight">microempreendedor</span> operar.
                    </h3>
                    <p class="mb-4">Tenha o controle total da sua empresa na palma da mão. Acesse relatórios, emita notas e acompanhe suas obrigações fiscais de onde estiver, com total segurança e praticidade.</p>
                    <a href="#contato" class="btn btn-white-primary">Fale com um especialista</a>
                </div>
            </div>
        </div>
        
        <!-- Footer -->
        <div class="row mt-5">
            <div class="col-12 text-center">
                <p class="h4 text-highlight fw-bold">E muito mais...</p>
            </div>
        </div>
    </div>
</section>



<!-- Growth Section --> ANTIGA SECTION DA MULHER
<section class="growth-section py-5" style="background-color: #ebeef1;">
    <div class="container">
        <div class="text-center mb-5">
            <h2 class="display-5 fw-bold mb-3">Tudo o que sua empresa precisa para crescer!</h2>
            <p class="lead text-muted">Tenha especialistas dedicados ao seu negócio, que cuidam diariamente de toda contabilidade da sua empresa.</p>
        </div>
        
        <div class="row g-4 align-items-center">
            <!-- Card Principal com Imagem -->
            <div class="col-lg-6">
                <div class="card border-0 shadow-lg h-100">
                    <img src="{% static 'img/sectioncrecimento.webp' %}" alt="Crescimento Empresarial" class="card-img-top rounded" width="600" height="400" loading="lazy">
                </div>
            </div>
            
            <!-- Cards de Benefícios -->
            <div class="col-lg-6">
                <div class="row g-4">
                    <!-- Card 2 - Praticidade -->
                    <div class="col-md-6">
                        <div class="card h-100 border-0 shadow-sm growth-card">
                            <div class="card-body p-4 text-center">
                                <div class="mb-3">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" fill="currentColor" class="text-primary" viewBox="0 0 16 16">
                                        <path d="M8 4.754a3.246 3.246 0 1 0 0 6.492 3.246 3.246 0 0 0 0-6.492zM5.754 8a2.246 2.246 0 1 1 4.492 0 2.246 2.246 0 0 1-4.492 0z"/>
                                        <path d="M9.796 1.343c-.527-1.79-3.065-1.79-3.592 0l-.094.319a.873.873 0 0 1-1.255.52l-.292-.16c-1.64-.892-3.433.902-2.54 2.541l.159.292a.873.873 0 0 1-.52 1.255l-.319.094c-1.79.527-1.79 3.065 0 3.592l.319.094a.873.873 0 0 1 .52 1.255l-.16.292c-.892 1.64.901 3.434 2.541 2.54l.292-.159a.873.873 0 0 1 1.255.52l.094.319c.527 1.79 3.065 1.79 3.592 0l.094-.319a.873.873 0 0 1 1.255-.52l.292.16c1.64.893 3.434-.902 2.54-2.541l-.159-.292a.873.873 0 0 1 .52-1.255l.319-.094c1.79-.527 1.79-3.065 0-3.592l-.319-.094a.873.873 0 0 1-.52-1.255l.16-.292c.893-1.64-.902-3.433-2.541-2.54l-.292.159a.873.873 0 0 1-1.255-.52l-.094-.319z"/>
                                    </svg>
                                </div>
                                <h5 class="card-title fw-bold">Praticidade</h5>
                                <p class="card-text text-muted small">Tudo online, rápido e sem complicação</p>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Card 3 - Especialista Contábil -->
                    <div class="col-md-6">
                        <div class="card h-100 border-0 shadow-sm growth-card">
                            <div class="card-body p-4 text-center">
                                <div class="mb-3">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" fill="currentColor" class="text-primary" viewBox="0 0 16 16">
                                        <path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6Zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0Zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4Zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10Z"/>
                                    </svg>
                                </div>
                                <h5 class="card-title fw-bold">Especialista Contábil</h5>
                                <p class="card-text text-muted small">Time dedicado ao seu negócio</p>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Card 4 - Transparência -->
                    <div class="col-md-6">
                        <div class="card h-100 border-0 shadow-sm growth-card">
                            <div class="card-body p-4 text-center">
                                <div class="mb-3">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" fill="currentColor" class="text-primary" viewBox="0 0 16 16">
                                        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
                                    </svg>
                                </div>
                                <h5 class="card-title fw-bold">Transparência</h5>
                                <p class="card-text text-muted small">Informações claras e acessíveis</p>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Card 5 - Segurança -->
                    <div class="col-md-6">
                        <div class="card h-100 border-0 shadow-sm growth-card">
                            <div class="card-body p-4 text-center">
                                <div class="mb-3">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" fill="currentColor" class="text-primary" viewBox="0 0 16 16">
                                        <path d="M5.338 1.59a61.44 61.44 0 0 0-2.837.856.481.481 0 0 0-.328.39c-.554 4.157.726 7.19 2.253 9.188a10.725 10.725 0 0 0 2.287 2.233c.346.244.652.42.893.533.12.057.218.095.293.118a.55.55 0 0 0 .101.025.615.615 0 0 0 .1-.025c.076-.023.174-.061.294-.118.24-.113.547-.29.893-.533a10.726 10.726 0 0 0 2.287-2.233c1.527-1.997 2.807-5.031 2.253-9.188a.48.48 0 0 0-.328-.39c-.651-.213-1.75-.56-2.837-.855C9.552 1.29 8.531 1.067 8 1.067c-.53 0-1.552.223-2.662.524zM5.072.56C6.157.265 7.31 0 8 0s1.843.265 2.928.56c1.11.3 2.229.655 2.887.87a1.54 1.54 0 0 1 1.044 1.262c.596 4.477-.787 7.795-2.465 9.99a11.775 11.775 0 0 1-2.517 2.453 7.159 7.159 0 0 1-1.048.625c-.28.132-.581.24-.829.24s-.548-.108-.829-.24a7.158 7.158 0 0 1-1.048-.625 11.777 11.777 0 0 1-2.517-2.453C1.928 10.487.545 7.169 1.141 2.692A1.54 1.54 0 0 1 2.185 1.43 62.456 62.456 0 0 1 5.072.56z"/>
                                        <path d="M10.854 5.146a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 1 1 .708-.708L7.5 7.793l2.646-2.647a.5.5 0 0 1 .708 0z"/>
                                    </svg>
                                </div>
                                <h5 class="card-title fw-bold">Segurança</h5>
                                <p class="card-text text-muted small">Dados protegidos e confidenciais</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>


<!-- O que faremos por você Section -->
<!-- <section class="py-5 bg-white" style="background-color: rgb(235, 238, 241) !important;">
    <div class="container">
        <div class="text-center mb-5">
            <h2 class="display-5 fw-bold text-dark">O que faremos por você na Vetorial</h2>
        </div>
        <div class="row g-4"> -->
            <!-- Card 1 -->
            <!-- <div class="col-lg-3 col-md-6 col-12">
                <div class="card h-100 border-0 shadow-sm service-card">
                    <div class="card-body p-4 d-flex flex-column">
                        <h5 class="card-title fw-bold text-orange mb-3">ABRIR MINHA EMPRESA</h5>
                        <p class="card-text text-muted mb-4 flex-grow-1">Nós fazemos todo o processo por você rápido, 100% online e com orientações fáceis, sem complicações.</p>
                        <a href="/abrir-empresa/" class="btn btn-purple w-100 rounded-pill text-uppercase fw-bold">ABRIR MINHA EMPRESA</a>
                    </div>
                </div>
            </div> -->
            <!-- Card 2 -->
            <!-- <div class="col-lg-3 col-md-6 col-12">
                <div class="card h-100 border-0 shadow-sm service-card">
                    <div class="card-body p-4 d-flex flex-column">
                        <h5 class="card-title fw-bold text-orange mb-3">TRANSFORME SEU MEI</h5>
                        <p class="card-text text-muted mb-4 flex-grow-1">Analisamos seu MEI e mostramos o enquadramento ideal para sua empresa crescer do jeito certo.</p>
                        <a href="/deixar-mei/" class="btn btn-purple w-100 rounded-pill text-uppercase fw-bold">TRANSFORMAR MEU MEI</a>
                    </div>
                </div>
            </div> -->
            <!-- Card 3 -->
            <!-- <div class="col-lg-3 col-md-6 col-12">
                <div class="card h-100 border-0 shadow-sm service-card">
                    <div class="card-body p-4 d-flex flex-column">
                        <h5 class="card-title fw-bold text-orange mb-3">TROQUE DE CONTADOR</h5>
                        <p class="card-text text-muted mb-4 flex-grow-1">A Vetorial cuida de toda a migração, fornecendo uma gestão contábil que economiza tempo, reduz custos e melhora sua operação.</p>
                        <a href="/trocar-contador/" class="btn btn-purple w-100 rounded-pill text-uppercase fw-bold">MIGRAR PARA A VETORIAL</a>
                    </div>
                </div>
            </div> -->
            <!-- Card 4 -->
            <!-- <div class="col-lg-3 col-md-6 col-12">
                <div class="card h-100 border-0 shadow-sm service-card">
                    <div class="card-body p-4 d-flex flex-column">
                        <h5 class="card-title fw-bold text-orange mb-3">ENDREÇO VIRTUAL</h5>
                        <p class="card-text text-muted mb-4 flex-grow-1">Obtenha um endereço fiscal profissional para sua empresa sem precisar alugar um espaço físico. Ideal para abrir CNPJ, regularizar seu negócio e transmitir mais credibilidade tudo de forma simples, econômica e 100% online.</p>
                        <a href="/endereco-virtual/" class="btn btn-purple w-100 rounded-pill text-uppercase fw-bold">CONHEÇA A VETORIAL</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section> -->




<!-- Porque escolher a Vetorial -->
<!-- <section class="features-section py-5" style="background-color: #ebeef1;">
    <div class="container">
        <div class="text-center mb-5">
            <h2 class="display-5 fw-bold mb-3">Por que escolher a Vetorial?</h2>
        </div>
        <div class="row g-4"> -->
            <!-- Card 1 - Atendimento em todo o brasil -->
            <!-- <div class="col-lg-3 col-md-6 col-12">
                <div class="card h-100 border-0 shadow-sm feature-card">
                    <div class="card-body p-4 text-center">
                        <div class="feature-icon mb-4">
                            <img src="{% static 'img/brasil.webp' %}" alt="Brasil" class="img-fluid" width="70" height="70" loading="lazy">
                        </div>
                        <h5 class="card-title fw-bold mb-3">Atendimento em todo o brasil</h5>
                        <p class="card-text text-muted">Somos uma contabilidade online pronta para atender a sua empresa, em qualquer cidade brasileira.</p>
                    </div>
                </div>
            </div> -->
            
            <!-- Card 2 - Totalmente online -->
            <!-- <div class="col-lg-3 col-md-6 col-12">
                <div class="card h-100 border-0 shadow-sm feature-card">
                    <div class="card-body p-4 text-center">
                        <div class="feature-icon mb-4">
                            <img src="{% static 'img/online.webp' %}" alt="Online" class="img-fluid" width="70" height="70" loading="lazy">
                        </div>
                        <h5 class="card-title fw-bold mb-3">Totalmente online</h5>
                        <p class="card-text text-muted">Todo o atendimento e fluxo de documentos para a contabilidade se dá através do nosso sistema, basta ter acesso à internet.</p>
                    </div>
                </div>
            </div> -->
            
            <!-- Card 3 - Baixo Custo -->
            <!-- <div class="col-lg-3 col-md-6 col-12">
                <div class="card h-100 border-0 shadow-sm feature-card">
                    <div class="card-body p-4 text-center">
                        <div class="feature-icon mb-4">
                            <img src="{% static 'img/custo.webp' %}" alt="Baixo Custo" class="img-fluid" width="70" height="70" loading="lazy">
                        </div>
                        <h5 class="card-title fw-bold mb-3">Baixo Custo</h5>
                        <p class="card-text text-muted">Economize recursos para aplicar no seu negócio, tecnologia de ponta e contadores de primeira trazem para você o melhor custo benefício.</p>
                    </div>
                </div>
            </div> -->
            
            <!-- Card 4 - Atendimento Humanizado -->
            <!-- <div class="col-lg-3 col-md-6 col-12">
                <div class="card h-100 border-0 shadow-sm feature-card">
                    <div class="card-body p-4 text-center">
                        <div class="feature-icon mb-4">
                            <img src="{% static 'img/atendimento.webp' %}" alt="Atendimento Humanizado" class="img-fluid" width="70" height="70" loading="lazy">
                        </div>
                        <h5 class="card-title fw-bold mb-3">Atendimento Humanizado</h5>
                        <p class="card-text text-muted">Tenha um contador online pronto para atender e te ajudar na tomada de decisão do seu negócio.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section> -->

<!-- Benefícios Section -->
<!-- <section class="benefits-section py-5" style="background-color: #ebeef1;">
    <div class="container">
        <div class="text-center mb-5">
            <h2 class="display-5 fw-bold mb-3">Benefícios exclusivos para você e sua empresa</h2>
        </div>
        <div class="row g-4 justify-content-center"> -->
            <!-- Card 1 - Atendimento por WhatsApp -->
            <!-- <div class="col-lg-3 col-md-6 col-sm-6 col-12">
                <div class="flip-card">
                    <div class="flip-card-inner">
                        <div class="flip-card-front">
                            <div class="benefit-image-wrapper">
                                <img src="{% static 'img/atendimento-wpp.webp' %}" alt="Atendimento por WhatsApp" class="benefit-image" width="250" height="210" loading="lazy">
                            </div>
                            <h5 class="benefit-title">Atendimento por WhatsApp</h5>
                        </div>
                        <div class="flip-card-back">
                            <div class="flip-card-back-content">
                                <h5 class="fw-bold mb-3">Atendimento por WhatsApp</h5>
                                <p>Na Vetorial, todos os planos oferecem suporte direto pelo WhatsApp, rápido, prático e com a atenção do nosso time de especialistas.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div> -->

            <!-- Card 2 - Escritório Virtual -->
            <!-- <div class="col-lg-3 col-md-6 col-sm-6 col-12">
                <div class="flip-card">
                    <div class="flip-card-inner">
                        <div class="flip-card-front">
                            <div class="benefit-image-wrapper">
                                <img src="{% static 'img/escritorio-virtual.webp' %}" alt="Escritório Virtual" class="benefit-image" width="250" height="210" loading="lazy">
                            </div>
                            <h5 class="benefit-title">Escritório Virtual</h5>
                        </div>
                        <div class="flip-card-back">
                            <div class="flip-card-back-content">
                                <h5 class="fw-bold mb-3">Escritório Virtual</h5>
                                <p>Com o nosso Escritório Virtual, você garante um endereço fiscal profissional para o seu negócio, recebimento e gestão de correspondências, além de suporte direto pelo WhatsApp.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div> -->

            <!-- Card 3 - Certificado Digital -->
            <!-- <div class="col-lg-3 col-md-6 col-sm-6 col-12">
                <div class="flip-card">
                    <div class="flip-card-inner">
                        <div class="flip-card-front">
                            <div class="benefit-image-wrapper">
                                <img src="{% static 'img/certificado-digital.webp' %}" alt="Certificado Digital" class="benefit-image" width="250" height="210" loading="lazy">
                            </div>
                            <h5 class="benefit-title">Certificado Digital</h5>
                        </div>
                        <div class="flip-card-back">
                            <div class="flip-card-back-content">
                                <h5 class="fw-bold mb-3">Certificado Digital</h5>
                                <p>Emita seu Certificado Digital de forma rápida, segura e totalmente online. Oferecemos atendimento direto pelo WhatsApp e suporte personalizado para garantir que você conclua o processo sem burocracia.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div> -->

            <!-- Card 4 - Redução de Impostos -->
            <!-- <div class="col-lg-3 col-md-6 col-sm-6 col-12">
                <div class="flip-card">
                    <div class="flip-card-inner">
                        <div class="flip-card-front">
                            <div class="benefit-image-wrapper">
                                <img src="{% static 'img/reducao-impostos.webp' %}" alt="Redução de Impostos" class="benefit-image" width="250" height="210" loading="lazy">
                            </div>
                            <h5 class="benefit-title">Redução de Impostos</h5>
                        </div>
                        <div class="flip-card-back">
                            <div class="flip-card-back-content">
                                <h5 class="fw-bold mb-3">Redução de Impostos</h5>
                                <p>Calculamos automaticamente se sua empresa pode usar o Fator R, do Simples Nacional, para pagar menos impostos de forma legal e eficiente.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section> -->





# pdf generator
import io
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.utils import timezone
from django.conf import settings
import base64
from pypdf import PdfWriter, PdfReader

def generate_contract_pdf(processo):
    """
    Gera o PDF do contrato de prestação de serviços com base no conteúdo da Vetorial.
    Utiliza um papel timbrado como fundo.
    """
    # 1. Gerar o conteúdo do contrato (texto) em memória
    content_buffer = io.BytesIO()
    doc = SimpleDocTemplate(content_buffer, pagesize=A4,
                            rightMargin=20*mm, leftMargin=20*mm,
                            topMargin=40*mm, bottomMargin=30*mm) # Margens maiores para o papel timbrado
    
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, leading=14))
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER, leading=14, spaceAfter=20))
    styles.add(ParagraphStyle(name='ContractHeading1', fontSize=14, leading=16, alignment=TA_CENTER, spaceAfter=12, spaceBefore=12, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='ContractHeading2', fontSize=12, leading=14, alignment=TA_JUSTIFY, spaceAfter=8, spaceBefore=8, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='BodyTextIndent', parent=styles['Justify'], firstLineIndent=10))

    story = []
    
    # Título do Contrato
    story.append(Paragraph("<b>CONTRATO DE PRESTAÇÃO DE SERVIÇOS E LICENÇA DE SOFTWARE</b>", styles['Center']))
    story.append(Spacer(1, 10*mm))
    
    # Dados do Contratante
    nome_contratante = f"<b>{processo.nome_completo or '____________________'}</b>"
    cpf_contratante = processo.cpf or "____________________"
    endereco_contratante = f"{processo.endereco or ''}, {processo.numero or ''}, {processo.bairro or ''}, {processo.cidade or ''}-{processo.estado or ''}"
    
    texto_contratante_dados = f"""
    Este contrato estabelece como serão prestados os serviços e licenciado software pela Vetorial. Ao aceitá-lo você, doravante denominado <b>CONTRATANTE</b>: <br/> {nome_contratante}, CPF {cpf_contratante}, residente e domiciliado em {endereco_contratante}, confirma que leu, entendeu e concordou com todos os termos e condições e também com o Aviso de Privacidade da Vetorial.
    """
    story.append(Paragraph(texto_contratante_dados, styles['Justify']))
    story.append(Spacer(1, 5*mm))

    # Dados das Contratadas (Vetorial)
    texto_contratadas_vetorial = """
    Nossos serviços serão prestados por: <br/>
    <b>CH CONTABILIDADE - GESTÃO CONTABIL & CONSULTORIA LTDA.</b> (CNPJ: 57.397.355/0001-83 e CRC/BA: 009504/O-3), com sede na Rua Almirante Alves Camara, número 73, sala 02, Engenho Velho de Brotas, Salvador - BA (ou apenas <b>Vetorial Contabilidade</b>).<br/><br/>
    O software é licenciado por: <br/>
    <b>CH CONTABILIDADE - GESTÃO CONTABIL & CONSULTORIA LTDA.</b> (CNPJ: 57.397.355/0001-83, com sede na Rua Almirante Alves Camara, número 73, sala 02, Engenho Velho de Brotas, Salvador - BA (ou apenas <b>Vetorial Tecnologia</b>).<br/><br/>
    Quando em conjunto, as duas empresas serão chamadas de <b>Vetorial</b> neste contrato, doravante denominada <b>CONTRATADA</b>.
    """
    story.append(Paragraph(texto_contratadas_vetorial, styles['Justify']))
    story.append(Spacer(1, 5*mm))
    
    # Cláusulas do Contrato Vetorial
    
    story.append(Paragraph("<b>1. SERVIÇOS PRESTADOS E SOFTWARE LICENCIADO PELA VETORIAL:</b>", styles['ContractHeading2']))
    story.append(Paragraph(
        "1.1 A depender do plano pelo qual você optou, a Vetorial poderá:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;a) Prestar serviços de assessoria contábil, fiscal e de folha de pagamento (“Assessoria Mensal”);<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;b) Licenciar o software Plataforma Vetorial (“Licenciamento de Software” e “Software”) para que o cliente possa inserir os dados pertinentes e usufruir das funcionalidades descritas nas cláusulas 4.1 e 5.2 deste Contrato, compreendendo tanto a abertura de empresa (“Abertura de Empresa”) quanto às funcionalidades adicionais (“Funcionalidades Adicionais”), respectivamente.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "1.2 Os serviços prestados e o acesso às funcionalidades do Software licenciado pela Vetorial e a sua interação com clientes acontecerão sempre de forma online, por meio da Plataforma Vetorial ou por e-mail. A depender do plano escolhido, as comunicações também poderão acontecer por WhatsApp ou telefone. Para sua segurança, os atendimentos se darão exclusivamente pelos endereços e números cadastrados por você na Plataforma Vetorial, podendo nossos atendentes solicitar informações cadastrais para confirmação de sua identidade.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "1.3 Os planos da Vetorial podem variar em seus serviços e valores, de acordo com a liberação de módulos do nosso sistema, as características e necessidades da sua empresa. Você poderá consultar todos os detalhes de seu plano na Plataforma Vetorial.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "1.4 O cadastro de informações e o envio de documentos solicitados deverão ocorrer por meio da Plataforma Vetorial dentro dos prazos estabelecidos. A Vetorial não se responsabiliza pelas consequências de informações ou documentações incompletas, não verdadeiras ou não apresentadas por você.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "1.5 Os documentos e informações necessárias para a prestação de serviços e correta funcionalidade de nosso software deverão ser enviados conforme informações fornecidas pela Vetorial. Em não havendo prazo nos atendimentos ou plataforma, os documentos e informações necessários deverão ser enviados em, no máximo, 30 (trinta) dias, contados da data da solicitação pela Vetorial. Se a Plataforma Vetorial estiver indisponível, você deverá enviar para o e-mail contabilidadevetorial@gmail.com dentro do prazo estabelecido.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "1.6 A assinatura e confirmação de todo e qualquer termo disponível na Plataforma Vetorial será de sua inteira responsabilidade.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "1.7 O comparecimento físico aos órgãos governamentais ou reguladores serão realizados exclusivamente por você, quando e se necessários, de acordo com as orientações dadas pela Vetorial, salvo campanhas promocionais especiais ou condições específicas de seu plano.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "1.8 Os módulos, funcionalidades e serviços adicionais poderão ser contratados separadamente, diretamente na plataforma, e estarão sempre vinculados ao presente contrato. Em nossa plataforma você encontrará a descrição completa das funções e serviços disponíveis para contratação, com indicação dos prazos estimados para a conclusão, preços e formas de pagamento.",
        styles['Justify']
    ))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph("<b>2. PRAZO DE DURAÇÃO DOS SERVIÇOS E DO LICENCIAMENTO DE SOFTWARE:</b>", styles['ContractHeading2']))
    story.append(Paragraph(
        "2.1 A prestação dos serviços e o Licenciamento de Software previstos neste contrato terá vigência conforme abaixo:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;a) Se você contratou apenas a Abertura de Empresa (sem os serviços de Assessoria Mensal): O prazo de duração será pelo tempo necessário à finalização de seu processo de abertura, contados a partir do aceite deste contrato. No entanto, se você não finalizar seu cadastro na plataforma ou não enviar todas as informações e documentações necessárias dentro prazo estabelecido em atendimento (no máximo 90 dias), seu contrato será terminado e nenhum valor pago será restituído.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;b) Se você está mudando de contador e contratou apenas os serviços de Assessoria Mensal (sem os serviços de Abertura de Empresa): O prazo de duração será de 12 (doze) meses, contados do início da responsabilidade técnica da Vetorial e renovado ano após ano, pelo mesmo período, desde que a Vetorial ou você não encerre a relação por uma das formas que estão previstas neste contrato.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;c) Se você contratou a Abertura de Empresa juntamente com os serviços de Assessoria Mensal (com fidelidade): o prazo de duração será de, no mínimo, 12 (doze) meses de fidelidade, contados a partir da data de emissão do seu CNPJ, e renovado ano após ano, pelo mesmo período, desde que a Vetorial ou você não encerre a relação por uma das formas que estão previstas neste contrato. No entanto, se você não finalizar seu cadastro na plataforma ou não enviar todas as informações e documentações necessárias dentro prazo estabelecido em atendimento (no máximo 90 dias), seu contrato será terminado e nenhum valor pago será restituído.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "2.2 Na contratação da Abertura de Empresa juntamente com os serviços de Assessoria Mensal, como você terá a isenção da cobrança da Abertura de Empresa (conforme cláusula 3.2), será aplicada a fidelidade mínima de 12 (doze) meses, contada a partir da data de emissão do seu CNPJ.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "2.3 A responsabilidade técnica da Vetorial Contabilidade, no caso de troca de contador (migração), se iniciará apenas a partir da confirmação do recebimento de todos os documentos solicitados, desde que estejam de acordo com as orientações da Vetorial. No caso de abertura de empresa, se iniciará a partir da data de inscrição da sua empresa no CNPJ.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "2.4 Não haverá suspensão da vigência do prazo de abertura de empresa ou deste contrato caso você deixe de cumprir com seus deveres e obrigações (incluindo protocolos, apresentação de documentos e informações e pagamento de taxas) para a conclusão da abertura da empresa.",
        styles['Justify']
    ))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph("<b>3. PREÇOS E PAGAMENTOS:</b>", styles['ContractHeading2']))
    story.append(Paragraph(
        "3.1 Os valores dos serviços de Assessoria Mensal e das funcionalidades de software correspondentes à Abertura de Empresa e às Funcionalidades Adicionais podem variar de acordo com o plano contratado e as características de sua empresa. Os valores estão disponíveis para consulta na Plataforma Vetorial.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "3.2 A contratação do Licenciamento de Software para Abertura de Empresa tem o custo de R\$ 999,00 (novecentos e noventa e nove reais) à vista ou R\$ 1.049,90 (mil e quarenta e nove reais e noventa centavos) parcelados em até 3 vezes. No entanto, esse valor será isento se você contratar essa funcionalidade de Software juntamente com os serviços de Assessoria Mensal com fidelidade de 12 (doze) meses.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "3.3 A isenção será concedida após o pagamento antecipado do valor correspondente a uma mensalidade do plano de Assessoria Mensal escolhido, que ficará como crédito para abater da primeira mensalidade que será cobrada a partir da emissão do CNPJ de sua empresa.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "3.4 Os valores dos planos mensais poderão variar a depender de: a) ser a empresa prestadora de serviços ou ter atividades de comércio; b) forma de pagamento mensal, semestral ou anual; c) regime tributário; d) quantidade de sócios; e) quantidade de empregados; f) faturamento mensal; g) local de sua sede; h) forma de comunicação ou atendimento; i) volume de notas fiscais e/ou boletos emitidos no mês; j) dentre outros.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "3.5 As mensalidades serão pagas de forma antecipada até o 15º (décimo quinto) dia de cada mês, por boleto bancário, pix ou cartão de crédito, e as notas fiscais serão emitidas em separado pelas duas empresas (os serviços prestados, pela Vetorial Contabilidade e o licenciamento do nosso software, pela Vetorial Tecnologia).",
        styles['Justify']
    ))
    story.append(Paragraph(
        "3.6 Sobre os valores em atraso incidirá multa moratória de 2% (dois por cento) e juros de mora de 0,033% (zero vírgula zero trinta e três por cento) por dia de atraso. Nós nos reservamos o direito de protestar a fatura em atraso nos cartórios e órgãos de proteção ao crédito.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "3.7 Os valores dos planos, dos serviços e do Licenciamento de Software descritos neste contrato poderão sofrer alterações mediante aviso prévio de 30 (trinta) dias.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "3.8 Mesmo que a sua empresa fique inativa ou com baixa movimentação, as mensalidades contratadas serão devidas até a solicitação de cancelamento, sem qualquer abatimento, uma vez que as suas obrigações contábeis, fiscais e trabalhistas permanecerão existindo.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "3.9 Todas as taxas devidas perante quaisquer órgãos e que sejam necessárias para o regular funcionamento de sua empresa deverão ser pagas diretamente por você, conforme orientações da Vetorial. Por questões de segurança, caso você receba qualquer cobrança de qualquer natureza, comunique a Vetorial antes de efetuar o pagamento.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "3.10 A ausência de pagamento das mensalidades poderá ocasionar a suspensão dos serviços, interrupção de seus acessos ao software licenciado e o cancelamento de seu contrato e eventuais benefícios que tenha direito, conforme o plano escolhido. A Vetorial poderá realizar a inscrição de sua empresa em órgãos de proteção ao crédito, ceder os direitos de crédito deste contrato a terceiros, bem como terceirizar procedimentos de cobrança, de forma que seus dados poderão ser cedidos a terceiros para esta finalidade em especial, caso haja o inadimplemento.",
        styles['Justify']
    ))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph("<b>4. COMO SERÁ REALIZADA A ABERTURA DE EMPRESA:</b>", styles['ContractHeading2']))
    story.append(Paragraph(
        "4.1 Para a Abertura de Empresa, as seguintes funcionalidades do Software da Vetorial Tecnologia estarão disponíveis:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;a) Consulta em órgãos públicos: consulta prévia da localização do imóvel onde se pretende instalar a empresa na Prefeitura e da viabilidade de nome na Junta Comercial;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;b) Elaboração e transmissão dos seguintes documentos necessários para a abertura de empresa: Contrato Social (para Sociedade Limitada e Sociedade Simples); Requerimento de Empresário (para Empresário Individual); Documento Básico de Entrada (DBE) na Receita Federal; Outros documentos obrigatórios para registro na Junta Comercial e Prefeitura (Inscrições Municipais, Alvarás e Licenças); Solicitação de Enquadramento no Simples Nacional (apenas se a empresa preencher os requisitos legais para tal).<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;c) Protocolos (quando forem digitais/online e a depender do sistema de cada localidade) de documentos e processos na Junta Comercial e Prefeitura.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "4.2 <b>NÃO ESTÃO INCLUSOS</b> nas funcionalidades de software na Abertura de Empresa:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;a) Protocolos de documentos e processos físicos na Junta Comercial ou Prefeitura; <br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;b) Registro da empresa ou sócios em órgãos representativos de classe, como CRA, CRC, CREA, OAB, exceto se você contratou um dos planos Master (anexo I); <br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;c) Coordenação ou acompanhamento de vistorias e avaliação do corpo de bombeiros e demais órgãos; <br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;d) Projeto técnico para obtenção de alvará; <br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;e) Documentos específicos solicitados pelos órgãos para abertura da sua empresa, como PGRSS (Programa de Gerenciamento de Resíduos, Cnes (Cadastro Nacional de Estabelecimentos de Saúde), Habite-se, entre outros; <br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;f) Consulta de marcas e patentes no Instituto Nacional de Propriedade Intelectual (INPI).",
        styles['Justify']
    ))
    story.append(Paragraph(
        "4.3 Para que a Abertura de Empresa seja realizada, você se compromete a:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;a) Enviar as informações e documentos necessários dentro dos prazos que forem solicitados, inclusive realizando impressões e digitalizações quando necessário;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;b) Cumprir os prazos indicados neste contrato ou pela Vetorial;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;c) Emitir o Certificado Digital da sua empresa (e-CNPJ) Modelo A1 ou outro modelo indicado pela Vetorial, assim que possível, e conforme as orientações repassadas pela Vetorial, sendo possível a utilização deste certificado em todos os sistemas necessários para a abertura da sua Empresa;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;d) Emitir a Procuração nos sistemas oficiais, autorizando a Vetorial como responsável pela Contabilidade de sua Empresa;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;e) Protocolar o processo de abertura de empresa ou documentos em órgãos públicos, quando houver necessidade (salvo campanhas promocionais especiais).<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;f) Registrar a empresa nos órgãos que regulamentam a sua atividade comercial, quando exigido (exceto na contratação dos planos Experts, conforme anexo I).<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;g) Atender toda e qualquer exigência dos órgãos públicos dentro do prazo solicitado pelas autoridades.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;h) Efetuar o pagamento de todas as taxas públicas ou eventuais despesas adicionais necessárias e decorrentes da Abertura de Empresa, conforme orientações da Vetorial.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;i) Confirmar a Razão Social e o Nome Fantasia da sua empresa na Plataforma Vetorial, além de incluir a descrição das atividades econômicas que vai explorar, escolha do regime tributário, bem como o endereço de sua empresa, sendo de sua inteira responsabilidade esta informação, mesmo quando a Vetorial fizer sugestões. Quaisquer solicitações de alterações serão tratadas como “Funcionalidade Adicional” com a cobrança de serviço adicional além do pagamento de taxas/custas.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;j) NÃO EXERCER ATIVIDADE EMPRESARIAL ANTES DA CONCLUSÃO DO REGISTRO DE SUA EMPRESA E DA OBTENÇÃO DE LICENÇAS E ALVARÁS, conforme determina o Artigo 967 do Código Civil. A Vetorial não se responsabilizará por qualquer prejuízo ou consequência que resultar da atividade iniciada antes da conclusão do processo de Abertura de Empresa.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "4.4 Decorrido o prazo estabelecido e (ou) informado pelo atendimento, ou na ausência de prazo estipulado pelo atendimento, e decorrido o prazo convencionado na cláusula 1.5, contados do aceite deste contrato, sem a finalização da Abertura de Empresa por sua culpa ou inércia, você precisará contratá-los novamente, pagando mais uma vez os valores relativos a eles.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "4.5 A Vetorial não se responsabiliza pelos prazos ou exigências feitas pelas juntas comerciais ou outros órgãos e que possam interferir no tempo da abertura de sua empresa.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "4.6 A escrituração contábil e a entrega de declarações acessórias devem, por lei, ser realizadas desde a data de abertura de inscrição da empresa no cartão CNPJ. Caso seja necessária a emissão de declaração retroativa de não movimentação a fim de garantir a regularidade contábil e tributária de sua empresa, a Vetorial poderá efetuar a cobrança da mensalidade de seu plano antes do término do processo de abertura da empresa.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "4.7 Após a conclusão do processo de abertura da empresa, e em estrita observância à legislação vigente, é obrigatório que os campos de e-mail e telefone no Cadastro Nacional da Pessoa Jurídica (CNPJ) sejam preenchidos exclusivamente com os dados da empresa.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "4.8 Na hipótese de você não responder à previsão constante na cláusula 4.7 para indicação dos dados de e-mail e telefone a serem informados no CNPJ, as equipes da Vetorial estarão autorizadas a utilizar os dados de e-mail e telefone do administrador/titular constantes na Plataforma Vetorial (Plataforma 3.0). Esta prerrogativa está em conformidade com os termos da Cláusula 9.4 do presente Contrato de Prestação de Serviços, contando com o devido respaldo técnico e jurídico.",
        styles['Justify']
    ))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph("<b>5. COMO SERÃO REALIZADOS OS SERVIÇOS DE ASSESSORIA CONTÁBIL, COM ROTINAS MENSAIS FISCAIS E DE FOLHA DE PAGAMENTO:</b>", styles['ContractHeading2']))
    story.append(Paragraph(
        "5.1 É condição essencial para a prestação dos serviços de Assessoria Mensal, sob pena de cancelamento dos serviços e término do contrato, que você adquira e nos forneça o certificado digital de sua empresa (e-CNPJ) Modelo A1, emitido pelo sócio administrador responsável na Receita Federal do Brasil, bem como Procuração e-CAC para a Vetorial Contabilidade, cuja falta pode sujeitar você a multas e penalidades não reembolsáveis pela Vetorial.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "5.2 O Software licenciado pela Vetorial Tecnologia possui as seguintes funcionalidades para garantir a realização de rotinas mensais fiscais e trabalhistas:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;a) Cálculo e emissão de guias de imposto, pró-labore, transmissão de obrigações acessórias mensais como, por exemplo, o SPED e demais guias obrigatórias por lei;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;b) Transmissão de declarações como, por exemplo, DIRF, DIMOB e DMED;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;c) Cálculo e disponibilização das guias de FGTS, INSS e IRRF;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;d) Preenchimento de informações de folha de pagamento e holerite;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;e) Elaboração de contratos de experiência de empregados;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;f) Elaboração de documentos para homologação de rescisões trabalhistas;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;g) Orientação da comunicação ao sindicato de admissão e demissão de empregados;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;h) Elaboração de recibos de férias;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;i) Outros procedimentos relacionados aos acima descritos e obrigatórios pela legislação brasileira.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "5.3 A Vetorial Contabilidade prestará os seguintes serviços:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;a) Escrituração Contábil: contabilização de todas as operações da empresa de acordo com normas e princípios contábeis vigentes; emissão de balancetes; elaboração de balanço patrimonial anual; demonstração de resultados; transmissão da escrituração contábil digital para a RFB via ECD - Escrituração Contábil Digital e demais demonstrações contábeis obrigatórias;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;b) Escrituração Fiscal: escrituração digital dos registros fiscais de todos os livros obrigatórios perante o governo federal, estadual e municipal;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;c) Demais exigências legais: atendimento às demais exigências previstas na legislação brasileira e que sejam serviços privativos de Contador, como por exemplo, a emissão de comprovante de rendimento de empregado e empregador, entre outras, conforme legislação vigente.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "5.4 Serviços contábeis assim como outras funcionalidades de Software, incluindo fiscais ou de folha de pagamento que não estejam descritos nas cláusulas 5.2 e 5.4 poderão ser contratados separadamente caso estejam listados entre os serviços e funcionalidades de Software adicionais disponíveis no Anexo I, e estão passíveis de cobranças, conforme tabela de serviços adicionais.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "5.5 A Vetorial não se responsabiliza por declarações a serem feitas ao BACEN ou Receita Federal, relacionados a valores mantidos pela empresa no exterior.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "5.6 Para os serviços de Assessoria Mensal você se compromete a:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;a) Adquirir e renovar periodicamente o Certificado Digital da sua empresa (e-CNPJ) Modelo A1, emitido pelo sócio administrador responsável na Receita Federal do Brasil, enviando para a Vetorial no prazo solicitado, assim como a emissão de Procuração e-CAC para a Vetorial Contabilidade no mesmo prazo.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;b) Manter todos os seus dados devidamente atualizados na Plataforma Vetorial.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;c) Providenciar a documentação fiscal-contábil listada neste contrato, em formato eletrônico e pela Plataforma Vetorial até o terceiro dia útil de cada mês ou no prazo informado pelo atendimento.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;d) Emitir suas Notas Fiscais Eletrônicas, imediatamente após o fato gerador, ou seja, quando do término da prestação do serviço, por meio da Plataforma Vetorial ou importá-las na Plataforma se emitidas por outro sistema ou plataforma.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;e) Importar para a Plataforma Vetorial o extrato bancário mensal de todas as suas contas PJ até o dia 10 (dez) do mês subsequente, no formato ofx.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;f) Encaminhar, através da Plataforma Vetorial, os comprovantes de pagamentos de impostos e demais despesas.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;g) Responder às solicitações da Vetorial referentes aos documentos e dados sobre movimentações financeiras realizadas no Brasil ou no Exterior, não se responsabilizando a Vetorial pela transmissão de informações incompletas, imprecisas ou enviadas fora do prazo.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;h) Fornecer e manter atualizados, na Plataforma Vetorial, usuários e senhas dos sistemas da Prefeitura e Receita Federal e do Certificado Digital para a transmissão das suas informações contábeis aos órgãos necessários.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;i) Informar, todo início de mês, os pagamentos recebidos, impostos e tributos pagos, notas fiscais emitidas e de serviços por você contratados (serviços tomados).<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;j) Enviar, todo início de mês, documentos relativos a outras operações realizadas pela empresa, tais como aquisição de créditos financeiros, bens móveis e imóveis, participação societária em outras empresas, recebimento de investimentos, entre outros.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;k) Fornecer, antes do encerramento de cada exercício social, CARTA DE RESPONSABILIDADE DA ADMINISTRAÇÃO, conforme artigo 3º da Resolução CFC nº 1.590/2020 do Conselho Federal de Contabilidade, que será disponibilizada anualmente junto à Plataforma Vetorial para leitura e aceite.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;l) Realizar, junto à Plataforma Vetorial, o processamento de folha de pagamento dos seus empregados. O presente contrato poderá ser rescindido caso o processamento de folha de salário seja realizado por terceiros que não a Vetorial.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;m) Responsabilizar-se pelo envio correto, conteúdo, legalidade e veracidade de todos os documentos e informações na Plataforma Vetorial. Inclusive, pela identificação das receitas e despesas correspondentes aos documentos importados.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;n) Entrar em contato com a Vetorial em caso de dúvidas sobre a tributação das suas atividades e/ou sempre que você executar atividades esporádicas.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;o) Encaminhar imediatamente, através da Plataforma Vetorial, eventuais alterações contratuais, transformações e demais atos regulatórios e societários que não forem realizados pela Vetorial.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;p) Se porventura receber antecipadamente quaisquer valores por serviços a serem prestados ou mercadorias a serem entregues, nos enviar mensalmente e até o dia 10 (dez) do mês subsequente o controle de recebimentos e respectivas Notas Fiscais emitidas.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;q) Realizar e enviar mensalmente à Vetorial, até o dia 10 (dez) de cada mês, seu controle de estoque de mercadorias (inventário), caso exerça atividades de comércio.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;r) Caso você receba rendas de outras fontes, tais como, de vínculos empregatícios no regime CLT, enviar mensalmente à Vetorial, até o dia 10 (dez) de cada mês, os respectivos holerites.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;s) Ao contratar colaboradores, cumprir todas as obrigações de SST (Saúde e Segurança do Trabalho), incluindo exames admissionais, demissionais, periódicos e de retorno ao trabalho, bem como providenciar os laudos conforme o grau de risco de sua empresa. Você está ciente de que o cumprimento destas obrigações são de sua responsabilidade e que o não cumprimento pode acarretar em multas e penalizações.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;t) Informar imediatamente à Vetorial sobre qualquer alteração no contrato social de sua empresa realizada por outras contabilidades.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;u) Caso você trabalhe com intermediação de serviços e receba valores na conta de sua empresa para repasse a terceiros, deverá manter os controles das operações, vinculando as entradas com as saídas de valores para justificar a não tributação dos totais recebidos. Esses controles são de sua responsabilidade exclusiva e não competem à Vetorial.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;v) Para as funcionalidades relacionadas à folha de pagamento, você deverá garantir que todos os seus empregados, incluindo estagiários, estejam devidamente registrados na Plataforma Vetorial. Eventuais lançamentos/descontos de folha, alterações contratuais (salário/carga horária), admissões e rescisões deverão ser informadas dentro dos prazos estabelecidos durante o atendimento, encaminhados por e-mail ou disponibilizados na Plataforma Vetorial.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "5.7 O não cumprimento dos itens da cláusula 5.7 poderá inviabilizar o fechamento contábil anual da sua empresa, incluindo a emissão do informe de rendimentos de sócios e empregados, além de comprometer a assertividade do software no cálculo e geração de guias para recolhimento de seus tributos, folha de pagamento e entrega de obrigações acessórias.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "5.8 Ao aceitar esse contrato, você declara estar de acordo que a Vetorial armazene e solicite a senha do certificado de sua empresa (e-CNPJ) Modelo A1 para o devido cumprimento da prestação dos serviços contábeis contratados. A Vetorial declara que adota todas as medidas de segurança necessárias e que utilizará o certificado exclusivamente para o envio de todas as obrigações de sua empresa perante os órgãos competentes, geração de guias de recolhimento, emissão de notas fiscais eletrônicas (quando contratado ou incluído em seu plano), para a identificação/confirmação de contas bancárias de sua empresa no sistema Registrato do Banco Central do Brasil, e para o acesso às áreas e órgãos que se fizerem necessárias para a correta prestação dos serviços de assessoria mensal e entrega de documentos e obrigações através de nosso software.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "5.8.1 Você está ciente que alguns sistemas necessários para a prestação dos serviços da Vetorial (ex.: Gov.br e sistemas das prefeituras municipais) possuem mecanismos de verificação de acesso em duas etapas. Caso você opte por habilitar esses mecanismos, isso poderá afetar a prestação dos serviços da Vetorial e o cumprimento dos prazos estabelecidos neste contrato. Nestes casos, é importante que você informe a Vetorial e siga todas as orientações repassadas pelas equipes de atendimento.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "5.9 A Vetorial se responsabilizará por eventuais multas aplicadas em razão da entrega de declarações fora do prazo por culpa exclusiva e comprovada da Vetorial. A responsabilidade estará limitada ao valor da multa e juros, não abrangendo o valor principal de impostos (sua obrigação).",
        styles['Justify']
    ))
    story.append(Paragraph(
        "5.10 A Vetorial não se responsabiliza por multas que você venha a dar causa por qualquer motivo, incluindo, mas não limitado ao atraso ou não entrega de informações, documentos, certificado digital e de declarações em tempo hábil mínimo de 3 (três) dias para a execução os serviços, inclusão de informações imprecisas ou erradas em nosso software ou mesmo por ações e omissões de entidades e pessoas que não sejam empregados ou prestadores de serviços da Vetorial.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "5.11 Caso a Vetorial identifique qualquer irregularidade, omissão ou débito fiscal nas informações fornecidas por você, ou em relação à legislação tributária aplicável, a Vetorial se compromete a comunicar o fato à você por escrito, indicando a natureza da irregularidade e os procedimentos necessários para sua regularização.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "5.12 Você se compromete a adotar as medidas necessárias para regularizar as irregularidades apontadas pela Vetorial no prazo estabelecido. Caso você não regularize a situação, a Vetorial poderá suspender a prestação dos serviços até que a irregularidade seja sanada.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "5.13 A não regularização das irregularidades apontadas pela Vetorial implicará na sua responsabilidade exclusiva perante o Fisco, isentando a Vetorial de qualquer responsabilidade solidária ou subsidiária.",
        styles['Justify']
    ))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph("<b>6. SERVIÇOS PRESTADOS POR PARCEIROS DA VETORIAL:</b>", styles['ContractHeading2']))
    story.append(Paragraph(
        "6.1 A Vetorial poderá disponibilizar, em caráter não-contributário, serviços, produtos e ferramentas de empresas parceiras com condições especiais e até com integração à Plataforma Vetorial, tais como: contas digitais, serviços e soluções financeiras, planos de saúde, produtos de seguros, softwares, sistemas de gestão e outros. Tais produtos, serviços e ferramentas são fornecidos pelas empresas parceiras da Vetorial e seu fornecimento é de exclusiva responsabilidade destas. Esses serviços não fazem parte dos serviços fornecidos pela Vetorial, de forma que a Vetorial não está obrigada a manter sua ativação disponível ao longo da vigência deste contrato.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "6.2 A Vetorial não se responsabiliza pelos produtos fornecidos, prestação de serviços realizados, tampouco pelas ferramentas disponibilizadas por parceiros à você, nem pela emissão de suas correspondentes Notas Fiscais.",
        styles['Justify']
    ))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph("<b>7. CANCELAMENTO DOS SERVIÇOS, DO LICENCIAMENTO DE SOFTWARE E TÉRMINO DO CONTRATO:</b>", styles['ContractHeading2']))
    story.append(Paragraph(
        "7.1 A Vetorial poderá solicitar o término deste contrato a qualquer tempo, mediante aviso prévio de 30 (trinta) dias. Você também poderá solicitar o encerramento do contrato e, consequentemente, o cancelamento dos serviços e/ou do Licenciamento de Software, desde que observado o aviso prévio de 30 (trinta) dias e as condições abaixo:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;a) Cancelamento durante o processo de Abertura de Empresa: será aplicada uma multa no valor de R\$ 200,00 (duzentos reais). Após o processamento dos documentos ou emissão de seu CNPJ pelo software, o valor adiantado pelo licenciamento não será mais devolvido e, caso a abertura da empresa tenha sido contratada em conjunto com a assessoria contábil, com rotinas mensais fiscais e de folha de pagamento, também serão aplicadas outras multas previstas neste contrato. Seu contrato será automaticamente cancelado pela Vetorial, sem direito a devolução dos valores já pagos, se após o prazo estabelecido pelo atendimento, ou se após o prazo da cláusula 1.5, contados a partir do aceite deste contrato, você não finalizar seu cadastro na Plataforma Vetorial, não enviar os documentos e informações solicitadas ou deixar de realizar pagamentos e protocolos necessários para a abertura de sua empresa.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;b) Cancelamento dos serviços de Assessoria Mensal: Caso você tenha contratado algum dos planos com serviços vinculados a fidelidade mínima de 12 (doze) meses e solicite o encerramento do contrato/ou der causa ao encerramento no curso desse prazo e após a emissão seu CNPJ, será cobrada uma multa no valor de 30% (trinta por cento) sobre as parcelas que ainda estiverem por vencer até o fim do prazo da fidelidade. Caso você tenha contratado apenas a Assessoria Mensal (sem a Abertura de Empresa), você poderá solicitar o cancelamento dos serviços a qualquer tempo, mediante aviso prévio de 30 (trinta) dias.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "7.2 Este contrato poderá ser terminado pela Vetorial sem o cumprimento do aviso prévio, nos seguintes casos:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;a) Não cumprimento dos termos ou obrigações estabelecidas neste contrato;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;b) Não pagamento de 2 (duas) mensalidades consecutivas;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;c) Caso haja indícios da prática de atos contrários às legislações ou às Políticas internas da Vetorial, tais como: corrupção, sonegação de impostos, falsificação de informações e documentos, oferta ou pagamento de vantagens indevidas a agentes públicos ou a empregados da Vetorial;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;d) Condutas que caracterizem desrespeito, assédio, ou qualquer forma de discriminação, seja por escrito ou verbalmente;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;e) A prática de ações antiéticas ou que impeçam a prestação de serviços em conformidade com as normas gerais da contabilidade;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;f) Caso você utilize a Plataforma Vetorial para fins comerciais e terceirização de serviços, como por exemplo, a prestação de serviços contábeis e fiscais a terceiros.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "7.3 Em caso de cancelamento do contrato durante o período de abertura do CNPJ por qualquer dos motivos mencionados no item 7.2, você deverá reembolsar à Vetorial todas as taxas pagas a órgãos públicos para a abertura do seu CNPJ, sem prejuízo da aplicação das penalidades previstas neste contrato.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "7.4 Se houver mensalidades atrasadas ou por vencer durante o aviso prévio, você precisará realizar o pagamento de todos os valores em aberto até a data fixada para o encerramento do contrato.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "7.5 Os danos causados em decorrência da não entrega dos serviços contábeis ou indisponibilidade de acesso ao Software durante seu período de inadimplência não serão de responsabilidade da Vetorial. Seu contrato poderá ser reativado mediante a quitação de todas as pendências financeiras em aberto - incluindo faturas correspondentes a contratações avulsas. Para retomar nosso contrato, poderemos exigir a realização de serviços de regularização do período em que sua empresa ficou sem contador.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "7.6 Se você tiver aproveitado de alguma outra condição promocional, a Vetorial poderá cobrar a devolução dos valores correspondentes aos benefícios concedidos e usufruídos caso você solicite o término antecipado do contrato. O mesmo acontecerá se você decidir solicitar a mudança do seu plano para outro de menor valor (downgrade) antes de completados 6 (seis) meses no plano de maior valor.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "7.7 Em caso de solicitação de cancelamento antes do cumprimento integral de eventual acordo realizado entre você e a Vetorial, no qual a Vetorial tenha antecipado algum valor com expectativa de restituição futura, você deverá restituir o valor antecipado à Vetorial no momento do cancelamento.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "7.8 A partir da data do término do contrato, os profissionais da Vetorial Contabilidade não terão mais responsabilidade técnica sobre contabilidade da sua empresa, nos termos Resolução CFC n.º 1590/2020. Os documentos e Livros Contábeis de sua empresa serão devidamente entregues a você, sendo de sua inteira responsabilidade o envio deles ao novo responsável técnico (contador).",
        styles['Justify']
    ))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph("<b>8. RESPONSABILIDADE DE ADMINISTRAÇÃO</b>", styles['ContractHeading2']))
    story.append(Paragraph(
        "8.1 Ao assinar este contrato você declara que:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;a) A atividade exercida por você e pela sua empresa não é ilegal;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;b) Todas informações que serão fornecidas para escrituração e elaboração das demonstrações contábeis, obrigações acessórias, apuração de tributos e arquivos eletrônicos exigidos pela fiscalização federal, estadual, municipal, trabalhista e previdenciária são legais, exatos e verdadeiros;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;c) Você é responsável pelas decisões de seu negócio e pelos controles internos de sua empresa, inclusive pela gestão de seu estoque, e que estes são adequados para o volume de transações ao tipo de atividade de seu negócio;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;d) Tomou conhecimento da Lei nº. 9.613/1998, que dispõe sobre lavagem de dinheiro, e que seguirá fielmente suas disposições;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;e) Não praticou ou tem conhecimento de qualquer fato ou violações de leis, normas e regulamentos praticados por terceiros cujos efeitos possam afetar a continuidade da operação da sua empresa ou devam ser considerados nas demonstrações contábeis, ou mesmo dar origem ao registro de provisão para contingências passivas;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;f) Está ciente que é de sua responsabilidade a manutenção e atualização de seu cadastro junto aos órgãos públicos e na Plataforma Vetorial;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;g) Autoriza a Vetorial a armazenar e alterar, quando necessário, suas senhas, logins e cadastros junto aos órgãos públicos, bem como criar acessos exigidos pela legislação. Essa autorização inclui a possibilidade da Vetorial gerar e assinar procurações em nome de sua empresa e/ou sócios para o cumprimento de qualquer obrigação regulatória, fiscal ou contábil, em especial, mas não se limitando, às autoridades municipais, estaduais e federais;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;h) Autoriza a Vetorial a consultar sua agenda de recebíveis e informações sobre existência de conta bancária e operações financeiras no BACEN e demais órgãos, com a finalidade de melhoria e otimização de sua prestação de serviços bem como oferecer produtos e propor soluções ao seu negócio e, eventualmente, auditar informações financeiras prestadas por você e serão escrituradas por nós;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;i) A Plataforma Vetorial será acessada por meio do usuário e senha criados por você, não sendo de responsabilidade da Vetorial, qualquer problema causado por pessoas a quem você tenha fornecido o acesso. O uso do Software por você será feito de forma lícita, apenas para seus fins internos, não incluindo a prestação de serviços a terceiros, sendo o acesso limitado a você ou pessoas devidamente autorizadas por você, que atuarão sob a sua responsabilidade e risco, observando os termos e condições de uso previstos neste contrato, especialmente aqueles previstos na cláusula 10;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;j) A Vetorial não tomará partido em casos de conflitos entre os sócios de sua empresa, podendo conceder o acesso a informações e documentos de sua empresa aos sócios solicitantes, após confirmação da identidade e vínculos.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;k) Caso você realize alterações e renovações de contrato social, alvarás ou licenças fora do sistema licenciado pela Vetorial (por meio de outro software, por conta própria ou por meio de algum prestador de serviços terceiro), você se compromete a atualizar suas informações cadastrais na Plataforma Vetorial. Caso você não realize essa atualização e a Vetorial gere informações imprecisas que lhe causem prejuízos, você não terá direito a qualquer indenização.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;l) Está ciente que é sua responsabilidade a renovação anual de Alvarás e Licenças de Funcionamento da sua empresa, inclusive o pagamento de eventuais taxas.",
        styles['Justify']
    ))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph("<b>9. LEI GERAL DE PROTEÇÃO DE DADOS</b>", styles['ContractHeading2']))
    story.append(Paragraph(
        "9.1 Ao aceitar os termos e condições deste contrato, você autoriza a Vetorial a acessar e usar todas as informações fornecidas por você durante o cadastro ou durante o atendimento, incluindo seus dados pessoais. Seus dados e informações permanecerão armazenados enquanto você for cliente, estiver utilizando os produtos e serviços da Vetorial.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "9.2 Mesmo após o cancelamento deste contrato, a Vetorial poderá armazenar seus dados pessoais pelo prazo necessário, em conformidade com a base legal que justifique a retenção dos dados, para fins de auditoria, cumprimento de obrigações legais ou regulatórias ou para exercício regular de direitos da Vetorial.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "9.3 A Vetorial se compromete a utilizar seus dados pessoais apenas nos limites estabelecidos neste Contrato e de seu Política de Privacidade, realizando o tratamento de acordo com a Lei nº 13.709/2018 - Lei Geral de Proteção de Dados (LGPD) e adotando todas as medidas de segurança necessárias que protejam do acesso, do uso e da divulgação não autorizadas de seus dados.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "9.4 A Vetorial não irá compartilhar suas informações com terceiros, salvo se: a) expressamente autorizado por você; b) necessário para a execução deste Contrato; c) para o cumprimento de obrigação legal ou regulatória pelo controlador; d) forem solicitadas por órgãos governamentais, administrativos ou judiciais; c) forem solicitadas pelo CRC, CFC e demais órgãos regulatórios e de fiscalização, incluindo o COAF sempre que necessário e nos termos da Resolução 1.530 do CFC e da Lei 8.137/90; d) forem necessárias para instruir processo administrativo ou judicial; e) para empresas do grupo Vetorial, a fim de que estas possam oferecer produtos e propor soluções ao seu negócio; f) forem necessárias, e no limite da necessidade, para empresas especializadas em cobrança ou órgãos de proteção ao crédito para no caso do seu inadimplemento com a Vetorial, nos termos da cláusula 3.10.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "9.5 Você declara que leu e está de acordo com nosso aviso de privacidade que integra este contrato por referência, para todos os fins e efeitos de direito e cuja versão atualizada está disponível no website da Vetorial (https://www.vetorial.com.br/documentos/politica-de-privacidade.pdf)",
        styles['Justify']
    ))
    story.append(Paragraph(
        "9.5.1 A Vetorial poderá alterar sua Política de Privacidade a qualquer momento, desde que dê publicidade à nova versão.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "9.6 Todas as notificações, solicitações, ou dúvidas relativas a Dados Pessoais que estejam sendo Tratados em razão deste Contrato deverão ser enviadas para o e-mail de contato: contabilidadevetorial@gmail.com.",
        styles['Justify']
    ))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph("<b>10. LICENÇA DE USO DA PLATAFORMA Vetorial:</b>", styles['ContractHeading2']))
    story.append(Paragraph(
        "10.1 Você declara e reconhece que a Plataforma Vetorial e todo material nela disponível, inclusive modificações, atualizações e novas versões, são de propriedade da Vetorial Tecnologia Ltda e são protegidos pela legislação de direitos autorais e demais direitos de propriedade intelectual e de software.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "10.2 A Vetorial Tecnologia, na qualidade de legítima licenciadora da Plataforma Vetorial, concede a você o direito temporário, não-exclusivo, limitado e intransferível de uso dela, de acordo com os termos e condições descritos neste contrato.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "10.3 É expressamente proibido, salvo se expressamente autorizado pela Vetorial Tecnologia: a) transferir, comercializar, sublicenciar, emprestar, alugar, arrendar ou, de qualquer outra forma, alienar a Plataforma Vetorial; b) utilizar a Plataforma com o intuito de comercializar e/ou terceirizar serviços; c) efetuar modificações, acréscimos ou derivações da Plataforma Vetorial, por você o ou através da contratação de terceiros; d) fazer engenharia reversa, descompilar ou desmontar a Plataforma Vetorial, ou qualquer outra medida que possibilite o acesso ao seu código-fonte; e) Copiar, total ou parcialmente, a Plataforma Vetorial ou sua documentação, ou usá-la de modo diverso do estipulado neste Contrato.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "10.4 A prática de qualquer das ações listadas no item 10.3 resultará no cancelamento e término imediato deste contrato sem que você tenha direito ao aviso prévio, sem prejuízo de você responder civil ou criminalmente pelas condutas.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "10.5 A Vetorial Tecnologia garante o funcionamento adequado da Plataforma Vetorial, SALVO: a) se a falha resultar de acidente, violação, mau uso ou de culpa exclusiva sua ou de terceiro; b) se os problemas, erros ou danos forem causados por uso concomitante de outros softwares que não tenham sido licenciados ou desenvolvidos pela Vetorial; c) por problemas decorrentes de ataques de programas de terceiros à Plataforma, incluindo vírus e malwares; d) em decorrência de qualquer descumprimento seu ao presente contrato.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "10.6 O funcionamento adequado da Plataforma Vetorial dependerá de sistemas operacionais e infraestrutura compatível, tais como acesso à Internet e serviços de telecomunicações, que não são fornecidos pela Vetorial e cuja responsabilidade de contratação é exclusivamente sua, não podendo ser responsabilizada pelo funcionamento inadequado da Plataforma por problemas decorrentes de serviços prestados por terceiros, inclusive equipamentos e navegadores de internet.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "10.7 A Vetorial não se responsabiliza por perdas e danos indiretos de qualquer natureza, inclusive lucros cessantes e reclamações de terceiros, custos de fornecimento de bens substitutos, serviços ou tecnologia alternativos ou custos com paralisações. A responsabilidade se limita aos danos diretos cuja responsabilidade ficar demonstrada, não excedendo a quantia paga por você durante a vigência deste contrato.",
        styles['Justify']
    ))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph("<b>11. CONDIÇÕES GERAIS:</b>", styles['ContractHeading2']))
    story.append(Paragraph(
        "11.1 Os serviços e funcionalidades oferecidos pela Vetorial são prestados, nos termos deste contrato, nas localidades, CNAES, regimes tributários e societários específicos em que atua, conforme especificados na Plataforma Vetorial.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "11.2 A Vetorial poderá extinguir planos ou alterar seus valores, a seu exclusivo critério, caso em que você será notificado com 30 (trinta) dias de antecedência. Em caso de extinção de seu plano, você poderá optar por outro plano vigente ou rescindir seu contrato sem aplicação de multas. No entanto, não havendo manifestação em contrário, você terá seu plano migrado automaticamente para o plano que, ao critério da Vetorial, seja o mais adequado para sua empresa, de forma que o valor da sua mensalidade poderá sofrer alterações, conforme a tabela de valores dos planos vigentes.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "11.3 Todos os valores gastos com materiais para execução de serviços, tais como livros, correios, carimbos, pastas de arquivos, CDS, cópias e etc. serão antecipados por nós e reembolsados por você, mediante apresentação dos respectivos comprovantes.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "11.4 A Vetorial presta serviços e licencia sua Plataforma para empresas de comércio desde que sejam optantes pelo simples nacional, emitam notas fiscais eletrônicas (nfc-e e nf-e), tenham a inscrição estadual ativa e atuem dentro da área atendida pela Vetorial.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "11.5 A Vetorial não presta serviços ou licencia Software para empresas de comércio ou serviço que: a) tenham filiais ou venham a ter durante a execução do contrato; b) que exerçam atividades de comércio de importação e exportação; c) com mais de 20 empregados; d) que realizem atividades industriais ou equiparadas à indústria; e) atuem com regime de caixa; f) façam cessão de mão de obra; e g) figurem como sócio PJ (pessoa jurídica) em outra empresa.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "11.6 Se alguma dessas condições nas cláusulas 11.5 e 11.6 se alterar durante a execução do contrato, a Vetorial poderá rescindi-lo, independente de notificação e aviso prévio.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "11.7 A Vetorial não será responsabilizada solidariamente perante órgãos públicos por seus atos ou omissões, exceto se comprovado que a Vetorial tinha conhecimento prévio e inequívoco de tais condutas.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "11.8 A responsabilidade da Vetorial se limita à prestação dos serviços contratados, não se estendendo a seus atos ou omissões que possam configurar ilícitos fiscais ou outros crimes.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "11.9 A Vetorial não se responsabilizará por qualquer ato ilícito praticado por você, incluindo, mas não se limitando à sonegação de impostos, fraudes fiscais ou outras condutas que violem a legislação. Você reconhece que a Vetorial não possui autoridade para alterar ou omitir informações nas demonstrações contábeis com o objetivo de dissimular a ocorrência de fatos geradores de tributos ou de fraudar a fiscalização.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "11.10 A Vetorial manterá sob sigilo todos os seus documentos e informações, exceto quando obrigada por lei a divulgá-los. Você autoriza a Vetorial a utilizar seus documentos e informações exclusivamente para a prestação dos serviços contratados.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "11.11 Na hipótese de a Vetorial ser responsabilizada por qualquer dano causado ao Cliente em decorrência da prestação dos serviços, o Cliente se compromete a indenizar a Vetorial por quaisquer prejuízos sofridos, inclusive honorários advocatícios.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "11.12 A Vetorial poderá aditar o presente contrato, caso seja necessário.",
        styles['Justify']
    ))
    story.append(Paragraph(
        "11.13 Fica eleito o foro da Comarca de Salvador, Estado da Bahia, para dirimir quaisquer dúvidas ou litígios decorrentes deste Contrato, renunciando expressamente a qualquer outro, mesmo que privilegiado.",
        styles['Justify']
    ))
    story.append(Spacer(1, 10*mm))
    
    # Data e Local
    cidade = processo.cidade or "Cidade de Exemplo"
    estado = processo.estado or "UF"
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
            story.append(Paragraph(f"<b>{nome_contratante}</b><br/>CONTRATANTE", styles['Center']))
        except Exception as e:
            story.append(Paragraph(f"[Erro ao carregar assinatura: {str(e)}]", styles['Center']))
    else:
        story.append(Paragraph("____________________________________________", styles['Center']))
        story.append(Paragraph(f"<b>{nome_contratante}</b><br/>CONTRATANTE", styles['Center']))
        
    story.append(Spacer(1, 10*mm))
    
    # Assinatura da Contratada (Placeholder ou imagem fixa se tivesse)
    story.append(Paragraph("____________________________________________", styles['Center']))
    story.append(Paragraph("<b>VETORIAL CONTABILIDADE LTDA</b><br/>CONTRATADA", styles['Center']))
    
    doc.build(story)
    content_buffer.seek(0)

    # -------------------------------------------------------------------------
    # Aplicação do Papel Timbrado (Background)
    # -------------------------------------------------------------------------
    try:
        # Tenta localizar o arquivo de background
        # 1. Tenta em settings.STATIC_ROOT / pdf / ... (produção)
        # 2. Tenta em static/pdf/... (desenvolvimento)
        
        bg_candidates = [
            os.path.join(settings.BASE_DIR, 'static', 'pdf', 'papeltimbrado.pdf'),
            os.path.join(settings.BASE_DIR, 'vetorial_project', 'static', 'pdf', 'papeltimbrado.pdf'),
        ]
        if hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT:
             bg_candidates.insert(0, os.path.join(settings.STATIC_ROOT, 'pdf', 'papeltimbrado.pdf'))

        bg_path = None
        for p in bg_candidates:
            if os.path.exists(p):
                bg_path = p
                break
        
        if bg_path:
            reader_content = PdfReader(content_buffer)
            reader_bg = PdfReader(bg_path)
            
            if len(reader_bg.pages) > 0:
                bg_page = reader_bg.pages[0]
                
                # --- Criar Mascara Branca para reduzir opacidade ---
                # Isso desenha um retangulo branco semitransparente sobre o background original
                try:
                    mask_buffer = io.BytesIO()
                    c = canvas.Canvas(mask_buffer, pagesize=A4)
                    c.setFillAlpha(0.40)
                    c.setFillColorRGB(1, 1, 1)
                    c.rect(0, 0, A4[0], A4[1], fill=True, stroke=False)
                    c.save()
                    mask_buffer.seek(0)
                    
                    reader_mask = PdfReader(mask_buffer)
                    if len(reader_mask.pages) > 0:
                        mask_page = reader_mask.pages[0]
                        bg_page.merge_page(mask_page, over=True)
                except Exception as e:
                    print(f"Erro ao criar mascara de opacidade: {e}")

                writer = PdfWriter()

                for page in reader_content.pages:
                    # Mescla o background (bg_page) SOB a pagina de conteudo
                    # over=False coloca o bg_page ATRAS do conteudo atual
                    page.merge_page(bg_page, over=False)
                    writer.add_page(page)
                
                final_buffer = io.BytesIO()
                writer.write(final_buffer)
                final_buffer.seek(0)
                return final_buffer
        
        # Se não encontrou background ou erro, retorna original
        return content_buffer

    except Exception as e:
        print(f"Erro ao aplicar papel timbrado: {e}")
        content_buffer.seek(0)
        return content_buffer