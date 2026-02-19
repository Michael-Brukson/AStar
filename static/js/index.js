const canvas = document.getElementById('drawingCanvas');
const ctx = canvas.getContext('2d', { willReadFrequently: true });
const drawingLabel = document.getElementById('drawingLabel');
const imagesContainer = document.getElementById('imagesContainer');
const submitMap = document.getElementById('submitMap');
const clearMap = document.getElementById('clearMap');
const radios = document.querySelectorAll('input[name="pencil"]');
let drawing = false;

var source = [];
var destination = [];

function isEmpty(arr) {return !(arr.length > 0)};

// R, G, B, alpha
const RED = [255, 0, 0, 255];
const BLUE = [0, 0, 255, 255];
const COLORS = {"source":"red", "draw":"black", "destination":"blue"};

submitMap.addEventListener('click', submitCanvas);
clearMap.addEventListener('click', clearCanvas);

canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('mousemove', drawLine);

canvas.addEventListener('touchstart', (e) => {
    startDrawing(e.touches[0]);
});
canvas.addEventListener('touchend', stopDrawing);
canvas.addEventListener('touchmove', (e) => {
    drawLine(e.touches[0]);
    e.preventDefault();
});

initCanvas();

function getCursorPosition(event) {
    const rect = canvas.getBoundingClientRect(); 
    const scaleX = canvas.width / rect.width; 
    const scaleY = canvas.height / rect.height; 

    return {
        x: (event.clientX - rect.left) * scaleX,
        y: (event.clientY - rect.top) * scaleY
    };
}

function startDrawing(event) {
    drawing = true;

    const radioVal = getCurrentRadioValue();
    const pos = getCursorPosition(event);

    // TODO: Make a little less ugly
    if (radioVal === "source"){
        if (!isEmpty(source)) drawDot(source[0], source[1], 'white', radius=6);
        source = [pos.x, pos.y]; 
        drawDot(pos.x, pos.y, COLORS[radioVal]);
        drawing = false;
    } else if (radioVal === "destination"){
        if (!isEmpty(destination)) drawDot(destination[0], destination[1], 'white', radius=6);
        destination = [pos.x, pos.y];
        drawDot(pos.x, pos.y, COLORS[radioVal]);
        drawing = false;
    }

    ctx.beginPath();
    ctx.moveTo(pos.x, pos.y);
}

function stopDrawing() {
    drawing = false;
    ctx.beginPath();
}

function drawDot(x, y, color, radius=5){
    ctx.beginPath();

    ctx.arc(x, y, radius, 0, Math.PI * 2);

    ctx.fillStyle = color;

    ctx.fill();

    ctx.closePath();
}

// TODO: Add erasing. (just drawing white)
function drawLine(event) {
    if (!drawing) return;
    const radioVal = getCurrentRadioValue();
    const pos = getCursorPosition(event);

    ctx.lineWidth = 10;
    ctx.lineCap = 'round';
    ctx.strokeStyle = COLORS[radioVal];

    ctx.lineTo(pos.x, pos.y);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(pos.x, pos.y);
}

function getCurrentRadioValue(){
    const radio = document.querySelector('input[name="pencil"]:checked')
    return radio.value;
}

async function sendImage(dataURL){
    const blob = dataURLToBlob(dataURL);
    const formData = new FormData();

    const time = new Date().toISOString();
    formData.append('upload', blob, `${time}.png`);

    const response = await fetch('/get_path', {
        method: 'POST',
        body: formData
    });

    if (!response.ok) {
        console.log('Upload failed');
        throw new Error('Upload failed');
    }

    const json = await response.json();

    return json;
}

// function to check if value at location in image matches value in parameter
function matches(coords, value){
    [x, y] = coords;
    const pixel = ctx.getImageData(x, y, 1, 1).data;
    return pixel.join('') === value.join('');
}

function isValidCanvas(){
    if (isEmpty(source) || isEmpty(destination)){
        alert('the source or destination does not exist!');
        return false;
    }
    if (!(matches(source, RED) && matches(destination, BLUE))){
        alert('the source or destination does not exist!');
        return false;
    }
    return true;
}

function drawPath(path){
    ctx.beginPath();
    ctx.lineWidth = 5;
    ctx.strokeStyle = 'green';

    ctx.moveTo(path[0][1], path[0][0]);

    for (let i = 1; i < path.length; i++) {
        ctx.lineTo(path[i][1], path[i][0]);
    }

    ctx.stroke();
}

// TODO: add separate canvas and drawing of path from source to destination
async function submitCanvas(event) {
    if(!isValidCanvas()) return;
    const dataURL = canvas.toDataURL('image/png');

    const img = document.createElement('img');
    img.src = dataURL;
    img.width = canvas.width / 5;
    img.height = canvas.height / 5;
    imagesContainer.appendChild(img);

    const path = await sendImage(dataURL);

    if (!isEmpty(path)){
        drawPath(path);
    }
    else {
        alert('destination is unreachable!');
    }
}

function clearCanvas(event) {
    source.length = 0;
    destination.length = 0;

    ctx.fillStyle = '#FFFFFF';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
};

// remove transparency from canvas
function initCanvas(){
    ctx.fillStyle = '#FFFFFF';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.save();
}

function dataURLToBlob(dataURL) {
    const parts = dataURL.split(',');
    const byteString = atob(parts[1]);
    const mimeString = parts[0].split(':')[1].split(';')[0];
    const ab = new ArrayBuffer(byteString.length);
    const ia = new Uint8Array(ab);
    for (let i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }
    return new Blob([ab], { type: mimeString });
}