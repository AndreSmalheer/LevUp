import { switch_window, hide_current_window } from "../system.js";
import { load_user_data } from "../status.js";

document
  .getElementById("add_user_form")
  .addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const userName = formData.get("user_name");

    fetch("/create_user/" + userName)
      .then((response) => response.json())
      .then(async (data) => {
        load_user_data(
          data.data.level,
          data.data.xp,
          data.data.coins,
          data.data.xp_to_next_level,
          data.data.name
        );

        hide_current_window();

        setTimeout(() => {
          window.location.reload();
        }, 500);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });
