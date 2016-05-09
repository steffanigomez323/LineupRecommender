
$(document).ready(function() {
	var formatDate = d3.time.format("%Y-%m-%d");
	gi
	$("#viz").height(600);
	var q = d3_queue.queue(1);
	q.defer(function(callback) {
      d3.csv("static/data/visualization.csv", function(d) {
      	console.log(d);
      	/*if (d["Dates"] === "current") {
      		var dater = new Date();
      		d["Dates"] =  dater.getFullYear().toString().concat("-").concat((dater.getMonth() + 1).toString()).concat("-").concat(dater.getDate().toString());
      	}
  		d["Dates"] = formatDate.parse(d["Dates"]);*/
  		//d["Score"] = +d["Score"];

  		d["Assists"] = +d["Assists"];
  		d["Blocks"] = +d["Blocks"];
  		d["Points"] = +d["Points"];
  		d["Rebounds"] = +d["Rebounds"];
  		d["Steals"] = +d["Steals"];
  		d["Turnovers"] = +d["Turnovers"];

  		var score = d['Points'] + (1.2 * d['Rebounds']) + (1.5 * d['Assists']) + (2 * d['Blocks']) + (2 * d['Steals']) + (-1 * d['Turnovers'])
  		d["Score"] = score;

  		console.log(d);
  		return d;		
      },
      function(data) { 
      	console.log(data);
      	addTable(data);
      	barChart(data);
      	callback(null, data) });
    	});
		q.await(function(err, results) {
			console.log(results);
			var tbody = document.getElementById("tbody");
		    var rows = tbody.getElementsByTagName("tr");
		    for(i = 0; i < rows.length; i++) {
		        var currentRow = rows[i];
		        //$('#' + currentRow.id).on('mouseover', function() {
		        //	linegraph(results, this);
		        //});
		        $('#' + currentRow.id).on('mouseleave', function() {
		        	$("#viz").empty();
		        	barChart(results);
		        });
		    };
		})

});

function camelCaseName(player) {
	var lowername = player.substring(4, player.length).replace(/-/g, " ");
	var namesplit = lowername.split(" ");
	var propername = "";
	for (var i = 0; i < namesplit.length; i++) {
		var first = namesplit[i].substring(0, 1);
		propername += first.toUpperCase();
		propername += namesplit[i].substring(1, namesplit[i].length).concat(" ");
	}
	return propername;
}

function barChart(data) {
	//var lineData = [];
	lineData = data;
	count = 9;
	var name = data[0].Player;
	/*for (var i = 0; i < data.length; i++) {
		if (count <= 0) {
			break;
		}
    	if (data[i + 1].Player !== name) {
    		count--;
    		name = data[i + 1].Player;
    		lineData.push(data[i]);
		}
	}*/
	var margin = {top: 20, right: 20, bottom: 30, left: 30},
    width = $("#viz").width() - margin.left - margin.right,
    height = $("#viz").height() - margin.top - margin.bottom;

	var x0 = d3.scale.ordinal()
	    .rangeRoundBands([0, width], .1);

	var x1 = d3.scale.ordinal();

	var y = d3.scale.linear()
	    .range([height, 0]);

	var color = d3.scale.ordinal()
	    .range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c"]);

	var xAxis = d3.svg.axis()
	    .scale(x0)
	    .orient("bottom");

	var yAxis = d3.svg.axis()
	    .scale(y)
	    .orient("left");

	var svg = d3.select("#viz").append("svg")
	    .attr("width", width + margin.left + margin.right)
	    .attr("height", height + margin.top + margin.bottom)
	  .append("g")
	    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	var names =  ["Score", "Points", "Assists", "Blocks", "Turnovers", "Rebounds"];
	  lineData.forEach(function(d) {
	    d.stats = names.map(function(name) { return {name: name, value: +d[name]}; });
	  });

	  x0.domain(lineData.map(function(d) { return d.Regression; }));//camelCaseName(d.Player); }));
	  x1.domain(names).rangeRoundBands([0, x0.rangeBand()]);
	  y.domain([0, d3.max(lineData, function(d) { return d.Score; })]);//return d.Score; })]);

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
	      .data(lineData)
	    .enter().append("g")
	      .attr("class", "state")
	      .attr("transform", function(d) { return "translate(" + x0(d.Regression) + ",0)"; });//x0(camelCaseName(d.Player)) + ",0)"; });

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
}

function linegraph(data, row) {
	var lineData = data.filter(function(d) {
		return d.Player === row.id;
	});
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
}

function addTable(data) {

    var viz = document.getElementById("lineup-table");
    var table = document.createElement('table');
    table.setAttribute("id", "table");
    table.className = "table table-hover table-striped";
	viz.appendChild(table);
	table = document.getElementById('table');
	table.border = "1px";

	var header = table.createTHead();
	var hrow = header.insertRow(0);     
	var cell0 = hrow.insertCell(0);
	var cell1 = hrow.insertCell(1);
	var cell2 = hrow.insertCell(2);
	var cell3 = hrow.insertCell(3);
	var cell4 = hrow.insertCell(4);
	var cell5 = hrow.insertCell(5);
	var cell6 = hrow.insertCell(6);
	var cell7 = hrow.insertCell(7);
	cell0.innerHTML = "Regression Name";
    cell1.innerHTML = "Projected Score";
    cell2.innerHTML = "Projected Points";
    cell3.innerHTML = "Projected Assists";
    cell4.innerHTML = "Projected Steals";
    cell5.innerHTML = "Projected Blocks";
    cell6.innerHTML = "Projected Turnovers";
    cell7.innerHTML = "Projected Rebounds";

    var body = document.createElement('tbody');
    body.setAttribute("id", "tbody");
    	//count = 9;
    	console.log(data);
    	var name = data[0].Regression;
    	for (var i = 0; i < data.length; i++) {
    		// if (count <= 0) {
    		// 	break;
    		// }
	    	//if (data[i + 1].Player !== name) {
	    		//count--;

	    		//name = data[i + 1].Player;

		    	var row = body.insertRow(body.rows.length);
		    	row.id = data[i].Regression.split(" ")[0];
		    	
			    cell0 = row.insertCell(0);
			    cell1 = row.insertCell(1);
			    cell2 = row.insertCell(2);
			    cell3 = row.insertCell(3);
			    cell4 = row.insertCell(4);
			    cell5 = row.insertCell(5);
			    cell6 = row.insertCell(6);
			    cell7 = row.insertCell(7);

			    var score = data[i].Points + (1.2 * data[i].Rebounds) + (1.5 * data[i].Assists) + (2 * data[i].Blocks) + (2 * data[i].Steals) + (-1 * data[i].Turnovers)
			    cell0.innerHTML = data[i].Regression;//camelCaseName(data[i].Regression);
			    cell1.innerHTML = truncateDecimals(score, 2);
			    cell2.innerHTML = truncateDecimals(data[i].Points, 2);
			    cell3.innerHTML = truncateDecimals(data[i].Assists, 2);
			    cell4.innerHTML = truncateDecimals(data[i].Steals, 2);
			    cell5.innerHTML = truncateDecimals(data[i].Blocks, 2);
			    cell6.innerHTML = truncateDecimals(data[i].Turnovers, 2);
			    cell7.innerHTML = truncateDecimals(data[i].Rebounds, 2);

			//}
		}
	table.appendChild(body);
}


// helper function from stackoverflow
truncateDecimals = function (number, digits) {
    var multiplier = Math.pow(10, digits),
        adjustedNum = number * multiplier,
        truncatedNum = Math[adjustedNum < 0 ? 'ceil' : 'floor'](adjustedNum);

    return truncatedNum / multiplier;
};