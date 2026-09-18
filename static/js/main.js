// StudyMate - Interactive Client Script

document.addEventListener('DOMContentLoaded', function() {
    // 1. Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            try {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            } catch(e) {}
        }, 5000);
    });

    // 2. Client-side Real-time Filter (on Year and Quantum pages)
    const clientSearchInput = document.getElementById('client-notes-search');
    if (clientSearchInput) {
        clientSearchInput.addEventListener('input', function(e) {
            const term = e.target.value.toLowerCase().trim();
            const noteCards = document.querySelectorAll('.note-searchable-item');
            const subjectContainers = document.querySelectorAll('.subject-container-item');
            
            let visibleTotal = 0;
            noteCards.forEach(function(card) {
                const title = card.getAttribute('data-title') || '';
                const chapter = card.getAttribute('data-chapter') || '';
                const subject = card.getAttribute('data-subject') || '';
                
                if (!term || title.includes(term) || chapter.includes(term) || subject.includes(term)) {
                    card.style.display = '';
                    visibleTotal++;
                } else {
                    card.style.display = 'none';
                }
            });

            // Hide subjects if all their notes are hidden
            subjectContainers.forEach(function(container) {
                const visibleCards = container.querySelectorAll('.note-searchable-item:not([style*="display: none"])');
                if (visibleCards.length === 0 && term !== '') {
                    container.style.display = 'none';
                } else {
                    container.style.display = '';
                }
            });

            const countBadge = document.getElementById('search-match-count');
            if (countBadge) {
                if (term) {
                    countBadge.textContent = `${visibleTotal} match${visibleTotal === 1 ? '' : 'es'} found`;
                    countBadge.style.display = 'inline-block';
                } else {
                    countBadge.style.display = 'none';
                }
            }
        });
    }

    // 3. Dropzone File Input Handler
    const dropzoneInput = document.getElementById('note-file-input');
    const dropzoneBox = document.getElementById('file-dropzone');
    const fileIndicator = document.getElementById('selected-file-info');
    const fileNameSpan = document.getElementById('selected-file-name');
    const fileSizeSpan = document.getElementById('selected-file-size');

    if (dropzoneInput && dropzoneBox) {
        ['dragenter', 'dragover'].forEach(eventName => {
            dropzoneBox.addEventListener(eventName, (e) => {
                e.preventDefault();
                dropzoneBox.classList.add('dragover');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropzoneBox.addEventListener(eventName, (e) => {
                e.preventDefault();
                dropzoneBox.classList.remove('dragover');
            }, false);
        });

        dropzoneBox.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            if (files.length) {
                dropzoneInput.files = files;
                updateFileInfo(files[0]);
            }
        });

        dropzoneInput.addEventListener('change', function(e) {
            if (this.files && this.files[0]) {
                updateFileInfo(this.files[0]);
            }
        });

        function updateFileInfo(file) {
            if (fileIndicator && fileNameSpan) {
                fileNameSpan.textContent = file.name;
                const sizeKb = (file.size / 1024).toFixed(1);
                const sizeMb = (file.size / (1024 * 1024)).toFixed(2);
                const displaySize = file.size > 1048576 ? `${sizeMb} MB` : `${sizeKb} KB`;
                if (fileSizeSpan) fileSizeSpan.textContent = `(${displaySize})`;
                fileIndicator.style.display = 'flex';
            }
        }
    }

    // 4. Dynamic Chapter Fetching when Subject changes in Add Note form
    const subjectSelect = document.getElementById('subject-select-dropdown');
    const chapterSelect = document.getElementById('chapter-select-dropdown');
    const chapterLoading = document.getElementById('chapter-loading-indicator');

    if (subjectSelect && chapterSelect) {
        subjectSelect.addEventListener('change', function() {
            const subjectId = this.value;
            if (!subjectId) {
                chapterSelect.innerHTML = '<option value="">-- First Select a Subject --</option>';
                chapterSelect.disabled = true;
                return;
            }

            if (chapterLoading) chapterLoading.style.display = 'inline-block';
            chapterSelect.disabled = true;

            fetch(`/api/chapters/${subjectId}/`)
                .then(res => res.json())
                .then(data => {
                    chapterSelect.innerHTML = '';
                    if (data.chapters && data.chapters.length > 0) {
                        chapterSelect.innerHTML = '<option value="">-- Choose Existing Chapter / Unit --</option>';
                        data.chapters.forEach(c => {
                            const opt = document.createElement('option');
                            opt.value = c.id;
                            opt.textContent = c.name;
                            chapterSelect.appendChild(opt);
                        });
                        chapterSelect.disabled = false;
                    } else {
                        chapterSelect.innerHTML = '<option value="">(No chapters yet - use New Chapter below)</option>';
                        chapterSelect.disabled = true;
                        // Auto open new chapter toggle if available
                        const newChapterToggle = document.getElementById('btn-toggle-new-chapter');
                        if (newChapterToggle && !document.getElementById('new-chapter-wrapper').classList.contains('show')) {
                            newChapterToggle.click();
                        }
                    }
                })
                .catch(err => {
                    console.error('Error fetching chapters:', err);
                })
                .finally(() => {
                    if (chapterLoading) chapterLoading.style.display = 'none';
                });
        });
    }
});
