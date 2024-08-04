function addToCart(id, name, price){
    fetch('/api/cart', {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price
        }),
        headers: {
            'Content-Type': "application/json"
        }
    }).then(function(res){
        return res.json();
    }).then(function(data){
        let c = document.getElementsByClassName('cart-counter');
        for (let d of c)
            d.innerText = data.total_quantity

        let p = document.getElementsByClassName('price-counter');
        for (let k of p)
            k.innerText = data.total_amount
    })
}

function updateCart(id, obj){ // obj là input có this trong cart.html
    obj.disabled = true; // vô hiệu hóa kh cho click tránh xung đột bất đồng bộ
    fetch(`/api/cart/${id}`,{
        method: 'put',
        body: JSON.stringify({
            "quantity": obj.value //dữ liệu đã nhập lên

        }),
        headers: {
            'Content-Type': "application/json"
        }
    }).then(res => res.json()).then(data => {
        obj.disabled = false;
        let c = document.getElementsByClassName('cart-counter');
        for (let d of c)
            d.innerText = data.total_quantity

        let p = document.getElementsByClassName('price-counter');
        for (let k of p)
            k.innerText = data.total_amount
    })
}

function deleteCart(id, obj){ // obj là input có this trong cart.html
    if (confirm("Bạn chắc chắn xóa không ?") === true){
        obj.disabled = true;
        fetch(`/api/cart/${id}`,{
            method: 'delete',
            body: JSON.stringify({
                "quantity": obj.value //dữ liệu đã nhập lên

            }),
        }).then(res => res.json()).then(data => {
            obj.disabled = false;
            let c = document.getElementsByClassName('cart-counter');
            for (let d of c)
                d.innerText = data.total_quantity

            let r = document.getElementById(`product${id}`);
            r.style.display = 'none'

            let p = document.getElementsByClassName('price-counter');
            for (let k of p)
                k.innerText = data.total_amount
        });
    }
}

function pay(){
    if(confirm("Bạn chắc chắn thanh toán ?") === true){
        fetch('/api/pay', {
            method: "post"
            }).then(res => res.json()).then(data => {
        if(data.status === 200)
            location.reload();
        else
           alert(data.err_msg);
    })
}}

//function addComment(id){
//    if(confirm("Bạn chắc chắn bình luận?") === true) {
//    fetch(`/api/products/${id}/comments`, {
//            method: 'post',
//            body: JSON.stringify({
//                "content": document.getElementById('comment').value
//            }),
//            headers: {
//                'Content-Type': 'application/json'
//            }
//        }).then(res => res.json()).then(data => {
//            if (data.status === 200){
//                let d = document.getElementById("comments");
//                d.innerHTML = `
//                <div class="row mt-4 rounded" style="background: #dadada; padding: 2rem">
//                    <div class="col-md-1" style="margin: auto">
//                        <img src="${c.user.avatar}" class="img-fluid" style="width:80px; height:80px; border-radius: 50%;"/>
//                    </div>
//                    <div class="col-md-11">
//                        <p style="font-size: 1.4rem; font-weight: 700">${ c.user.name }</p>
//                        <p style="font-size: 1.25rem;">${ c.content }</p>
//                        <p>Bình luận vào lúc: <span class="my-date"> ${ moment(c.created_date).locale("vi").fromNow() } </span></p>
//                    </div>
//                </div>`
//                 + d.innerHTML;
//
//            }
//        })
//}}