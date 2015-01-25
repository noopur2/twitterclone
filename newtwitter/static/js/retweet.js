jQuery(document).ready(function($) 
    {
	$(".retweet_form").submit(function(e) 
		{
		    e.preventDefault(); 
		    var btn = $("button", this);
		    var l_id = $(".hidden_id", this).val();
		    btn.attr('disabled', true);
		    $.post("/retweet/", $(this).serializeArray(),
			  function(data) {
			      if(data["retweetobj"]) {
				  btn.text("-");
			      }
			      else {
				  btn.text("+");
			      }
			  });
		    btn.attr('disabled', false);
		});
    });