$(document).ready(()=>{
    $(".form form").on( "submit", function( event ) {
        if (
            $("select[name=\"node\"]").val()=="_"
            ||
            $("select[name=\"egg\"]").val()=="_"
        ) {
            alert("Please fill out the form.")
            event.preventDefault();
        }
        
      });
})