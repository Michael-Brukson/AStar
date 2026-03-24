// attempted fix at IOS moving screen on draw, error: $ is not defined
// $(window).bind(
//   'touchmove',
//    function(e) {
//     e.preventDefault();
//   }
// );

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
    document.documentElement.style.setProperty('--brushSizeThumbThickness', String(value) + 'px');
    brushSizeDisplay.innerHTML = String(value) + ' px';
}