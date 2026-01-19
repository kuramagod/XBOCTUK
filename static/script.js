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
const products = document.querySelectorAll('.product_card');


products.forEach(product => {
        product.querySelector('.details_button').addEventListener('click', () => {
            modal.style.display = 'flex';
            document.body.style.overflow = 'hidden';

            modal.querySelector('img').src = product.dataset.image;
            modal.querySelector('.price_modal').textContent = product.dataset.price;
            modal.querySelector('.description_modal').textContent = product.dataset.description;

            modal.querySelector('#product_code').textContent =
                `Код товара: ${product.dataset.code}`;
            modal.querySelector('#product_category').textContent =
                `Категория: ${product.dataset.category}`;
            modal.querySelector('#product_brand').textContent =
                `Бренд: ${product.dataset.brand}`;
            modal.querySelector('#product_country').textContent =
                `Страна производства: ${product.dataset.country}`;
            modal.querySelector('#product_material').textContent =
                `Материал: ${product.dataset.material}`;
            modal.querySelector('#product_age').textContent =
                `Возраст питомца: ${product.dataset.age}`;
            })
        })

closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
    document.body.style.overflow = '';
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