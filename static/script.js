document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('generatorForm');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoader = submitBtn.querySelector('.btn-loader');
    const statusMessage = document.getElementById('statusMessage');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Reset state
        setLoading(true);
        statusMessage.textContent = 'Generating your business plan...';
        statusMessage.className = 'status-message success';

        const formData = new FormData(form);
        const data = {};

        // Convert FormData to JSON following BusinessPlanInputs schema (camelCase for Pydantic aliases)
        formData.forEach((value, key) => {
            // Handle number conversions
            if (key === 'buildableM2' || key === 'purchasePrice') {
                data[key] = parseFloat(value);
            } else if (key === 'exitYear') {
                data[key] = parseInt(value);
            } 
            // Handle boolean conversions
            else if (key === 'bankLoanNeeded' || key === 'constructionProject') {
                data[key] = value === 'true';
            }
            else {
                data[key] = value;
            }
        });

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to generate plan');
            }

            // Get the blob and trigger download
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            
            // Try to extract filename from header
            const disposition = response.headers.get('content-disposition');
            let filename = 'BusinessPlan.xlsx';
            if (disposition && disposition.indexOf('filename=') !== -1) {
                filename = disposition.split('filename=')[1].trim().replace(/"/g, '');
            }
            
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

            statusMessage.textContent = 'Success! Your file is descending.';
            statusMessage.className = 'status-message success';
            
            // Reset button after 2s
            setTimeout(() => {
                statusMessage.textContent = '';
                setLoading(false);
            }, 3000);

        } catch (error) {
            console.error('Error:', error);
            statusMessage.textContent = `Error: ${error.message}`;
            statusMessage.className = 'status-message error';
            setLoading(false);
        }
    });

    function setLoading(isLoading) {
        submitBtn.disabled = isLoading;
        btnLoader.hidden = !isLoading;
        if (isLoading) {
            btnText.textContent = 'Preparing Excel...';
            submitBtn.style.opacity = '0.7';
            submitBtn.style.cursor = 'not-allowed';
        } else {
            btnText.textContent = 'Generate Business Plan';
            submitBtn.style.opacity = '1';
            submitBtn.style.cursor = 'pointer';
        }
    }
});
