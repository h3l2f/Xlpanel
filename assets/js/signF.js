function passwdToggle(e, name) {
    $(e).children("i").hide()
    if ($(e).parent().children(`input[name="${name}"]`).attr("type") == "password") {
        $(e).children("i[d=f]").show()
    } else {
        $(e).children("i[d=n]").show()
    }
    $(e).parent().children(`input[name="${name}"]`).attr("type", ($(e).parent().children(`input[name="${name}"]`).attr("type") == "password" ? "text" : "password"))
}

function chEq() {
    i1 = $("input[d=\"i1\"]")
    i2 = $("input[d=\"i2\"]")

    if (!i1.val() || !i2.val()) {
        i2.css("border-color","#0000aa");
        return;
    }

    if (i1.val() != i2.val()) i2.css("border-color","#aa0000");
    else i2.css("border-color","");
}

$(document).ready(()=>{
    $( "form[name=\"register\"]" ).on( "submit", function( event ) {
        i1 = $("input[d=\"i1\"]")
        i2 = $("input[d=\"i2\"]")
        if ( i1.val() == i2.val() ) {
          return;
        }
        event.preventDefault();
      });
})