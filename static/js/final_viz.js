$(document).ready(function() {
    $("#viz").width('100%');
    $("#viz").height(600);
    d3.json('static/data/optimal_lineup.json', function(error, data) {
        
        console.log(data);
        
        //data.forEach(function(d) {

        sorteddata = []

        for (var i = 0; i < data.length; i++) {
            if (data[i].position === 'PG') {
                sorteddata.push(data[i]);
            }
        }

        for (var i = 0; i < data.length; i++) {
            if (data[i].position === 'SG') {
                sorteddata.push(data[i]);
            }
        }

        for (var i = 0; i < data.length; i++) {
            if (data[i].position === 'SF') {
                sorteddata.push(data[i]);
            }
        }

        for (var i = 0; i < data.length; i++) {
            if (data[i].position === 'C') {
                sorteddata.push(data[i]);
            }
        }
        
        sorteddata.forEach(function(d) {

        //console.log(data);
            
            var table = document.getElementById("chart").getElementsByTagName('tbody')[0];
            
            var row = table.insertRow(table.rows.length);
            row.id = d.name;
            //row.onmouseover = function() {
            //    linegraph(row);
            //}
            /*row.onmouseleave = function() {
                $("#viz").empty();
                 var margin = {top: 20, right: 20, bottom: 30, left: 30},
    width = $("#viz").width() - margin.left - margin.right,
    height = $("#viz").height() - margin.top - margin.bottom;

    var x0 = d3.scale.ordinal()
        .rangeRoundBands([0, width], .1);

    var x1 = d3.scale.ordinal();

    var y = d3.scale.linear()
        .range([height, 0]);

    var color = d3.scale.ordinal()
        .range(["#98abc5"]);

    var xAxis = d3.svg.axis()
        .scale(x0)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

   d3.json('static/data/optimal_lineup.json', function(d) {

    //    d.projection = +d.projection
//
 //   },function(error, data) {

        console.log(data);

        var svg = d3.select("#viz").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
          .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        var names = ["projection"];
          data.forEach(function(d) {
            d.stats = names.map(function(name) { return {name: name, value: +d[name]}; });
          });

          x0.domain(data.map(function(d) { return d.name; }));
          x1.domain(names).rangeRoundBands([0, x0.rangeBand()]);
          y.domain([0, d3.max(data, function(d) { return d.projection; })]);

          svg.append("g")
              .attr("class", "x axis")
              .attr("transform", "translate(0," + height + ")")
              .call(xAxis);

          svg.append("g")
              .attr("class", "y axis")
              .call(yAxis);
            /*.append("text")
              .attr("transform", "rotate(-90)")
              .attr("y", 6)
              .attr("dy", ".71em")
              .style("text-anchor", "end")
              .text("Scores, Points, Assists");*/

              /*var player = svg.selectAll(".player")
                  .data(data)
                .enter().append("g")
                  .attr("class", "projection")
                  .attr("transform", function(d) { return "translate(" + x0(d.name) + ",0)"; });

              player.selectAll("rect")
                  .data(function(d) { return d.stats; })
                .enter().append("rect")
                  .attr("width", x1.rangeBand())
                  .attr("x", function(d) { return x1(d.name); })
                  .attr("y", function(d) { return y(d.value); })
                  .attr("height", function(d) { return height - y(d.value); })
                  .style("fill", function(d) { return color(d.name); });

              var legend = svg.selectAll(".legend")
                  .data(names.slice().reverse())
                .enter().append("g")
                  .attr("class", "legend")
                  .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

              legend.append("rect")
                  .attr("x", width - 18)
                  .attr("width", 18)
                  .attr("height", 18)
                  .style("fill", color);

              legend.append("text")
                  .attr("x", width - 24)
                  .attr("y", 9)
                  .attr("dy", ".35em")
                  .style("text-anchor", "end")
                  .text(function(d) { return d; });
        });
            };*/
            
            var cell1 = row.insertCell(0);
            var cell2 = row.insertCell(1);
            var cell3 = row.insertCell(2);
            var cell4 = row.insertCell(3);
            var cell5 = row.insertCell(4);

            var game = "<strong>" + d.player_team + "</strong>";

            if (d.playing_at_home === true) {
                game += " vs. " + d.opponent_team;
            } else {
                game += " @ " + d.opponent_team;
            }

            console.log(game);

            cell1.innerHTML = d.position;
            cell2.id = "name";
            cell2.innerHTML = d.name;
            cell3.innerHTML = game;//d.player_team;
            cell4.innerHTML = d.projection.toString().substring(0, 5);
            cell5.innerHTML = d.salary;
            
        });

        var margin = {top: 20, right: 20, bottom: 30, left: 30},
    width = $("#viz").width() - margin.left - margin.right,
    height = $("#viz").height() - margin.top - margin.bottom;

    var x0 = d3.scale.ordinal()
        .rangeRoundBands([0, width], .1);

    var x1 = d3.scale.ordinal();

    var y = d3.scale.linear()
        .range([height, 0]);

    var color = d3.scale.ordinal()
        .range(["#98abc5"]);

    var xAxis = d3.svg.axis()
        .scale(x0)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

   // d3.json('static/data/optimal_lineup.json', function(d) {

    //    d.projection = +d.projection
//
 //   },function(error, data) {

        console.log(data);

        var svg = d3.select("#viz").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
          .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        var names = ["projection"];
          data.forEach(function(d) {
            d.stats = names.map(function(name) { return {name: name, value: +d[name]}; });
          });

          x0.domain(data.map(function(d) { return d.name; }));
          x1.domain(names).rangeRoundBands([0, x0.rangeBand()]);
          y.domain([0, d3.max(data, function(d) { return d.projection; })]);

          svg.append("g")
              .attr("class", "x axis")
              .attr("transform", "translate(0," + height + ")")
              .call(xAxis);

          svg.append("g")
              .attr("class", "y axis")
              .call(yAxis);
            /*.append("text")
              .attr("transform", "rotate(-90)")
              .attr("y", 6)
              .attr("dy", ".71em")
              .style("text-anchor", "end")
              .text("Scores, Points, Assists");*/

              var player = svg.selectAll(".player")
                  .data(data)
                .enter().append("g")
                  .attr("class", "projection")
                  .attr("transform", function(d) { return "translate(" + x0(d.name) + ",0)"; });

              player.selectAll("rect")
                  .data(function(d) { return d.stats; })
                .enter().append("rect")
                  .attr("width", x1.rangeBand())
                  .attr("x", function(d) { return x1(d.name); })
                  .attr("y", function(d) { return y(d.value); })
                  .attr("height", function(d) { return height - y(d.value); })
                  .style("fill", function(d) { return color(d.name); });

              var legend = svg.selectAll(".legend")
                  .data(names.slice().reverse())
                .enter().append("g")
                  .attr("class", "legend")
                  .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

              legend.append("rect")
                  .attr("x", width - 18)
                  .attr("width", 18)
                  .attr("height", 18)
                  .style("fill", color);

              legend.append("text")
                  .attr("x", width - 24)
                  .attr("y", 9)
                  .attr("dy", ".35em")
                  .style("text-anchor", "end")
                  .text(function(d) { return d; });
        //});
        
    });

});


function linegraph(row) {

    d3.csv('static/data/optimal_lineup.json', function(error, data) {
        var lineData = data.filter(function(d) {
            return d.name === row.id;
        });

        console.log(lineData);
        $("#viz").empty();
        var margin = {top: 10, right: 20, bottom: 20, left: 40},
            width = $("#viz").width() - margin.left - margin.right,
            height = $("#viz").height() - margin.top - margin.bottom;

        var chart = d3.select("#viz")
            .append("svg") 
            .attr("width", width + (2 * margin.left) + margin.right)    //set width
            .attr("height", height + margin.top + margin.bottom)  //set height
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


        var x = d3.time.scale()
            .range([0, width]);

        var y = d3.scale.linear()
            .range([height, 0]);



        x.domain(d3.extent(lineData, function(d) { return d["Dates"]; }));
        y.domain(d3.extent(lineData, function(d) { return d["Score"]; }));

        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom");

        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left");


        chart.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + height + ")")
          .call(xAxis);

        chart.append("g")
          .attr("class", "y axis")
          .call(yAxis)
          .append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", 6)
          .attr("dy", ".71em")
          .style("text-anchor", "end")
          .text("FanDuel Scores");

        var line = d3.svg.line()
            .x(function(d) { return x(d["Dates"]); })
            .y(function(d) { return y(d["Score"]); });

        chart.append("path")
            .datum(lineData)
            .attr("class", "line")
            .attr("d", line);


        $("svg").on('click', function() {

            $("#viz").empty();
            //addTable(data);
            barChart(data);
            var tbody = document.getElementById("tbody");
            var rows = tbody.getElementsByTagName("tr");
            for(i = 0; i < rows.length; i++) {
                var currentRow = rows[i];
                $('#' + currentRow.id).on('mouseover', function() {
                    linegraph(data, this);
                });
                $('#' + currentRow.id).on('mouseleave', function() {
                    linegraph(results, this);
                });
            };  
        });
});
}