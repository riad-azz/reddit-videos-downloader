// DOWNLOAD REDDIT VIDEO
try {
  (() => {
    const downloadForm = document.getElementById("download-form");
    const downloadButton = document.getElementById("download-button");
    const loadingButton = document.getElementById("loading-button");
    const errorElement = document.getElementById("error-message");

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

    const downloadVideo = async (url) => {
      const filename = url.substring(url.lastIndexOf("/") + 1);
      const response = await fetch(url);
      const blob = await response.blob();
      const downloadUrl = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = downloadUrl;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    };

    const fetchVideo = async (postUrl) => {
      const downloadAjax = "/ajax/download?url=" + postUrl;

      await fetch(downloadAjax)
        .then((response) => response.json())
        .then(async (json) => {
          const downloadUrl = json.media;
          if (downloadUrl) {
            await downloadVideo(downloadUrl);
            hideError();
          } else {
            showError(json.error);
          }
        })
        .catch((error) => showError(error));
    };

    downloadForm.onsubmit = async (event) => {
      event.preventDefault();
      toggleButton();

      const formData = new FormData(downloadForm);
      const postUrl = formData.get("url");

      try {
        await fetchVideo(postUrl);
      } catch (e) {
        console.error(e);
        showError();
      }

      toggleButton();
    };
  })();
} catch (error) {
  console.error(error);
}
