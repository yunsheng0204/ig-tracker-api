fetch("https://ig-tracker-api.onrender.com/api/visit", {
  method: "POST"
});

function submitIG() {
  const igUsername = document.getElementById("igInput").value.trim();

  if (igUsername === "") {
    alert("請輸入 IG 帳號");
    return;
  }

  fetch("https://ig-tracker-api.onrender.com/api/log", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ username: igUsername })
  })
  .then(res => res.json())
  .then(data => {
    console.log("記錄成功：", data);
    window.location.href = "https://yunsheng0204.github.io/my-web/index.html";
  })
  .catch(err => {
    alert("記錄失敗");
    console.error(err);
  });
}
