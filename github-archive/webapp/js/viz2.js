;(function(){
  /**
   * viz1 - Pull Request Latencies
   *
   **/
   
  
  // canvas width/height/margin
  var margin = {top: 10, right: 40, bottom: 60, left: 40},
      width = 960 - margin.left - margin.right,
      height = 500 - margin.top - margin.bottom;

  var draw = function(data) {
    var svg = getCanvas(width, height, margin);
    
    var x0 = d3.scale.ordinal().rangeRoundBands([0, width], .1);
    var x1 = d3.scale.ordinal();
    var yL = d3.scale.linear().range([height, 0]);

    var color = d3.scale.ordinal().range(["#98abc5", "#6b486b"]);
    var countValues = ['cnt_neg', 'cnt_pos'];
    var valueLine = d3.svg.line()
        .x(function(d) { return x0(d.date); });

    data.forEach(function(d) {
      d.values = countValues.map(function(name) { return {'k': name, 'v': +d[name]}; });
    });
    
    x0.domain(data.map(function(d) { return d.date; }));
    x1.domain(countValues).rangeRoundBands([0, x0.rangeBand()]);
    yL.domain([0, d3.max(data, function(d) { return d3.max(d.values, function(d) { return d.v; }); })]);
  
    // Tooltip
    var tip = d3.tip()
      .attr('class', 'd3-tip')
      .offset([-10, 0])
      .html(function(d) {
        return "Positive: <span style='color:green'>" + d.cnt_pos + "</span><br />" + 
               "Negative: <span style='color:red'>" + d.cnt_neg + "</span>";
    });
  
    var xAxis = d3.svg.axis()
      .scale(x0)
      .orient("bottom");
    var yAxisLeft = d3.svg.axis()
      .scale(yL)
      .orient("left")
      .tickFormat(d3.format(".2s"));
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis)
        .selectAll("text")
          .style("text-anchor", "end")
          .attr("dx", "-.6em")
          .attr("dy", ".10em")
          .attr("transform", "rotate(-65)" );

    svg.append("g")
        .attr("class", "y axis left-axis")
        .call(yAxisLeft)
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", -40)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Number of commits");
  
    var bars = svg.selectAll(".lang")
        .data(data)
      .enter().append("g")
      .attr("class", "g")
      .attr("transform", function(d) { return "translate(" + x0(d.date) + ",0)"; });

    bars.append("rect")
      .attr("class", "bar1")
      .attr("x", function(d) { return x1("cnt_pos"); })
      .attr("width", x1.rangeBand())
      .attr("y", function(d) { return yL(d.cnt_pos); })
      .attr("height", function(d,i,j) { return height - yL(d.cnt_pos); })
      .style("fill", function(d) { return color("cnt_pos"); })
      .on('mouseover', tip.show)
      .on('mouseout', tip.hide); 
        
    bars.append("rect")
      .attr("class", "bar2")
      .attr("x", function(d) { return x1("cnt_neg"); })
      .attr("width", x1.rangeBand())
      .attr("y", function(d) { return yL(d.cnt_neg); })
      .attr("height", function(d,i,j) { return height - yL(d.cnt_neg); })
      .style("fill", function(d) { return color("cnt_neg"); })
      .on('mouseover', tip.show)
      .on('mouseout', tip.hide);
            
    var legend = svg.selectAll(".legend")
        .data(['cnt_pos', 'cnt_neg'])
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

    svg.call(tip);
  };

  showCommitSentiments = function(e) {
    e.preventDefault();
    var QUERY1 = $( "#query1" ).text();
    var QUERY2 = $( "#query2" ).text();
  
    startLoading();
    SQLQuery.execute(QUERY1).success(function(res1){
      SQLQuery.execute(QUERY2).success(function(res2) {
        // Concat values of two result-set
        res1['cols'][2] = "cnt_neg";
        for (var i=0; i<res1['rows'].length; i++) {
          res1['rows'][i] = res1['rows'][i].concat(res2['rows'][i][1]);
        }
        
        // Use concat result-set
        var data = res1.toObjectArray();
        draw(data);
        finishLoading();
        showSqlResult(res1['rowCount'] + res2['rowCount'], res1['duration'] + res2['duration']);
      }).error(function(e) {
        finishLoading(e.error);
      });
      
    }).error(function(e){
      finishLoading(e.error);
    }).always(function(res){
    });
  };

})();
