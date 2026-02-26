const equation = document.getElementById('equation');

h_method_dropdown.addEventListener('change', updateEquation);
brushSize.addEventListener('input', updateBrushSizeDisplay);

updateBrushSizeDisplay();
updateEquation();

function updateEquation(){
    equation.innerText = h_methods[h_method_dropdown.value];
    MathJax.typesetPromise([equation]);
}

function updateBrushSizeDisplay(){
    let value = parseFloat(brushSize.value);
    value = value.toFixed(2);
    brushSizeDisplay.innerHTML = value;
}