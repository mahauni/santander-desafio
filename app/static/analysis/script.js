const btn = document.getElementById("showBtn");
const img = document.getElementById("analysisImage");
const text = document.getElementById("analysisText");

btn.addEventListener("click", () => {
  img.style.display = "block";
  text.style.display = "block";
});

$(document).ready(function () {
  $("#showBtn").click(function () {
    $.ajax({
      url: "get_image",
      type: "GET",
      success: function (_response) {
        $("#analysisImage").attr("src", "get_image");
      },
      error: function (_xhr) {},
    });
  });
});
