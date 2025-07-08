let isAnimation = false;

document.querySelectorAll('.review-username').forEach(elem => {
    elem.addEventListener('click', async (event) => {
        event.preventDefault();
        if (isAnimation) return;

        const userId = elem.dataset.userId;
        const detailBox = document.getElementById(`other-user-${userId}`);

        if (detailBox.classList.contains('anime-in')) return;

        isAnimation = true;

        if (detailBox.innerHTML.trim() !== "") {
            detailBox.style.display = "block";
            detailBox.classList.remove('anime-out');
            detailBox.classList.add('anime-in');
            detailBox.addEventListener('animationend', () => {
                isAnimation = false;
            }, { once: true });
            return;
        }

        try {
            const response = await fetch(`/users/${userId}/ajax/`);
            if (!response.ok) throw new Error("Network response was not OK");
            const html = await response.text();
            detailBox.innerHTML = html;

            detailBox.style.display = "block";
            detailBox.classList.remove('anime-out');
            detailBox.classList.add('anime-in');
            detailBox.addEventListener('animationend', () => {
                isAnimation = false;
            }, { once: true });
        } catch (error) {
            detailBox.innerHTML = "<p style='color:red;'>読み込み失敗</p>";
            detailBox.style.display = "block";
            detailBox.classList.remove('anime-out');
            detailBox.classList.add('anime-in');
            detailBox.addEventListener('animationend', () => {
                isAnimation = false;
            }, { once: true });
        }
    });
});


document.addEventListener('click', (event) => {
    if (event.target.closest('.review-username')) return;
    if (isAnimation) return;

    const boxes = document.querySelectorAll('.anime-in');
    if (boxes.length === 0) return;

    isAnimation = true;
    boxes.forEach(box => {
        box.classList.remove('anime-in');
        box.classList.add('anime-out');
        box.addEventListener('animationend', () => {
            box.style.display = "none";
            isAnimation = false;
        }, { once: true });
    });
});
