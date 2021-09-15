
var buttonInc = document.getElementById("button1");
var buttonDec = document.getElementById("button2");
var counter = document.getElementById("counter1");
var smiley = document.getElementById("smiley1");

var buttonChangeAuthor = document.getElementById("changeAuthor");
var authorElems = document.getElementsByClassName("author");

var count = 0;

buttonInc.onclick = function () {
    counter.innerHTML = ++count;
    getSmiley();
}

buttonDec.onclick = function () {
    counter.innerHTML = --count;
    getSmiley();
}

buttonChangeAuthor.onclick = function () {
    console.log("clicked");
    for (let authorElem of authorElems)
    {
        if (authorElem.innerHTML == "Dimitri VINET")
        {
            authorElem.innerHTML = "NOT Dimitri VINET";
        }
        else
        {
            authorElem.innerHTML = "Dimitri VINET"
        }
    }
}

function getSmiley()
{
    if (count == 0)
    {
        smiley.innerHTML = "😐";
    }
    else
    {
        smiley.innerHTML = count <= 0 ?  "🙁" : "😊";
    }
}

console.log("hello from js!");
