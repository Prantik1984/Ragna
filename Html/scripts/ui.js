function showSection(id) {
  document.querySelectorAll('#home, #documents, #settings, #help')
    .forEach(el => el.classList.add('hidden'));
  document.getElementById(id).classList.remove('hidden');
}