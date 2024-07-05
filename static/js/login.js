document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('https://qic534o8o0.execute-api.us-east-1.amazonaws.com/validacionUsuarios/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2ZW50YXMiOiJ0b2tlbl92ZW50YXMifQ._EO1cFamwcGzpJ47DWAHcRB2JqndgLgZOccsGVUukC0/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: username, password: password }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.access) {
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);
            alert('Login successful');
            // Redirigir a la página deseada después del login exitoso
            window.location.href = '/home/';
        } else {
            alert('Login failed: ' + data.detail);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred');
    });
});