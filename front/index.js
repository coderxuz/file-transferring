const filePath = document.getElementById('filePath');
const websocket = new WebSocket('ws://192.168.1.20:8000/ws');
const urls = document.querySelector('.urls');

websocket.onopen = () => {
    console.log('WebSocket connection established');
};

websocket.onmessage = async (event) => {
    const fileLocation = event.data;
    console.log('Received file location:', fileLocation);

    // Fetch the file as a Blob
    const fileResponse = await fetch(`http://192.168.1.20:8000?file_location=${fileLocation}`);
    if (fileResponse.ok) {
        const blob = await fileResponse.blob();

        // Create a download link from the Blob
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = fileLocation.split('/').pop(); // Set the filename
        link.textContent = `new file: ${fileLocation}`;
        urls.appendChild(link);

        // Clean up the URL object after the link is clicked
        link.addEventListener('click', () => {
            setTimeout(() => URL.revokeObjectURL(link.href), 100);
        });
    } else {
        console.error('Failed to fetch file:', fileResponse.statusText);
    }
};

document.getElementById('uploadForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    
    const fileInput = document.getElementById('fileInput');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('http://192.168.1.20:8000', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const result = await response.json();
            console.log('File uploaded successfully:', result);
            filePath.textContent = `${result.location} copied to clipboard`;

            // Auto-copy the file path to the clipboard
            const location = result.location;

            // Send the URL via WebSocket
            websocket.send(location);
        } else {
            console.error('Failed to upload file:', response.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
    }
});