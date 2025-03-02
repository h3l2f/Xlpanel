function sh() {
    $(".nav .name").toggle()
    $(".nav .items").css({
        "margin-top": ($(".nav .items").css("margin-top")=="30px"?"10px":"30px"),
        "padding-bottom": ($(".nav .items").css("padding-bottom")=="30px"?"0":"30px")
    })
    $(".nav .items .it it").toggle()
    $(".nav .users").toggle()
    $(".nav").css("width",($(".nav").css("width")=="55px"?"100%":"55px"))
    $(".nav .items .it").css("text-align", ($(".nav .items .it").css("text-align")=="center"?"left":"center"))
}