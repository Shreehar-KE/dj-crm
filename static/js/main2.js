const button = document.querySelector("button"),
toast = document.querySelector(".cstm-toast");
closeIcon = document.querySelector(".cstm-close"),
progress = document.querySelector(".cstm-progress");

let timer1, timer2;

button.addEventListener("click", () => {
toast.classList.add("cstm-active");
progress.classList.add("cstm-active");

timer1 = setTimeout(() => {
toast.classList.remove("cstm-active");
}, 5000);

timer2 = setTimeout(() => {
progress.classList.remove("cstm-active");
}, 5300);
});

closeIcon.addEventListener("click", () => {
toast.classList.remove("cstm-active");

setTimeout(() => {
progress.classList.remove("cstm-active");
}, 300);

clearTimeout(timer1);
clearTimeout(timer2);
});