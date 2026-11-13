const addExercise = document.getElementById("addExercise");
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

const type_of_workout = document.getElementById("type_of_workout");
const freeWeightButton = document.getElementById("freeWeightButton");
const bodyWeightButton = document.getElementById("bodyWeightButton");
const cardioButton = document.getElementById("cardioButton");
const bandsButton = document.getElementById("bandsButton");
const muscle = document.getElementById("muscle");
const maxTime = document.getElementById("maxTime");
const maxReps = document.getElementById("maxReps");
const bandStrength = document.getElementById("bandStrength");

const submitMuscle = document.getElementById("submitMuscle");
const submitMaxReps = document.getElementById("submitMaxReps");
const submitBandStrength = document.getElementById("submitBandStrength");
const submitMaxTime = document.getElementById("submitMaxTime");

const muscleInput = document.getElementById("muscleInput");
const maxRepsInput = document.getElementById("maxRepsInput");
const bandStrengthInput = document.getElementById("bandStrengthInput");
const maxTimeInput = document.getElementById("maxTimeInput");

const button = document.getElementById("button");
// 1. Fixed: Changed getElementsById to getElementById
const box = document.getElementById("buttons");

button.addEventListener("click", () => {
  box.classList.toggle("clicked");
  // 2. Fixed: Changed classlList to classList
  button.classList.toggle("clicked");
});
addExercise.addEventListener("click", () => {
  addExercise.style.display = "none";
  promptBox.style.display = "block";
});

submitExerciseName.addEventListener("click", () => {
  type_of_workout.style.display = "block";
  exerciseInput.readOnly = true;
});

freeWeightButton.addEventListener("click", () => {
  type_of_workout.style.display = "none";
  repSection.style.display = "block";
});

bodyWeightButton.addEventListener("click", () => {
  type_of_workout.style.display = "none";
  maxReps.style.display = "block";
});

cardioButton.addEventListener("click", () => {
  type_of_workout.style.display = "none";
  maxTime.style.display = "block";
});

bandsButton.addEventListener("click", () => {
  type_of_workout.style.display = "none";
  bandStrength.style.display = "block";
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
  muscle.style.display = "block";
});

submitMaxWeight2.addEventListener("click", () => {
  submitMaxWeight2.style.display = "none";
  threeRepInput.readOnly = true;
  muscle.style.display = "block";
});

submitMuscle.addEventListener("click", () => {
  muscleInput.readOnly = true;
});

submitMaxReps.addEventListener("click", () => {
  maxReps.style.display = "none";
  maxRepsInput.readOnly = true;
  muscle.style.display = "block";
});

submitBandStrength.addEventListener("click", () => {
  bandStrength.style.display = "none";
  bandStrengthInput.readOnly = true;
  muscle.style.display = "block";
});

submitMaxTime.addEventListener("click", () => {
  maxTime.style.display = "none";
  maxTimeInput.readOnly = true;
  muscle.style.display = "block";
});
