function initializeDropdowns() {
    // Function to close all dropdowns
    function closeAllDropdowns() {
        document.querySelectorAll('.dropdown-menu').forEach(function (dropdownMenu) {
            dropdownMenu.style.display = 'none';
        });
    }

    // Add click event listener to each dropdown toggle
    document.querySelectorAll('.dropdown-toggle').forEach(function (dropdownToggle) {
        dropdownToggle.addEventListener('click', function (e) {
            const dropdownMenu = e.target.nextElementSibling;

            // Check if the clicked dropdown is already open
            const isOpen = dropdownMenu.style.display === 'block';

            // Close all dropdowns first
            closeAllDropdowns();

            // If the clicked dropdown was not open, open it
            if (!isOpen) {
                dropdownMenu.style.display = 'block';
            }

            console.log("Dropdown toggled");
        });
    });

    // Optional: Close dropdown when clicking outside of it
    document.addEventListener('click', function (e) {
        if (!e.target.matches('.dropdown-toggle') && !e.target.closest('.dropdown-menu')) {
            closeAllDropdowns();
        }
    });
}

function initializeDropdownsRep() {
    // Function to close all dropdowns
    function closeAllDropdowns() {
        document.querySelectorAll('.dropdown-menu-rep').forEach(function (dropdownMenu) {
            dropdownMenu.style.display = 'none';
        });
    }

    // Add click event listener to each dropdown toggle
    document.querySelectorAll('.dropdown-toggle-rep').forEach(function (dropdownToggle) {
        dropdownToggle.addEventListener('click', function (e) {
            const dropdownMenu = e.target.nextElementSibling;

            // Check if the clicked dropdown is already open
            const isOpen = dropdownMenu.style.display === 'block';

            // Close all dropdowns first
            closeAllDropdowns();

            // If the clicked dropdown was not open, open it
            if (!isOpen) {
                dropdownMenu.style.display = 'block';
            }

            console.log("Dropdown toggled");
        });
    });

    // Optional: Close dropdown when clicking outside of it
    document.addEventListener('click', function (e) {
        if (!e.target.matches('.dropdown-toggle-rep') && !e.target.closest('.dropdown-menu-rep')) {
            closeAllDropdowns();
        }
    });
}

// Função para inicializar as notificações
function initializeNotifications() {
    var notifications = document.querySelectorAll('.notification');

    notifications.forEach(function(notification) {
        var progressBar = notification.querySelector('.progress-bar');
        var closeBtn = notification.querySelector('.close');

        // Iniciar a animação da barra de progresso
        setTimeout(function() {
            progressBar.style.width = '0%';
        }, 100);  // Pequeno atraso para garantir a transição

        // Remover a notificação após 5 segundos
        setTimeout(function() {
            notification.remove();
        }, 5000);

        // Fechar a notificação quando o botão de fechar for clicado
        closeBtn.addEventListener('click', function() {
            notification.remove();
        });
    });
}

// Chamar as funções quando o DOM estiver carregado
window.addEventListener('DOMContentLoaded', function () {
    initializeDropdowns();
    initializeDropdownsRep();
    initializeNotifications();
});

document.addEventListener("htmx:beforeRequest", function(evt) {
    evt.detail.triggeringElement = evt.target;
    console.log(evt)
    console.log(evt.detail)
    console.log(evt.target)
    // quero saber se o id delete-link-btn está dentro do target.id
    if(evt.target.id.includes('delete-link-btn')){
        evt.preventDefault();

        Swal.fire({
            title: 'Are you sure?',
            text: "Do you want to delete the post?",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: 'rgb(124, 0, 254)',
            cancelButtonColor: '#d33',
            cancelButtonText: 'No, cancel!',
            confirmButtonText: 'Yes, delete it!',
            
        }).then((result) => {
            if(result.isConfirmed){
                htmx.ajax("POST", evt.detail.pathInfo.finalRequestPath, {
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    swap: 'outerHTML',  // This defines where the response should be swapped
                    target: '#my-body-base',  // This defines the element to receive the response
                    values: new FormData(evt.target)
                });
            }
        });
    }

    if(evt.target.id.includes('delete-comment-btn')){
        evt.preventDefault();

        Swal.fire({
            title: 'Are you sure?',
            text: "Do you want to delete the comment?",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: 'rgb(124, 0, 254)',
            cancelButtonColor: '#d33',
            cancelButtonText: 'No, cancel!',
            confirmButtonText: 'Yes, delete it!',
            
        }).then((result) => {
            if(result.isConfirmed){
                htmx.ajax("POST", evt.detail.pathInfo.finalRequestPath, {
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    swap: 'outerHTML',  // This defines where the response should be swapped
                    target: '#post-open-cont',  // This defines the element to receive the response
                    values: new FormData(evt.target)
                });
            }
        });
    }

});
// Reaplicar as funções após um hx-swap
document.addEventListener('htmx:afterRequest', function (event) {
    if(!event.target.id.startsWith("like_counting_sp") || event.detail.triggeringElement.id === "cancel-edit-post") // tirar essa gambiarra aqui
    {    
        initializeDropdowns();
        initializeNotifications();
        initializeDropdownsRep();
    }
});

document.addEventListener('htmx:afterSettle', function (event) {
    if(event.target.id.startsWith("like_counting_sp")){
        initializeDropdowns();
        initializeNotifications();
        initializeDropdownsRep();
    }
});
