document.getElementById('input-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const cities = document.getElementById('cities').value.split(',');
    const distances = document.getElementById('distances').value.split('\n').map(line => {
        const [from, to, distance] = line.split(',');
        return { from, to, distance: parseFloat(distance) };
    });
    const start = document.getElementById('start').value;
    const goal = document.getElementById('goal').value;

    fetch('/solve', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ cities, distances, start, goal }),
    })
        .then(response => response.json())
        .then(data => {
            const output = document.getElementById('output');
            output.innerHTML = `<h2>Shortest Path</h2><p>${data.path.join(' → ')}</p>`;
        });
});
