// This file contains JavaScript code for the web frontend. It handles client-side interactions, such as making AJAX requests to the Flask backend and updating the UI dynamically.

document.addEventListener('DOMContentLoaded', function() {
    const configForm = document.getElementById('config-form');
    const configKeyInput = document.getElementById('config-key');
    const configValueInput = document.getElementById('config-value');
    const configList = document.getElementById('config-list');

    // Fetch and display the current configuration
    function fetchConfig() {
        fetch('/config')
            .then(response => response.json())
            .then(data => {
                const configDisplay = document.getElementById('config-display');
                configDisplay.innerHTML = `<pre>${JSON.stringify(data, null, 4)}</pre>`;
            })
            .catch(error => console.error('Error fetching config:', error));
    }


    // Fetch and display a specific block
    function fetchBlock(block) {
        fetch(`/config/${block}`)
            .then(response => response.json())
            .then(data => {
                const textarea = document.getElementById(`${block}-config`);
                console.log(`Fetching block: ${block}`, textarea);
                if (textarea) {
                    textarea.value = data[block].join('\n');
                } else {
                    console.error(`Element with id '${block}-config' not found.`);
                }
            })
            .catch(error => console.error('Error fetching block:', error));
    }

    // Update a specific block
    function updateBlock(block) {
        const textarea = document.getElementById(`${block}-config`);
        const lines = textarea.value.split('\n').filter(line => line.trim() !== '');

        fetch(`/config/${block}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(lines),
        })
            .then(response => response.json())
            .then(data => {
                alert(data.message || 'Block updated successfully');
            })
            .catch(error => console.error('Error updating block:', error));
    }

    // Reload Squid configuration
    function reloadSquid() {
        fetch('/reload', {
            method: 'POST',
        })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    alert(data.message);
                } else if (data.error) {
                    alert(`Error: ${data.error}`);
                }
            })
            .catch(error => console.error('Error reloading Squid configuration:', error));
    }

    // Initial fetch of the configuration
    fetchConfig();

    // Fetch all blocks on page load
    fetchBlock('basic');
    fetchBlock('acls');
    fetchBlock('allow_access');
    fetchBlock('deny_access');
    fetchBlock('cache_settings');
    fetchBlock('logging');
    fetchBlock('dns_settings');
});