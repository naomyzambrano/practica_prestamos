# -prestamo_unicahsilvia

**Nombre:** Silvia Naomy Zambrano Alonso  
**Número de cuenta:** 0210200500884
## Respuestas

### Paso 1. Catálogo de equipos

**1. ¿Qué pasa con un equipo cuando se desmarca el campo Activo? ¿Por qué es mejor que borrarlo?**

Cuando se desmarca el campo Activo, el equipo deja de aparecer normalmente en las listas, pero sigue guardado en el sistema. Es mejor que borrarlo porque así se conserva su información y el historial de los préstamos anteriores.

**2. ¿Para qué sirve copy=False en el campo codigo?**

Sirve para evitar que al duplicar un equipo se copie también su código de inventario. Así cada equipo puede tener su propio código y no se repiten los códigos por accidente.

### Paso 2. Registro de préstamos

**1. Este modelo usa _name y _inherit al mismo tiempo. ¿Qué hace cada uno aquí?**

_name sirve para crear un modelo nuevo llamado prestamo.prestamo, donde se guarda la información de los préstamos. _inherit permite utilizar las funciones del modelo mail.thread, para tener el historial de mensajes y cambios en el chatter.

**2. ¿Qué hace tracking=True  en el campo state?**

Sirve para que los cambios que se hagan en el estado del préstamo queden registrados en el chatter. Así se puede revisar cuándo cambió el estado y qué modificación se realizó.

### Paso 3. Equipos del préstamo

**1. En fields.One2many("prestamo.linea", "prestamo_id"), ¿qué indica cada parámetro?**

El primer parámetro indica el modelo relacionado, que es prestamo.linea. El segundo indica el campo prestamo_id, que conecta cada línea con su préstamo. Esto permite que un préstamo pueda tener varios equipos registrados.

**2. ¿Qué pasa con las líneas cuando se borra un préstamo? ¿Qué parte del código lo define?**

Cuando se borra un préstamo, también se eliminan las líneas relacionadas con él. Esto lo define ondelete="cascade" en el campo prestamo_id, para evitar que queden líneas sin un préstamo al que pertenecer.

### Paso 4. Flujo de estados

**1. Los botones ya se ocultan según el estado. ¿Por qué los métodos vuelven a validar el estado?**

Porque ocultar los botones solamente controla lo que se muestra en la pantalla. La validación dentro de los métodos sirve para evitar que se realice una acción incorrecta, aunque se intente ejecutar de otra manera. Así se protege mejor la información.

**2. ¿Qué hace prestamo.linea_ids.equipo_id.write(...)? ¿Por qué no hace falta un for para cada equipo?**

Ese código permite cambiar el estado de todos los equipos relacionados con las líneas del préstamo. No hace falta utilizar un for porque Odoo permite aplicar el método write() directamente a varios registros al mismo tiempo.

### Paso 5. Reglas del préstamo

**1. El campo equipo_id ya filtra los equipos disponibles. ¿Por qué hace falta el TODO 5?**

Porque el filtro solamente muestra los equipos disponibles al momento de seleccionarlos. Pero el estado de un equipo puede cambiar después. Por eso hace falta volver a comprobar que siga disponible antes de realizar el préstamo.

**2. ¿En qué momento se ejecuta un método con @api.constrains? ¿Y la validación de action_prestar?**

El método con @api.constrains se ejecuta cuando se crea o modifica un registro y cambian los campos indicados en la restricción. En cambio, la validación de action_prestar se ejecuta cuando se presiona el botón Prestar. Cada una sirve para controlar diferentes reglas del sistema.

### Paso 6. Contacto, kanban y búsqueda

**1. ¿Qué pasa si arrastra una tarjeta del kanban a otra columna? ¿Por qué?**

Al arrastrar una tarjeta a otra columna, el equipo cambia al estado de esa columna, porque el kanban está agrupado por el campo estado. De esta manera se puede actualizar el estado desde la misma vista.

**2. El campo prestamo_ids se agregó a res.partner. ¿Se crea una columna nueva en la tabla de contactos? Explique.**

No se crea una columna nueva en la tabla de contactos, porque prestamo_ids es un campo One2many que permite consultar los préstamos relacionados con un contacto. La relación se guarda desde el campo Many2one partner_id que está en el modelo de préstamos.

