import { getTaskDetails } from "../api.js";
import { show_window, switch_window } from "../system.js";

export function accept_punishment(task_id) {
  if ((task_id = `none`)) {
    console.warn("no task idea previded");
    return;
  }

  console.log(task_id);

  // add punisment as a task
  // remove failed task
}

export async function setup_accepet_punishment_window(task_id) {
  let task = await getTaskDetails(task_id);

  document.getElementById("punishment_task").innerHTML = task.task.task_name;

  // get punishment info
  // document.getElementById("punishment").innerHTML = task_id;

  switch_window("penelty_window");
}
