var comp_id = "";
var season_id = "";
var match_id = "";
var comp_name = "";

function loadItems() {
  $("#proceed").css("background", "#707070");
  $("#proceed").unbind("click");
  $(".item").fadeIn();
  $(".item").each(function () {
    $(this).css(
      "background",
      "hsla(" + ~~(360 * Math.random()) + "," + "70%," + "80%,1)"
    );
  });
  $(".item").hover(
    function () {
      $(this).find(".item-slide").addClass("active");
    },
    function () {
      $(this).find(".item-slide").removeClass("active");
    }
  );
  $(".item").click(function () {
    var clickedObject = $(this);
    var type = clickedObject.attr("type");
    var id = clickedObject.attr("id");
    $("#proceed").css("background", "#7aff7a");
    $("#proceed").unbind();
    $("#proceed").click(function () {
      if (type === "competition") {
        comp_id = id;
        comp_name = clickedObject.find("h2").text();
        $.ajax({
          type: "POST",
          url: "getSeasons",
          data: { comp_id: comp_id },
          dataType: "json",
          success: function (response) {
            $("#select-type").fadeTo(500, 0.01, function () {
              $("#select-type").text("season").fadeTo(500, 1);
            });
            var elements = [];
            response.forEach((szn) => {
              var el = $(
                "<div id=" +
                  szn.season_id +
                  " class='item' type='season' style='display: none'><div class='item-color'></div><div class='item-nfo'><div class='item-slide'></div><div class='item-content-container'><h2>" +
                  szn.season_name +
                  "</h2><h4>" +
                  comp_name +
                  "</h4></div></div></div>"
              ).hide();
              elements.push(el);
            });
            $("#selection-scroller")
              .children()
              .fadeOut(500, function () {
                $("#selection-scroller").empty();
                $("#selection-scroller").append(elements);
                loadItems();
                $(".item").fadeIn(500, function () {});
              });
          },
        });
      }
      if (type === "season") {
        season_id = id;
        $.ajax({
          type: "POST",
          url: "getMatches",
          data: { comp_id: comp_id, season_id: season_id },
          dataType: "json",
          success: function (response) {
            $("#select-type").fadeTo(500, 0.01, function () {
              $("#select-type").text("match").fadeTo(500, 1);
            });
            var elements = [];
            response.forEach((match) => {
              var el = $(
                "<div id=" +
                  match.id +
                  " class='item' type='match' style='display: none'><div class='item-color'></div><div class='item-nfo'><div class='item-slide'></div><div class='item-content-container'><h2><span>" +
                  match.home +
                  " &emsp; " +
                  match.h_score +
                  "</span> - <span>" +
                  match.a_score +
                  " &emsp; " +
                  match.away +
                  "</span></h2><h4>" +
                  match.date +
                  "</h4><h5>MW " +
                  match.mw +
                  "</h5></div></div></div>"
              ).hide();
              elements.push(el);
            });
            $("#selection-scroller")
              .children()
              .fadeOut(500, function () {
                $("#selection-scroller").empty();
                $("#selection-scroller").append(elements);
                loadItems();
                $(".item").fadeIn(500, function () {});
              });
          },
        });
      }
      if (type === "match") {
        match_id = id;
        var homeSpanText = clickedObject
          .find("h2")
          .find("span")[0]
          .textContent.split(" ");
        var awaySpanText = clickedObject
          .find("h2")
          .find("span")[1]
          .textContent.split(" ");
        var date = clickedObject.find("h4")[0].textContent;

        sessionStorage["teams"] = [
          homeSpanText.slice(0, -2).join(" "),
          awaySpanText.slice(2).join(" "),
        ].join(" - ");
        sessionStorage["scores"] = [
          homeSpanText[homeSpanText.length - 1],
          awaySpanText[0],
        ].join(" - ");
        sessionStorage["date"] = date;

        window.location = "/grapher?match_id=" + match_id;
      }
    });
    $(".item").hover(
      function () {
        $(this).find(".item-slide").addClass("active");
      },
      function () {
        $(this).find(".item-slide").removeClass("active");
      }
    );
    $(this).unbind("mouseleave");
    $(".item-slide").each(function () {
      $(this).removeClass("active");
    });
    $(this).find(".item-slide").addClass("active");
  });
}

$(function () {
  $("#selection-container").hide().fadeIn(1000);
  loadItems();
});
