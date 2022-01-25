# Pendientes a corto plazo
## Generales
- [x] Descargar Markdown all in one para Visual Code
- [x] Crear script de Menús intermedios
- [ ] Crear método para actualizar información

## Logueo y administracion
- [x] Desarrollar GUI logueo2 Recuperar contrasena
- [x] Desarrollar GUI logueo3 Cambiar contrasena
- [x] Ajustar tamaños de pantalla de administracion
- [x] Generar cuadros de dialogo en administracion (reemplazando los prints)
- [x] Generar cuadros de dialogo en logueo (reemplazando los prints)

## vsf
- [x] Integrar a elementos_de_gui
- [x] Ajustar el tamaño de la fila de la vitrina
- [x] Cambiar el color del encabezado
- [x] (Opcional) Tooltip sobre los textos (Texto con puntos suspensivos)
- [x] Acondicionar tooltip para que funcione con el loop

## ventanas_busqueda
- [x] Widget de fecha con predeterminado vacío (Observación)
- [x] Agregar nuevo filtro en reemplazo del filtro de fecha
- [x] Crear pantalla de búsqueda de doc emitidos
- [x] Crear método de asociar
- [x] Relacionar el ID interno con el ID del aplicativo
- [x] Actualizar tabla de RELACIONES con su historial
- [x] Mejora del código de búsqueda
- [x] Búsqueda por palabra clave
- [x] Pantalla de Búsqueda de problemas
- [x] Actualizar vitrina_busqueda con Tooltip
- [x] Eliminar frame con entries al "Limpiar"
- [x] Necesario: Añadir texto de "No se han encontrado resultado de búsqueda"
- [x] Necesario: Al hacer click en volver, actualizar la pantalla con "actualizar_vista"
- [x] Necesario: Búsqueda de macroproblemas
- [x] Necesario: Búsqueda de administrados
- [x] Necesario: Pantalla de pendientes jefe 1 (Pantalla de búsqueda DE firmar con filtro)
- [x] Necesario: Pantalla de pendientes jefe 2 (Pantalla de búsqueda DR por asignar)
- [ ] Programar: No permitir asociar documentos ya asociados 

## ventanas_vista
- [x] Mostrar inicialmente la vitrina vacía
- [x] Mostrar label cuando no hayan valores o cambiar fondo de tabla vacía
- [x] Actualizar entries, según tamaño que corresponda
- [x] Agregar entry con scrolltext
- [x] Crear método de generar vitrina
- [x] Crear método de actualizar vitrina
- [x] Crear método para eliminar documentos asociados
- [x] Crear tabla con historial de relaciones
- [x] Actualizar método de enviar DE con información con historial
- [x] Actualizar método de guardar DE con modificación
- [x] Crear método de actualización de ventana con datos modificados
- [x] Crear pantalla de navegación
- [x] Crear botones provisionales para facilitar navegación
- [x] Simplificación del uso de código/id de usuario/interno
- [x] Replicar métodos para la clase de documentos recibidos
- [x] Mover rejilla para facilitar el ingreso de información al administrativo
- [x] EP: Primer entry sea el código de problema
- [x] EP: Agregar botón con "Prioridad" y vista de puntaje
- [x] EP: Agregar vista de f_creación y f_actualización
- [x] Necesario: Definir ID con número de oficio para problema
- [x] Necesario: Crear método para la creación de ID extremos
- [x] Necesario: Pantalla de vista de macroproblemas
- [x] Programar: Crear método para la asociación de más de 2 relaciones (transitividad)
- [x] Programar: Simplificación y abstracción de método de generar vitrina
- [x] Programar: Simplificación de método de actualización de vitrinas en vista
- [x] Programar: Simplificación y abstracción de método de eliminar objeto
- [x] Programar: Simplificación y abstracción de títulos y botones principales en Frame
- [x] Programar: Simplificación y abstracción de método de agregar objeto
- [x] Programar: No permitir ingresar un código de interfaz (de usuario) igual (Mensaje de error)
- [x] Programar: Agregar timestamp (tiempo para cada clase de objeto)

## Nuevas ventanas
- [x] Creación de pantallas de menú
- [x] Creación de pantallas equipo administrativo
- [x] Crear pantalla de extremo de problemas [Lucho]
- [x] Crear pantalla de búsqueda de extremo de problema [Lucía]
- [x] Crear tabla de relaciones entre documentos y extremos de problemas [Ambos]
- [x] Pendientes por asignar (Perfil de jefe)
- [x] Pendientes por firmar (Perfil de jefe)
- [x] Creación de pantallas de macroproblema
- [x] Crear pantalla de búsqueda de administrados [Lucía]
- [x] Creación de asignaciones pendientes Equipo 1
- [x] Creación de asignaciones pendientes Equipo 2
- [x] Creación de programaciones Equipo 2
- [ ] Crear pantalla de registro de administrados [Lucho]

## Retos
- [x] Investigar: Visualización de información en vitrina con texto flotante
- [x] Diseñar: Métodos que consideren la transitividad de las relaciones 
- [x] Investigar: Lista desplegable condicionada de tres niveles
- [x] Investigar: Eliminación de widgets de tipo de DateEntry o seteo como valor vacío
- [x] Investigar: Ventanas de vista con scrollbar para visualizar vitrinas
- [x] Investigar: Crear franja superior e inferior para la ventana


## A corto plazo
## Migración de información
- [x] Armar tablas preliminares con datos reales para docs recibidos (Lucho)
- [x] Armar tablas preliminares con datos reales para docs emitidos (Lucia)
- [ ] Migrar información de extremos de problemas
- [ ] Revisar tablas de datos y realizar la comparación con las tablas actuales

## A mediano plazo
- [ ] Implementación de diccionario de datos para selección de columnas
### ventanas_vista
- [ ] Programar: Selección automática de documento emitido en función de Destinatario
- [ ] Programar: Selección automática de especialista equipo 2 en función al EP
- [ ] Investigar: Ventana emergente con resultado de calculadora
- [ ] Investigar: Cálculo de plazo en días hábiles para el vencimiento
- [ ] Investigar: Cálculo de Estado de Documentos Emitidos (En Plazo, Vencido)
### ventanas_busqueda
- [ ] Programar: Eliminar de la vitrina de búsqueda los objetos ya asociados
- [ ] Programar: Abstracción de métodos e inclusión en funcionalidades_ospa
- [ ] Programar: Se podrán agregar EP a DE (EP solo dentro de los DR asociados)

### Logueo y administración
- [ ] Evaluar combinar los archivos administracion y logueo
- [ ] Simplificar funciones con elementos comunes // Posible creación de la class Usuario.

### Observaciones del piloto
- [ ] Búsqueda por ht que transforme las minúsculas en mayúsculas.
- [ ] Búsqueda por código en pantalla de extremos que sea por palabra clave.
- [ ] Revisión de conversión de los antiguos códigos a los nuevos.
- [ ] Evaluar si nos quedamos con la forma de creación de códigos antigua o nueva.
- [ ] Revisar la creación de nuevos códigos debido a que existen correlativos largos.
- [ ] Colocar los nombres en los botones para el menú en lugar del "Ir".
- [ ] Agrandar el tamaño de los desplegables que contienen EFA.
- [ ] Duplicar los datos a la hora de crear extremos similares.
- [ ] Evaluar trabajo paralelo entre el equipo 1 y 2.
