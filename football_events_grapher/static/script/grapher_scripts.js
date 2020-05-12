var pitchColor = "#7aff7a"; // color of the pitch
var lineColor = "#ffffff"; // color of the lines
var successColor = "#3a34eb";
var failColor = "#ed0909";
var winColor = "#f7c305"; // goal or assist

var timeMin = 1;
var timeMax = 90;

var selectedEvents;
var eventsToDraw = [];

// time range slider controller
$(function () {
  if (sessionStorage.getItem("teams") === null) location.href = "/404";
  $("dt").click(function () {
    $(this).toggleClass("open");
    if ($(this).hasClass("open")) $("dt").not(this).removeClass("open");
  });
  $(".stat-num").click(function () {
    if (!$(this).hasClass("selected")) {
      let team = parseInt($(this).parent().parent().attr("team_id"));
      let start = $(this).parent().parent().attr("start");
      let player = parseInt($(this).parent().parent().attr("player_id"));
      let event = $(this).parent().attr("?");
      let outcome = $(this).attr("?");

      team = events.teams.find((t) => {
        return t.id === team;
      });
      if (start === "start") start = team.starters;
      else start = team.subs;
      player = start.find((p) => {
        return p.id === player;
      });
      selectedEvents = player.events.filter((e) => {
        return e.type === event;
      });
      if (outcome === "F")
        selectedEvents = selectedEvents.filter((e) => {
          return e.outcome === false;
        });
      if (outcome === "S")
        selectedEvents = selectedEvents.filter((e) => {
          return e.outcome === true;
        });
      eventsToDraw = selectedEvents.filter((e) => {
        return e.minute >= timeMin && e.minute <= timeMax;
      });
    } else {
      eventsToDraw = [];
    }
    $(this).toggleClass("selected");
    if ($(this).hasClass("selected"))
      $(".stat-num").not(this).removeClass("selected");
  });
  $("#context-h").find("h1").text(sessionStorage["teams"]);
  $("#context-h").find("h2").text(sessionStorage["scores"]);
  $("#context-h").find("h4").text(sessionStorage["date"]);
  $("#time-bar").slider({
    range: true,
    min: 1,
    max: 90,
    values: [1, 90],
    slide: function (event, ui) {
      timeMin = ui.values[0];
      timeMax = ui.values[1];
      $("#amount").val(timeMin + " - " + timeMax);
      eventsToDraw = selectedEvents.filter((e) => {
        return e.minute >= timeMin && e.minute <= timeMax;
      });
    },
  });
  $("#amount").val(
    $("#time-bar").slider("values", 0) +
      " - " +
      $("#time-bar").slider("values", 1)
  );
});

// p5 setup function
function setup() {
  var canvasDiv = document.getElementById("pitch");
  var height = canvasDiv.offsetHeight;
  canvasDiv.style.background = pitchColor;
  var canvas = createCanvas(height * 1.5, height);
  canvas.parent("pitch");
  background(pitchColor);
}

// p5 draw function
function draw() {
  var canvasDiv = document.getElementById("pitch");
  var height = canvasDiv.offsetHeight;
  var width = height * 1.5;

  var leftEnd = 0.04 * width;
  var rightEnd = 0.96 * width;
  var pitchW = rightEnd - leftEnd;
  var topEnd = 0.055 * height;
  var bottomEnd = 0.945 * height;
  var pitchH = bottomEnd - topEnd;

  var topBox = topEnd + pitchH / 4.44;
  var bottomBox = bottomEnd - pitchH / 4.44;
  var leftBoxEdge = leftEnd + pitchW / 6.66;
  var rightBoxEdge = rightEnd - pitchW / 6.66;

  var topPost = topEnd + pitchH / 2.22;
  var bottomPost = bottomEnd - pitchH / 2.22;

  var top6yd = topEnd + pitchH / 2.66;
  var bottom6yd = bottomEnd - pitchH / 2.66;
  var left6ydEdge = leftEnd + pitchW / 20;
  var right6ydEdge = rightEnd - pitchW / 20;

  var leftPen = leftEnd + pitchW / 10;
  var rightPen = rightEnd - pitchW / 10;

  stroke(lineColor);
  strokeWeight(1);
  rectMode(CORNERS);
  rect(0, 0, width, height); // background
  rect(leftEnd, topEnd, rightEnd, bottomEnd); // pitch
  circle((leftEnd + rightEnd) / 2, (topEnd + bottomEnd) / 2, pitchH / 3.71); // center circle
  circle(leftPen, (topEnd + bottomEnd) / 2, pitchH / 3.71); // left circle
  circle(rightPen, (topEnd + bottomEnd) / 2, pitchH / 3.71); // right circle
  line((leftEnd + rightEnd) / 2, topEnd, (leftEnd + rightEnd) / 2, bottomEnd); // halfway line
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

  eventsToDraw.forEach((e) => {
    let startLoc = createVector(
      leftEnd + pitchW / (120 / e.location[0]),
      topEnd + pitchH / (80 / e.location[1])
    );
    let dest;
    switch (e.type) {
      case "Pass":
        dest = createVector(
          leftEnd + pitchW / (120 / e.destination[0]),
          topEnd + pitchH / (80 / e.destination[1])
        );
        drawLine(startLoc, dest, e.outcome, e.assist);
        break;

      case "Shot":
        dest = createVector(
          leftEnd + pitchW / (120 / e.destination[0]),
          topEnd + pitchH / (80 / e.destination[1])
        );
        drawLine(startLoc, dest, e.outcome, e.goal);
        break;

      default:
        drawPoint(startLoc, e.outcome);
        break;
    }
  });
}

// p5 resize functon
function windowResized() {
  var canvasDiv = document.getElementById("pitch");
  var height = canvasDiv.offsetHeight;
  resizeCanvas(height * 1.5, height);
}

function drawLine(start, end, outcome, win) {
  push();
  let myColor;
  if (outcome) myColor = successColor;
  else myColor = failColor;
  if (win) myColor = winColor;
  stroke(myColor);
  strokeWeight(3);
  fill(myColor);
  line(start.x, start.y, end.x, end.y);
  var angle = atan2(start.y - end.y, start.x - end.x);
  translate(end.x, end.y);
  rotate(angle - HALF_PI);
  triangle(-7 * 0.5, 7, 7 * 0.5, 7, 0, -7 / 2);
  pop();
}

function drawPoint(placement, outcome) {
  push();
  let myColor;
  if (outcome) myColor = successColor;
  else myColor = failColor;
  fill(myColor);
  stroke(myColor);
  circle(placement.x, placement.y, 7);
  pop();
}
