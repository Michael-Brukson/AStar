const canvas = document.getElementById('drawingCanvas');
const ctx = canvas.getContext('2d', { willReadFrequently: true });
const drawingLabel = document.getElementById('drawingLabel');
const imagesContainer = document.getElementById('imagesContainer');
const submitDrawing = document.getElementById('submitDrawing');
const clearDrawing = document.getElementById('clearDrawing');
const radios = document.querySelectorAll('input[name="pencil"]');
let drawing = false;

var source = [];
var destination = [];

const COLORS = {"source":"red", "draw":"black", "destination":"blue"};

submitDrawing.addEventListener('click', submitCanvas);
clearDrawing.addEventListener('click', clearCanvas);

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
        if (source.length > 0) drawDot(source[0], source[1], 'white', radius=6);
        source = [pos.x, pos.y]; 
        drawDot(pos.x, pos.y, COLORS[radioVal]);
        drawing = false;
    } else if (radioVal === "destination"){
        if (destination.length > 0) drawDot(destination[0], destination[1], 'white', radius=6);
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

// TODO: add check to make sure that source and destination still exist in canvas (make sure that color at coords is red/blue respectively)
// TODO: add separate canvas and drawing of path from source to destination
async function submitCanvas(event) {
    if (!ctx.getImageData(0, 0, canvas.width, canvas.height).data.some(channel => channel !== 0)) {
        alert('You have not drawn anything!');
        return;
    }

    const dataURL = canvas.toDataURL('image/png');

    const img = document.createElement('img');
    img.src = dataURL;
    img.width = canvas.width / 5;
    img.height = canvas.height / 5;
    imagesContainer.appendChild(img);

    const response = await sendImage(dataURL);
    console.log(response);
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