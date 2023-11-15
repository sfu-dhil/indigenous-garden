// handle UI language
const setLanguage = (language) => {
    localStorage.setItem('garden_locale', language);
    document.body.classList.remove('english');
    document.body.classList.remove('western_scientific');
    document.body.classList.remove('halkomelem');
    document.body.classList.remove('squamish');
    document.body.classList.add(language);
    const languageRadioBtn = document.getElementById(`language-select-${language}`);
    languageRadioBtn.checked = true;
}
setLanguage(localStorage.getItem('garden_locale') || 'english');
const languageToggle = (language) => {
    if (localStorage.getItem('garden_locale') != language) {
        setLanguage(language);
    }
}
const languageRadioBtns = document.getElementsByName(`language-select`);
languageRadioBtns.forEach( (languageRadioBtn) => {
    languageRadioBtn.onclick = () => {
        languageToggle(languageRadioBtn.value);
    }
});