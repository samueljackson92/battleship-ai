function heatmap(container, data) {
    var gridSize = 50,
        h = gridSize,
        w = gridSize,
        rectPadding = 60;

    var colorLow = 'green', colorMed = 'yellow', colorHigh = 'red';

    var margin = {top: 20, right: 80, bottom: 30, left: 50},
        width = 640 - margin.left - margin.right,
        height = 380 - margin.top - margin.bottom;

    var colorScale = d3.scale.linear()
         .domain([0, 0.02])
         .range([colorLow, colorMed, colorHigh]);

    var svg = d3.select(container).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var heatMap = svg.selectAll(".heatmap")
        .data(data, function(d) { return d.col + ':' + d.row; })
      .enter().append("svg:rect")
        .attr("x", function(d) { return d.row * w; })
        .attr("y", function(d) { return d.col * h; })
        .attr("width", function(d) { return w; })
        .attr("height", function(d) { return h; })
        .style("fill", function(d) { return colorScale(d.score); });
}
