const recetas = [];              // declaraciones   
let html_str  = '';              // de variables
let modal;
let i         = 0;             //

// fetch devuelve una promise
fetch('http://localhost:5000/api/recipes/')           // GET por defecto,
.then(res => res.json())        // respuesta en json, otra promise
.then(filas => {                // arrow function
     filas.forEach(fila => {     // bucle ES6, arrow function
          i++;
          recetas.push(fila);      // se guardan para después sacar cada una             
          // ES6 templates
          html_str += `<tr>
                       <td>${i}</td>
                       <td>
                            <button onclick="detalle('${i-1}')" 
                               type="button" class="btn btn-outline btn-sm"
                                  data-bs-toggle="modal" data-bs-target="#detailModal${i-1}">
                            ${fila.name}
                            </button>
                            <div id="recetas${i-1}"></div>
                       </td>
                       <td>
                            <button type="button" class="btn btn-warning btn-sm">Edit</button>
                            <a href="/"><button type="button" onclick="deleteCoctel(${i-1})" class="btn btn-danger btn-sm">Delete</button></a>
                       </td>
                    </tr>`;       // ES6 templates

          // Creaciond el modal 
          ingredientes_html = lista_ingredientes(recetas[i-1]);
          instrucciones_html = html_instrucciones(recetas[i-1]);

          html_str += `<div class="modal" id="detailModal${i-1}" tabindex="-1" role="dialog">
                    <div class="modal-dialog" role="document">
                         <div class="modal-content">
                              <div class="modal-header">
                                   <h5 class="modal-title">${recetas[i-1].name}</h5>
                                   <button type="button" class="close" data-bs-dismiss="modal" aria-label="Close">
                                        <span aria-hidden="true">&times;</span>
                                   </button>
                              </div>
                              <div class="modal-body">
                                   <h6>Ingredientes:</h6>
                                   <ul>
                                        ${ingredientes_html}
                                   </ul>
                                   <h6>Preparación</h6>
                                   <p>${instrucciones_html}</p>
                              </div>
                         </div>
                    </div>
               </div>`;
     });

     document.getElementById('tbody').innerHTML=html_str  // se pone el html en su sitio
});

function deleteCoctel(i) {
     fetch(`http://localhost:5000/api/recipes/${recetas[i]._id}`, {method: 'DELETE'})
     .then(response => response.json())
     .then(response => console.log(JSON.stringify(response)));
}

function addCoctel() {
     var name = document.getElementById("name").value;
     var ingredientes = document.getElementById("ingredientes").value;
     var instrucciones = document.getElementById("instrucciones").value;
     let ingredientesArray = ingredientes.split("-");
     ingredientesArray.shift();

     console.log(name);
     console.log(ingredientesArray);
     console.log(instrucciones);

     let ingredientesArrayDict = [];
     ingredientesArray.forEach(ingrediente => {
          ingredientesArrayDict.push({ name : ingrediente.replace("\n", "") });
     });

     console.log(ingredientesArrayDict)

     let instruccionesArray = instrucciones.split("\n");
     
     let coctel = {
          "name": name,
          "ingredients": ingredientesArrayDict,
          "instructions": instruccionesArray
     };
     console.log(JSON.stringify(coctel));

     fetch('http://localhost:5000/api/recipes/', {
           method: 'POST',
           headers: {
           'Accept': 'application/json',
           'Content-Type': 'application/json'
           },
           body: JSON.stringify(coctel)
     })
     .then(response => response.json())
     .then(response => console.log(JSON.stringify(response)))
}


function lista_ingredientes(receta) {
     const ingredientes = [];
     let ingrediente_html = '';
     let j = 0;

     receta["ingredients"].forEach(ingrediente => {
          j++;
          ingredientes.push(ingrediente);
          ingrediente_html += `<li>${ingrediente.name}</li>`;
     });
     return ingrediente_html;
}

function html_instrucciones(receta) {
     const instrucciones = [];
     let instruccion_html = '';
     let k = 0;

     receta["instructions"].forEach(instruccion => {
          k++;
          instrucciones.push(instruccion);
          instruccion_html += `<p>- ${instruccion}</p>`
     })
     return instruccion_html;
}

function detalle(i) { 
     console.log(`Click en receta ${i}`);
}

