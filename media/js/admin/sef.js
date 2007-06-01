window.onload=function(){
    var title = document.getElementById("id_title");
    var sef_title = document.getElementById("id_sef_title");

    title.onkeyup = function(){
        var str = title.value;

        str = str.replace(/ş/g, "s");
        str = str.replace(/ı/g, "i");
        str = str.replace(/ç/g, "c");
        str = str.replace(/ü/g, "u");
        str = str.replace(/ğ/g, "g");
        str = str.replace(/ö/g, "o");
        str = str.replace(/Ş/g, "S");
        str = str.replace(/İ/g, "I");
        str = str.replace(/Ç/g, "C");
        str = str.replace(/Ü/g, "U");
        str = str.replace(/Ğ/g, "G");
        str = str.replace(/Ö/g, "O");
        str = str.replace(/ /g, "_");
        str = str.replace(/\./g, "_");
        str = str.replace(/\?/g, "_");
        str = str.replace(/\&/g, "_");
        str = str.replace(/\=/g, "_");
        str = str.replace(/\)/g, "_");
        str = str.replace(/\(/g, "_");
        str = str.replace(/\//g, "_");
        str = str.replace(/\%/g, "_");
        str = str.replace(/\+/g, "_");
        str = str.replace(/\^/g, "_");
        str = str.replace(/\'/g, "_");
        str = str.replace(/\"/g, "_");
        str = str.replace(/\!/g, "_");
        str = str.replace(/\\/g, "_");
        str = str.replace(/\,/g, "_");
        str = str.replace(/\;/g, "_");
        str = str.replace(/\</g, "_");
        str = str.replace(/\>/g, "_");
        str = str.replace(/\:/g, "_");
        str = str.replace(/\-/g, "_");

        str = str.toLowerCase()

        sef_title.value = str;
    };
}
