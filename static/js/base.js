var _0x9b78=["\x23\x6E\x61\x76\x44\x72\x6F\x70\x64\x6F\x77\x6E","\x3A\x76\x69\x73\x69\x62\x6C\x65","\x69\x73","\x68\x69\x64\x65","\x64\x69\x73\x70\x6C\x61\x79","\x66\x6C\x65\x78","\x63\x73\x73","\x63\x6C\x69\x63\x6B","\x23\x68\x61\x6D\x62\x4D\x65\x6E\x75\x54\x6F\x67\x67\x6C\x65","\x72\x65\x61\x64\x79"];$(document)[_0x9b78[9]](function(){$(_0x9b78[8])[_0x9b78[7]]((_0x5161x1)=>{dropdown= $(_0x9b78[0]);if(dropdown[_0x9b78[2]](_0x9b78[1])){dropdown[_0x9b78[3]]()}else {dropdown[_0x9b78[6]](_0x9b78[4],_0x9b78[5])}})})

function search() {
    let searchInput = $("#searchInput").val();

    if (searchInput)
        window.location.href = `/search?query=${searchInput}`
}

function toggleCartPopUp() {
    dropdown = $("#cartPopup");

    if (dropdown.is(":visible"))
        dropdown.hide();
        
    else
        dropdown.css("display", "flex");
}

$(document).ready(() => {
    $("#searchButton").click(search);
    $("#searchInput").on("keyup input", e => {
        if (e.which === 13 || e.keyCode === 13)
        {
            e.preventDefault();
            search();
        }
    })
    $("#cartPopupToggle").click(toggleCartPopUp)
})