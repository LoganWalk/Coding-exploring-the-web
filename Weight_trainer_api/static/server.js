const addButton = document.getElementById("addButton");
const promptBox = document.getElementById("promptBox");
const submitExerciseName = document.getElementById("submitExerciseName");
const exerciseInput = document.getElementById("exerciseInput");
const result = document.getElementById("result");

const repSection = document.getElementById("repSection");
const oneRepButton = document.getElementById("oneRepButton");
const threeRepButton = document.getElementById("threeRepButton");

const oneRepSection = document.getElementById("oneRepSection");
const threeRepSection = document.getElementById("threeRepSection");
const submitMaxWeight = document.getElementById("submitMaxWeight");
const submitMaxWeight2 = document.getElementById("submitMaxWeight2");
const oneRepInput = document.getElementById("oneRepInput");
const threeRepInput = document.getElementById("threeRepInput");

addButton.addEventListener("click", () => {
  promptBox.style.display = "block";
});

submitExerciseName.addEventListener("click", () => {
  repSection.style.display = "block";
  submitExerciseName.style.display = "none";
  exerciseInput.readOnly = true;
});
oneRepButton.addEventListener("click", () => {
  oneRepSection.style.display = "block";
  repSection.style.display = "none";
});
threeRepButton.addEventListener("click", () => {
  threeRepSection.style.display = "block";
  repSection.style.display = "none";
});

submitMaxWeight.addEventListener("click", () => {
  submitMaxWeight.style.display = "none";
  oneRepInput.readOnly = true;
});
submitMaxWeight2.addEventListener("click", () => {
  submitMaxWeight2.style.display = "none";
  threeRepInput.readOnly = true;
});
