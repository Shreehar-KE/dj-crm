const toast = document.querySelector(".cstm-toast");

const closeIcon = document.querySelector(".cstm-close");
const progress = document.querySelector(".cstm-progress");

let timer1, timer2;

document.addEventListener("htmx:messages", (evt) => {
  const message = JSON.parse(evt.detail); // Parse the JSON data from the event
  const messageElement = toast.querySelector(".cstm-message .cstm-text-2");
  messageElement.textContent = message.message;

  // Show the toast and progress bar (assuming classes are the same)
  toast.classList.add("cstm-active");
  progress.classList.add("cstm-active");

  // Implement timers or logic for automatic disappearance as before (optional)
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


