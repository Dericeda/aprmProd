document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('applicationForm');
  const successMessage = document.getElementById('successMessage');

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    let isValid = true;

    // Проверка обязательных полей
    form.querySelectorAll('input[required], textarea[required], select[required]').forEach(function(field) {
      field.classList.remove('field-error');
      if (!field.value.trim()) {
        field.classList.add('field-error');
        isValid = false;
      }
    });

    if (!isValid) {
      alert('Пожалуйста, заполните обязательные поля!');
      form.scrollIntoView({ behavior: 'smooth' });
      return;
    }

    // Отправка формы через fetch
    const formData = new FormData(form);

    fetch(window.location.pathname, {
      method: 'POST',
      body: formData,
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
      }
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        form.style.display = 'none';
        successMessage.style.display = 'block';
      } else if (data.errors) {
        document.querySelectorAll('.field-error').forEach(el => el.classList.remove('field-error'));
        for (const [fieldName, messages] of Object.entries(data.errors)) {
          const field = form.querySelector(`[name="${fieldName}"]`);
          if (field) field.classList.add('field-error');
        }
        alert('⚠️ Пожалуйста, исправьте ошибки в форме.');
      }
    })
    .catch(err => {
      alert('Произошла ошибка при отправке формы.');
      console.error(err);
    });
  });
});
