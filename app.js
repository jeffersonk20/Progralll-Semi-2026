document.addEventListener("DOMContentLoaded", () => {
    // Inicializar Alertify
    if (typeof alertify !== 'undefined') {
        alertify.set('notifier', 'position', 'top-right');
    }

    // Configurar menú de navegación
    const navOpciones = document.getElementById('navOpciones');
    if (navOpciones) {
        navOpciones.addEventListener('click', e => {
            e.preventDefault();
            const form = e.target.dataset.form;
            if (form) {
                cargarForm(form);
            }
        });
    }

    // Traer la ventana activa al frente al hacer clic en ella
    $(document).on('mousedown', '.position-absolute', function () {
        $('.position-absolute').css('z-index', 1000);
        $(this).css('z-index', 1050);
    });

    // Requisito 5: El login debe ser el primero que se muestre al ejecutar el servidor
    cargarLoginInicial();
});

// Carga del formulario de login inicial obligatorio
function cargarLoginInicial() {
    fetch('/vistas?form=login')
        .then(response => response.text())
        .then(html => {
            $('#login_contenedor').html(html);
        })
        .catch(() => {
            if (typeof alertify !== 'undefined') {
                alertify.error('Error al conectar con el servidor.');
            }
        });
}

// Desbloquea el sistema tras una autenticación exitosa
function loginExitoso(usuario) {
    document.getElementById('auth_overlay').style.display = 'none';
    document.getElementById('areaTrabajo').style.display = 'block';
    document.getElementById('navOpciones').style.display = 'flex';
    document.getElementById('usuarioActivoInfo').style.display = 'block';
    document.getElementById('btnCerrarSesion').style.display = 'inline-block';
    document.getElementById('lblUsuarioLogueado').textContent = usuario.nombre || usuario.usuario;

    if (typeof alertify !== 'undefined') {
        alertify.success(`Bienvenido al sistema, ${usuario.nombre || usuario.usuario}`);
    }

    // Cargar automáticamente el formulario de usuarios y búsqueda
    cargarForm('usuarios');
}

// Cierra la sesión activa y regresa al login bloqueante
function cerrarSesion() {
    document.getElementById('auth_overlay').style.display = 'flex';
    document.getElementById('areaTrabajo').style.display = 'none';
    document.getElementById('navOpciones').style.display = 'none';
    document.getElementById('usuarioActivoInfo').style.display = 'none';
    document.getElementById('btnCerrarSesion').style.display = 'none';
    document.getElementById('lblUsuarioLogueado').textContent = '';

    // Limpiar contenido de módulos
    $('#usuarios_contenedor').html('').hide();
    $('#busqueda_usuarios_contenedor').html('').hide();

    // Recargar vista login
    cargarLoginInicial();

    if (typeof alertify !== 'undefined') {
        alertify.message('Sesión cerrada correctamente.');
    }
}

// Carga dinámica de formularios en ventanas flotantes
function cargarForm(form, callback) {
    const contenedorId = `#${form}_contenedor`;
    if ($(contenedorId).children().length === 0) {
        fetch(`/vistas?form=${form}`)
            .then(response => response.text())
            .then(vistaHtml => {
                $(contenedorId).html(vistaHtml).show().draggable({
                    handle: ".card-header"
                });
                configurarCierreVentana();
                if (callback) callback();
            })
            .catch(() => {
                if (typeof alertify !== 'undefined') {
                    alertify.error(`Error al cargar el módulo ${form}.`);
                }
            });
    } else {
        $(contenedorId).show();
        if (callback) callback();
    }
}

// Configuración de los botones cerrar en las tarjetas
function configurarCierreVentana() {
    $('.btn-close').off('click').on('click', function (e) {
        e.preventDefault();
        const form = $(this).data('form');
        if (form) {
            $(`#${form}_contenedor`).hide();
        }
    });
}
