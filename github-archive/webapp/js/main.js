;(function($){
  var LOADER = $('#loader');
  LOADER.hide();
  
  var ERROR = $('#error');
  ERROR.hide();

  startLoading = function(){
    LOADER.show();
    ERROR.hide();
  };

  finishLoading = function(e){
    LOADER.hide();
    if (typeof e != 'undefined') {
      ERROR.text(e.message);
      ERROR.show();
    }
  };
  
  showSqlResult = function(rowCount, duration) {
    $("#result").html("SELECT " + rowCount + " rows in set (" + duration / 1000 + " sec)");
  };
  
  getCanvas = function(width, height, margin){
    return d3.select('#viz')
      .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .attr("class", "viz")
        .append("g")
          .attr("class", "viewport")
          .attr("transform", function(d){ return "translate("+ [margin.left, margin.top] +")"; })
  };

  $('#btn-viz0').on('click', function(e){ $("#viz").empty(); showPrLanguages(e); });
  $('#btn-viz1').on('click', function(e){ $("#viz").empty(); showPrLatencies(e); });
  $('#btn-viz2').on('click', function(e){ $("#viz").empty(); showCommitSentiments(e); });

}(jQuery));
