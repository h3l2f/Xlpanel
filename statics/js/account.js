$(document).ready(()=>{
    $(".cpass form").on( "submit", function( event ) {
        nwp = $("input[name='nwpasswd']")
        cnwp = $("input[name='cnwpasswd']")
        if (nwp.val() != cnwp.val()) {
            alert("Please confirm your new password.")
            event.preventDefault();
        }
      });
})