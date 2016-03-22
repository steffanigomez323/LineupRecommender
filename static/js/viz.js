d3.csv('static/data/lineup.csv', function(d) {
    console.log(d);

    var colors = ['#6d2d01', '#9c5812', '#ae7d33', '#c1a259', '#d8d478'];

    var c = 0;
    var pg = 0;
    var sg = 0;
    var sf = 0;
    var pf = 0;
    var colindex = 0;

  for (var i = 0; i < d.length; i++) {
    var color = "black";
    if (d[i].Position === "PG" && pg < 1) {
      pg = pg + 1;
      drawCircle(d[i].Position, d[i], colors[colindex]);
      colindex = colindex + 1;
    }
    else if (d[i].Position === "SG" && sg < 1) {
      sg = sg + 1;
      drawCircle(d[i].Position, d[i], colors[colindex]);
      colindex = colindex + 1;
    }
    else if (d[i].Position === "SF" && sf < 1) {
      sf = 1;
      color = colors[2];
      drawCircle(d[i].Position, d[i], colors[colindex]);
      colindex = colindex + 1;
    }
    else if (d[i].Position === "PF" && pf < 1) {
      pf = 1;
      color = colors[3];
      console.log(colindex);
      console.log(colors[colindex]);
      drawCircle(d[i].Position, d[i], colors[colindex]);
      colindex = colindex + 1;
    }
    else {
      if (c < 1) {
        c = 1;
        drawCircle(d[i].Position, d[i], colors[colindex]);
        colindex = colindex + 1;
      }
    }
    if (c ==1 && pg == 1 && sf == 1 && pf == 1 && sg == 1) {
      break;
    }
  }


  });

  function drawCircle(pos, d, color) {

    var tooltip = d3.tip().attr("class", "d3-tip")
    .offset([100, 85])
    .html("Name: " + d.Name + "<br>" + "Team: " + d.Team + "<br>" + "Position: " + d.Position + "<br>" + "Projection: " + d.Projection + "<br>" + "Salary: " + d.Salary + "<br>" + "Injury Status: " + d['Injury Status']
    );

  
var svg = d3.select("#" + pos)
  .append("svg")
  .attr("class", "sample")
  .attr("width", 50)
  .attr("height", 50).append("g");


  svg.call(tooltip);

  d3.select("#" + pos + " svg").append("text")
    .attr("dx", 17)
    .attr("dy", 30)
    .text(pos)
    .attr("fill", "white");


  svg.append("circle")
      .attr("r", 25)
      .attr("stroke", "black")
      .attr("fill", color)
      .attr("r", 25)
      .attr("cx", 25)
      .attr("cy", 25)

  .on("mouseover", tooltip.show)
  .on("mousemove", function(){
    return tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");})
  .on("mouseout", tooltip.hide); 


  };