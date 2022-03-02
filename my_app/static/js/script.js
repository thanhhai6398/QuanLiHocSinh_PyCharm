function thanhToanMoMo() {
    fetch("/api/thanh-toan-momo", {
        method: 'post',
    }).then(function(res) {
        return res.json()
    }).then(function(data) {
        location.href = data.payUrl
    })

}