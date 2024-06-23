document.addEventListener('DOMContentLoaded', (event) => {
    let url = `ws://${window.location.host}/ws/socket-server/`;
    const servers = document.querySelectorAll('.all_servers');

    servers.forEach(server => {
        const choose_server = server.querySelector('.choose_server');
        const server_entity = server.querySelector('.server_entity');
        const servers_entities = document.querySelectorAll('.server_entity');
        const serverChosen = choose_server.querySelector('#server_name').innerHTML;
        
        choose_server.addEventListener('submit', (event) => {
            event.preventDefault();
            const serverSocket = new WebSocket(url);
            
            
            serverSocket.onopen = function() {
                console.log('WebSocket connection established');
                serverSocket.send(JSON.stringify({
                    'server_name': serverChosen,
                }));
                console.log('Message sent:', serverChosen);
            };

            serverSocket.onmessage = function(e) {
                console.log('Message received');
                let data = JSON.parse(e.data);
                
                server_entity.style.display = "flex";
                server_entity.innerHTML = '';
                server_entity.insertAdjacentHTML('beforeend', `
                    ${data.screens ? `<h3>Uptime : ${data.uptime}</h3>` : ''}
                    <h3>CPU : ${data.cpu_usage} %       RAM : ${data.used_memory} / ${data.total_memory} Go</h3>
                    ${data.screens ? `<h3>${data.screens}</h3>` : ''}
                    ${data.errors ? `<h3>${data.errors}</h3>` : ''}
                `);
            };
        });
    });
});