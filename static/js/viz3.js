$(document).ready(function() {
	var formatDate = d3.time.format("%Y-%m-%d");
	var q = d3_queue.queue(1);
	q.defer(function(callback) {
      d3.csv("static/data/projection_visuals.csv", function(d) {
      	if (d["Dates"] === "current") {
      		var dater = new Date();
      		d["Dates"] =  dater.getFullYear().toString().concat("-").concat((dater.getMonth() + 1).toString()).concat("-").concat(dater.getDate().toString());
      	}
  		d["Dates"] = formatDate.parse(d["Dates"]);
  		d["Score"] = +d["Score"];
  		d["Assists"] = +d["Assists"];
  		d["Blocks"] = +d["Blocks"];
  		d["Points"] = +d["Points"];
  		d["Rebounds"] = +d["Rebounds"];
  		d["Steals"] = +d["Steals"];
  		d["Turnovers"] = +d["Turnovers"];
  		return d;		
      },
      function(data) { 
      	addTable(data);
      	callback(null, data) });
    	});
		q.await(function(err, results) {
			var tbody = document.getElementById("tbody");
		    var rows = tbody.getElementsByTagName("tr");
		    for(i = 0; i < rows.length; i++) {
		        var currentRow = rows[i];
		        $('#' + currentRow.id).on('click', function() {
		        	linegraph(results, this);
		        });
		    };
		})

});



function linegraph(data, row) {
	var lineData = data.filter(function(d) {
		return d.Player === row.id;
	});
	$("#viz").empty();
	$("#viz").width(750);
	$("#viz").height(600);
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
		$("#viz").width(0);
		$("#viz").height(0);
		//addTable(data);
		var tbody = document.getElementById("tbody");
	    var rows = tbody.getElementsByTagName("tr");
	    for(i = 0; i < rows.length; i++) {
	        var currentRow = rows[i];
	        $('#' + currentRow.id).on('click', function() {
	        	linegraph(data, this);
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
	cell0.innerHTML = "Player Name";
    cell1.innerHTML = "Projected Score";
    cell2.innerHTML = "Projected Points";
    cell3.innerHTML = "Projected Assists";
    cell4.innerHTML = "Projected Steals";
    cell5.innerHTML = "Projected Blocks";
    cell6.innerHTML = "Projected Turnovers";
    cell7.innerHTML = "Projected Rebounds";

    var body = document.createElement('tbody');
    body.setAttribute("id", "tbody");
    	count = 9;
    	var name = data[0].Player;
    	for (var i = 0; i < data.length; i++) {
    		if (count <= 0) {
    			break;
    		}
	    	if (data[i + 1].Player !== name) {
	    		count--;

	    		name = data[i + 1].Player;

		    	var row = body.insertRow(body.rows.length);
		    	row.id = data[i].Player;
		    	
			    cell0 = row.insertCell(0);
			    cell1 = row.insertCell(1);
			    cell2 = row.insertCell(2);
			    cell3 = row.insertCell(3);
			    cell4 = row.insertCell(4);
			    cell5 = row.insertCell(5);
			    cell6 = row.insertCell(6);
			    cell7 = row.insertCell(7);

			    cell0.innerHTML = data[i].Player.substring(4, data[i].Player.length).replace(/-/g, " ");
			    cell1.innerHTML = data[i].Score;
			    cell2.innerHTML = data[i].Points;
			    cell3.innerHTML = data[i].Assists;
			    cell4.innerHTML = data[i].Steals;
			    cell5.innerHTML = data[i].Blocks;
			    cell6.innerHTML = data[i].Turnovers;
			    cell7.innerHTML = data[i].Rebounds;

			}
		}
	table.appendChild(body);
}