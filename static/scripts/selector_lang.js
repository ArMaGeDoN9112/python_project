const input = document.getElementById("site-language-selector");
input.onchange = (e) => {
  var val = document.getElementById("site-language-selector").value;
  window.location.replace("/"+val.toLowerCase());
};