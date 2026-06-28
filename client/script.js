const eventList = document.querySelector("#event-list");
const eventForm = document.querySelector("form");
const titleInput = document.querySelector("#title");

function renderEvent(event) {
  const li = document.createElement("li");
  li.textContent = event.title;
  eventList.appendChild(li);
}

fetch("http://localhost:5000/events")
  .then((response) => response.json())
  .then((events) => {
    eventList.innerHTML = "";
    events.forEach(renderEvent);
  });

eventForm.addEventListener("submit", (e) => {
  e.preventDefault();

  const title = titleInput.value.trim();
  if (!title) return;

  fetch("http://localhost:5000/events", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  })
    .then((response) => response.json())
    .then((event) => {
      renderEvent(event);
      eventForm.reset();
    });
});
