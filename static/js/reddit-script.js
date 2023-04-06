// DOWNLOAD REDDIT VIDEO
try {
  (() => {
    const downloadForm = document.getElementById("download-form");
    const downloadButton = document.getElementById("download-button");
    const loadingButton = document.getElementById("loading-button");
    const errorElement = document.getElementById("error-message");

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

    const toggleButton = () => {
      downloadButton.classList.toggle("hidden");
      loadingButton.classList.toggle("hidden");
    };

    const handleResponse = async (response) => {
      if (response.status === 200) {
        const json = await response.json();
        const filename = json.media.substring(json.media.lastIndexOf("/") + 1);
        const mediaResponse = await fetch(json.media);
        if (mediaResponse.status != 200) {
          return showError(
            "Too many download requests. please try again later (around 5 min)."
          );
        } else {
          const mediaBlob = await mediaResponse.blob();
          const downloadUrl = URL.createObjectURL(mediaBlob);
          const link = document.createElement("a");
          link.href = downloadUrl;
          link.download = filename;
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);

          hideError();
        }
      } else {
        try {
          const json = await response.json();
          return showError(json.error);
        } catch (error) {
          console.log(error);
          return showError("Something went wrong...");
        }
      }
    };

    downloadForm.onsubmit = async (event) => {
      event.preventDefault();
      toggleButton();

      const formData = new FormData(downloadForm);
      const url = formData.get("url");
      const requestUrl = downloadUrl + url;

      try {
        await fetch(requestUrl).then((response) => handleResponse(response));
      } catch (error) {
        console.log(error);
        showError("Something went wrong. Try again.");
      }
      toggleButton();
    };
  })();
} catch (error) {
  console.error(error);
}
