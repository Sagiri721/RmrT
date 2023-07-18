const panel = document.getElementById("page");
const text = document.getElementById("text");

const urlParams = new URLSearchParams(window.location.search);

const ratio = urlParams.get('ratio');
const start = urlParams.get('start');
const dist = urlParams.get('dist');

// Draw selection mask
if(ratio != null && start != null && dist != null){

    
}

let xx = 0, yy = 0;

panel.addEventListener("dragstart", (event) => {

    // When start dragging set up drag movement and store start x position

    xx = event.clientX;
    yy = event.clientY;

    event.dataTransfer.setDragImage(new Image(), 0, 0);
});

panel.addEventListener("dragend", (event) => {

    // When stop dragging store information and send it to the application

    const distance = [event.clientX - xx, event.clientY - yy].map(Math.abs);
    const start = [Math.min(event.clientX, xx), Math.min(event.clientY, yy)];

    const curSize = panel.clientWidth;
    const realImg = new Image();
    realImg.src = panel.src;

    realImg.onload = ()=>{

        const ratio = realImg.width / curSize;
        window.open("?ratio=".concat(ratio).concat("&start=").concat(start.join(".")).concat("&dist=").concat(distance.join(".")), "_self");
    }
});

function translateText(){

    const t = text.innerText;
    window.open("https://translate.google.com/?sl=ja&tl=en&text="+t+"&op=translate", '_blank');
}

function copyText(){

    const t = text.innerText;
    navigator.clipboard.writeText(t);
}

function getWordDetails(word){

    const wordData = cached_sentence.find(w => w.origin == word);
    //console.log(wordData);

    document.getElementById("word").innerText = wordData.origin;
    document.getElementById("kana").innerText = wordData.reading;

    document.getElementById("search").onclick = () => {window.open("https://www.weblio.jp/content/" + wordData.origin, "_blank")};

    let definitions = wordData.senses.map(d => `<p><b>${d.english_definitions.join(", ")}</b></p><p>${d.parts_of_speech} ${d.see_also=="" ? "" : (", " + d.see_also)} ${d.tags=="" ? "" : (", " + d.tags)}</p>`);
    let html = "<ol><li>" + definitions.join("</li><li>") + "</li></ol>";
    document.getElementById("meanings").innerHTML = html;
}

var cached_sentence = [];

// Ajax to get the words meaning
$(document).ready(function() {

    const container = $("#word-container");
    const containerElement = document.getElementById("word-container");

    if(text.innerText != "..."){
        
        $.ajax({
            type: "get",
            url: "/parser?func=0",
            data: {
                contents: text.innerText
            },
            contentType: "application/json",
            success: function (response) {
                
                //console.log(response);
                let word_list = response.words[0];
                word_list.forEach(word => {
                    
                    // Fetch word meaning
                    $.ajax({
                        type: "get",
                        url: "/parser?func=1",
                        data: {
                            word: word
                        },
                        contentType: "application/json",
                        success: function (response) {
                            
                            // Create word element
                            const data = response["meaning"];
                            //console.log(data);

                            if(data == undefined) return;

                            cached_sentence.push(data);

                            var newWord = $(`
                                <div class="word-card" onclick='getWordDetails("${data.origin}")'>
                                    <div class="container-seperated">
                                        <h2>${data.origin}</h2>
                                        <p>«${data.reading}»</p>
                                    </div>
                                    <p> <strong>${data.jlpt.join(", ")}</strong>${data.common ? " <span class='common'>Common word</span>" : ""}</p>
                                    <br/>
                                    <p>${data.grammar || "なし"}・ ${data.wtype || "なし"}・ ${data.details || "なし"}</p>
                                    <br>
                                    ${data.tags.length == 0 ? "" : '<p class="tags"><span>'+data.tags.join("</span><span>")+'</span></p>'}
                                </div>
                            `);
                            container.append(newWord);
                        }
                    });
                });
            }
        });
    }
});