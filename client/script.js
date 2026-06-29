const eventList = document.querySelector("#event-list");
const eventForm = document.querySelector("form");
const titleInput = document.querySelector("#title");
const messageBox = document.querySelector("#message");

function showMessage(text, isError = false) {
  messageBox.textContent = text;
  messageBox.style.color = isError ? "#b45309" : "#166534";
}

function renderEvent(event) {
  const li = document.createElement("li");
  li.textContent = event.title;
  eventList.appendChild(li);
}

function loadEvents() {
  fetch("http://localhost:5000/events")
    .then((response) => {
      if (!response.ok) {
        throw new Error("Unable to load events");
      }
      return response.json();
    })
    .then((events) => {
      eventList.innerHTML = "";
      events.forEach(renderEvent);
      showMessage("");
    })
    .catch(() => {
      showMessage("Unable to load events right now.", true);
    });
}

loadEvents();

eventForm.addEventListener("submit", (e) => {
  e.preventDefault();

  const title = titleInput.value.trim();
  if (!title) {
    showMessage("Please enter an event title.", true);
    return;
  }

  fetch("http://localhost:5000/events", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  })
    .then((response) => response.json().then((data) => ({ ok: response.ok, data })))
    .then(({ ok, data }) => {
      if (!ok) {
        throw new Error(data.error || "Unable to add event");
      }

      renderEvent(data);
      eventForm.reset();
      showMessage(`Added "${data.title}".`);
    })
    .catch((error) => {
      showMessage(error.message || "Unable to add event.", true);
    });
});
