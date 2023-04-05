// DOWNLOAD REDDIT VIDEO
try {
  (() => {
    const downloadForm = document.getElementById("download-form");
    const downloadButton = document.getElementById("theme-button");

    downloadForm.onsubmit = async (event) => {
      event.preventDefault();
      downloadButton.disabled = true;

      const formData = new FormData(downloadForm);
      const url = formData.get("url");
      console.log(url);

      downloadButton.disabled = false;
    };
  })();
} catch (error) {
  console.error(error);
}
