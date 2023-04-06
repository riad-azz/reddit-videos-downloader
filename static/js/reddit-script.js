// DOWNLOAD REDDIT VIDEO
try {
  (() => {
    const downloadForm = document.getElementById("download-form");
    const downloadButton = document.getElementById("theme-button");
    const errorElement = document.getElementById("error-message");

    const formDataset = downloadForm.dataset;
    const csrfToken = formDataset.csrfToken;
    const downloadUrl = "/ajax/download?url=";

    const showError = (error) => {
      console.log(error);
      errorElement.style.display = "block";
      errorElement.textContent = error;
    };

    const hideError = () => {
      errorElement.style.display = "none";
      errorElement.textContent = "";
    };

    const handleResponse = async (response) => {
      if (response.status < 200 || response.status > 299) {
        const json = await response.json();
        if (json.error) {
          return showError(json.error);
        }
      } else {
        hideError();
      }
    };

    downloadForm.onsubmit = async (event) => {
      event.preventDefault();
      downloadButton.disabled = true;

      const formData = new FormData(downloadForm);
      const url = formData.get("url");
      const requestUrl = downloadUrl + url;

      await fetch(requestUrl, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
        },
      })
        .then((response) => handleResponse(response))
        .catch((error) => showError(error));

      downloadButton.disabled = false;
    };
  })();
} catch (error) {
  console.error(error);
}
