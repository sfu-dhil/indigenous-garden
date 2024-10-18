Trix.config.blockAttributes.heading2 = {
    tagName: "h2",
    breakOnReturn: true,
    group: false,
    terminal: true
}

Trix.config.blockAttributes.heading3 = {
    tagName: "h3",
    breakOnReturn: true,
    group: false,
    terminal: true
}

Trix.config.blockAttributes.heading4 = {
    tagName: "h4",
    breakOnReturn: true,
    group: false,
    terminal: true
}

Trix.config.blockAttributes.p = {
    tagName: "p",
    breakOnReturn: true,
    terminal: true
}

Trix.config.textAttributes.underlined = {
    tagName: "u",
    inheritable: true,
    parser(element) {
        const style = window.getComputedStyle(element);
        return style.textDecoration === "underline";
    },
}

// custom code
Trix.config.textAttributes.fontFamily = {
    inheritable: true,
    style: { fontFamily: "First Nations Unicode" },
    parser: function(element) {
        return element.style.fontFamily.match(/First Nations Unicode/)
    },
}

document.addEventListener("trix-before-initialize", () => {
    Trix.config.toolbar.getDefaultHTML = () => document.getElementById("trix-toolbar").innerHTML
})
