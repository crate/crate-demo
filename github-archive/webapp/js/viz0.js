;(function(){
  /**
   * viz0 - Pull Request Languages
   *
   **/

  var QUERY = $( "#query" ).text();

  // canvas width/height/margin
  var margin = {top: 10, right: 40, bottom: 30, left: 40},
      width = 960 - margin.left - margin.right,
      height = 500 - margin.top - margin.bottom;


  var draw = function(data) {
    var svg = getCanvas(width, height, margin);

    var x0 = d3.scale.ordinal().rangeRoundBands([0, width], .1);
    var x1 = d3.scale.ordinal();
    var yL = d3.scale.linear().range([height, 0]);
    var yR = d3.scale.linear().range([height, 0]);

    var color = d3.scale.ordinal().range(["#98abc5", "#6b486b", "#ff8c00"]);
    var countValues = ['num_pull_requests', 'num_repos'];
    var valueLine = d3.svg.line()
        .x(function(d) { return x0(d.language); })
        .y(function(d) { return yR(d.prs_per_repo); });

    data.forEach(function(d) {
      d.values = countValues.map(function(name) { return {'k': name, 'v': +d[name]}; });
    });

    x0.domain(data.map(function(d) { return d.language; }));
    x1.domain(countValues).rangeRoundBands([0, x0.rangeBand()]);
    yL.domain([0, d3.max(data, function(d) { return d3.max(d.values, function(d) { return d.v; }); })]);
    yR.domain([0, d3.max(data, function(d) { return d.prs_per_repo; })]);

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
        .call(xAxis);
    svg.append("g")
        .attr("class", "y axis left-axis")
        .call(yAxisLeft);
    svg.append("g")
        .attr("class", "y axis right-axis")
        .attr("transform", "translate(" + width + " ,0)")
        .call(yAxisRight);

    var lang = svg.selectAll(".lang")
        .data(data)
      .enter().append("g")
        .attr("class", "g")
        .attr("transform", function(d) { return "translate(" + x0(d.language) + ",0)"; });

    lang.selectAll("rect")
        .data(function(d) { return d.values; })
      .enter().append("rect")
        .attr("width", x1.rangeBand())
        .attr("x", function(d) { return x1(d.k); })
        .attr("y", function(d) { return yL(d.v); })
        .attr("height", function(d) { return height - yL(d.v); })
        .style("fill", function(d) { return color(d.k); });

    svg.append('path')
        .style('stroke', color('prs_per_repo'))
        .style('fill', 'transparent')
        .attr('d', valueLine(data));

    var legend = svg.selectAll(".legend")
        .data(['num_repos', 'num_pull_requests', 'prs_per_repo'])
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

  showPrLanguages = function(e) {
    e.preventDefault();
    startLoading();
    SQLQuery.execute(QUERY).success(function(res){
      var data = res.toObjectArray();
      data.map(function(o, idx){
        o['prs_per_repo'] = o['num_pull_requests'] / o['num_repos'];
        return o;
      });
      draw(data);
      finishLoading();
    }).error(function(e){
      finishLoading(e.error);
    }).always(function(res){
    });
  };

})();
