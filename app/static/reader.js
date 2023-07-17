const panel = document.getElementById("page");
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