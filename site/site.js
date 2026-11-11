(() => {
  const config = window.OTAROO_SITE_CONFIG;

  if (!config) {
    throw new Error("Otaroo site configuration is missing. Check site/config.js.");
  }

  const isPublicHttpsUrl = (value) => {
    if (typeof value !== "string" || value.trim() === "") {
      return false;
    }

    try {
      return new URL(value).protocol === "https:";
    } catch {
      return false;
    }
  };

  const storeLinks = document.querySelectorAll("[data-store-link]");
  let configuredStoreCount = 0;
  storeLinks.forEach((link) => {
    const key = link.dataset.storeLink;
    const destination = config[key];

    if (isPublicHttpsUrl(destination)) {
      link.href = destination;
      link.hidden = false;
      configuredStoreCount += 1;
    }
  });

  if (configuredStoreCount < storeLinks.length) {
    document.querySelectorAll("[data-store-placeholder]").forEach((note) => {
      note.hidden = false;
    });
  } else {
    document.querySelectorAll("[data-store-placeholder]").forEach((note) => {
      note.hidden = true;
    });
  }

  document.querySelectorAll("[data-current-year]").forEach((year) => {
    year.textContent = String(new Date().getFullYear());
  });
})();
