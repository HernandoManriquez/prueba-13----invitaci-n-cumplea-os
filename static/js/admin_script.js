document.addEventListener('DOMContentLoaded', function() {
    function loadUserData() {
        fetch('/admin/users')
            .then(response => response.json())
            .then(users => {
                const tbody = document.querySelector('#user-data tbody');
                tbody.innerHTML = ''; // Limpia la tabla antes de cargar nuevos datos
                users.forEach(user => {
                    const row = tbody.insertRow();
                    row.insertCell(0).textContent = user.nombre;
                    row.insertCell(1).textContent = user.apellido;
                    row.insertCell(2).textContent = user.agreement ? 'Sí' : 'No';
                    
                    const videoCell = row.insertCell(3);
                    if (user.video_filename) {
                        const videoLink = document.createElement('a');
                        videoLink.href = `/uploads/${user.video_filename}`;
                        videoLink.textContent = 'Ver video';
                        videoLink.target = '_blank';
                        videoCell.appendChild(videoLink);
                    } else {
                        videoCell.textContent = 'No subió video';
                    }
                    
                    row.insertCell(4).textContent = new Date(user.fecha_creacion).toLocaleString();
                });
            })
            .catch(error => console.error('Error:', error));
    }

    loadUserData();
    // Opcionalmente, puedes establecer un intervalo para actualizar los datos periódicamente
    // setInterval(loadUserData, 60000); // Actualiza cada minuto
});