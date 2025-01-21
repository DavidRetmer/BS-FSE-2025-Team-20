document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.querySelector('.navbar');

    window.addEventListener('scroll', function() {
        // Si la posición del scroll es mayor a 50px, cambiamos la barra a sólida
        if (window.scrollY > 50) {
            navbar.classList.add('solid');  // Añadimos la clase 'solid'
            navbar.classList.remove('transparent');  // Eliminamos la clase 'transparent'
        } else {
            navbar.classList.remove('solid');  // Eliminamos la clase 'solid'
            navbar.classList.add('transparent');  // Añadimos la clase 'transparent'
        }
    });
});
