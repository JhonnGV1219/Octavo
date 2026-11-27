(() => {
  "use strict";

  const toast = (icon, title) => {
    if (!window.Swal) return;
    Swal.fire({toast:true,position:"top-end",icon,title,showConfirmButton:false,timer:3200,timerProgressBar:true});
  };

  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-app-toast]").forEach((item) => toast(item.dataset.icon || "success", item.textContent.trim()));

    document.querySelectorAll("form.needs-validation").forEach((form) => {
      const controls = form.querySelectorAll("input, select, textarea");
      controls.forEach((control) => {
        control.addEventListener("input", () => {
          if (!control.willValidate) return;
          control.classList.toggle("is-valid", control.checkValidity());
          control.classList.toggle("is-invalid", !control.checkValidity());
        });
        control.addEventListener("change", () => {
          if (!control.willValidate) return;
          control.classList.toggle("is-valid", control.checkValidity());
          control.classList.toggle("is-invalid", !control.checkValidity());
        });
      });
      form.addEventListener("submit", (event) => {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
          form.classList.add("was-validated");
          form.querySelector(":invalid")?.focus();
          form.reportValidity();
        }
      });
    });

    document.querySelectorAll("form.delete-form").forEach((form) => {
      form.addEventListener("submit", async (event) => {
        if (form.dataset.confirmed === "true") return;
        event.preventDefault();
        if (!window.Swal) {
          if (window.confirm("¿Deseas eliminar este registro?")) form.submit();
          return;
        }
        const result = await Swal.fire({
          title:"¿Eliminar registro?",
          text:`Esta acción eliminará ${form.dataset.confirmDelete || "el registro"}.`,
          icon:"warning",
          showCancelButton:true,
          confirmButtonText:"Sí, eliminar",
          cancelButtonText:"Cancelar",
          confirmButtonColor:"#c2273a",
          reverseButtons:true,
          focusCancel:true
        });
        if (result.isConfirmed) {
          form.dataset.confirmed = "true";
          form.requestSubmit();
        }
      });
    });

    const table = document.querySelector("[data-entity-table]");
    if (table && window.DataTable) {
      new DataTable(table, {
        pageLength:10,
        lengthMenu:[[10,25,50,-1],[10,25,50,"Todos"]],
        order:[],
        responsive:true,
        language:{
          search:"Filtrar:",lengthMenu:"Mostrar _MENU_",
          info:"Mostrando _START_–_END_ de _TOTAL_",
          infoEmpty:"Sin registros",zeroRecords:"No hay coincidencias",
          emptyTable:"No hay registros disponibles",
          paginate:{first:"Primero",last:"Último",next:"Siguiente",previous:"Anterior"},
          buttons:{copy:"Copiar",csv:"CSV",excel:"Excel",pdf:"PDF",print:"Imprimir"}
        },
        layout:{
          topStart:{buttons:[
            {extend:"copyHtml5",text:'<i class="bi bi-copy" aria-hidden="true"></i> Copiar',exportOptions:{columns:":not(.no-export)"}},
            {extend:"csvHtml5",text:'<i class="bi bi-filetype-csv" aria-hidden="true"></i> CSV',exportOptions:{columns:":not(.no-export)"}},
            {extend:"excelHtml5",text:'<i class="bi bi-file-earmark-excel" aria-hidden="true"></i> Excel',exportOptions:{columns:":not(.no-export)"}},
            {extend:"pdfHtml5",text:'<i class="bi bi-file-earmark-pdf" aria-hidden="true"></i> PDF',orientation:"landscape",pageSize:"A4",exportOptions:{columns:":not(.no-export)"}},
            {extend:"print",text:'<i class="bi bi-printer" aria-hidden="true"></i> Imprimir',exportOptions:{columns:":not(.no-export)"}}
          ]},
          topEnd:"search",
          bottomStart:"info",
          bottomEnd:"paging"
        }
      });
    }

    document.querySelectorAll('input[type="file"][data-preview]').forEach((input) => {
      if (window.jQuery && window.jQuery.fn.fileinput) {
        window.jQuery(input).fileinput({showUpload:false,showRemove:true,previewFileType:"image",allowedFileExtensions:["jpg","jpeg","png","pdf"]});
      }
    });

    const tourButton = document.querySelector("[data-start-tour]");
    if (tourButton && window.driver?.js?.driver) {
      const tour = window.driver.js.driver({
        showProgress:true,
        nextBtnText:"Siguiente",
        prevBtnText:"Anterior",
        doneBtnText:"Finalizar",
        steps:[
          {element:"[data-tour='dashboard-stats']",popover:{title:"Resumen del sistema",description:"Consulta el total de registros por entidad."}},
          {element:"[data-tour='dashboard-nav']",popover:{title:"Navegación",description:"Abre los módulos de provincias, cantones, estudiantes y universidades."}},
          {element:"[data-tour='recent-records']",popover:{title:"Actividad reciente",description:"Accede rápidamente a los últimos estudiantes actualizados."}}
        ]
      });
      tourButton.addEventListener("click", () => tour.drive());
    }
  });
})();
