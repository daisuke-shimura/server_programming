document.querySelectorAll('.review-username').forEach(elem => {
  elem.addEventListener('mouseenter', async () => {
    const userId = elem.dataset.userId;
    const detailBox = document.getElementById(`other-user-${userId}`);

    // すでに表示済みならスキップ
    if (detailBox.innerHTML.trim() !== "") {
      detailBox.style.display = "block";
      return;
    }

    try {
      const response = await fetch(`/users/${userId}/ajax/`);
      if (!response.ok) throw new Error("Network response was not OK");
      const html = await response.text();
      detailBox.innerHTML = html;
      detailBox.style.display = "block";
    } catch (error) {
      detailBox.innerHTML = "<p style='color:red;'>読み込み失敗</p>";
      detailBox.style.display = "block";
    }
  });

  elem.addEventListener('mouseleave', () => {
    const userId = elem.dataset.userId;
    const detailBox = document.getElementById(`other-user-${userId}`);
    detailBox.style.display = "none";
  });
});
