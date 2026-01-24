async function loadProducts(category) {
    var url = `/api/product/`;
    
    if (category != "all") {
        url += `?category=${category}`;
    }

    const response = await fetch(url);
    const products = await response.json();

    productsList.innerHTML = '';
    products.forEach(product => {
        const productHTML =
        `<div class="product_card"
            data-image="/static/images/${product.image}"
            data-price="${Math.round(product.price)} ₽"
            data-description="${product.description}"
            data-code="${product.id}"
            data-category="${product.category}"
            data-brand="${product.brand}"
            data-country="${product.country}"
            data-material="${product.material}"
            data-age="${product.animal_age}"
        >
            <img width="215" height="173" src="/static/images/${product.image}" alt="Изображение товара">
            <p class="price">${Math.round(product.price)} ₽</p>
            <p class="description">${product.description}</p>
            <button class="details_button">Подробнее</button>
        </div>`;
        
        productsList.insertAdjacentHTML("beforeend", productHTML);
    });
};

document.addEventListener('DOMContentLoaded', async function () {
    // Загрузка каталога
    loadProducts("all");
    
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

    // Категории
    const buttons = document.querySelectorAll('.catalog_btn');

    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            buttons.forEach(b => b.classList.remove('active'));

            btn.classList.add('active');

            const category = btn.dataset.category;

            loadProducts(category);
        });
    });

    // Карточка товара
    const modal = document.getElementById('myModal');
    const closeBtn = modal.querySelector('.close_btn');

    function openModal(card) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';

        modal.querySelector('img').src = card.dataset.image;
        modal.querySelector('.price_modal').textContent = card.dataset.price;
        modal.querySelector('.description_modal').textContent = card.dataset.description;

        modal.querySelector('#product_code').textContent = `Код товара: ${card.dataset.code}`;
        modal.querySelector('#product_category').textContent = `Категория: ${card.dataset.category}`;
        modal.querySelector('#product_brand').textContent = `Бренд: ${card.dataset.brand}`;
        modal.querySelector('#product_country').textContent = `Страна производства: ${card.dataset.country}`;
        modal.querySelector('#product_material').textContent = `Материал: ${card.dataset.material}`;
        modal.querySelector('#product_age').textContent =`Возраст питомца: ${card.dataset.age}`;
    };

    document.addEventListener('click', (e) => {
        if (!e.target.classList.contains('details_button')) return;

        const card = e.target.closest('.product_card');
        if (!card) return;

        openModal(card);
    });

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

    // Отзыв
    const review_form = document.getElementById('review_form');

    review_form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(review_form);
        const data = Object.fromEntries(formData);

        const response = await fetch(`/api/review/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            window.location.reload();
        } else {
            console.log(response);
        }
    });
});