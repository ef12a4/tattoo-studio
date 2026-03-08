// Genel JavaScript Fonksiyonları

// Sayfa yüklendiğinde çalışacak fonksiyonlar
document.addEventListener('DOMContentLoaded', function() {
    // Tooltips'ı aktif et
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Form validasyonları
    initFormValidations();
    
    // Tarih saat picker'ları
    initDateTimePickers();
});

// Form validasyonları
function initFormValidations() {
    const forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

// Tarih ve saat picker'ları
function initDateTimePickers() {
    const dateInputs = document.querySelectorAll('input[type="datetime-local"]');
    dateInputs.forEach(function(input) {
        // Minimum tarihi bugün olarak ayarla
        const now = new Date();
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const day = String(now.getDate()).padStart(2, '0');
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        
        input.min = `${year}-${month}-${day}T${hours}:${minutes}`;
    });
}

// Sanatçı silme onayı
function deleteArtist(id) {
    if (confirm('Bu sanatçıyı silmek istediğinizden emin misiniz? Bu işlem geri alınamaz.')) {
        window.location.href = '/artists/delete/' + id;
    }
}

// Müşteri silme onayı
function deleteCustomer(id) {
    if (confirm('Bu müşteriyi silmek istediğinizden emin misiniz? Bu işlem geri alınamaz.')) {
        window.location.href = '/customers/delete/' + id;
    }
}

// Randevu silme onayı
function deleteAppointment(id) {
    if (confirm('Bu randevuyu silmek istediğinizden emin misiniz? Bu işlem geri alınamaz.')) {
        window.location.href = '/appointments/delete/' + id;
    }
}

// Portfolyo silme onayı
function deleteDesign(id) {
    if (confirm('Bu tasarımı silmek istediğinizden emin misiniz? Bu işlem geri alınamaz.')) {
        window.location.href = '/portfolio/delete/' + id;
    }
}

// Fiyat hesaplama
function calculatePrice() {
    const duration = document.getElementById('duration');
    const totalPrice = document.getElementById('total_price');
    const depositAmount = document.getElementById('deposit_amount');
    
    if (duration && duration.value) {
        // Basit fiyat hesaplama: dakika başına 2 TL
        const basePrice = parseInt(duration.value) * 2;
        if (totalPrice && !totalPrice.value) {
            totalPrice.value = basePrice;
        }
        
        // Kapora hesapla (%20)
        if (depositAmount && !depositAmount.value && totalPrice.value) {
            depositAmount.value = (parseFloat(totalPrice.value) * 0.2).toFixed(2);
        }
    }
}

// Dinamik fiyat hesaplama
document.addEventListener('input', function(e) {
    if (e.target && e.target.id === 'duration') {
        calculatePrice();
    }
});

// Sanatçı seçildiğinde uzmanlık alanlarını göster
function showArtistSpecialty() {
    const artistSelect = document.getElementById('artist_id');
    const specialtyDisplay = document.getElementById('artist_specialty');
    
    if (artistSelect && specialtyDisplay) {
        artistSelect.addEventListener('change', function() {
            const selectedOption = this.options[this.selectedIndex];
            const specialty = selectedOption.getAttribute('data-specialty');
            if (specialty) {
                specialtyDisplay.textContent = specialty;
                specialtyDisplay.style.display = 'block';
            } else {
                specialtyDisplay.style.display = 'none';
            }
        });
    }
}

// Resim önizleme
function previewImage(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.getElementById('image_preview');
            if (preview) {
                preview.src = e.target.result;
                preview.style.display = 'block';
            }
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// Ajax ile veri yükleme
function loadData(url, targetElement) {
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const element = document.getElementById(targetElement);
            if (element) {
                element.innerHTML = data.html;
            }
        })
        .catch(error => {
            console.error('Veri yüklenemedi:', error);
            showNotification('Veri yüklenirken bir hata oluştu.', 'error');
        });
}

// Bildirim göster
function showNotification(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('main .container-fluid, .container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // 5 saniye sonra otomatik kapat
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
}

// Loading spinner göster
function showLoading(element) {
    if (element) {
        element.disabled = true;
        element.innerHTML = '<span class="spinner"></span> Yükleniyor...';
    }
}

// Loading spinner gizle
function hideLoading(element, originalText) {
    if (element) {
        element.disabled = false;
        element.innerHTML = originalText;
    }
}

// Tablo arama
function searchTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);
    
    if (input && table) {
        input.addEventListener('keyup', function() {
            const filter = this.value.toLowerCase();
            const rows = table.getElementsByTagName('tr');
            
            for (let i = 1; i < rows.length; i++) {
                const cells = rows[i].getElementsByTagName('td');
                let found = false;
                
                for (let j = 0; j < cells.length; j++) {
                    const cellText = cells[j].textContent || cells[j].innerText;
                    if (cellText.toLowerCase().indexOf(filter) > -1) {
                        found = true;
                        break;
                    }
                }
                
                rows[i].style.display = found ? '' : 'none';
            }
        });
    }
}

// Print fonksiyonu
function printElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        const printWindow = window.open('', '_blank');
        printWindow.document.write(`
            <html>
                <head>
                    <title>Yazdır</title>
                    <style>
                        body { font-family: Arial, sans-serif; margin: 20px; }
                        table { width: 100%; border-collapse: collapse; }
                        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                        th { background-color: #f2f2f2; }
                    </style>
                </head>
                <body>
                    ${element.innerHTML}
                </body>
            </html>
        `);
        printWindow.document.close();
        printWindow.print();
    }
}

// Export to CSV
function exportToCSV(tableId, filename) {
    const table = document.getElementById(tableId);
    if (table) {
        let csv = [];
        const rows = table.querySelectorAll('tr');
        
        for (let i = 0; i < rows.length; i++) {
            const row = [], cols = rows[i].querySelectorAll('td, th');
            
            for (let j = 0; j < cols.length; j++) {
                let data = cols[j].innerText.replace(/(\r\n|\n|\r)/gm, '').replace(/"/g, '""');
                row.push('"' + data + '"');
            }
            
            csv.push(row.join(','));
        }
        
        const csvFile = new Blob([csv.join('\n')], { type: 'text/csv' });
        const downloadLink = document.createElement('a');
        downloadLink.download = filename;
        downloadLink.href = window.URL.createObjectURL(csvFile);
        downloadLink.style.display = 'none';
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
    }
}
