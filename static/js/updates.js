const h_method_dropdown = document.getElementById('h_method_dropdown');
const equation = document.getElementById('equation');
var slider = document.getElementById("brushSize");
var brushSizeDisplay = document.getElementById("brushSizeDisplay")

h_method_dropdown.addEventListener('change', updateEquation);
slider.addEventListener('input', updateBrushSizeDisplay);

updateBrushSizeDisplay();
updateEquation();

function updateEquation(){
    equation.innerText = h_methods[h_method_dropdown.value];
    MathJax.typesetPromise([equation]);
}

function updateBrushSizeDisplay(){
    let value = parseFloat(slider.value);
    value = value.toFixed(2);
    brushSizeDisplay.innerHTML = value;
}