const chainEl = document.getElementById("chain");
const progressFillEl = document.getElementById("progress-fill");
const progressLabelEl = document.getElementById("progress-label");
const pointerTrailEl = document.getElementById("pointer-trail");
const titleInput = document.getElementById("title-input");
const priorityInput = document.getElementById("priority-input");

const RING_CIRCUMFERENCE = 119.4;
let draggedId = null;
let lastState = null;

async function fetchState() {
  const res = await fetch("/api/state");
  return res.json();
}

function render(state) {
  lastState = state;
  const tasks = state.tasks;

  progressLabelEl.textContent = `${state.done_count}/${state.size}`;
  const ratio = state.size ? state.done_count / state.size : 0;
  progressFillEl.style.strokeDashoffset = String(RING_CIRCUMFERENCE * (1 - ratio));

  chainEl.innerHTML = "";

  if (tasks.length === 0) {
    const empty = document.createElement("div");
    empty.className = "chain-empty";
    empty.textContent = "head → null — add a task to start the chain";
    chainEl.appendChild(empty);
    return;
  }

  tasks.forEach((task, index) => {
    const row = buildRow(task, index === 0);
    chainEl.appendChild(row);

    if (index < tasks.length - 1) {
      const connector = document.createElement("div");
      connector.className = "connector";
      connector.innerHTML = `<span class="connector__line"></span><span class="connector__label">.next</span>`;
      chainEl.appendChild(connector);
    }
  });

  const nullRow = document.createElement("div");
  nullRow.className = "null-row";
  nullRow.id = "null-row";
  nullRow.textContent = "tail.next → null";
  chainEl.appendChild(nullRow);

  updatePointerTrail(tasks);
}

function buildRow(task, isHead) {
  const row = document.createElement("div");
  row.className = "node-row" + (isHead ? " node-row--head" : "") + (task.done ? " node-row--done" : "");
  row.draggable = true;
  row.dataset.id = task.id;

  row.innerHTML = `
    <span class="node-row__grip">⠿</span>
    <button class="node-row__check${task.done ? " node-row__check--checked" : ""}" data-role="check">
      <svg viewBox="0 0 16 16" fill="none"><path d="M3 8.5L6.2 12L13 4" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </button>
    <div class="node-row__body">
      <span class="node-row__title">${task.title}</span><br/>
      <span class="node-row__priority node-row__priority--${task.priority}">${task.priority}</span>
    </div>
    <button class="node-row__delete" data-role="delete">×</button>
  `;

  row.querySelector('[data-role="check"]').addEventListener("click", () => toggleTask(task.id));
  row.querySelector('[data-role="delete"]').addEventListener("click", () => removeTask(task.id));

  row.addEventListener("dragstart", (event) => {
    draggedId = task.id;
    row.classList.add("node-row--dragging");
    event.dataTransfer.effectAllowed = "move";
  });
  row.addEventListener("dragend", () => row.classList.remove("node-row--dragging"));
  row.addEventListener("dragover", (event) => {
    event.preventDefault();
    if (task.id !== draggedId) {
      row.classList.add("node-row--drop-target");
    }
  });
  row.addEventListener("dragleave", () => row.classList.remove("node-row--drop-target"));
  row.addEventListener("drop", (event) => {
    event.preventDefault();
    row.classList.remove("node-row--drop-target");
    if (draggedId === null || draggedId === task.id) return;

    const tasks = lastState.tasks;
    const draggedIndex = tasks.findIndex((t) => t.id === draggedId);
    const dropIndex = tasks.findIndex((t) => t.id === task.id);
    const targetIndex = draggedIndex < dropIndex ? dropIndex - 1 : dropIndex;

    moveTaskTo(draggedId, targetIndex);
    draggedId = null;
  });

  return row;
}

function updatePointerTrail(tasks) {
  const names = tasks.map((t) => t.title);
  pointerTrailEl.textContent = "head → " + names.join(" → ") + " → null";
}

async function addTask() {
  const title = titleInput.value.trim();
  if (!title) return;
  const priority = priorityInput.value;

  const res = await fetch("/api/add", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, priority }),
  });
  render(await res.json());
  titleInput.value = "";
}

async function toggleTask(taskId) {
  const res = await fetch(`/api/toggle/${taskId}`, { method: "POST" });
  render(await res.json());
}

async function removeTask(taskId) {
  const res = await fetch(`/api/remove/${taskId}`, { method: "POST" });
  render(await res.json());
}

async function clearCompleted() {
  const res = await fetch("/api/clear_completed", { method: "POST" });
  render(await res.json());
}

async function moveTaskTo(taskId, targetIndex) {
  const res = await fetch(`/api/move_to/${taskId}/${targetIndex}`, { method: "POST" });
  render(await res.json());
}

async function runTraversal() {
  const res = await fetch("/api/traverse");
  const { order } = await res.json();

  const rows = order.map((id) => chainEl.querySelector(`.node-row[data-id="${id}"]`));
  const nullRow = document.getElementById("null-row");

  pointerTrailEl.textContent = "head";

  for (let i = 0; i < rows.length; i++) {
    await sleep(420);
    rows.forEach((r) => r && r.classList.remove("node-row--traversing"));
    if (rows[i]) rows[i].classList.add("node-row--traversing");
    const task = lastState.tasks.find((t) => t.id === order[i]);
    pointerTrailEl.textContent += " → " + (task ? task.title : "?");
  }

  await sleep(420);
  rows.forEach((r) => r && r.classList.remove("node-row--traversing"));
  if (nullRow) nullRow.classList.add("null-row--active");
  pointerTrailEl.textContent += " → null";

  await sleep(700);
  if (nullRow) nullRow.classList.remove("null-row--active");
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

document.getElementById("add-btn").addEventListener("click", addTask);
document.getElementById("clear-btn").addEventListener("click", clearCompleted);
document.getElementById("traverse-btn").addEventListener("click", runTraversal);
titleInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") addTask();
});

fetchState().then(render);
