function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', () => {
    const csrftoken = getCookie('csrftoken');

    // Async Task Status Toggle
    document.querySelectorAll('.task-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', async (e) => {
            const url = e.target.dataset.url;
            const taskCard = e.target.closest('.task-item');
            try {
                const res = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'Content-Type': 'application/json'
                    }
                });
                if (res.ok) {
                    const data = await res.json();
                    taskCard.classList.toggle('completed', data.is_completed);
                    taskCard.dataset.status = data.is_completed ? 'completed' : 'pending';
                }
            } catch (err) {
                console.error('Toggle failed:', err);
            }
        });
    });

    // Live Search & Status Filtering
    const searchInput = document.getElementById('taskSearch');
    const statusFilter = document.getElementById('statusFilter');

    function filterTasks() {
        const query = searchInput ? searchInput.value.toLowerCase() : '';
        const status = statusFilter ? statusFilter.value : 'all';

        document.querySelectorAll('.task-item').forEach(item => {
            const matchesTitle = item.dataset.title.includes(query);
            const matchesStatus = status === 'all' || item.dataset.status === status;
            item.style.display = (matchesTitle && matchesStatus) ? 'flex' : 'none';
        });
    }

    if (searchInput) searchInput.addEventListener('input', filterTasks);
    if (statusFilter) statusFilter.addEventListener('change', filterTasks);
});
