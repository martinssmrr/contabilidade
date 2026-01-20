// ==================================
// JAVASCRIPT CUSTOMIZADO - GESTÃO 360
// ==================================

document.addEventListener('DOMContentLoaded', function() {
    // Navbar transparente que fica sólida ao rolar
    const navbar = document.querySelector('.navbar');
    const heroSection = document.querySelector('.hero-section');
    
    function updateNavbar() {
        if (!navbar) return;
        
        if (heroSection) {
            const scrollPosition = window.scrollY || document.documentElement.scrollTop;
            if (scrollPosition > 50) {
                navbar.classList.remove('transparent');
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.add('transparent');
                navbar.classList.remove('scrolled');
            }
        } else {
            navbar.classList.remove('transparent');
            navbar.classList.add('scrolled');
        }
    }

    if (navbar) {
        updateNavbar(); // Executa ao carregar para definir estado inicial
        window.addEventListener('scroll', updateNavbar);
    }

    // Auto-dismiss de mensagens após 5 segundos
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Confirmação antes de deletar
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Tem certeza que deseja excluir este item?')) {
                e.preventDefault();
            }
        });
    });

    // Máscara para CPF/CNPJ (exemplo básico)
    const cpfCnpjInput = document.querySelector('#id_cpf_cnpj');
    if (cpfCnpjInput) {
        cpfCnpjInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            
            if (value.length <= 11) {
                // Máscara de CPF: 000.000.000-00
                value = value.replace(/(\d{3})(\d)/, '$1.$2');
                value = value.replace(/(\d{3})(\d)/, '$1.$2');
                value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
            } else {
                // Máscara de CNPJ: 00.000.000/0000-00
                value = value.replace(/^(\d{2})(\d)/, '$1.$2');
                value = value.replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3');
                value = value.replace(/\.(\d{3})(\d)/, '.$1/$2');
                value = value.replace(/(\d{4})(\d)/, '$1-$2');
            }
            
            e.target.value = value;
        });
    }
});

// Função para formatar valores em Real (BRL)
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

// Função para exibir notificações toast
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'position-fixed top-0 end-0 p-3';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
    }
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    document.getElementById('toast-container').appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
}

// ==================================
// TOGGLE DE PLANOS (SERVIÇOS / COMÉRCIO)
// ==================================

document.addEventListener('DOMContentLoaded', function() {
    const toggleButtons = document.querySelectorAll('.toggle-btn');
    const planosServicos = document.getElementById('planos-servicos');
    const planosComercio = document.getElementById('planos-comercio');

    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const toggleType = this.getAttribute('data-toggle');

            // Remove a classe active de todos os botões
            toggleButtons.forEach(btn => btn.classList.remove('active'));

            // Adiciona a classe active no botão clicado
            this.classList.add('active');

            // Alterna a exibição dos planos
            if (toggleType === 'servicos') {
                planosServicos.style.display = 'block';
                planosComercio.style.display = 'none';
            } else if (toggleType === 'comercio') {
                planosServicos.style.display = 'none';
                planosComercio.style.display = 'block';
            }
        });
    });
});
