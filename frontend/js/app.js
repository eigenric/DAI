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
                            <button type="button" data-bs-toggle="modal" data-bs-target="#editModal${i-1}" class="btn btn-warning btn-sm">Edit</button>
                            <button type="button" data-bs-toggle="modal" data-bs-target="#eliminarModal${i-1}" class="btn btn-danger btn-sm">Delete</button></a>
                       </td>
                    </tr>`;       // ES6 templates

          html_str += `<!-- Confirmacion de eliminación -->
          <div class="modal fade" id="eliminarModal${i-1}" tabindex="-1" aria-labelledby="eliminarModal${i-1}Label" aria-hidden="true">
              <div class="modal-dialog">
              <div class="modal-content">
                  <div class="modal-header">
                  <h1 class="modal-title fs-5" id="eliminarModal${i-1}">Confirmación</h1>
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                  </div>
                  <div class="modal-body">
                  ¿Está seguro de que desea eliminar la receta?
                  </div>
                  <div class="modal-footer">
                  <button type="button" class="btn btn-primary" data-bs-dismiss="modal">No.</button>
                      <a href="/"><button type="button" class="btn btn-danger" onclick="deleteCoctel(${i-1})">Sí, eliminar.</button></a>
                  </div>
              </div>
              </div>
          </div>`;



          // Creaciond el modal 
          let ingredientes_html = lista_ingredientes(recetas[i-1]);
          let instrucciones_html = html_instrucciones(recetas[i-1]);

          html_str += `<div class="modal fade" id="detailModal${i-1}" tabindex="-1" role="dialog">
                    <div class="modal-dialog" role="document">
                         <div class="modal-content">
                              <div class="modal-header">
                                   <h5 class="modal-title">${fila.name}</h5>
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

          let ingredientes_txt = escape_ingredientes(recetas[i-1]);
          let instrucciones_txt = escape_instrucciones(recetas[i-1]);
          
          html_str += `<!-- Edit modal -->
          <div class="modal" id="editModal${i-1}" tabindex="-1" role="dialog" aria-labelledby="editModalLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
              <div class="modal-content">
                    <div class="modal-header">
                         <h5 class="modal-title" id="editModalLabel">Editar cóctel</h5>
                         <button type="button" class="close" data-bs-dismiss="modal" aria-label="Close">
                         <span aria-hidden="true">&times;</span>
                         </button>
                    </div>
                    <div class="modal-body">
                         <form action="/" id="editForm${i-1}" onsubmit="editCoctel(${i-1})">
                              <div class="form-group">
                                   <label>Nombre</label>
                                   <input type="text" class="form-control" id="name" value="${fila.name}">
                              </div>
                              <div class="form-group">
                              <label>Ingredientes</label>
                              <textarea class="form-control" id="editIngredientes${i-1}" rows="3">
                                    ${ingredientes_txt} 
                              </textarea>
                              </div>
                              <div class="form-group">
                              <label>Instrucciones</label>
                              <textarea class="form-control" id="editInstrucciones${i-1}" rows="3">
                                   ${instrucciones_txt}
                              </textarea>
                              </div>
                              <div class="form-group">
                              <button type="submit" class="btn btn-primary">Editar</button>
                              </div>
                         </form>
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

function editCoctel(i) {
     console.log("editCoctel ejecutado!");
     let name = document.getElementById(`editName${i}`).value;
     let ingredientes = document.getElementById(`editIngredientes${i}`).value;
     let instrucciones = document.getElementById(`editInstrucciones${i}`).value;
     let ingredientesArray = ingredientes.split("-");
     
     console.log("EDIT values");
     console.log(name);
     console.log(ingredientes);
     console.log(instrucciones);
     
     ingredientesArray.shift();

     ingredientesArray.shift();

     let ingredientesArrayDict = [];
     ingredientesArray.forEach(ingrediente => {
          ingredientesArrayDict.push({ name : ingrediente.replace("\n", "") });
     });

     console.log(ingredientesArrayDict);

     let instruccionesArray = instrucciones.split("\n");
     
     let coctel = {
          "name": name,
          "ingredients": ingredientesArrayDict,
          "instructions": instruccionesArray
     };
     console.log(JSON.stringify(coctel));

     fetch(`http://localhost:5000/api/recipes/${recetas[i]._id}`, {
           method: 'PUT',
           headers: {
           'Content-Type': 'application/json'
           },
           body: JSON.stringify(coctel)
     })
     .then(response => response.json())
     .then(response => console.log(JSON.stringify(response)));
}


function escape_ingredientes(receta) {
     const ingredientes = [];
     let ingrediente_txt = '';
     let j = 0;

     receta["ingredients"].forEach(ingrediente => {
          j++;
          ingredientes.push(ingrediente);
          ingrediente_txt += `- ${ingrediente.name}\n`;
     });
     return ingrediente_txt;
}

function escape_instrucciones(receta) {
     const instrucciones = [];
     let instruccion_html = '';
     let k = 0;

     receta["instructions"].forEach(instruccion => {
          k++;
          instrucciones.push(instruccion);
          instruccion_html += `- ${instruccion}\n`;
     })
     return instruccion_html;
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

