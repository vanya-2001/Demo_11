"use strict";

const elem = document.querySelector('#element');
const button = document.querySelector('#button');
const field = document.querySelector('#field');
let flag = false;
let textFlag = false;

let sum = (a, b) => a + b;

console.log(sum(4, 5));

//`<b>${temp}</b>`
button.addEventListener('click', () => {
    textFlag = !textFlag;
    let temp = elem.textContent;
    if (textFlag) {
        elem.innerHTML = `<b>${temp}</b>`;
        elem.style.color = 'red';
        button.value = 'Normal';
    } else {
        elem.innerHTML = `${temp}`;
        elem.style.color = '';
        button.value = 'Bold';
    }
});

field.addEventListener('focus', () => {
    flag = !flag;
    if (flag) {
        field.type = 'submit';
        field.value = 'Я теперь кнопка';
        field.style.backgroundColor = 'red';
    } else {
        field.type = 'text';
        field.value = 'Я теперь текстовое поле';
        field.style.backgroundColor = '';
    }
});

//console.log(elem.textContent)

// let a = 3;
// let b = 7;
// const PI = 3.14;
// let array = [1, 2, 3, 4, 5]; // массив
// let obj = { a: 5, b: 6, c: 7 }; // объект

// DOM - Document Object Model
// function sayHello(param = "John") {
//     console.log('Hello ' + param)
// }

// && - бинарный оператор "И"
// || - бинарный оператор "ИЛИ"
// if (b >= 0 && b <= 10)
//     console.log('Лежит в диапазоне');
// console.log(obj['a']);

// for "each" (let переменная of массив)
// for (let item of array) {
//     console.log(item);
// }

//полный цикл for
//      start  stop   step
// for(let i = 0; i < 5; i++) {
//     console.log(array[i]);
// }
//console.log(i);

// let count = 4;
// while (count > -1) {
//     console.log(array[count]);
//     count--; // декремент -= 1 ()
// }
// let res;
// if (a > b) {
//     console.log(a - b);
//     console.log(a * b);
// } else if (a == b) {
//     console.log('Переменные равны');
// } else {
//     res = 5;
//     console.log('a меньше b');
// }

// console.log(res);
// sayHello('Tom');