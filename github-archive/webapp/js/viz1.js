;(function(){
  /**
   * viz1 - Pull Request Latencies
   *
   **/
   
  var QUERY = $( "#query" ).text();
  
  // canvas width/height/margin
  var margin = {top: 10, right: 40, bottom: 60, left: 40},
      width = 960 - margin.left - margin.right,
      height = 500 - margin.top - margin.bottom;


  var draw = function(data) {
    var svg = getCanvas(width, height, margin);
    
    var x0 = d3.scale.ordinal().rangeRoundBands([0, width], .1);
    var x1 = d3.scale.ordinal();  
    var yL = d3.scale.linear().range([height, 0]);
    var yR = d3.scale.linear().range([height, 0]);

    var color = d3.scale.ordinal().range(["#98abc5", "#6b486b"]);
    var countValues = ['cnt', 'avg_diff'];
    var valueLine = d3.svg.line()
        .x(function(d) { return x0(d.created_at); })
        .y(function(d) { return yR(d.avg_diff); });

    data.forEach(function(d) {
      d.values = countValues.map(function(name) { return {'k': name, 'v': +d[name]}; });
    });
    
    x0.domain(data.map(function(d) { return d.created_at; }));
    x1.domain(countValues).rangeRoundBands([0, x0.rangeBand()]);
    yL.domain([0, d3.max(data, function(d) { return d3.max(d.values, function(d) { return d.v; }); })]);
    yR.domain([0, d3.max(data, function(d) { return d.avg_diff; })]);
    
    var xAxis = d3.svg.axis()
      .scale(x0)
      .orient("bottom");
    var yAxisLeft = d3.svg.axis()
      .scale(yL)
      .orient("left")
      .tickFormat(d3.format(".2s"));
    var yAxisRight = d3.svg.axis()
      .scale(yR)
      .orient("right")
      .tickFormat(d3.format(".2s"));
      
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis)
        .selectAll("text")
          .style("text-anchor", "end")
          .attr("dx", "-.8em")
          .attr("dy", ".15em")
          .attr("transform", "rotate(-65)" );
        
    svg.append("g")
        .attr("class", "y axis left-axis")
        .call(yAxisLeft)
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Number of PR");
        
    svg.append("g")
        .attr("class", "y axis right-axis")
        .attr("transform", "translate(" + width + " ,0)")
        .call(yAxisRight)
      .append("text")
        .attr("transform", "rotate(-270)")
        .attr("y", -40)
        .attr("dy", ".71em")
        .style("text-anchor", "start")
        .text("Avg. merge latency [min]");
        
    var bars = svg.selectAll(".lang")
        .data(data)
      .enter().append("g")
        .attr("class", "g")
        .attr("transform", function(d) { return "translate(" + x0(d.created_at) + ",0)"; });

    bars.append("rect")
      .attr("class", "bar1")
      .attr("x", function(d) { return x1("cnt"); })
      .attr("width", x1.rangeBand())
      .attr("y", function(d) { return yL(d.cnt); })
      .attr("height", function(d,i,j) { return height - yL(d.cnt); })
      .style("fill", function(d) { return color("cnt"); }); 
    
    bars.append("rect")
      .attr("class", "bar2")
      .attr("x", function(d) { return x1("avg_diff"); })
      .attr("width", x1.rangeBand())
      .attr("y", function(d) { return yR(d.avg_diff); })
      .attr("height", function(d,i,j) { return height - yR(d.avg_diff); })
      .style("fill", function(d) { return color("avg_diff"); });
    
    var legend = svg.selectAll(".legend")
        .data(['cnt', 'avg_diff'])
      .enter().append("g")
        .attr("class", "legend")
        .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

    legend.append("rect")
      .attr("x", width - 28)
      .attr("width", 18)
      .attr("height", 18)
      .style("fill", color);

    legend.append("text")
      .attr("x", width - 34)
      .attr("y", 9)
      .attr("dy", ".35em")
      .style("text-anchor", "end")
      .text(function(d) { return d; });

  };

  showPrLatencies = function(e) {
    e.preventDefault();
    startLoading();
    SQLQuery.execute(QUERY).success(function(res){
      var data = res.toObjectArray();
      draw(data);
      finishLoading();
      showSqlResult(res['rowCount'], res['duration']);
    }).error(function(e){
      finishLoading(e.error);
    }).always(function(res){
    });
  };

})();
