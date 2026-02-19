const h_method = document.getElementById('h_method');
const equation = document.getElementById('equation');

h_method.addEventListener('change', updateEquation);
updateEquation();

function updateEquation(){
    equation.innerText = h_methods[h_method.value];
    MathJax.typesetPromise([equation]);
}