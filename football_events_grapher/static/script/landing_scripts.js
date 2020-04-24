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
    var type = $(this).attr("type");
    var id = $(this).attr("id");
    $("#proceed").css("background", "#7aff7a");
    $("#proceed").click(function () {
      if (type === "competition") {
        // call
        $("#select-type").fadeTo(500, 0.01, function () {
          $("#select-type").text("season").fadeTo(500, 1);
        });
        var elements = [];
        var el = $(
          "<div class='item' type='season' style='display: none'><div class='item-color'></div><div class='item-nfo'><div class='item-slide'></div><div class='item-content-container'><h2>" +
            "####/##" +
            "</h2><h4>" +
            "Competition" +
            "</h4></div></div></div>"
        ).hide();
        elements.push(el);
        $("#selection-scroller")
          .children()
          .fadeOut(500, function () {
            $("#selection-scroller").empty();
            $("#selection-scroller").append(elements);
            loadItems();
            $(".item").fadeIn(500, function () {});
          });
      }
      if (type === "season") {
        // call
        $("#select-type").fadeTo(500, 0.01, function () {
          $("#select-type").text("match").fadeTo(500, 1);
        });
        var elements = [];
        var el = $(
          "<div class='item' type='match' style='display: none'><div class='item-color'></div><div class='item-nfo'><div class='item-slide'></div><div class='item-content-container'><h2><span>" +
            "Home Team" +
            " &emsp; " +
            "#" +
            "</span> - <span>" +
            "#" +
            " &emsp; " +
            "Away Team" +
            "</span></h2><h4>" +
            "##/##/####" +
            "</h4><h5>" +
            "MW ##" +
            "</h5></div></div></div>"
        ).hide();
        elements.push(el);
        $("#selection-scroller")
          .children()
          .fadeOut(500, function () {
            $("#selection-scroller").empty();
            $("#selection-scroller").append(elements);
            loadItems();
            $(".item").fadeIn(500, function () {});
          });
      }
      if (type === "match") {
        location.reload();
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
