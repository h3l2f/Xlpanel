function $_he() {
    $(".nav .name").toggle()
    $(".nav .items .it it").toggle()
    $(".nav .users").toggle()
}

function $_he_1() {
    $(".nav .name").delay(10).fadeIn()
    $(".nav .items .it it").delay(10).fadeIn()
    $(".nav .users").delay(10).fadeIn()
}

function sh() {
    $(".nav .items").css({
        "margin-top": ($(".nav .items").css("margin-top")=="30px"?"10px":"30px"),
        "padding-bottom": ($(".nav .items").css("padding-bottom")=="30px"?"0":"30px")
    })
    $(".nav .items .it").css("text-align", ($(".nav .items .it").css("text-align")=="center"?"left":"center"))
    if ($(".nav").css("width")!="65px") {
        $_he();
        $(".nav").css("width",($(".nav").css("width")=="65px"?"100%":"55px"))
    } else {
        $(".nav").css("width",($(".nav").css("width")=="65px"?"100%":"55px"))
        $_he_1()
    }
}