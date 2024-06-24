document.addEventListener('DOMContentLoaded', (event) => {
    let url = `ws://${window.location.host}/ws/socket-server/`;
    const servers = document.querySelectorAll('.all_servers');

    servers.forEach(server => {
        const choose_server = server.querySelector('.choose_server');
        const server_entity = server.querySelector('.server_entity');
        const buttonForm = choose_server.querySelector('#server_name');
        const serverChosen = choose_server.querySelector('#server_name').innerHTML;
        
        choose_server.addEventListener('submit', (event) => {
            event.preventDefault();
            const serverSocket = new WebSocket(url);
            
            
            serverSocket.onopen = function() {
                console.log('WebSocket connection established');
                serverSocket.send(JSON.stringify({
                    'server_name': serverChosen,
                }));
            };

            serverSocket.onmessage = function(e) {
                let data = JSON.parse(e.data);
                server_entity.style.display = "flex";
                server_entity.innerHTML = '';
                if (data.uptime) {
                    if ( data.screens.includes('No Sockets found in')) {data.screens = 'Aucun screens lancés'}
                    if (data.screens.includes('There is a screen on')) {
                        data.screens = data.screens.replace('There is a screen on', 'Il y a un screen')
                        data.screens = data.screens.replace(`1 Socket in /run/screen/S-${data.username}.`, '')
                    }
                    data.uptime = data.uptime.replace(/ load average: [\d\.,\s]+/, '');
                    data.uptime = data.uptime.replace(',', '');
                    data.uptime = data.uptime.replace(',', '');
                    buttonForm.style.color = "green";
                    server_entity.insertAdjacentHTML('beforeend', `
                    ${data.uptime ? `<h3 class="server_info">Uptime : ${data.uptime}</h3>` : ''}
                    <h3 class="server_info">CPU: ${data.cpu_usage}%        ________ RAM: ${data.used_memory} / ${data.total_memory} Go</h3>
                    ${data.screens ? `<h3 class="server_info">${data.screens}</h3>` : ''}
                    ${data.errors ? `<h3 class="server_info">${data.errors}</h3>` : ''}
                    `)
                } else {
                    buttonForm.style.color = "red";
                    server_entity.insertAdjacentHTML('beforeend', `<h2 class="server_info">Execution des commandes ssh, récupération des informations...</h2>`)
                    server_entity.insertAdjacentHTML('beforeend',` ${data.errors ? `<h2 class="server_info">${data.errors}</h2>` : '' }`)
                }
                if (data.errors) {console.log(data.errors)}
            };
        });
    });
});