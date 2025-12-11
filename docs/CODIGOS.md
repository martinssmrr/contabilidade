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