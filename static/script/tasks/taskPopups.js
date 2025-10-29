import { switch_window } from "../system.js";
import { removeTaskFromDOM } from "./domTasks.js";
import { show_window } from "../windows/edit_task_window.js";

export function initTaskPopUps() {
  const tasks = document.querySelectorAll(".task");
  const popUp = document.querySelector(".task-pop-up");
  let activeTask = null;

  tasks.forEach((task) => {
    task.addEventListener("contextmenu", (e) => {
      e.preventDefault();

      const popUp = document.querySelector(".task-pop-up");
      if (!popUp.dataset.original) {
        popUp.dataset.original = popUp.innerHTML;
      }

      if (task.classList.contains("failed")) {
        popUp.innerHTML = "<ul><li>Unavailable</li></ul>";
      } else {
        popUp.innerHTML = popUp.dataset.original;
      }

      popUp.style.left = `${e.pageX}px`;
      popUp.style.top = `${e.pageY}px`;
      popUp.classList.add("active");
      activeTask = task;
    });
  });

  document.addEventListener("click", (e) => {
    if (!popUp.contains(e.target)) popUp.classList.remove("active");
  });

  popUp.querySelectorAll("li").forEach((li) => {
    li.addEventListener("click", () => {
      const action = li.textContent.trim();
      if (action === "Edit Task") {
        show_window(activeTask);
      } else if (action === "Delete Task") {
        const taskName = activeTask
          .querySelector(".task_text")
          .textContent.trim();
        document.getElementById("delete_task_name").textContent = taskName;

        document.getElementById("confirm_delete_button").onclick = function () {
          removeTaskFromDOM(activeTask.id);
          removeTask(activeTask.id);
        };

        switch_window("delete_task_window");
      }
      popUp.classList.remove("active");
    });
  });
}

initTaskPopUps();
