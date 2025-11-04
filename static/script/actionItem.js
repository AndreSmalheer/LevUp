class Action {
  constructor(
    label,
    checkbox = false,
    clickfunc = false,
    popup = false,
    popupData = ""
  ) {
    this.label = label;
    this.checkbox = checkbox;
    this.clickfunc = clickfunc;
    this.popup = popup;
    this.popupData = popupData;
  }

  create() {
    const container = document.getElementById("tasks_container");
    const actionDiv = document.createElement("div");
    actionDiv.classList.add("task");

    const actionLabel = document.createElement("label");
    actionLabel.classList.add("task_label");
    actionDiv.appendChild(actionLabel);

    if (this.checkbox) {
      const input = document.createElement("input");
      input.type = "checkbox";
      input.classList.add("task_checkbox");
      input.addEventListener("click", (event) => {
        event.stopPropagation();
        const taskContainer = event.target.closest(".task");
        if (event.target.checked) {
          taskContainer.classList.add("completed");
        } else {
          taskContainer.classList.remove("completed");
        }
      });
      actionLabel.appendChild(input);
    }

    const labelSpan = document.createElement("span");
    labelSpan.classList.add("task_text");
    labelSpan.textContent = this.label;
    actionLabel.appendChild(labelSpan);

    if (this.clickfunc) {
      actionDiv.addEventListener("click", this.clickfunc);
    }

    if (this.popup) {
      pass;
    }

    container.appendChild(actionDiv);
  }
}

function hello() {
  console.log("Task clicked!");
}

const action = new Action(
  "Do the dishes",
  false,
  false,
  true,
  "<ul><li>Test</li></ul>"
);
action.create();
