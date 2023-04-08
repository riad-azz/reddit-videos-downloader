try {
  (() => {
    const downloadForm = document.getElementById("download-form");
    const downloadButton = document.getElementById("download-button");
    const loadingButton = document.getElementById("loading-button");
    const errorElement = document.getElementById("error-message");

    const fetchAjax = "ajax/fetch?url=";

    const showError = (error) => {
      error = error ?? "Something went wrong. Make a guess !!";
      errorElement.style.display = "block";
      errorElement.textContent = error;
    };

    const hideError = () => {
      errorElement.style.display = "none";
      errorElement.textContent = "";
    };

    const toggleButton = () => {
      downloadButton.classList.toggle("hidden");
      loadingButton.classList.toggle("hidden");
    };

    const isJsonResponse = (response) => {
      const contentType = response.headers.get("Content-Type");
      return contentType.includes("application/json");
    };

    const downloadVideo = async (filename, downloadUrl) => {
      const response = await fetch(downloadUrl);
      if (isJsonResponse(response)) {
        const data = await response.json();
        showError(data.error);
      } else {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const linkElement = document.createElement("a");
        linkElement.href = url;
        linkElement.download = filename;
        document.body.appendChild(linkElement);
        linkElement.click();
        linkElement.remove();
      }
    };

    const fetchVideo = async (postUrl) => {
      const requestUrl = fetchAjax + postUrl;
      const response = await fetch(requestUrl);
      if (!isJsonResponse(response)) {
        showError("Unexpected error from a third party.");
      } else {
        const data = await response.json();
        if (data.success) {
          await downloadVideo(data.filename, data.download_url);
        } else {
          showError(data.error);
        }
      }
    };

    downloadForm.onsubmit = async (event) => {
      event.preventDefault();
      toggleButton();

      const formData = new FormData(downloadForm);
      const postUrl = formData.get("url");
      try {
        hideError();
        await fetchVideo(postUrl);
      } catch (error) {
        console.log(`Error : ${error}`);
        showError("Unexpected error, something went wrong.");
      }

      toggleButton();
    };
  })();
} catch (error) {
  console.error(error);
}
