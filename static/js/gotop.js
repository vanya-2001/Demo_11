// получаем доступ к элементу кнопки "наверх"
const goTopBtn = document.querySelector("#go-top");
// значение однократной прокрутки в пикселях
const scrollStep = -150;

// обработчик события прокрутки окна
window.addEventListener("scroll", trackScroll);
// обработчик нажатия на кнопку (идём наверх)
window.addEventListener("click", goTop);

function trackScroll() {
    // положение "верхушки" страницы
    const scrolled = window.scrollY;
    // высота клиентской области окна
    const coords = document.documentElement.clientHeight;
    // если прокрутили на один экран, то кнопка появится
    if (scrolled > coords)
        goTopBtn.classList.add("go-top--show");
    else
        goTopBtn.classList.remove("go-top--show");
}

/* функция прокрутки наверх */
function goTop() {
    // если смещение есть (окно прокручено) 
    if(window.scrollY > 0) {
        // в этом случае "едем" наверх
        window.scrollTo(0, scrollStep, behavior="smooth"); // прокручиваем на заданную величину
        // рекурсивный вызов
        setTimeout(goTop, 0);
    }
}