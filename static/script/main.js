// --------------------
// Element References
// --------------------
const container = document.getElementById("system_container");
const sound = document.getElementById("openSound");
const msg = document.getElementById("activate_msg");

// --------------------
// System Activation
// --------------------
function activateSystem() {
  msg.style.opacity = 0;
  container.classList.add("active");
  sound.currentTime = 0;
  sound.play().catch(() => {});
  document.removeEventListener("click", activateSystem);
}

function show_add_task_window() {
  const container = document.getElementById("system_container");
  const task_container = document.getElementById("add_task_window");

  // Start the reverse animation
  container.classList.remove("active");
  void container.offsetWidth;
  container.classList.add("deactive");

  container.addEventListener("animationend", function handler() {
    // Hide system container immediately
    container.style.display = "none";

    // Delay 10ms before showing task window
    setTimeout(() => {
      sound.currentTime = 0;
      sound.play().catch(() => {});

      task_container.classList.add("active");
    }, 150);

    container.removeEventListener("animationend", handler);
  });
}

document.addEventListener("click", activateSystem);

const tasks = document.querySelectorAll(".task");
const popUp = document.querySelector(".task-pop-up");
let activeTask = null;

tasks.forEach((task) => {
  task.addEventListener("contextmenu", (e) => {
    e.preventDefault();

    popUp.style.left = `${e.pageX}px`;
    popUp.style.top = `${e.pageY}px`;
    popUp.classList.add("active");
    activeTask = task;
  });
});

document.addEventListener("click", (e) => {
  if (!popUp.contains(e.target)) {
    popUp.classList.remove("active");
  }
});

popUp.querySelectorAll("li").forEach((item) => {
  item.addEventListener("click", (e) => {
    console.log("Clicked menu item:", item.textContent.trim());
    console.log("On task:", activeTask.querySelector(".task_text").textContent);
    popUp.classList.remove("active");
    activePopUp = null;
  });
});

// --------------------
// XP & Level Handling
// --------------------
function set_xp(amount) {
  const progressBar = document.getElementById("progress_bar");
  const progressPercent = (amount / nextLevelXP) * 100;
  progressBar.style.width = `${progressPercent}%`;
}

function add_xp(amount) {
  const progressBar = document.getElementById("progress_bar");
  const xpContainer = document.getElementById("current_xp");

  currentXP += amount;

  // Handle level up
  while (currentXP >= nextLevelXP) {
    currentXP -= nextLevelXP;
    currentLevel++;
    nextLevelXP = Math.floor(nextLevelXP * 1.2);
    document.getElementById("level_container").querySelector("h1").innerHTML =
      currentLevel;
  }

  // Handle level down
  while (currentXP < 0 && currentLevel > 1) {
    currentLevel--;
    nextLevelXP = Math.floor(nextLevelXP / 1.2);
    currentXP += nextLevelXP;
    document.getElementById("level_container").querySelector("h1").innerHTML =
      currentLevel;
  }

  if (currentXP < 0) currentXP = 0;

  xpContainer.innerHTML = currentXP;

  // Update progress bar
  const progressPercent = (currentXP / nextLevelXP) * 100;
  progressBar.style.width = `${progressPercent}%`;
}

set_xp(currentXP);

// --------------------
// Coin Handling
// --------------------
function add_coins(amount) {
  const coinContainer = document.getElementById("coin_container");
  const h1 = coinContainer.querySelector("h1");

  current_coins += amount;
  h1.innerHTML = current_coins;
}

// --------------------
// Task Rewards
// --------------------
function getTaskRewards(taskLabel) {
  const coinElement = taskLabel.querySelector(
    ".reward_container .coin_container h1"
  );
  const xpElement = taskLabel.querySelector(
    ".reward_container .xp_container h1"
  );

  const coins = parseInt(coinElement.textContent, 10);
  const xp = parseInt(xpElement.textContent, 10);

  return { coins, xp };
}

function updateRewards(taskLabel, isChecked) {
  const { coins, xp } = getTaskRewards(taskLabel);
  const factor = isChecked ? 1 : -1;

  add_coins(coins * factor);
  add_xp(xp * factor);

  const taskTextSpan = taskLabel.querySelector(".task_text");
  if (!taskTextSpan) return;

  const taskName = taskTextSpan.textContent.trim();
  setTaskStatus(taskName, isChecked);
}

// --------------------
// Task Status Update
// --------------------
function setTaskStatus(taskName, completed) {
  const endpoint = completed ? "/completed_task/" : "/uncomplete_task/";
  const url = `${endpoint}${encodeURIComponent(taskName)}`;

  fetch(url, { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
      console.log(
        completed ? "✅ Task completed:" : "❌ Task uncompleted:",
        data
      );
    })
    .catch((err) => console.error("Error:", err));
}

// --------------------
// Task Checkbox Listeners
// --------------------
document.querySelectorAll(".task_checkbox").forEach((checkbox) => {
  checkbox.addEventListener("change", (event) => {
    const taskLabel = event.target.closest(".task_label");
    if (!taskLabel) return;

    updateRewards(taskLabel, checkbox.checked);
  });
});
