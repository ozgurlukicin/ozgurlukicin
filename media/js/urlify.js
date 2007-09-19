function URLify(s, num_chars) {
    removelist = ["a", "an", "as", "at", "before", "but", "by", "for", "from",
                  "is", "in", "into", "like", "of", "off", "on", "onto", "per",
                  "since", "than", "the", "this", "that", "to", "up", "via",
                  "with"];
    r = new RegExp('\\b(' + removelist.join('|') + ')\\b', 'gi');
    s = s.replace(r, '');
    s = s.replace(/ş/g, "s");
    s = s.replace(/ı/g, "i");
    s = s.replace(/ç/g, "c");
    s = s.replace(/ü/g, "u");
    s = s.replace(/ğ/g, "g");
    s = s.replace(/ö/g, "o");
    s = s.replace(/Ş/g, "S");
    s = s.replace(/İ/g, "I");
    s = s.replace(/Ç/g, "C");
    s = s.replace(/Ü/g, "U");
    s = s.replace(/Ğ/g, "G");
    s = s.replace(/Ö/g, "O");
    s = s.replace(/[^-\w\s]/g, '');
    s = s.replace(/^\s+|\s+$/g, '');
    s = s.replace(/[-\s]+/g, '-');
    s = s.toLowerCase();
    return s.substring(0, num_chars);
}