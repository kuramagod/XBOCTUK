// Хедер
const burger = document.getElementById('burger');
const menu = document.getElementById('mobileMenu');
let index = 0;

burger.addEventListener('click', () => {
    menu.classList.toggle('active');
});

menu.addEventListener('click', () => {
    menu.classList.remove('active');
});

// Карточка товара
const modal = document.getElementById('myModal');
const closeBtn = modal.querySelector('.close_btn');

function openModal() {
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    modal.style.display = 'none';
    document.body.style.overflow = '';
}

closeBtn.addEventListener('click', closeModal);

modal.addEventListener('click', (e) => {
    if (e.target === modal) {
        closeModal();
    }
});

// Слайдер
const slides = document.querySelectorAll('.slide');
const dots = document.querySelectorAll('.dot');

function showSlide(i) {
    slides.forEach(s => s.classList.remove('active'));
    dots.forEach(d => d.classList.remove('active'));

    slides[i].classList.add('active');
    dots[i].classList.add('active');
}

document.querySelector('.next').onclick = () => {
    index = (index + 1) % slides.length;
    showSlide(index);
};

document.querySelector('.prev').onclick = () => {
    index = (index - 1 + slides.length) % slides.length;
    showSlide(index);
};

dots.forEach((dot, i) => {
    dot.onclick = () => {
        index = i;
        showSlide(index);
    };
});

// Категории
const buttons = document.querySelectorAll('.catalog_btn');

buttons.forEach(btn => {
    btn.addEventListener('click', () => {
        buttons.forEach(b => b.classList.remove('active'));

        btn.classList.add('active');

        const category = btn.dataset.category;

        // loadProducts(category);
    });
});

// function loadProducts(category) {
//     fetch(`/api/products?category=${category}`)
//         .then(res => res.json())
//         .then(data => {
//             renderProducts(data);
//         });
// }