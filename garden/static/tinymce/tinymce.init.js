tinymce.init({
    selector: 'textarea[data-editor="tinymce"]',
    branding: false,
    height: 250,
    menubar: false,
    content_css: 'kubi',
    skin: (localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')) === 'dark' ? 'oxide-dark' : 'oxide',
    plugins: [
      'autolink',
      'code',
      'link',
      'anchor',
      'lists',
      'media',
      'table',
      'image',
      'quickbars',
      'wordcount',
      'pagebreak',
      'nonbreaking',
    ],
    toolbar: 'undo redo | numlist bullist | fontfamily | fontsize | alignleft aligncenter alignright | link anchor | hr | removeformat',
    quickbars_insert_toolbar: false,
    quickbars_selection_toolbar: 'bold italic underline strikethrough | fontfamily | fontsize | forecolor | blockquote',
    contextmenu: 'undo redo | inserttable | cell row column deletetable',
    font_family_formats: 'Arial=arial,helvetica,sans-serif;First Nations Unicode="First Nations Unicode";',
    init_instance_callback : function(editor) {
      const getTheme = () => localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
      editor.contentDocument.body.setAttribute('data-theme', getTheme());

      editor.on('init', function () {
        editor.getContainer().style.transition='border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out';
      });
      editor.on('focus', function () {
        editor.getContainer().classList.add("is-focus");
      });
      editor.on('blur', function () {
        editor.getContainer().classList.remove("is-focus");
      });
    }
});
