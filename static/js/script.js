"use strict";
let a = 3;
let b = 7;
let array = [1, 2, 3, 4, 5]; // массив
let obj = {a: 5, b: 6, c: 7}; // объект

function sayHello(param="John") {
    console.log('Hello ' + param)
}


console.log(obj['a']);

// for "each" (let переменная of массив)
// for (let item of array) {
//     console.log(item);
// }

//полный цикл for
//      start  stop   step 
for(let i = 0; i < 5; i++) {
    console.log(array[i]);
}
//console.log(i);

// let count = 4;
// while (count > -1) {
//     console.log(array[count]);
//     count--; // декремент -= 1 ()
// }
let res;
if (a > b) {
    console.log(a - b);
    console.log(a * b);
} else if (a == b) {
    console.log('Переменные равны');
} else {
    res = 5;
    console.log('a меньше b');
}

console.log(res);
sayHello('Tom');