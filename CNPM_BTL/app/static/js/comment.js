function addComment(productId){
    if(confirm("Bạn muốn bình luận ?") === true){
        fetch(`/api/product/${productId}/comments`,{
            method: "post",
            body: JSON.stringify({
                "content": document.getElementById("comment").value,
            }),
            headers: {
                'Content-Type': "application/json"
            }
        }).then(function(res) {
            return res.json();
        }).then(function(data) {
            if (data.status === 200){
                let c = data.comment;
                let d = document.getElementById("comments");
                d.innerHTML = `
                <div class="row mt-4 rounded" style="background: #dadada; padding: 2rem">
                    <div class="col-md-1" style="margin: auto">
                        <img src="${c.user.avatar}" class="img-fluid" style="width:80px; height:80px; border-radius: 50%;"/>
                    </div>
                    <div class="col-md-11">
                        <p style="font-size: 1.4rem; font-weight: 700">${ c.user.name }</p>
                        <p style="font-size: 1.25rem;">${ c.content }</p>
                        <p>Bình luận vào lúc: <span class="my-date"> ${ moment(c.created_date).locale("vi").fromNow() } </span></p>
                    </div>
                </div>
                 ` + d.innerHTML;
            }else
                alert(data.err_msg)
        });
}}