function buy(elem) {
    _name = amount = $(elem).parent().children("select").attr("name")
    amount = $(elem).parent().children("select").val()
    $("#sbi").val(_name)
    $("#sba").val(amount)
    $("#hehe").submit()
}