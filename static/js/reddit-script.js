// DOWNLOAD REDDIT VIDEO
try {
  (() => {
    const downloadForm = document.getElementById("download-form");
    const downloadButton = document.getElementById("download-button");
    const loadingButton = document.getElementById("loading-button");
    const errorElement = document.getElementById("error-message");
    const downloadUrl = "/ajax/download?url=";
    const requestUrl = "/ajax/request-video?url=";

    const showError = (error) => {
      error = error ?? "Something went wrong...";
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
      const downloadAjax = downloadUrl + postUrl;
      const requestAjax = requestUrl + postUrl;
      // Download the video if it exists on the server
      const primaryRes = await fetch(downloadAjax);
      const primaryJson = await primaryRes.json();
      if (primaryJson.media) {
        let mediaUrl = primaryJson.media;
        await downloadVideo(mediaUrl);
        hideError();
      } else {
        // Request the server to download the video and store it
        const requestRes = await fetch(requestAjax);
        if (requestRes.status === 429) {
          return showError("Too many requests max limit reached (10 per hour)");
        }
        // Try to fetch the video again
        const secondaryRes = await fetch(downloadAjax);
        const secondaryJson = await secondaryRes.json();
        if (secondaryJson.media) {
          let mediaUrl = secondaryJson.media;
          await downloadVideo(mediaUrl);
          hideError();
        } else {
          showError(secondaryJson.error);
        }
      }
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
