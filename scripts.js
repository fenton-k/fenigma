window.addEventListener("DOMContentLoaded", (event) => {
  // handlers for input fields

  // starting point input field
  document
    .getElementById("input-start")
    .addEventListener("input", getGeocodingUrl);
  document.getElementById("input-start").addEventListener("blur", geocode);

  // destination input field
  document
    .getElementById("input-destination")
    .addEventListener("input", getGeocodingUrl);
  document
    .getElementById("input-destination")
    .addEventListener("blur", geocode);
});

function getGeocodingUrl(evt) {
  const el = document.getElementById(evt.target.id);

  if (el.value) {
    return (
      "https://api.geoapify.com/v1/geocode/search?text=" +
      el.value +
      "&format=json&apiKey=5c772d8dcef74a719c12a22f542d36e4"
    );
  }

  return null;
}

function geocode(evt) {
  elm = document.getElementById(evt.target.id);
  textElm = elm.parentElement.querySelector("p");

  const url = getGeocodingUrl(evt);

  if (!url) {
    console.log("Cannot geocode nothing!");
    elm.classList.add("input-card-bad");
    textElm.classList.add("coords-bad");
    textElm.textContent = "Uh oh! Please enter SOMEWHERE!";
    return null;
  }

  if (textElm.classList.contains("coords-bad")) {
    textElm.classList.remove("coords-bad");
  }

  if (elm.classList.contains("input-card-bad")) {
    elm.classList.remove("input-card-bad");
  }
  textElm.textContent = "...thinking";

  retrieveURL(url, evt.target.id).then((data) => {
    // if geocoding failed, alert user and set input states to bad
    if (data["results"].length == 0) {
      console.log("failed to geocode");
      textElm.classList.add("coords-bad");
      textElm.textContent = "Oops, cannot find that place. Try again?";
      elm.classList.add("input-card-bad");
      return;
    }

    //
    if (elm.classList.contains("input-card-bad")) {
      elm.classList.remove("input-card-bad");
    }

    if (textElm.classList.contains("coords-bad")) {
      textElm.classList.remove("coords-bad");
    }

    place = data["results"][0];
    (lat = place.lat), (lon = place.lon);
    textElm.textContent = `(${lat.toFixed(2)}, ${lon.toFixed(2)})`;
  });
}

async function retrieveURL(url, target) {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(
        `Network response was not ok: ${response.status} on ${target}`
      );
    }
    return response.json();
  } catch (error) {
    console.error("There was a problem with the fetch operation:", error);
  }
}

function handleEnigmaButton() {
  // check if valid to click
  startCoords = document.getElementById("start-coords").textContent;
  destCoords = document.getElementById("dest-coords").textContent;

  if (!startCoords.includes("(") || !destCoords.includes("(")) {
    console.log("not ready to run");
    return;
  } else {
    console.log("ready to run");
  }

  // enable loading screen
  document.getElementById("search-card").style.display = "none";
  document.getElementById("loading-div").style.display = "grid";

  let backendUrl = `https://mikipapa.pythonanywhere.com/fenigma-api/search/${startCoords},${destCoords}`;

  retrieveURL(backendUrl, null).then((data) => {
    sessionStorage.setItem("apiData", JSON.stringify(data));
    window.location.href = "results.html";
  });
}

function buildCards() {
  jsonData = JSON.parse(sessionStorage.getItem("apiData"));
  console.log(jsonData);
  // check that we have data

  var container = document.getElementById("div-results");

  const shapes = [
    "grid-column: span 2; grid-row: span 3",
    "grid-column: span 1; grid-row: span 2",
    "grid-row: span 2;",
    "grid-row: span 3;",
    "grid-row: span 1; grid-column: span 1",
    "grid-row: span 1; grid-column: span 1",
    "grid-row: span 1; grid-column: span 1",
    "grid-row: span 1; grid-column: span 1",
  ];

  jsonData.forEach((engima) => {
    title = engima.title;
    desc = engima.subtitle;
    loc = engima.location;
    img = engima.thumbnail_url ? engima.thumbnail_url : "travel.jpg";
    link = engima.url;
    shape = shapes[Math.floor(Math.random() * shapes.length)];
    posOrNeg = Math.random() > 0.5 ? -1 : 1;
    console.log(img);
    rotation = Math.floor(Math.random() * 15) * posOrNeg;

    card = `
    <card
      class="card-result" 
      style="background-image: url(${img}); ${shape}; transform: rotate(${rotation}deg)"
      onclick="window.open('${link}')">
      <div>
      <h2>${title}</h2>
        <p>
          ${desc}
        </p>
        </div>
        <em style="display:inline-block; align-self: flex-end">${loc}</em>

    </card>
`;
    container.innerHTML += card;
  });
}

window.onload = buildCards;
