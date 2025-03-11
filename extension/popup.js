function transfer() {
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    if (tabs.length === 0) return;

    const test_url = tabs[0].url;
    console.log("Sending URL:", test_url);

    document.getElementById('loader').classList.remove('hidden');

    fetch("http://localhost:8000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: test_url })
    })
      .then(response => response.json())
      .then(data => {
        document.getElementById('loader').classList.add('hidden');

        if (data.result === "SAFE") {
          document.getElementById('div1').textContent = data.result;
        } else {
          document.getElementById('div2').textContent = data.result;
        }
      })
      .catch(error => {
        console.error("Error:", error);
        document.getElementById('loader').classList.add('hidden');
      });
  });
}

document.addEventListener("DOMContentLoaded", function () {
  document.querySelector("button").addEventListener("click", transfer);
});
