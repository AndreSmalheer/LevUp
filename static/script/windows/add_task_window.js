import { addTaskToDOM } from "../tasks/domTasks.js";
import { switch_window } from "../system.js";

document
  .getElementById("add_task_form")
  .addEventListener("submit", async (e) => {
    e.preventDefault();

    const endTimeInput = document.getElementById("end_time").value;
    if (endTimeInput) {
      const now = new Date();
      const [hours, minutes] = endTimeInput.split(":").map(Number);
      const endTime = new Date();
      endTime.setHours(hours, minutes, 0, 0);

      if (endTime < now) {
        alert("End time cannot be earlier than the current time!");
        return; // stop form submission
      }
    }

    const formData = new FormData(e.target);

    const response = await fetch("/add_task", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();

    addTaskToDOM(result.task);

    // Close popup and reset form
    switch_window("system_container");
    e.target.reset();
  });
