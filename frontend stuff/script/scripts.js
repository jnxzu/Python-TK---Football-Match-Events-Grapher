let pitchColor = "#7aff7a";
let lineColor = "#ffffff";

$(function () {
  $("#time-bar").slider({
    range: true,
    min: 1,
    max: 90,
    values: [1, 90],
    slide: function (event, ui) {
      $("#amount").val(ui.values[0] + " - " + ui.values[1]);
    },
  });
  $("#amount").val(
    $("#time-bar").slider("values", 0) +
      " - " +
      $("#time-bar").slider("values", 1)
  );
});

function setup() {
  var canvasDiv = document.getElementById("pitch");
  var height = canvasDiv.offsetHeight;
  canvasDiv.style.background = pitchColor;
  var canvas = createCanvas(height * 1.5, height);
  canvas.parent("pitch");
  background(pitchColor);
}

function draw() {
  var canvasDiv = document.getElementById("pitch");
  var height = canvasDiv.offsetHeight;
  var width = height * 1.5;

  var leftEnd = 0.05 * width;
  var rightEnd = 0.95 * width;
  var pitchW = rightEnd - leftEnd;
  var topEnd = 0.075 * height;
  var bottomEnd = 0.925 * height;
  var pitchH = bottomEnd - topEnd;

  var topBox = topEnd + pitchH / 4.86;
  var bottomBox = bottomEnd - pitchH / 4.86;
  var leftBoxEdge = leftEnd + pitchW / 6.3;
  var rightBoxEdge = rightEnd - pitchW / 6.3;

  var topPost = topEnd + pitchH / 2.24;
  var bottomPost = bottomEnd - pitchH / 2.24;

  var top6yd = topEnd + pitchH / 2.736;
  var bottom6yd = bottomEnd - pitchH / 2.736;
  var left6ydEdge = leftEnd + pitchW / 18.9;
  var right6ydEdge = rightEnd - pitchW / 18.9;

  var leftPen = leftEnd + pitchW / 9.455;
  var rightPen = rightEnd - pitchW / 9.455;

  stroke(lineColor);
  strokeWeight(1);
  noFill();
  rectMode(CORNERS);
  rect(leftEnd, topEnd, rightEnd, bottomEnd); // pitch
  line((leftEnd + rightEnd) / 2, topEnd, (leftEnd + rightEnd) / 2, bottomEnd); // halfway line
  circle((leftEnd + rightEnd) / 2, (topEnd + bottomEnd) / 2, pitchH / 3.71); // center circle
  circle(leftPen, (topEnd + bottomEnd) / 2, pitchH / 3.71); // left circle
  circle(rightPen, (topEnd + bottomEnd) / 2, pitchH / 3.71); // right circle
  fill(pitchColor);
  rect(leftEnd, topBox, leftBoxEdge, bottomBox); // left box
  rect(rightBoxEdge, topBox, rightEnd, bottomBox); // right box
  rect(leftEnd - 3, topPost, leftEnd, bottomPost); // left goal
  rect(rightEnd, topPost, rightEnd + 3, bottomPost); // right goal
  rect(leftEnd, top6yd, left6ydEdge, bottom6yd); // left 6yd box
  rect(right6ydEdge, top6yd, rightEnd, bottom6yd); // right 6yd box
  strokeWeight(8);
  point((leftEnd + rightEnd) / 2, (topEnd + bottomEnd) / 2); // kickoff
  point(leftPen, (topEnd + bottomEnd) / 2); // left penalty
  point(rightPen, (topEnd + bottomEnd) / 2); // right penalty
}

function windowResized() {
  var canvasDiv = document.getElementById("pitch");
  var height = canvasDiv.offsetHeight;
  var canvas = resizeCanvas(height * 1.5, height);
  canvas.parent("pitch");
}
