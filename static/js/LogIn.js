$(function(){
	$('#btnLogIn').click(function(){
		var user = $('#txtUsername').val();
		var pass = $('#txtPass').val();
		$.ajax({
			url: '/checkUserLogIn',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				if(response){
					if(response.status == false){
						alert(response.msg)
					}else{
						document.write(response)
					}
				}
				else{
					console.log('error occured')
				}
			},
			error: function(error){
				console.log('error occured')
			}
		});
	});
});