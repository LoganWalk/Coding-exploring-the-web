const startingInput = document.getElementById("start");
const startingSubmit = document.getElementById("startSubmit");

const buttonBox = document.getElementById("button-box");

const steelTip = document.getElementById("steel-tip");
const softTip = document.getElementById("soft-tip");

const steelBox1 = document.getElementById("steel-box1");
const softBox1 = document.getElementById("soft-box1");
const inputSteel1 = document.getElementById("steel-input1");
const inputSoft1 = document.getElementById("soft-input1");
const steelSubmit1 = document.getElementById("steel-submit1");
const softSubmit1 = document.getElementById("soft-submit1");

const steelBox2 = document.getElementById("steel-box2");
const softBox2 = document.getElementById("soft-box2");
const inputSteel2 = document.getElementById("steel-input2");
const inputSoft2 = document.getElementById("soft-input2");
const steelSubmit2 = document.getElementById("steel-submit2");
const softSubmit2 = document.getElementById("soft-submit2");

const steelBox3 = document.getElementById("steel-box3");
const softBox3 = document.getElementById("soft-box3");
const inputSteel3 = document.getElementById("steel-input3");
const inputSoft3 = document.getElementById("soft-input3");
const steelSubmit3 = document.getElementById("steel-submit3");
const softSubmit3 = document.getElementById("soft-submit3");

startingSubmit.addEventListener("click", () => {
  startingSubmit.style.display = "none";
  buttonBox.style.display = "block";
  startingInput.readOnly = true;
});

softTip.addEventListener("click", () => {
  softTip.style.display = "none";
  softBox1.style.display = "block";
});
steelTip.addEventListener("click", () => {
  steelTip.style.display = "none";
  steelBox1.style.display = "block";
});

steelSubmit1.addEventListener("click", () => {
  steelSubmit1.style.display = "none";
  inputSteel1.readOnly = true;
  steelBox2.style.display = "block";
});
softSubmit1.addEventListener("click", () => {
  softSubmit1.style.display = "none";
  inputSoft1.readOnly = true;
  softBox2.style.display = "block";
});

steelSubmit2.addEventListener("click", () => {
  steelSubmit2.style.display = "none";
  inputSteel2.readOnly = true;
  steelBox3.style.display = "block";
});
softSubmit2.addEventListener("click", () => {
  softSubmit2.style.display = "none";
  inputSoft2.readOnly = true;
  softBox3.style.display = "block";
});

steelSubmit3.addEventListener("click", () => {
  steelSubmit3.style.display = "none";
  inputSteel3.readOnly = true;
});
softSubmit3.addEventListener("click", () => {
  softSubmit3.style.display = "none";
  inputSoft3.readOnly = true;
});
