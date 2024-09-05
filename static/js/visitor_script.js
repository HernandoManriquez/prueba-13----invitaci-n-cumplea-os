document.addEventListener('DOMContentLoaded', function() {
    const house = document.getElementById('snoopy-house');
    const videoContainer = document.getElementById('video-container');
    const formContainer = document.getElementById('form-container');
    const introVideo = document.getElementById('intro-video');
    const userForm = document.getElementById('user-form');

    house.addEventListener('click', function() {
        house.style.display = 'none';
        videoContainer.style.display = 'block';
        ground.style.display= 'none';
        introVideo.play();
    });

    introVideo.addEventListener('ended', function() {
        videoContainer.style.display = 'none';
        formContainer.style.display = 'block';
    });

    userForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        
        fetch('/submit', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => Promise.reject(err));
            }
            return response.json();
        })
        .then(data => {
            alert('Gracias por tu participación!');
            userForm.reset();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Hubo un error al enviar los datos: ' + (error.error || 'Error desconocido'));
        });
    });
});

function createBalloons() {
    const colors = ['#ff6b6b', '#4bcffa', '#ff9ff3', '#feca57', '#48dbfb'];
    const balloonCount = window.innerWidth < 768 ? 10 : 20;
    for (let i = 0; i < balloonCount; i++) {
      const balloon = document.createElement('div');
      balloon.classList.add('balloon');
      balloon.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
      balloon.style.left = `${Math.random() * 100}%`;
      balloon.style.top = `${Math.random() * 100}%`;
      balloon.style.animationDelay = `${Math.random() * 5}s`;
      document.body.appendChild(balloon);
    }
}

window.onload = createBalloons;
window.addEventListener('resize', function() {
    document.querySelectorAll('.balloon').forEach(el => el.remove());
    createBalloons();
});