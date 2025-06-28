function $_he() {
    $(".nav .name").toggle()
    $(".nav .items .it it").toggle()
    $(".nav .users").delay(10).css("display", "none")
}

function $_he_1() {
    $(".nav .name").delay(10).fadeIn()
    $(".nav .items .it it").delay(10).fadeIn()
    $(".nav .users").delay(10).css("display", "flex")
}

function sh() {
    $(".nav .items").css({
        "margin-top": ($(".nav .items").css("margin-top")=="30px"?"10px":"30px"),
        "padding-bottom": ($(".nav .items").css("padding-bottom")=="30px"?"0":"30px")
    })
    if ($(".nav").css("width")!="65px") {
        tged = 1;
        $_he();
        $(".nav").css("width",($(".nav").css("width")=="65px"?"100%":"65px"))
    } else {
        $(".nav").css("width",($(".nav").css("width")=="65px"?"100%":"65px"))
        $_he_1()
    }
}