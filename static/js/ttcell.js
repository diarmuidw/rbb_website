// March 2012, Bahri Okuroglu
// Quick and dirty module to draw cells on Google maps

var bounds = null;

var d2r = Math.PI/180 ;                // degrees to radians
var r2d = 180/Math.PI ;                // radians to degrees

function infoWindow(map, lac, cid, msg) 
{
	var l = "L" + lac;
	var c = "C" + cid;
	
	if (l in cells) {
		if (c in cells[l]) {
			var cell = cells[l][c];
			cell.infoWindow(map, msg);
		}
	}
}

function drawCell(map, lac, cid)
{
	var l = "L" + lac;
	var c = "C" + cid;
	
	if (l in cells) {
		if (c in cells[l]) {
			var cell = cells[l][c];
			cell.log();
			cell.draw(map);
		}
	}
}

function drawCellWithTA(map, lat, lon, st, end, distance)
{
    //alert(lon);
    //alert(lat);
    //alert(st);
    //alert(end);
    //alert(distance);
    var cell = new ttCell(1, 1, lat, lon, st, end, distance);
    cell.log();
    cell.drawWithTA(map, 1);

}

function drawCellWithColor(map, lac, cid, color)
{
	var l = "L" + lac;
	var c = "C" + cid;
	
	if (l in cells) {
		if (c in cells[l]) {
			var cell = cells[l][c];
			cell.log();
			cell._draw(map, color);
		}
	}
}

function mark(map, lac, cid)
{
	var l = "L" + lac;
	var c = "C" + cid;
	
	if (l in cells) 
		if (c in cells[l]) 
			cells[l][c].mark(map);
}

function markAll(map)
{
	for (l in cells)
		for (c in cells[l]) {
			cell = cells[l][c];
			if (cell.lat < 41.025)
				continue;
			if (cell.lat > 41.0458)
				continue;
			if (cell.lon < 28.9649)
				continue;
			if (cell.lon > 28.9914)
				continue;
				
			// continue;
			cell.mark(map);
		}
}

function ttCell(lac, cid, lat, lon, startAngle, stopAngle, radius)
{
	this.lac = lac;
	this.cid = cid;
	this.lat = lat;
	this.lon = lon;
	this.startAngle = startAngle;
	this.stopAngle = stopAngle;
	this.radius = radius;
	
	this.width = (stopAngle + 360 - startAngle) % 360;
    //var myLatlng = new google.maps.LatLng(markerData['lat'], markerData['long']);
	//this.center = new GLatLng(lat, lon);
	
    this.center = new google.maps.LatLng(lat, lon);
	this.rLat = (this.radius/3963) * r2d ;      //  using 3963 as earth's radius
	this.rLng = this.rLat/Math.cos(this.lat * d2r);

	this.log = function () {
		console.log("LAC: " + this.lac + ", CID: " + this.cid + ", lat: " + this.lat + ", lon: " + this.lon + ", start: " + this.startAngle + ", stop: " + this.stopAngle + ", radius: " + this.radius + ", width: " + this.width);
	}
	
	this.getPoint = function (radius, angle) {
		var theta = d2r * angle;
  
		var rLat = (radius/3963) * r2d ;      //  using 3963 as earth's radius
		var rLng = rLat/Math.cos(this.lat * d2r);

		var x = this.lon + (rLng * Math.cos(theta));
		var y = this.lat + (rLat * Math.sin(theta));
		
		
        return new google.maps.LatLng(y, x);
	}
	
	this.calculateMidpoint = function () {
		var angle = (this.startAngle + this.width / 2);
		
		this.midpoint = this.getPoint(this.radius/2, angle);
	}

	this.calculateMidpoint();
	
	this.add = function (points, angle) {
		var theta = d2r * angle;
  
		x = this.lon + (this.rLng * Math.cos(theta));
		y = this.lat + (this.rLat * Math.sin(theta));
		
		//var point = new GLatLng(y, x);
        var point = new google.maps.LatLng(y, x);
		bounds.extend(point);
		points.push(point);
	}
	
	this._draw = function (map, color, ta) {
		var points = [] ;

		if (bounds == null) 
        {
			
            bounds = new google.maps.LatLngBounds(this.center);
        }
		points.push(this.center);
        //console.log(points);
		var steps = 72;
		
		for (i=0; i<this.width; i+=(360/steps)) 
			this.add(points, (this.startAngle + i) % 360);
		this.add(points, this.stopAngle);

		//map.setCenter(bounds.getCenter(), map.getBoundsZoomLevel(bounds));


        
  bermudaTriangle = new google.maps.Polygon({
    paths: points,
    strokeColor: "#FF0000",
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: "#FF0000",
    fillOpacity: 0.35
  })     
bermudaTriangle.setMap(map);   
        
		//alert('after poly setmap');

	}
	
	this.draw = function (map) {
	    this._draw(map, "#ff0000", -1);
	}
	
	this.drawWithTA = function (map, ta) {
	    this._draw(map, "#ff0000", ta);
        ////alert('drawwith');
	}
	
	this.infoWindow = function (map, msg) {
		map.openInfoWindowHtml(this.midpoint, "<font face='Verdana'>" + msg + '</font>');
	}
}


var cells = {};
