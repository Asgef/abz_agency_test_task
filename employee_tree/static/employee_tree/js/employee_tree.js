
    document.addEventListener('DOMContentLoaded', function() {
        // Функция для обработки элемента <details> и загрузки подчиненных
        function loadChildren(detailElement) {
            if (detailElement.open && !detailElement.dataset.loaded) {
                const employeeId = detailElement.dataset.employeeId;
                
                // AJAX получение подчиненных
                fetch(`/employee-children/${employeeId}/`)
                    .then(response => response.json())
                    .then(children => {
                        const ulElement = detailElement.querySelector('ul');
                        children.forEach(child => {
                            const li = document.createElement('li');
                            li.innerHTML = `
                                <details data-employee-id="${child.id}">
                                    <summary><strong>${child.position}: ${child.name}</strong></summary>
                                    <ul></ul>
                                </details>`;
                            ulElement.appendChild(li);

                            // Обработчик для вновь добавленного элемента <details>
                            const newDetailElement = li.querySelector('details');
                            newDetailElement.addEventListener('toggle', function() {
                                loadChildren(newDetailElement);
                            });
                        });
                        detailElement.dataset.loaded = 'true';
                    })
                    .catch(error => {
                        console.error('Ошибка при загрузке подчиненных:', error);
                    });
            }
        }

        // Обработчик уровней <details>
        document.querySelectorAll('details[data-employee-id]').forEach(function(detailElement) {
            detailElement.addEventListener('toggle', function() {
                loadChildren(detailElement);
            });
        });
    });


    document.addEventListener('DOMContentLoaded', function() {
        // Развернуть первый и второй уровень иерархии
        document.querySelectorAll('#employee-tree > ul > li > details, #employee-tree > ul > li > details > ul > li > details').forEach(function(detailElement) {
            detailElement.setAttribute('open', 'open');
        });
    });