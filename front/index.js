const filePath = document.getElementById('filePath');
document.getElementById('uploadForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    
    const fileInput = document.getElementById('fileInput');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('http://127.0.0.1:8000', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const result = await response.json();
            console.log('File uploaded successfully:', result);
            filePath.textContent = `${result.location} copied to clipboard`;

            // Auto-copy the file path to the clipboard
            const location = result.location
            await navigator.clipboard.writeText(location);
            console.log('File path copied to clipboard');
            const a = document.createElement('a')
            a.innerHTML = `http://127.0.0.1:8000?file_location=${location}`
            a.href = `http://127.0.0.1:8000?file_location=${location}`
            a.download =`${location}`
            document.body.appendChild(a)
            a.click()
            document.body.removeChild(a)
        } else {
            console.error('Failed to upload file:', response.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
    }
});