const btnRegistrar = document.getElementById("btnRegistrar");
const loader = document.getElementById("loader");

document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");
  const loader = document.getElementById("loader");
  const btn = document.getElementById("btnRegistrar");

  form.addEventListener("submit", (e) => {
    e.preventDefault(); // Evita que se envíe de inmediato
    btn.disabled = true;
    loader.classList.add("show");
    loader.setAttribute("aria-hidden", "false");

    // Espera 1 segundo (1000 ms) antes de enviar el formulario
    setTimeout(() => {
      form.submit(); // Envío real del formulario
    }, 1000);
  });
});
