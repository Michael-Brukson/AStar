const canvas = document.getElementById('drawingCanvas');
const ctx = canvas.getContext('2d');
const drawingLabel = document.getElementById('drawingLabel');
const imagesContainer = document.getElementById('imagesContainer')
const radios = document.querySelectorAll('input[name="pencil"]');
let drawing = false;

console.log(radios)

const source = [];
const destination = [];

canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('mousemove', draw);

canvas.addEventListener('touchstart', (e) => {
    startDrawing(e.touches[0]);
});
canvas.addEventListener('touchend', stopDrawing);
canvas.addEventListener('touchmove', (e) => {
    draw(e.touches[0]);
    e.preventDefault();
});

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
    ctx.beginPath();
    const pos = getCursorPosition(event);
    ctx.moveTo(pos.x, pos.y);
}

function stopDrawing() {
    drawing = false;
    ctx.beginPath();
}

function draw(event) {
    if (!drawing) return;
    console.log(getCurrentRadioValue());
    const pos = getCursorPosition(event);
    ctx.lineWidth = 10;
    ctx.lineCap = 'round';
    ctx.strokeStyle = 'black';

    ctx.lineTo(pos.x, pos.y);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(pos.x, pos.y);
}

function getCurrentRadioValue(){
    const radio = document.querySelector('input[name="pencil"]:checked')
    return radio.value;
}

function sendImage(dataURL){
    const blob = dataURLToBlob(dataURL);
    const formData = new FormData();

    const time = new Date().toISOString();
    formData.append('upload', blob, `${time}.png`);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload', true);
    xhr.onload = function () {
        if (xhr.status === 200) {
            console.log('Uploaded successfully');
            
            const img = document.createElement('img');
            img.src = dataURL;
            img.width, img.height = 100, 300;
            imagesContainer.appendChild(img);
        } else {
            console.log('Upload failed');
        }
    };
    xhr.send(formData);
    return JSON.parse(xhr.responseText);
}

document.getElementById('submitDrawing').addEventListener('click', function () {
    if (!ctx.getImageData(0, 0, canvas.width, canvas.height).data.some(channel => channel !== 0)) {
        alert('You have not drawn anything!');
        return;
    }

    const dataURL = canvas.toDataURL('image/png');

    const response = sendImage(dataURL);

    ctx.clearRect(0, 0, canvas.width, canvas.height);
});

clearDrawing.addEventListener('click', function () {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
});

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