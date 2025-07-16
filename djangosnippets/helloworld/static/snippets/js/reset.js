  document.getElementById('reset-button').addEventListener('click', function () {
    document.querySelector('input[name="q_name"]').value = '';
    document.querySelector('input[name="q_university"]').value = '';
    document.querySelector('select[name="q_year"]').value = '';
  });