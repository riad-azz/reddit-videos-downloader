const data = document.currentScript.dataset;
const themeUrl = data.themeUrl;
const csrfToken = data.csrfToken;

// NAVBAR DROPDOWN MENU
try {
  (() => {
    const navMenu = document.getElementById("nav-menu");
    const navMenuBtn = document.getElementById("burger-button");

    const toggleMenu = () => {
      navMenu.classList.toggle("hidden");
    };

    navMenuBtn.onclick = toggleMenu;
  })();
} catch (error) {
  console.error(error);
}

// CHANGE THEM (DARK/LIGHT)
try {
  (() => {
    const themeButton = document.getElementById("theme-button");

    const toggleTheme = async () => {
      themeButton.disabled = true;
      document.documentElement.classList.toggle("dark");
      const newTheme = document.documentElement.classList.contains("dark")
        ? "dark"
        : "light";
      fetch(`${themeUrl}?theme=${newTheme}`, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
        },
      });
      themeButton.disabled = false;
    };

    themeButton.onclick = toggleTheme;
  })();
} catch (error) {
  console.error(error);
}
