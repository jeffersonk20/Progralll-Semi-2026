document.addEventListener("DOMContentLoaded", events => {
    const mnx = document.getElementById('mnxImpuestos');
    if (mnx) {
        mnx.addEventListener('click', e => {
            e.preventDefault();
            let form = e.target.dataset.form;
            if (form) cargarForm(form);
        });
    }

    // Traer la ventana activa al frente al hacer clic
    $(document).on('mousedown', '.position-absolute', function () {
        $('.position-absolute').css('z-index', 1000);
        $(this).css('z-index', 1050);
    });
});

function cargarForm(form, callback) {
    if ($(`#${form} > form`).length <= 0) {
        fetch(`/vistas?form=${form}`)
            .then(response => response.text())
            .then(ventana => {
                $(`#${form}`).html(ventana).show().draggable({
                    handle: ".card-header"
                });
                cerrarVentana();
                if (callback) callback();
            })
            .catch(() => {});
    } else {
        $(`#${form}`).show();
        if (callback) callback();
    }
}

function cerrarVentana() {
    $('.btn-close').off('click').on('click', e => {
        e.preventDefault();
        let form = e.target.dataset.form;
        if (form) {
            $(`#${form}`).hide();
        }
    });
}