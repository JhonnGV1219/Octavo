# Octavo: uso de los CRUD

## Módulos incluidos
- Provincias: listado, búsqueda, creación, edición, detalle y eliminación.
- Cantones: las mismas operaciones, vinculados a una provincia.
- Estudiantes: las mismas operaciones, vinculados a un cantón.
- Universidades: CRUD completo basado en los campos definidos en `TbUniversidades`.

Los modelos actuales usan `managed = False`; Django espera que las tablas MySQL existentes estén creadas. Django no cambia el esquema ni crea migraciones para estos modelos.

## Validaciones aplicadas
- Longitudes y campos requeridos según el modelo.
- Código de provincia positivo y único; nombre de provincia único.
- Cantón único dentro de la provincia elegida.
- Cédula de exactamente 10 dígitos y única.
- Fecha de nacimiento no futura.
- Nombre de universidad único.
- Las eliminaciones se procesan por POST y muestran confirmación; si una relación impide eliminar el registro, se informa al usuario.

## Paquetes del layout
Se conserva la plantilla compartida `principal/plantillaPrincipal.html` y se le añaden Bootstrap Icons 1.11.3, Bootstrap File Input 5.5.4, DataTables 2.3.8, Buttons 3.2.6, Responsive 3.0.7, SweetAlert2 11 y Driver.js. JSZip y pdfmake habilitan Excel y PDF.

`Octavo/static/assets/css/app.css` concentra los estilos del panel; `Octavo/static/assets/js/app.js` configura tablas, validación, confirmaciones, toasts y el tutorial. Para agregar una carga de imagen o archivo, incorpora primero un campo al modelo y al formulario con `data-preview`; el esquema actual no contiene adjuntos, así que no se inventó un campo.

## Flujo de uso
1. Abre Resumen desde la navegación superior.
2. Elige un módulo y usa búsqueda, ordenamiento, paginación o exportación.
3. Usa los iconos de fila para ver, editar o eliminar.
4. Para cambios, completa todos los campos requeridos y atiende los mensajes de validación.

Las dependencias se cargan desde CDN y requieren conexión a Internet en el navegador.
