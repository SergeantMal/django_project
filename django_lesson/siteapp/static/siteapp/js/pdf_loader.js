document.addEventListener('DOMContentLoaded', function () {
    // Считываем путь к PDF из data-атрибута
    const pdfPath = document.getElementById('pdf-canvas').getAttribute('data-pdf-path');
    const canvas = document.getElementById('pdf-canvas');
    const ctx = canvas.getContext('2d');

    pdfjsLib.getDocument(pdfPath).promise.then(pdf => {
        return pdf.getPage(1);
    }).then(page => {
        const viewport = page.getViewport({ scale: 1.5 });
        canvas.width = viewport.width;
        canvas.height = viewport.height;
        page.render({ canvasContext: ctx, viewport: viewport });
    }).catch(err => {
        console.error('Ошибка загрузки PDF:', err);
    });
});