document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('generatorForm');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoader = submitBtn.querySelector('.btn-loader');
    const statusMessage = document.getElementById('statusMessage');

    // Preview Elements
    const previewSection = document.getElementById('previewSection');
    const previewContent = document.getElementById('previewContent');
    const tabBtns = document.querySelectorAll('.tab-btn');

    let activePreviews = {};

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Reset state
        setLoading(true);
        statusMessage.textContent = 'Analyzing and generating your plan...';
        statusMessage.className = 'status-message success';
        previewSection.hidden = true;

        const formData = new FormData(form);
        const data = {};

        formData.forEach((value, key) => {
            if (key === 'buildableM2' || key === 'purchasePrice') {
                data[key] = parseFloat(value);
            } else if (key === 'exitYear') {
                data[key] = parseInt(value);
            } else if (key === 'bankLoanNeeded' || key === 'constructionProject') {
                data[key] = value === 'true';
            } else {
                data[key] = value;
            }
        });

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to generate plan');
            }

            const result = await response.json();

            // 1. Store previews
            activePreviews = result.previews;

            // 2. Trigger Download
            const downloadUrl = result.downloadUrl;
            const a = document.createElement('a');
            a.href = downloadUrl;
            a.download = result.filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);

            // 3. Show Preview
            showPreview('Projections');
            previewSection.hidden = false;

            // Smooth scroll to preview
            setTimeout(() => {
                previewSection.scrollIntoView({ behavior: 'smooth' });
            }, 100);

            statusMessage.textContent = 'Success! File downloaded and preview ready below.';
            statusMessage.className = 'status-message success';
            setLoading(false);

        } catch (error) {
            console.error('Error:', error);
            statusMessage.textContent = `Error: ${error.message}`;
            statusMessage.className = 'status-message error';
            setLoading(false);
        }
    });

    // Tab Logic
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const sheet = btn.getAttribute('data-sheet');

            // Update UI
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            showPreview(sheet);
        });
    });

    function showPreview(sheetName) {
        if (activePreviews[sheetName]) {
            previewContent.innerHTML = activePreviews[sheetName];
        } else {
            previewContent.innerHTML = '<div class="preview-placeholder">No data available for this sheet.</div>';
        }
    }

    function setLoading(isLoading) {
        submitBtn.disabled = isLoading;
        btnLoader.hidden = !isLoading;
        if (isLoading) {
            btnText.textContent = 'Processing Data...';
            submitBtn.style.opacity = '0.7';
        } else {
            btnText.textContent = 'Generate Business Plan';
            submitBtn.style.opacity = '1';
        }
    }
});
