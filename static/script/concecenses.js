import { attachPopUpListeners } from "./tasks/taskPopups.js";

function addConsequenceToDom(consequenceText) {
  const consequencesContainer = document.getElementById(
    "consequences_container"
  );

  // Create wrapper div
  const consequenceDiv = document.createElement("div");
  consequenceDiv.classList.add("consequence");

  // Create label
  const label = document.createElement("label");
  label.classList.add("consequence_label");

  // Create text span
  const span = document.createElement("span");
  span.classList.add("consequence_text");
  span.textContent = consequenceText;

  // Build structure
  label.appendChild(span);
  consequenceDiv.appendChild(label);
  consequencesContainer.appendChild(consequenceDiv);

  initConsequencePopUps();
}

function removeTaskFromDOM(consequenceId) {}

export function initConsequencePopUps() {
  const consequences = document.querySelectorAll(".consequence");
  const popUp = document.querySelector(".task-pop-up");
  attachPopUpListeners(
    consequences,
    popUp,
    updateConsequencePopUp,
    handleConsequenceAction
  );
}

function handleConsequenceAction(action, activeConsequence, popUp) {
  popUp.classList.remove("active");
}

function updateConsequencePopUp(popUp, consequence) {
  // Save original content if not already saved
  if (!popUp.dataset.original) {
    popUp.dataset.original = popUp.innerHTML;
  }

  // Set popup content for consequences
  popUp.innerHTML = `
    <ul>
      <li>Edit Consequence</li>
      <li>Delete Consequence</li>
    </ul>
  `;

  return true;
}

addConsequenceToDom("Sample Consequence 1");

document
  .getElementById("add_consequence_form")
  .addEventListener("submit", async (e) => {
    e.preventDefault();

    addConsequenceToDom(
      document.getElementById("consequence_name").value.trim()
    );

    switch_window("system_container");
    e.target.reset();
  });

initConsequencePopUps();
