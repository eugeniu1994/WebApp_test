function uploadFile(input) {
    if (input.files && input.files[0]) {
        divResultId = document.getElementById('divResultId')
        divResultId.innerHTML = ""

        divForImage = document.createElement('div')
        divForImage.setAttribute('id', 'divForImage')
        divResultId.append(divForImage)

        a = document.createElement('a')
        a.setAttribute('id','hyperlinkId')

        divResultId.append(a)

        csv_div = document.createElement('div')
        csv_div.setAttribute('id','csv')
        divResultId.append(csv_div)

        var form_data = new FormData();
        form_data.append("files", input.files[0]);

        $.ajax({
            url: 'upload_document',
            dataType: 'json',
            cache: false,
            contentType: false,
            processData: false,
            data: form_data,
            type: 'post',
            success: function (response) {
                if(response) {
                    if (response.status) {
                        var image = document.createElement("img")
                        image.src = "data:image/png;base64," + response.encoded_img;
                        image.setAttribute('class','responsive')
                        $("#divForImage").append(image)
                        a.innerText = 'Download file'
                        a.setAttribute('href',"/getCsv")
                        $('#csv').html(response.csv_table)
                    } else {
                        console.log(response.msg)
                    }
                }
            },
            error: function (response) {
                console.log(response.msg);
            }
        });
    }
}
