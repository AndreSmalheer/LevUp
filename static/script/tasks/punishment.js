import { getTaskDetails, getPunishmentDetail } from "../api.js";
import { show_window, switch_window } from "../system.js";

export function accept_punishment(punishment, task) {
  if (punishment == `none`) {
    console.warn("no punishment previded");
    return;
  }

  let exported_task = {
    task_name: punishment.name,
    coin_reward: task.coin_reward * -2,
    xp_reward: task.xp_reward * -2,
  };

  // add punisment as a task
  // remove failed task
}

export async function setup_accepet_punishment_window(task_id) {
  let task = await getTaskDetails(task_id);
  const punishment = await getPunishmentDetail(task.task.penelty_id);

  document.getElementById("punishment_task").innerHTML = task.task.task_name;

  const accept_button = document.getElementById("accept_punishment_button");
  document.getElementById("punishment").innerHTML = punishment["name"];

  accept_button.addEventListener("click", () =>
    accept_punishment(punishment, task.task)
  );

  switch_window("penelty_window");
}
