const element = (tag, props = {}) =>
  Object.assign(document.createElement(tag), props);
const append = (par, ...sibs) =>
  sibs.reduce((p, sib) => (p.appendChild(sib), p), par);
const queryEl = (qStr, el = document) => el.querySelector(qStr);

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

    $.ajax({
      url: "get_analysis",
      type: "GET",
      success: function (response) {
        response.forEach((item) => {
          const el = element("p", {
            id: "analysisText",
            className: "analysis",
          });
          el.textContent = item[1];
          el.style.display = "block";
          append(queryEl("#analysisDivText"), el);
        });
      },
      error: function (_xhr) {},
    });
  });
});
