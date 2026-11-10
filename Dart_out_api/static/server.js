const startBox = document.getElementById("start-num-box");
const startingInput = document.getElementById("start");
const startingSubmit = document.getElementById("startSubmit");

const buttonBox = document.getElementById("button-box");

const doubleOut = document.getElementById("double-out");
const straightOut = document.getElementById("straight-out");

const doubleBox1 = document.getElementById("double-box1");
const straightBox1 = document.getElementById("straight-box1");
const inputDouble1 = document.getElementById("double-input1");
const inputStraight1 = document.getElementById("straight-input1");
const doubleSubmit1 = document.getElementById("double-Submit1");
const straightSubmit1 = document.getElementById("straight-Submit1");

const doubleBox2 = document.getElementById("double-box2");
const straightBox2 = document.getElementById("straight-box2");
const inputDouble2 = document.getElementById("double-input2");
const inputStraight2 = document.getElementById("straight-input2");
const doubleSubmit2 = document.getElementById("double-Submit2");
const straightSubmit2 = document.getElementById("straight-Submit2");

const doubleBox3 = document.getElementById("double-box3");
const straightBox3 = document.getElementById("straight-box3");
const inputDouble3 = document.getElementById("double-input3");
const inputStraight3 = document.getElementById("straight-input3");
const doubleSubmit3 = document.getElementById("double-Submit3");
const straightSubmit3 = document.getElementById("straight-Submit3");

let outType = null; // "double" or "straight"

function onSubmit(btn, next) {
  btn.addEventListener("click", async (e) => {
    e.preventDefault();
    try {
      const data = new FormData(btn.form);
      if (btn.name) data.append(btn.name, btn.value);
      const res = await fetch(btn.form.action, { method: "POST", body: data });
      if (!res.ok) {
        console.error("Server returned", res.status, "for", btn.form.action);
        return;
      }
      next();
    } catch (err) {
      console.error("Request failed:", err);
    }
  });
}

// Step 1: out type
onSubmit(doubleOut, () => {
  outType = "double";
  doubleOut.style.display = straightOut.style.display = "none";
  startBox.style.display = "block";
});
onSubmit(straightOut, () => {
  outType = "straight";
  doubleOut.style.display = straightOut.style.display = "none";
  startBox.style.display = "block";
});

// Step 2: starting number
onSubmit(startingSubmit, () => {
  startingSubmit.style.display = "none";
  startingInput.readOnly = true;
  (outType === "double" ? doubleBox1 : straightBox1).style.display = "block";
});

// Step 3: first dart
onSubmit(doubleSubmit1, () => {
  doubleSubmit1.style.display = "none";
  inputDouble1.readOnly = true;
  doubleBox2.style.display = "block";
});
onSubmit(straightSubmit1, () => {
  straightSubmit1.style.display = "none";
  inputStraight1.readOnly = true;
  straightBox2.style.display = "block";
});

// Step 4: second dart
onSubmit(doubleSubmit2, () => {
  doubleSubmit2.style.display = "none";
  inputDouble2.readOnly = true;
  doubleBox3.style.display = "block";
});
onSubmit(straightSubmit2, () => {
  straightSubmit2.style.display = "none";
  inputStraight2.readOnly = true;
  straightBox3.style.display = "block";
});

// Step 5: third dart
onSubmit(doubleSubmit3, () => {
  doubleSubmit3.style.display = "none";
  inputDouble3.readOnly = true;
});
onSubmit(straightSubmit3, () => {
  straightSubmit3.style.display = "none";
  inputStraight3.readOnly = true;
});
