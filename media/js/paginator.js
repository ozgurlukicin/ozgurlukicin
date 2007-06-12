var Paginator =
{
    jumpToPage: function(pages)
    {
        var page = prompt("Sayfa atlamak için 1 ve " + pages + " arasında bir sayı girin", "");
        if (page != undefined)
        {
            page = parseInt(page, 10)
            if (!isNaN(page) && page > 0 && page <= pages)
            {
                window.location.href = "?page=" + page;
            }
        }
    }
};
