
function httpGet(dst){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", dst, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

function httpPost(dst,pData){
    let xhr = new XMLHttpRequest();
    xhr.open("POST", dst, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(
        pData));
}

//this is called when a branch status button is pressed
function setBranchStatus(bNum) {
    let bData
    b = document.getElementById("branch" + bNum + "-status")
    console.log(b.textContent)
    if(b.textContent == "shedable"){
        b.textContent = "critical"
        bData = {branch: bNum, status :1}
    } else {
        b.textContent = "shedable"
        bData = {branch: bNum, status:0}
    }

    httpPost("http://localhost:5000/input",bData)
}

function updateScreen(){
    updateSystem()
    updateSite()
}

function updateSystem(){
    sData = JSON.parse(httpGet("http://localhost:5000/api?data=system"))
    console.log(sData)
    mC.innerHTML = "Modules: " + sData['system']['modules']
    aV.innerHTML = "Array voltage: : " + sData['pv']['voltage']
    aC.innerHTML = "Array current: : " + sData['pv']['current']
    aP.innerHTML = "Array power: : " + sData['pv']['current']
    lV.innerHTML = "Total load voltage: " + sData['load']['voltage']
    lC.innerHTML = "Total load current: " + sData['load']['current']
    lP.innerHTML = "Total load power: " + sData['load']['power']

    if(sData['system']['branchState'][1] == 1){
        bs1.innerHTML = "Branch 1: on"
        b1.style.backgroundColor = "green"
    } else {
        bs1.innerHTML = "Branch 1: off"
        b1.style.backgroundColor = "red"
    }

    if(sData['system']['branchState'][2] == 1){
        bs2.innerHTML = "Branch 2: on"
        b2.style.backgroundColor = "green"
    } else {
        bs2.innerHTML = "Branch 2: off"
        b2.style.backgroundColor = "red"
    }

    if(sData['system']['branchState'][3] == 1){
        bs3.innerHTML = "Branch 3: on"
        b3.style.backgroundColor = "green"

    } else {
        bs3.innerHTML = "Branch 3: off"
        b3.style.backgroundColor = "red"
    }

}


function updateSite(){
    
}

//System Specs
mC = document.getElementById("moduleCount")
aV = document.getElementById("arrayVoltage")
aC = document.getElementById("arrayCurrent")
aP = document.getElementById("arrayPower")
lV = document.getElementById("loadVoltage")
lC = document.getElementById("loadCurrent")
lP = document.getElementById("loadPower")

b1 = document.getElementById("branch1")
b2 = document.getElementById("branch2")
b3 = document.getElementById("branch3")

//live branch state (on/off)
bs1 = document.getElementById("branch1-state")
bs2 = document.getElementById("branch2-state")
bs3 = document.getElementById("branch3-state")

//branch status buttons
b1Stat = document.getElementById("branch1-status")
b2Stat = document.getElementById("branch2-status")
b3Stat = document.getElementById("branch3-status")

//Site Specs
sLoc = document.getElementById("location")
todW = document.getElementById("todayWeather")
tomW = document.getElementById("tomorrowWeather")
aTomW = document.getElementById("dayAfterTomorrowWeather")
todS = document.getElementById("todaySun")
tomS = document.getElementById("tomorrowSun")
aTomS = document.getElementById("dayAfterTomorrowSun")
pTodS = document.getElementById("todaySunP")
pTomS = document.getElementById("tomorrowSunP")
pATomS = document.getElementById("dayAfterTomorrowSunP")

updateScreen()

setInterval(updateScreen, 5000); 


