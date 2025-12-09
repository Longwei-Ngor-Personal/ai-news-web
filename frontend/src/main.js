async function renderArticles() {
  const container = document.getElementById("articles");
  container.innerHTML = "<p>Loading...</p>";

  try {
    const articles = await fetchArticles(50);

    if (!articles.length) {
      container.innerHTML = "<p>No articles available yet.</p>";
      return;
    }

    container.innerHTML = "";

    articles.forEach((article) => {
      const card = document.createElement("div");
      card.className = "article-card";

      const published = new Date(article.published_at).toLocaleString();

      card.innerHTML = `
        <h2>${article.title}</h2>
        <p>${article.summary || ""}</p>
        <p><a href="${article.url}" target="_blank" rel="noopener noreferrer">Read original →</a></p>
        <div class="article-meta">
          <span>${article.source}</span> • <span>${published}</span>
          ${article.category ? ` • <span>${article.category}</span>` : ""}
        </div>
      `;

      container.appendChild(card);
    });
  } catch (err) {
    console.error(err);
    container.innerHTML = `<p>Error loading articles: ${err.message}</p>`;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const refreshBtn = document.getElementById("refresh-btn");
  refreshBtn.addEventListener("click", () => renderArticles());
  renderArticles();
});
