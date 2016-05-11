d3.csv("static/data/lineup2.csv", function(data) {
    
    data.forEach(function(d) {
        
        var table = document.getElementById("viz").getElementsByTagName('tbody')[0];
        
        var row = table.insertRow(table.rows.length);
        
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        var cell3 = row.insertCell(2);
        var cell4 = row.insertCell(3);
        var cell5 = row.insertCell(4);

        cell1.innerHTML = d.Position;
        cell2.id = "name";
        cell2.innerHTML = d.Name;
        cell3.id = "team";
        cell3.innerHTML = d.Team;
        cell4.innerHTML = d['FanDuel Points'];
        cell5.innerHTML = d.Salary;
        
    })
    
})
