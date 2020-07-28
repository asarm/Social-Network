        function change_to_follow(){
            document.getElementById("unfollow").className = "btn btn-block btn-success";
            document.getElementById("unfollow").innerText = "Follow";
                        console.log("follow post is working!"); // sanity check

        }
        function change_to_unfollow(){
            document.getElementById("follow").className = "btn btn-block btn-warning";
            document.getElementById("unfollow").innerText = "Unfollow";
        }

        // AJAX for posting
      /*  function create_post() {
             $.ajax({
                    url : "", // the endpoint
                    type : "POST", // http method
                    data : { the_post : $('#post-val').val() }, // data sent with the post request

                    // handle a successful response
                    success : function(json) {
                        $('#post-val').val(''); // remove the value from the input
                        console.log(json); // log the returned json to the console
                        console.log("success"); // another sanity check
                    },

                    // handle a non-successful response
                    error : function(xhr,errmsg,err) {
                        $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                            " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                    }
                });
        }

        $('#like-form').on('submit', function(event){
            event.preventDefault();
            console.log("form submitted!"); // sanity check
            var className = document.getElementById("post-val").className;
            if(className === 'btn btn-sm btn-danger'){
                document.getElementById("post-val").className = 'btn btn-sm btn-success';
                document.getElementById("post-val").innerText = 'Like';
            }
            else {
                document.getElementById("post-val").className = 'btn btn-sm btn-danger';
                document.getElementById("post-val").innerText = 'Unlike';

            }
            create_post();
});
*/

       $('.likebutton').click(function(){
            var catid;
            var total;
            var value;
            catid = $(this).data("catid");

            $.ajax(
            {
                type:"GET",
                url: "/likepost",
                data:{
                        post_id: catid
                },
                success: function( data )
                {
                    total = $('#'+ catid).attr("data-total");
                    if ($('#'+catid).attr("data-value") == 'Like'){
                        $( '#liked'+catid ).text((parseInt(total) + 1));
                        $( '#heart'+catid ).css('color', 'limegreen');
                        $('#'+catid).attr("data-total", parseInt(total) + 1);
                        $('#'+catid).attr("data-value", 'Unlike')
                    }
                    else{
                        $( '#liked'+catid ).text((parseInt(total) - 1));
                        $( '#heart'+catid ).css('color', 'black');
                        $('#'+catid).attr("data-total", parseInt(total) - 1);
                        $('#'+catid).attr("data-value", 'Like')
                    }
                }
            })


        });

        $(function() {
            $( 'a[href$="#"]' ).each(function() {
                $( this ).attr( 'href','javascript:void(0);' )
            });
        });