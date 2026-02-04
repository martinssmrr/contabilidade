document.addEventListener("DOMContentLoaded", function () {
    const scrollContainers = document.querySelectorAll(".testimonials-scroll");
    
    scrollContainers.forEach(container => {
        // IMPORTANTE: Garantir que o comportamento de rolagem seja imediato para a animação JS funcionar
        container.style.scrollBehavior = "auto";

        const originalCards = Array.from(container.children);
        if (originalCards.length === 0) return;

        // Clonar os itens para criar o efeito infinito
        originalCards.forEach(card => {
            const clone = card.cloneNode(true);
            container.appendChild(clone);
        });

        // Configurações
        const speed = 1.0; // Velocidade em pixels por frame
        let scrollPos = container.scrollLeft;
        let isHovered = false;
        
        // Pausar na interação do usuário
        const pause = () => isHovered = true;
        const resume = () => isHovered = false;

        container.addEventListener('mouseenter', pause);
        container.addEventListener('mouseleave', resume);
        container.addEventListener('touchstart', pause);
        container.addEventListener('touchend', resume);
        
        function autoScroll() {
            if (!isHovered) {
                // O limite é a distância até o primeiro clone
                // Assim que o scroll chega nesse ponto, a visualização é idêntica ao início
                const firstClone = container.children[originalCards.length];
                
                if (firstClone) {
                    const limit = firstClone.offsetLeft - container.children[0].offsetLeft;
                    
                    scrollPos += speed;

                    if (scrollPos >= limit) {
                        // Reset suave: volta para o início subtraindo o comprimento do conjunto original
                        // Isso mantém a fluidez se o frame rate oscilar
                        scrollPos -= limit;
                    }

                    container.scrollLeft = scrollPos;
                }
            } else {
                // Sincronizar posição caso o usuário role manualmente
                scrollPos = container.scrollLeft;
            }
            requestAnimationFrame(autoScroll);
        }
        
        // Iniciar loop
        requestAnimationFrame(autoScroll);
    });
});
