//showBaymap.js
//Display Google Map of the Chesapeake Bay

//globals
var myMarkers = new Array();
var markerColors = new Array();
var map;
var showing = true;
var first = true;
var nOrP = false;
var allocLoads = new Object();
var nutrAllocLoads = new Object();
var redN = "../images/RedNFlag.png";
var greenN = "../images/GreenNFlag.png";
var yellowN = "../images/YellowNFlag.png";
var redP = "../images/RedPFlag.png";
var greenP = "../images/GreenPFlag.png";
var yellowP = "../images/YellowPFlag.png";
var nFlags = new Array(redN, yellowN, greenN);
var pFlags = new Array(redP, yellowP, greenP);

function initialize(points, messages, loads, basin){

    allocLoads["EN"] = 2.438;
    allocLoads["JN"] = 1.660;
    allocLoads["SN"] = 2.112;
    allocLoads["RN"] = 1.559;
    allocLoads["WN"] = 4.391;
    allocLoads["PN"] = 2.257;
    allocLoads["XN"] = 2.291;
    allocLoads["YN"] = 1.265;

    allocLoads["EP"] = 0.2632;
    allocLoads["JP"] = 0.1660;
    allocLoads["SP"] = 0.0750;
    allocLoads["RP"] = 0.2392;
    allocLoads["WP"] = 0.2080;
    allocLoads["PP"] = 0.1839;
    allocLoads["XP"] = 0.1708;
    allocLoads["YP"] = 0.1258;

//    allocLoads["ES"] = 2.438;
//    allocLoads["JS"] = 1.660;
//    allocLoads["SS"] = 2.112;
//    allocLoads["RS"] = 1.559
//    allocLoads["WS"] = 4.391
//    allocLoads["PS"] = 2.257;
//    allocLoads["XS"] = 2.291;
//    allocLoads["YS"] = 1.265;

//    var theNutr = nutrient;
//    var myLoads = loads;
    var cent = new google.maps.LatLng(points[0][0], points[0][1]);
//    var basinIn = basin;
    var myOptions = {
      zoom: 9, 
      center: cent,
      mapTypeId: google.maps.MapTypeId.HYBRID,
      scrollwheel:false
    };
    map = new google.maps.Map(document.getElementById("map_canvas"),
            myOptions);

    var whereStr = 'MAJ = \'' + basin + '\'';
    //Fusion Table Title: RiverSegsBasins
    var segs = new google.maps.FusionTablesLayer({
        query: {
            select: 'geometry',
            from: '1252197',
            where: whereStr
        },
        styles: [{
            polygonOptions:{
                fillColor: "FFA319",
                fillOpacity: 0.3
            }
        }]
    });
    segs.setMap(map);

    var myPoints = new Array();
    var myInfoWins = new Array();
    var myListeners = new Array();
    var basinnut = basin.substring(0, 1) + "N";
    var tmdl = allocLoads[basinnut];
    var maxLoadN = tmdl; 
    basinnut = basin.substring(0, 1) + "P";
    tmdl = allocLoads[basinnut];
    var maxLoadP = tmdl;

    for (var i = 0; i < points.length; i++){
        myPoints[i] = new google.maps.LatLng(points[i][0], points[i][1]);
        myMarkers[i]= new google.maps.Marker({position: myPoints[i], map: map});
        attachData(myMarkers[i], i, messages, loads[i], basin, maxLoadN, maxLoadP);
    };
    
    var latLngBnd = new google.maps.LatLngBounds();
    for (var i = 0; i < points.length; i++){
        latLngBnd.extend(myPoints[i]); 
    }
    
    map.fitBounds(latLngBnd);


    //Workaround for the fusion tables "Data may still be loading..." problem
    setTimeout(function(){
        $("img[src*='googleapis']").each(function(){
            $(this).attr("src", $(this).attr("src")+"&"+(new Date()).getTime());
        });
    },5000);
}

//function sleep(ms){
//    var dt = new Date();
//    dt.setTime(dt.getTime() + ms);
//    while (new Date().getTime() < dt.getTime());
//}

//function shiftMap(){
//    var oldCtr = map.getCenter();
//    var newLat = oldCtr.lat() + 1;
//    var newLng = oldCtr.lng() + 1;
//    var newCtr = new google.maps.LatLng(newLat, newLng);
////    alert(String(oldCtr.lat()) +" " + String(newLat));
//    map.panTo(newCtr);
//    sleep(2000);
////    alert("stop");
//    map.panTo(oldCtr);
//}

// Function to add the load data to the GMapMarker and set the flag icon
function attachData(marker, num, messages, thisLoad, theBasin, redLoadN, redLoadP){
//    var messagesIn = messages;
//    marker = myMarkers[num];
    var infowindow = new google.maps.InfoWindow({content: messages[num]});   
    google.maps.event.addListener(marker, 'click', function() {
        infowindow.open(map, marker);
    });
//    alert(String(thisLoad));
//    var temp1 = theBasin[0]+"N";
//    var temp2 = allocLoads[temp1]*1.1;
//    window.alert(temp2);
    var yellowLoadN = redLoadN * 0.9;
    var yellowLoadP = redLoadP * 0.9;
    var nFlagColor = 0;
    var pFlagColor = 0;
//    alert(String(maxLoad) + " " + String(yellowLoad));i

    //determine n flag color
    if (thisLoad[3] > redLoadN * 1.1){
        nFlagColor = 0;
    } else if (thisLoad[3] > yellowLoadN) { 
        nFlagColor = 1;
    } else {
        nFlagColor = 2;
    }

    //determine p flag color
    if (thisLoad[4] > redLoadP * 1.1){
        pFlagColor = 0;
    } else if (thisLoad[4] > yellowLoadP) { 
        pFlagColor = 1;
    } else {
        pFlagColor = 2;
    }
    markerColors.push([nFlagColor, pFlagColor]);
    marker.setIcon(nFlags[nFlagColor]);

}
//function to change between N and P flags on a marker
function changeNutrientFlag(i, n){
    if (nOrP){
        myMarkers[i].setIcon(nFlags[markerColors[i][0]]);
    } else {
        myMarkers[i].setIcon(pFlags[markerColors[i][1]]);
    }

}
 
// Function to toggle the display of a GMapMarker
function togMark(i){
    if (myMarkers[i].getVisible()){
         myMarkers[i].setVisible(false);
    } else {
        myMarkers[i].setVisible(true);
    }
}

// Failed workaround for the fusion table prob...
//function reloadMap(){
//    var map_contents = document.getElementById("map_canvas").innerHTML;
//    document.getElementById("map_canvas").innerHTML = map_contents;
//}

// Function to call togMark on all markers
function togAll(){
    if (showing){
        for (var i = 0; i < myMarkers.length; i++){
            myMarkers[i].setVisible(false);
        }
        showing = false; 
    } else {
        for (var i = 0; i < myMarkers.length; i++){
            myMarkers[i].setVisible(true);
        }
        showing = true;
    }
}

//function to call changeNutrientFlag on all markers
function changeAll(){
    for (var i = 0; i < myMarkers.length; i++){
        changeNutrientFlag(i);
    }
    nOrP = !nOrP;
}
