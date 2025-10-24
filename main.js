const container = document.getElementById("system_container");
const sound = document.getElementById("openSound");
const msg = document.getElementById("activate_msg");

function activateSystem() {
  msg.style.opacity = 0;
  container.classList.add("active");
  sound.currentTime = 0;
  sound.play().catch(() => {});
  document.removeEventListener("click", activateSystem);
}

document.addEventListener("click", activateSystem);
